# ============================================================
# BREAKOUT SCANNER - PRODUCTION V1
# ============================================================
#
# INPUT:
#   Scanner/ohlcv.csv
#
# CSV FORMAT:
#   instrument_key;name;timestamp;open;high;low;close;volume;
#   open_interest;Till (Date);CreationDate;Date
#
# STRATEGY:
#
#   1. Latest Close > Previous 20-Day High
#   2. Latest Volume >= 1.5 × Previous 20-Day Average Volume
#   3. EMA 20 > EMA 50
#   4. ADX 14 >= 25
#
# SCORE:
#
#   Price Breakout Strength = 30
#   Volume Confirmation     = 25
#   EMA Trend Strength      = 20
#   ADX Trend Strength      = 25
#
#   TOTAL = 100
#
# IMPORTANT:
#   Only completed historical candles are used.
#   No live market data is used.
#   No look-ahead bias.
#
# ============================================================

from pathlib import Path
import logging
import sys
import time

import pandas as pd
import pandas_ta as ta


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("BREAKOUT_SCANNER")


# ============================================================
# PATH
# ============================================================

# Test_Breakout.py is inside:
#
# C:\Users\dhruv.tomar\Desktop\Scanner
#
# Therefore .parent is Scanner.

PROJECT_ROOT = Path(__file__).resolve().parent

HISTORICAL_DATA_FILE = (
    PROJECT_ROOT / "ohlcv.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT / "breakout_results.csv"
)


# ============================================================
# STRATEGY CONFIGURATION
# ============================================================

DONCHIAN_PERIOD = 20
VOLUME_PERIOD = 20

EMA_FAST_PERIOD = 20
EMA_SLOW_PERIOD = 50

ADX_PERIOD = 14

MIN_ADX = 25.0
MIN_VOLUME_RATIO = 1.50


# ============================================================
# SCORE CONFIGURATION
# ============================================================

PRICE_SCORE_MAX = 30.0
VOLUME_SCORE_MAX = 25.0
EMA_SCORE_MAX = 20.0
ADX_SCORE_MAX = 25.0

MAX_BREAKOUT_STRENGTH_FOR_SCORE = 10.0
MAX_VOLUME_RATIO_FOR_SCORE = 3.0
MAX_EMA_SPREAD_FOR_SCORE = 10.0
MAX_ADX_FOR_SCORE = 50.0


# ============================================================
# REQUIRED INPUT COLUMNS
# ============================================================

CSV_REQUIRED_COLUMNS = [
    "instrument_key",
    "name",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "Date",
]


# ============================================================
# NORMALIZED COLUMNS
# ============================================================

REQUIRED_COLUMNS = [
    "instrument_key",
    "stock_name",
    "date",
    "open",
    "high",
    "low",
    "close",
    "volume",
]


# ============================================================
# READ HISTORICAL DATA
# ============================================================

def read_historical_data() -> pd.DataFrame:

    logger.info("=" * 70)
    logger.info("Loading historical data")
    logger.info("=" * 70)

    logger.info(
        "Historical data file: %s",
        HISTORICAL_DATA_FILE,
    )

    # --------------------------------------------------------
    # Check file
    # --------------------------------------------------------

    if not HISTORICAL_DATA_FILE.exists():

        logger.error(
            "Historical data file not found: %s",
            HISTORICAL_DATA_FILE,
        )

        logger.error(
            "Place ohlcv.csv inside: %s",
            PROJECT_ROOT,
        )

        sys.exit(1)

    # --------------------------------------------------------
    # Read CSV
    # --------------------------------------------------------

    try:

        df = pd.read_csv(
            HISTORICAL_DATA_FILE,
            sep=";",
            low_memory=False,
        )

    except Exception as exc:

        logger.exception(
            "Failed to read CSV: %s",
            exc,
        )

        sys.exit(1)

    logger.info(
        "CSV loaded successfully. Rows: %d",
        len(df),
    )

    logger.info(
        "CSV columns: %s",
        list(df.columns),
    )

    # --------------------------------------------------------
    # Validate columns
    # --------------------------------------------------------

    missing_columns = [
        column
        for column in CSV_REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:

        logger.error(
            "Missing required CSV columns: %s",
            missing_columns,
        )

        sys.exit(1)

    # --------------------------------------------------------
    # Rename columns
    # --------------------------------------------------------

    df = df.rename(
        columns={
            "name": "stock_name",
            "Date": "date",
        }
    )

    # --------------------------------------------------------
    # Keep only columns required by scanner
    # --------------------------------------------------------

    df = df[
        REQUIRED_COLUMNS
    ].copy()

    # --------------------------------------------------------
    # Clean instrument key / stock name
    # --------------------------------------------------------

    df["instrument_key"] = (
        df["instrument_key"]
        .astype(str)
        .str.strip()
    )

    df["stock_name"] = (
        df["stock_name"]
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------------
    # Date conversion
    # --------------------------------------------------------

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce",
    ).dt.normalize()

    # --------------------------------------------------------
    # Numeric conversion
    # --------------------------------------------------------

    numeric_columns = [
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]

    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    # --------------------------------------------------------
    # Remove completely invalid rows
    # --------------------------------------------------------

    before = len(df)

    df = df.dropna(
        subset=REQUIRED_COLUMNS
    )

    removed = before - len(df)

    if removed:

        logger.warning(
            "Removed %d rows with missing/invalid required values",
            removed,
        )

    # --------------------------------------------------------
    # Remove invalid prices
    # --------------------------------------------------------

    before = len(df)

    valid_price_mask = (
        (df["open"] > 0)
        & (df["high"] > 0)
        & (df["low"] > 0)
        & (df["close"] > 0)
        & (df["volume"] >= 0)
    )

    df = df[
        valid_price_mask
    ].copy()

    removed = before - len(df)

    if removed:

        logger.warning(
            "Removed %d rows with invalid OHLC/volume values",
            removed,
        )

    # --------------------------------------------------------
    # Validate OHLC relationships
    #
    # High must be >= Open, Close, Low
    # Low must be <= Open, Close, High
    # --------------------------------------------------------

    before = len(df)

    valid_ohlc_mask = (
        (df["high"] >= df["open"])
        & (df["high"] >= df["close"])
        & (df["high"] >= df["low"])
        & (df["low"] <= df["open"])
        & (df["low"] <= df["close"])
    )

    df = df[
        valid_ohlc_mask
    ].copy()

    removed = before - len(df)

    if removed:

        logger.warning(
            "Removed %d rows with invalid OHLC relationships",
            removed,
        )

    # --------------------------------------------------------
    # Remove duplicate instrument/date candles
    # --------------------------------------------------------

    before = len(df)

    df = df.drop_duplicates(
        subset=[
            "instrument_key",
            "date",
        ],
        keep="last",
    )

    removed = before - len(df)

    if removed:

        logger.warning(
            "Removed %d duplicate candles",
            removed,
        )

    # --------------------------------------------------------
    # Sort
    # --------------------------------------------------------

    df = df.sort_values(
        by=[
            "instrument_key",
            "date",
        ]
    ).reset_index(drop=True)

    # --------------------------------------------------------
    # Final validation
    # --------------------------------------------------------

    if df.empty:

        logger.error(
            "No valid historical data remains after validation."
        )

        sys.exit(1)

    # --------------------------------------------------------
    # Information
    # --------------------------------------------------------

    unique_instruments = (
        df["instrument_key"].nunique()
    )

    first_date = df["date"].min()
    latest_date = df["date"].max()

    logger.info(
        "Valid rows: %d",
        len(df),
    )

    logger.info(
        "Unique instruments: %d",
        unique_instruments,
    )

    logger.info(
        "First date: %s",
        first_date.strftime("%Y-%m-%d"),
    )

    logger.info(
        "Latest date: %s",
        latest_date.strftime("%Y-%m-%d"),
    )

    return df


# ============================================================
# CALCULATE INDICATORS
# ============================================================

def calculate_breakout_indicators(
    stock_df: pd.DataFrame,
) -> pd.DataFrame:

    stock_df = stock_df.copy()

    # --------------------------------------------------------
    # Previous 20-day high
    #
    # IMPORTANT:
    # shift(1) excludes today's candle.
    # --------------------------------------------------------

    stock_df["previous_20_day_high"] = (
        stock_df["high"]
        .rolling(
            window=DONCHIAN_PERIOD,
            min_periods=DONCHIAN_PERIOD,
        )
        .max()
        .shift(1)
    )

    # --------------------------------------------------------
    # Previous 20-day average volume
    #
    # IMPORTANT:
    # shift(1) excludes today's volume.
    # --------------------------------------------------------

    stock_df["previous_20_day_avg_volume"] = (
        stock_df["volume"]
        .rolling(
            window=VOLUME_PERIOD,
            min_periods=VOLUME_PERIOD,
        )
        .mean()
        .shift(1)
    )

    # --------------------------------------------------------
    # Volume ratio
    # --------------------------------------------------------

    stock_df["volume_ratio"] = 0.0

    valid_volume = (
        stock_df["previous_20_day_avg_volume"] > 0
    )

    stock_df.loc[
        valid_volume,
        "volume_ratio",
    ] = (
        stock_df.loc[
            valid_volume,
            "volume",
        ]
        / stock_df.loc[
            valid_volume,
            "previous_20_day_avg_volume",
        ]
    )

    # --------------------------------------------------------
    # EMA 20
    # --------------------------------------------------------

    stock_df["ema_20"] = ta.ema(
        stock_df["close"],
        length=EMA_FAST_PERIOD,
    )

    # --------------------------------------------------------
    # EMA 50
    # --------------------------------------------------------

    stock_df["ema_50"] = ta.ema(
        stock_df["close"],
        length=EMA_SLOW_PERIOD,
    )

    # --------------------------------------------------------
    # ADX 14
    # --------------------------------------------------------

    adx_result = ta.adx(
        high=stock_df["high"],
        low=stock_df["low"],
        close=stock_df["close"],
        length=ADX_PERIOD,
    )

    stock_df["adx"] = pd.NA

    if (
        adx_result is not None
        and not adx_result.empty
    ):

        expected_column = (
            f"ADX_{ADX_PERIOD}"
        )

        adx_column = None

        if expected_column in adx_result.columns:

            adx_column = expected_column

        else:

            for column in adx_result.columns:

                if str(column).upper().startswith("ADX_"):

                    adx_column = column
                    break

        if adx_column is not None:

            # Use index alignment instead of relying
            # on positional assignment.

            stock_df["adx"] = (
                adx_result[
                    adx_column
                ]
                .reindex(stock_df.index)
            )

    return stock_df


# ============================================================
# CALCULATE SCORE
# ============================================================

def calculate_signal_score(
    breakout_strength: float,
    volume_ratio: float,
    ema_spread: float,
    adx: float,
):

    # --------------------------------------------------------
    # Price score - maximum 30
    # --------------------------------------------------------

    price_score = (
        min(
            max(breakout_strength, 0.0),
            MAX_BREAKOUT_STRENGTH_FOR_SCORE,
        )
        / MAX_BREAKOUT_STRENGTH_FOR_SCORE
    ) * PRICE_SCORE_MAX

    # --------------------------------------------------------
    # Volume score - maximum 25
    # --------------------------------------------------------

    volume_score = (
        min(
            max(volume_ratio, 0.0),
            MAX_VOLUME_RATIO_FOR_SCORE,
        )
        / MAX_VOLUME_RATIO_FOR_SCORE
    ) * VOLUME_SCORE_MAX

    # --------------------------------------------------------
    # EMA score - maximum 20
    # --------------------------------------------------------

    ema_score = (
        min(
            max(ema_spread, 0.0),
            MAX_EMA_SPREAD_FOR_SCORE,
        )
        / MAX_EMA_SPREAD_FOR_SCORE
    ) * EMA_SCORE_MAX

    # --------------------------------------------------------
    # ADX score - maximum 25
    # --------------------------------------------------------

    adx_score = (
        min(
            max(adx, 0.0),
            MAX_ADX_FOR_SCORE,
        )
        / MAX_ADX_FOR_SCORE
    ) * ADX_SCORE_MAX

    # --------------------------------------------------------
    # Total
    # --------------------------------------------------------

    signal_score = (
        price_score
        + volume_score
        + ema_score
        + adx_score
    )

    # Safety clamp
    signal_score = min(
        max(signal_score, 0.0),
        100.0,
    )

    return (
        round(price_score, 2),
        round(volume_score, 2),
        round(ema_score, 2),
        round(adx_score, 2),
        round(signal_score, 2),
    )


# ============================================================
# ANALYZE ONE STOCK
# ============================================================

def analyze_breakout(
    stock_df: pd.DataFrame,
):

    # --------------------------------------------------------
    # Minimum required history
    #
    # EMA 50 is the largest base requirement.
    # Extra buffer is kept for reliable indicators.
    # --------------------------------------------------------

    minimum_required_rows = 55

    if len(stock_df) < minimum_required_rows:

        return None

    # --------------------------------------------------------
    # Calculate indicators
    # --------------------------------------------------------

    stock_df = calculate_breakout_indicators(
        stock_df
    )

    # --------------------------------------------------------
    # Latest completed candle
    # --------------------------------------------------------

    latest = stock_df.iloc[-1]

    # --------------------------------------------------------
    # Validate required values
    # --------------------------------------------------------

    required_values = [
        latest["previous_20_day_high"],
        latest["previous_20_day_avg_volume"],
        latest["ema_20"],
        latest["ema_50"],
        latest["adx"],
    ]

    for value in required_values:

        if pd.isna(value):

            return None

    # --------------------------------------------------------
    # Extract values
    # --------------------------------------------------------

    close = float(
        latest["close"]
    )

    volume = float(
        latest["volume"]
    )

    previous_20_day_high = float(
        latest["previous_20_day_high"]
    )

    previous_20_day_avg_volume = float(
        latest["previous_20_day_avg_volume"]
    )

    ema_20 = float(
        latest["ema_20"]
    )

    ema_50 = float(
        latest["ema_50"]
    )

    adx = float(
        latest["adx"]
    )

    # --------------------------------------------------------
    # Volume ratio
    # --------------------------------------------------------

    if previous_20_day_avg_volume <= 0:

        return None

    volume_ratio = (
        volume
        / previous_20_day_avg_volume
    )

    # --------------------------------------------------------
    # CONDITION 1
    #
    # Latest close > previous 20-day high
    # --------------------------------------------------------

    price_breakout = (
        close > previous_20_day_high
    )

    # --------------------------------------------------------
    # CONDITION 2
    #
    # Latest volume >= 1.5 × previous 20-day average
    # --------------------------------------------------------

    volume_confirmation = (
        volume_ratio >= MIN_VOLUME_RATIO
    )

    # --------------------------------------------------------
    # CONDITION 3
    #
    # EMA 20 > EMA 50
    # --------------------------------------------------------

    ema_trend = (
        ema_20 > ema_50
    )

    # --------------------------------------------------------
    # CONDITION 4
    #
    # ADX 14 >= 25
    # --------------------------------------------------------

    strong_trend = (
        adx >= MIN_ADX
    )

    # --------------------------------------------------------
    # Final breakout
    # --------------------------------------------------------

    is_breakout = (
        price_breakout
        and volume_confirmation
        and ema_trend
        and strong_trend
    )

    if not is_breakout:

        return None

    # ========================================================
    # BREAKOUT STRENGTH
    # ========================================================

    if previous_20_day_high <= 0:

        return None

    breakout_strength = (
        (
            close
            - previous_20_day_high
        )
        / previous_20_day_high
    ) * 100.0

    # ========================================================
    # EMA SPREAD
    # ========================================================

    if ema_50 == 0:

        return None

    ema_spread = (
        (
            ema_20
            - ema_50
        )
        / ema_50
    ) * 100.0

    # ========================================================
    # SCORE
    # ========================================================

    (
        price_score,
        volume_score,
        ema_score,
        adx_score,
        signal_score,
    ) = calculate_signal_score(
        breakout_strength=breakout_strength,
        volume_ratio=volume_ratio,
        ema_spread=ema_spread,
        adx=adx,
    )

    # ========================================================
    # RESULT
    # ========================================================

    return {
        "instrument_key": str(
            latest["instrument_key"]
        ),

        "stock_name": str(
            latest["stock_name"]
        ),

        "date": latest["date"].strftime(
            "%Y-%m-%d"
        ),

        "open": round(
            float(latest["open"]),
            2,
        ),

        "high": round(
            float(latest["high"]),
            2,
        ),

        "low": round(
            float(latest["low"]),
            2,
        ),

        "close": round(
            close,
            2,
        ),

        "volume": int(
            volume
        ),

        "breakout_level": round(
            previous_20_day_high,
            2,
        ),

        "breakout_strength_percentage": round(
            breakout_strength,
            2,
        ),

        "volume_average_20": round(
            previous_20_day_avg_volume,
            2,
        ),

        "volume_ratio": round(
            volume_ratio,
            2,
        ),

        "ema_20": round(
            ema_20,
            2,
        ),

        "ema_50": round(
            ema_50,
            2,
        ),

        "ema_spread_percentage": round(
            ema_spread,
            2,
        ),

        "adx": round(
            adx,
            2,
        ),

        # Individual conditions
        "price_breakout": True,
        "volume_confirmation": True,
        "ema_trend": True,
        "adx_confirmation": True,

        # Scores
        "price_score": price_score,
        "volume_score": volume_score,
        "ema_score": ema_score,
        "adx_score": adx_score,

        "signal_score": signal_score,

        "signal": "BREAKOUT",
    }


# ============================================================
# RUN SCANNER
# ============================================================

def run_breakout_scanner(
    df: pd.DataFrame,
) -> pd.DataFrame:

    logger.info("=" * 70)
    logger.info("BREAKOUT SCANNER STARTED")
    logger.info("=" * 70)

    start_time = time.perf_counter()

    results = []

    total_instruments = (
        df["instrument_key"].nunique()
    )

    logger.info(
        "Total instruments: %d",
        total_instruments,
    )

    # --------------------------------------------------------
    # Group once.
    #
    # This is significantly faster than:
    #
    # df[df["instrument_key"] == instrument]
    #
    # for every instrument.
    # --------------------------------------------------------

    grouped = df.groupby(
        "instrument_key",
        sort=False,
    )

    processed = 0

    for instrument_key, stock_df in grouped:

        processed += 1

        # Data is already globally sorted,
        # but explicitly sort each group for safety.

        stock_df = stock_df.sort_values(
            "date"
        ).reset_index(
            drop=True
        )

        result = analyze_breakout(
            stock_df
        )

        if result is not None:

            results.append(
                result
            )

    # --------------------------------------------------------
    # Convert results
    # --------------------------------------------------------

    if not results:

        elapsed = (
            time.perf_counter()
            - start_time
        )

        logger.info(
            "No breakout stocks found."
        )

        logger.info(
            "Scanner execution time: %.2f seconds",
            elapsed,
        )

        return pd.DataFrame()

    result_df = pd.DataFrame(
        results
    )

    # --------------------------------------------------------
    # Sort
    # --------------------------------------------------------

    result_df = result_df.sort_values(
        by=[
            "signal_score",
            "breakout_strength_percentage",
            "volume_ratio",
        ],
        ascending=[
            False,
            False,
            False,
        ],
    ).reset_index(
        drop=True
    )

    elapsed = (
        time.perf_counter()
        - start_time
    )

    logger.info(
        "Breakout stocks found: %d",
        len(result_df),
    )

    logger.info(
        "Scanner execution time: %.2f seconds",
        elapsed,
    )

    return result_df


# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(
    result_df: pd.DataFrame,
):

    if result_df.empty:

        # Remove old result file so stale results
        # are never mistaken for today's results.

        if OUTPUT_FILE.exists():

            try:

                OUTPUT_FILE.unlink()

                logger.info(
                    "Removed old result file: %s",
                    OUTPUT_FILE,
                )

            except Exception as exc:

                logger.warning(
                    "Could not remove old result file: %s",
                    exc,
                )

        return

    try:

        result_df.to_csv(
            OUTPUT_FILE,
            index=False,
        )

        logger.info(
            "Results saved to: %s",
            OUTPUT_FILE,
        )

    except Exception as exc:

        logger.exception(
            "Failed to save results: %s",
            exc,
        )


# ============================================================
# DISPLAY RESULTS
# ============================================================

def display_results(
    result_df: pd.DataFrame,
):

    if result_df.empty:

        print()
        print("=" * 100)
        print("NO BREAKOUT STOCKS FOUND")
        print("=" * 100)

        return

    print()
    print("=" * 120)
    print("BREAKOUT SCANNER RESULTS")
    print("=" * 120)

    display_columns = [
        "stock_name",
        "date",
        "close",
        "breakout_level",
        "breakout_strength_percentage",
        "volume_ratio",
        "ema_20",
        "ema_50",
        "ema_spread_percentage",
        "adx",
        "signal_score",
        "signal",
    ]

    print(
        result_df[
            display_columns
        ].to_string(
            index=False
        )
    )

    print()
    print("=" * 120)

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print(
        f"Total Breakouts : {len(result_df)}"
    )

    print(
        f"Highest Score   : "
        f"{result_df.iloc[0]['signal_score']}"
    )

    print(
        f"Best Breakout   : "
        f"{result_df.iloc[0]['stock_name']}"
    )

    print("=" * 120)


# ============================================================
# MAIN
# ============================================================

def main():

    total_start = time.perf_counter()

    try:

        # ----------------------------------------------------
        # Load data
        # ----------------------------------------------------

        df = read_historical_data()

        # ----------------------------------------------------
        # Run scanner
        # ----------------------------------------------------

        result_df = run_breakout_scanner(
            df
        )

        # ----------------------------------------------------
        # Save results
        # ----------------------------------------------------

        save_results(
            result_df
        )

        # ----------------------------------------------------
        # Display
        # ----------------------------------------------------

        display_results(
            result_df
        )

        # ----------------------------------------------------
        # Total execution time
        # ----------------------------------------------------

        total_elapsed = (
            time.perf_counter()
            - total_start
        )

        logger.info("=" * 70)
        logger.info(
            "BREAKOUT SCANNER COMPLETED"
        )
        logger.info(
            "Total execution time: %.2f seconds",
            total_elapsed,
        )
        logger.info("=" * 70)

    except KeyboardInterrupt:

        logger.warning(
            "Scanner stopped by user."
        )

        sys.exit(1)

    except Exception as exc:

        logger.exception(
            "Scanner failed: %s",
            exc,
        )

        sys.exit(1)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()