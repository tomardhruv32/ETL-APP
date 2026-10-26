"""
============================================================
PULLBACK SCANNER
============================================================

Purpose:
    Find stocks in a bullish trend that have recently
    pulled back from their recent highs.

Input:
    ohlcv.csv

Output:
    pullback_results.csv

Strategy:

STRONG PULLBACK
    1. EMA20 > EMA50 > EMA200
    2. Close > EMA200
    3. 20-day return >= 5%
    4. Pullback from previous 20-day high >= 5%
    5. RSI between 45 and 65
    6. ADX >= 20

PULLBACK
    1. EMA20 > EMA50 > EMA200
    2. Close > EMA200
    3. 20-day return >= 2%
    4. Pullback from previous 20-day high >= 3%
    5. RSI between 40 and 65
    6. ADX >= 18

Uses completed daily candles only.

No:
    - Live market data
    - Upstox API
    - WebSocket
    - Redis
    - Intraday candles
"""

import logging
import time
from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

# Test_pullback.py is directly inside Scanner
PROJECT_ROOT = Path(__file__).resolve().parent

INPUT_FILE = PROJECT_ROOT / "ohlcv.csv"
OUTPUT_FILE = PROJECT_ROOT / "pullback_results.csv"


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# ============================================================
# SCANNER SETTINGS
# ============================================================

EMA_FAST = 20
EMA_MEDIUM = 50
EMA_SLOW = 200

RETURN_PERIOD = 20
HIGH_PERIOD = 20

RSI_PERIOD = 14
ADX_PERIOD = 14

VOLUME_PERIOD = 20


# ============================================================
# STRONG PULLBACK SETTINGS
# ============================================================

STRONG_MIN_RETURN = 5.0
STRONG_MIN_PULLBACK = 5.0
STRONG_MIN_ADX = 20.0

STRONG_RSI_MIN = 45.0
STRONG_RSI_MAX = 65.0


# ============================================================
# NORMAL PULLBACK SETTINGS
# ============================================================

PULLBACK_MIN_RETURN = 2.0
PULLBACK_MIN_PULLBACK = 3.0
PULLBACK_MIN_ADX = 18.0

PULLBACK_RSI_MIN = 40.0
PULLBACK_RSI_MAX = 65.0


# ============================================================
# MINIMUM HISTORY
# ============================================================

# EMA200 requires substantial historical data.
MIN_HISTORY = 220


# ============================================================
# REQUIRED INPUT COLUMNS
# ============================================================

REQUIRED_INPUT_COLUMNS = [
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
# OUTPUT COLUMNS
# ============================================================

OUTPUT_COLUMNS = [
    "instrument_key",
    "stock_name",
    "date",
    "close",
    "pullback_percentage",
    "price_return_20d",
    "previous_20d_high",
    "ema_20",
    "ema_50",
    "ema_200",
    "ema_spread_percentage",
    "distance_from_ema20",
    "distance_from_ema50",
    "rsi",
    "adx",
    "volume_ratio",
    "pullback_score",
    "signal",
]


# ============================================================
# LOAD HISTORICAL DATA
# ============================================================

def load_historical_data():
    """
    Load and validate OHLCV data from ohlcv.csv.
    """

    logger.info("=" * 70)
    logger.info("READING HISTORICAL DATA FROM CSV")
    logger.info("=" * 70)

    logger.info("Historical data file: %s", INPUT_FILE)

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Historical data file not found: {INPUT_FILE}"
        )

    # --------------------------------------------------------
    # Read CSV
    # --------------------------------------------------------

    df = pd.read_csv(
        INPUT_FILE,
        sep=";",
        low_memory=False,
    )

    logger.info("Rows loaded: %s", len(df))
    logger.info("CSV columns: %s", list(df.columns))

    # --------------------------------------------------------
    # Validate columns
    # --------------------------------------------------------

    missing_columns = [
        column
        for column in REQUIRED_INPUT_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # --------------------------------------------------------
    # Keep only columns required by scanner
    # --------------------------------------------------------

    df = df[
        [
            "instrument_key",
            "name",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "Date",
        ]
    ].copy()

    # --------------------------------------------------------
    # Rename columns to internal standard
    # --------------------------------------------------------

    df = df.rename(
        columns={
            "name": "stock_name",
            "Date": "date",
        }
    )

    # --------------------------------------------------------
    # Clean instrument and stock names
    # --------------------------------------------------------

    df["instrument_key"] = (
        df["instrument_key"]
        .astype("string")
        .str.strip()
    )

    df["stock_name"] = (
        df["stock_name"]
        .astype("string")
        .str.strip()
    )

    # --------------------------------------------------------
    # Convert date
    # --------------------------------------------------------

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce",
    )

    # --------------------------------------------------------
    # Convert numeric columns
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
    # Remove missing required values
    # --------------------------------------------------------

    before_drop = len(df)

    df = df.dropna(
        subset=[
            "instrument_key",
            "stock_name",
            "date",
            "open",
            "high",
            "low",
            "close",
            "volume",
        ]
    )

    removed_rows = before_drop - len(df)

    if removed_rows > 0:
        logger.warning(
            "Removed %s rows with missing/invalid required values",
            removed_rows,
        )

    # --------------------------------------------------------
    # Remove invalid OHLCV values
    # --------------------------------------------------------

    before_validation = len(df)

    valid_ohlcv = (
        (df["open"] > 0)
        & (df["high"] > 0)
        & (df["low"] > 0)
        & (df["close"] > 0)
        & (df["volume"] >= 0)
        & (df["high"] >= df["low"])
        & (df["high"] >= df["open"])
        & (df["high"] >= df["close"])
        & (df["low"] <= df["open"])
        & (df["low"] <= df["close"])
    )

    df = df[valid_ohlcv].copy()

    invalid_ohlcv = before_validation - len(df)

    if invalid_ohlcv > 0:
        logger.warning(
            "Removed %s rows with invalid OHLCV values",
            invalid_ohlcv,
        )

    # --------------------------------------------------------
    # Remove duplicate candles
    # --------------------------------------------------------

    before_duplicates = len(df)

    df = df.drop_duplicates(
        subset=[
            "instrument_key",
            "date",
        ],
        keep="last",
    )

    duplicate_rows = before_duplicates - len(df)

    if duplicate_rows > 0:
        logger.warning(
            "Removed %s duplicate instrument/date rows",
            duplicate_rows,
        )

    # --------------------------------------------------------
    # Sort
    # --------------------------------------------------------

    df = df.sort_values(
        [
            "instrument_key",
            "date",
        ]
    ).reset_index(drop=True)

    # --------------------------------------------------------
    # Final information
    # --------------------------------------------------------

    logger.info("Valid rows: %s", len(df))

    logger.info(
        "Unique instruments: %s",
        df["instrument_key"].nunique(),
    )

    logger.info(
        "First date: %s",
        df["date"].min().date(),
    )

    logger.info(
        "Latest date: %s",
        df["date"].max().date(),
    )

    logger.info("Historical data successfully loaded.")

    return df


# ============================================================
# RSI
# ============================================================

def calculate_rsi(close, period=RSI_PERIOD):
    """
    Calculate RSI using Wilder-style smoothing.
    """

    delta = close.diff()

    gain = delta.clip(lower=0)

    loss = -delta.clip(upper=0)

    average_gain = gain.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period,
    ).mean()

    average_loss = loss.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period,
    ).mean()

    rs = average_gain / average_loss

    rsi = 100 - (
        100 / (1 + rs)
    )

    return rsi


# ============================================================
# ADX
# ============================================================

def calculate_adx(
    high,
    low,
    close,
    period=ADX_PERIOD,
):
    """
    Calculate Average Directional Index.
    """

    previous_close = close.shift(1)

    tr1 = high - low

    tr2 = (
        high - previous_close
    ).abs()

    tr3 = (
        low - previous_close
    ).abs()

    true_range = pd.concat(
        [
            tr1,
            tr2,
            tr3,
        ],
        axis=1,
    ).max(axis=1)

    up_move = high.diff()

    down_move = -low.diff()

    plus_dm = pd.Series(
        np.where(
            (up_move > down_move)
            & (up_move > 0),
            up_move,
            0.0,
        ),
        index=high.index,
    )

    minus_dm = pd.Series(
        np.where(
            (down_move > up_move)
            & (down_move > 0),
            down_move,
            0.0,
        ),
        index=high.index,
    )

    atr = true_range.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period,
    ).mean()

    plus_dm_smooth = plus_dm.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period,
    ).mean()

    minus_dm_smooth = minus_dm.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period,
    ).mean()

    plus_di = (
        100
        * plus_dm_smooth
        / atr
    )

    minus_di = (
        100
        * minus_dm_smooth
        / atr
    )

    denominator = (
        plus_di + minus_di
    )

    dx = (
        100
        * (plus_di - minus_di).abs()
        / denominator.replace(
            0,
            np.nan,
        )
    )

    adx = dx.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period,
    ).mean()

    return adx


# ============================================================
# ANALYZE ONE STOCK
# ============================================================

def analyze_stock(stock_df):
    """
    Analyze one instrument and return a result if
    it qualifies as PULLBACK or STRONG PULLBACK.
    """

    # --------------------------------------------------------
    # Sort chronologically
    # --------------------------------------------------------

    stock_df = (
        stock_df
        .sort_values("date")
        .copy()
    )

    # --------------------------------------------------------
    # Minimum history
    # --------------------------------------------------------

    if len(stock_df) < MIN_HISTORY:
        return None

    close = stock_df["close"]
    high = stock_df["high"]
    low = stock_df["low"]
    volume = stock_df["volume"]

    # ========================================================
    # EMA20
    # ========================================================

    stock_df["ema_20"] = (
        close.ewm(
            span=EMA_FAST,
            adjust=False,
        ).mean()
    )

    # ========================================================
    # EMA50
    # ========================================================

    stock_df["ema_50"] = (
        close.ewm(
            span=EMA_MEDIUM,
            adjust=False,
        ).mean()
    )

    # ========================================================
    # EMA200
    # ========================================================

    stock_df["ema_200"] = (
        close.ewm(
            span=EMA_SLOW,
            adjust=False,
        ).mean()
    )

    # ========================================================
    # RSI14
    # ========================================================

    stock_df["rsi"] = calculate_rsi(
        close,
        RSI_PERIOD,
    )

    # ========================================================
    # ADX14
    # ========================================================

    stock_df["adx"] = calculate_adx(
        high,
        low,
        close,
        ADX_PERIOD,
    )

    # ========================================================
    # 20-DAY RETURN
    # ========================================================

    stock_df["price_return_20d"] = (
        (
            close
            / close.shift(RETURN_PERIOD)
        ) - 1
    ) * 100

    # ========================================================
    # PREVIOUS 20-DAY HIGH
    #
    # IMPORTANT:
    #
    # shift(1) prevents the current candle's high
    # from being included.
    # ========================================================

    stock_df["previous_20d_high"] = (
        high
        .rolling(HIGH_PERIOD)
        .max()
        .shift(1)
    )

    # ========================================================
    # PULLBACK %
    # ========================================================

    stock_df["pullback_percentage"] = (
        (
            (
                stock_df["previous_20d_high"]
                - close
            )
            / stock_df["previous_20d_high"]
        )
        * 100
    )

    # ========================================================
    # DISTANCE FROM EMA20
    # ========================================================

    stock_df["distance_from_ema20"] = (
        (
            (
                close
                - stock_df["ema_20"]
            )
            / stock_df["ema_20"]
        )
        * 100
    )

    # ========================================================
    # DISTANCE FROM EMA50
    # ========================================================

    stock_df["distance_from_ema50"] = (
        (
            (
                close
                - stock_df["ema_50"]
            )
            / stock_df["ema_50"]
        )
        * 100
    )

    # ========================================================
    # EMA SPREAD
    # ========================================================

    stock_df["ema_spread_percentage"] = (
        (
            (
                stock_df["ema_20"]
                - stock_df["ema_50"]
            )
            / stock_df["ema_50"]
        )
        * 100
    )

    # ========================================================
    # PREVIOUS 20-DAY AVERAGE VOLUME
    #
    # Current candle is excluded.
    # ========================================================

    stock_df["average_volume_20d"] = (
        volume
        .rolling(VOLUME_PERIOD)
        .mean()
        .shift(1)
    )

    # ========================================================
    # VOLUME RATIO
    # ========================================================

    stock_df["volume_ratio"] = (
        volume
        / stock_df["average_volume_20d"]
    )

    # ========================================================
    # LATEST COMPLETED CANDLE
    # ========================================================

    latest = stock_df.iloc[-1]

    # ========================================================
    # VALIDATE INDICATORS
    # ========================================================

    required_values = [
        latest["close"],
        latest["ema_20"],
        latest["ema_50"],
        latest["ema_200"],
        latest["rsi"],
        latest["adx"],
        latest["price_return_20d"],
        latest["previous_20d_high"],
        latest["pullback_percentage"],
    ]

    if any(
        pd.isna(value)
        for value in required_values
    ):
        return None

    # ========================================================
    # BULLISH TREND STRUCTURE
    # ========================================================

    bullish_structure = (
        latest["ema_20"]
        > latest["ema_50"]
        > latest["ema_200"]
    )

    # ========================================================
    # PRICE ABOVE EMA200
    # ========================================================

    price_above_ema200 = (
        latest["close"]
        > latest["ema_200"]
    )

    # ========================================================
    # STRONG PULLBACK
    # ========================================================

    strong_pullback = (
        bullish_structure
        and price_above_ema200
        and latest["price_return_20d"]
        >= STRONG_MIN_RETURN
        and latest["pullback_percentage"]
        >= STRONG_MIN_PULLBACK
        and STRONG_RSI_MIN
        <= latest["rsi"]
        <= STRONG_RSI_MAX
        and latest["adx"]
        >= STRONG_MIN_ADX
    )

    # ========================================================
    # NORMAL PULLBACK
    # ========================================================

    normal_pullback = (
        bullish_structure
        and price_above_ema200
        and latest["price_return_20d"]
        >= PULLBACK_MIN_RETURN
        and latest["pullback_percentage"]
        >= PULLBACK_MIN_PULLBACK
        and PULLBACK_RSI_MIN
        <= latest["rsi"]
        <= PULLBACK_RSI_MAX
        and latest["adx"]
        >= PULLBACK_MIN_ADX
    )

    # ========================================================
    # NO SIGNAL
    # ========================================================

    if not strong_pullback and not normal_pullback:
        return None

    # ========================================================
    # PULLBACK SCORE
    # ========================================================

    score = 0

    # --------------------------------------------------------
    # Bullish EMA structure
    # --------------------------------------------------------

    if bullish_structure:
        score += 25

    # --------------------------------------------------------
    # Price above EMA200
    # --------------------------------------------------------

    if price_above_ema200:
        score += 15

    # --------------------------------------------------------
    # 20-day return
    # --------------------------------------------------------

    if latest["price_return_20d"] >= 10:
        score += 15

    elif latest["price_return_20d"] >= 5:
        score += 10

    elif latest["price_return_20d"] >= 2:
        score += 5

    # --------------------------------------------------------
    # Pullback depth
    # --------------------------------------------------------

    if latest["pullback_percentage"] >= 8:
        score += 20

    elif latest["pullback_percentage"] >= 5:
        score += 15

    elif latest["pullback_percentage"] >= 3:
        score += 10

    # --------------------------------------------------------
    # RSI
    # --------------------------------------------------------

    if 50 <= latest["rsi"] <= 60:
        score += 10

    elif 45 <= latest["rsi"] <= 65:
        score += 7

    elif 40 <= latest["rsi"] <= 65:
        score += 5

    # --------------------------------------------------------
    # ADX
    # --------------------------------------------------------

    if latest["adx"] >= 35:
        score += 15

    elif latest["adx"] >= 25:
        score += 10

    elif latest["adx"] >= 20:
        score += 7

    elif latest["adx"] >= 18:
        score += 5

    # --------------------------------------------------------
    # Safety cap
    # --------------------------------------------------------

    score = min(score, 100)

    # ========================================================
    # SIGNAL
    # ========================================================

    if strong_pullback:
        signal = "STRONG PULLBACK"
    else:
        signal = "PULLBACK"

    # ========================================================
    # RESULT
    # ========================================================

    return {
        "instrument_key": latest["instrument_key"],
        "stock_name": latest["stock_name"],
        "date": latest["date"],
        "close": latest["close"],
        "pullback_percentage": latest[
            "pullback_percentage"
        ],
        "price_return_20d": latest[
            "price_return_20d"
        ],
        "previous_20d_high": latest[
            "previous_20d_high"
        ],
        "ema_20": latest["ema_20"],
        "ema_50": latest["ema_50"],
        "ema_200": latest["ema_200"],
        "ema_spread_percentage": latest[
            "ema_spread_percentage"
        ],
        "distance_from_ema20": latest[
            "distance_from_ema20"
        ],
        "distance_from_ema50": latest[
            "distance_from_ema50"
        ],
        "rsi": latest["rsi"],
        "adx": latest["adx"],
        "volume_ratio": latest["volume_ratio"],
        "pullback_score": score,
        "signal": signal,
    }


# ============================================================
# RUN SCANNER
# ============================================================

def run_pullback_scanner(df):
    """
    Analyze all instruments.
    """

    logger.info("=" * 70)
    logger.info("RUNNING PULLBACK ANALYSIS")
    logger.info("=" * 70)

    results = []

    grouped = df.groupby(
        "instrument_key",
        sort=False,
    )

    total = len(grouped)

    for index, (
        instrument_key,
        stock_df,
    ) in enumerate(
        grouped,
        start=1,
    ):

        try:

            result = analyze_stock(
                stock_df
            )

            if result is not None:
                results.append(result)

        except Exception as exc:

            logger.warning(
                "Failed to analyze %s: %s",
                instrument_key,
                exc,
            )

    logger.info(
        "Processed %s/%s instruments.",
        total,
        total,
    )

    if not results:
        return pd.DataFrame(
            columns=OUTPUT_COLUMNS
        )

    result_df = pd.DataFrame(results)

    # ========================================================
    # SORT
    #
    # Strong Pullback first, then score descending.
    # ========================================================

    result_df["signal_priority"] = (
        result_df["signal"]
        .map(
            {
                "STRONG PULLBACK": 0,
                "PULLBACK": 1,
            }
        )
    )

    result_df = result_df.sort_values(
        [
            "signal_priority",
            "pullback_score",
            "pullback_percentage",
            "price_return_20d",
        ],
        ascending=[
            True,
            False,
            False,
            False,
        ],
    ).reset_index(drop=True)

    result_df = result_df.drop(
        columns=["signal_priority"]
    )

    return result_df


# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(result_df):
    """
    Save results to CSV.
    """

    if result_df.empty:

        if OUTPUT_FILE.exists():
            OUTPUT_FILE.unlink()

        logger.info(
            "No opportunities found. "
            "Old result file removed if it existed."
        )

        return

    result_df.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    logger.info(
        "Results saved to: %s",
        OUTPUT_FILE,
    )


# ============================================================
# DISPLAY RESULTS
# ============================================================

def display_results(result_df):
    """
    Display results in terminal.
    """

    if result_df.empty:

        print()
        print("=" * 120)
        print("NO PULLBACK OPPORTUNITIES FOUND")
        print("=" * 120)
        print()

        return

    output = result_df[
        OUTPUT_COLUMNS
    ].copy()

    # --------------------------------------------------------
    # Round numerical values
    # --------------------------------------------------------

    numeric_columns = output.select_dtypes(
        include=["float64", "float32"]
    ).columns

    output[numeric_columns] = output[
        numeric_columns
    ].round(2)

    # ========================================================
    # STRONG PULLBACK
    # ========================================================

    strong = output[
        output["signal"]
        == "STRONG PULLBACK"
    ]

    if not strong.empty:

        print()
        print("=" * 140)
        print("STRONG PULLBACK OPPORTUNITIES")
        print("=" * 140)

        print(
            strong.to_string(
                index=False
            )
        )

    # ========================================================
    # NORMAL PULLBACK
    # ========================================================

    normal = output[
        output["signal"]
        == "PULLBACK"
    ]

    if not normal.empty:

        print()
        print("=" * 140)
        print("PULLBACK OPPORTUNITIES")
        print("=" * 140)

        print(
            normal.to_string(
                index=False
            )
        )

    # ========================================================
    # SUMMARY
    # ========================================================

    strong_count = len(strong)

    normal_count = len(normal)

    total_count = len(output)

    highest_score = output[
        "pullback_score"
    ].max()

    average_score = output[
        "pullback_score"
    ].mean()

    print()
    print("=" * 60)
    print("PULLBACK SUMMARY")
    print("=" * 60)

    print(
        f"STRONG PULLBACK       : {strong_count}"
    )

    print(
        f"PULLBACK              : {normal_count}"
    )

    print("-" * 60)

    print(
        f"Total opportunities   : {total_count}"
    )

    print(
        f"Highest pullback score: "
        f"{highest_score:.2f}"
    )

    print(
        f"Average pullback score: "
        f"{average_score:.2f}"
    )

    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

def main():

    start_time = time.perf_counter()

    logger.info("=" * 70)
    logger.info("PULLBACK SCANNER STARTED")
    logger.info("=" * 70)

    try:

        # ----------------------------------------------------
        # Load data
        # ----------------------------------------------------

        df = load_historical_data()

        # ----------------------------------------------------
        # Run scanner
        # ----------------------------------------------------

        result_df = run_pullback_scanner(df)

        # ----------------------------------------------------
        # Save results
        # ----------------------------------------------------

        save_results(result_df)

        # ----------------------------------------------------
        # Statistics
        # ----------------------------------------------------

        if not result_df.empty:

            strong_count = (
                result_df["signal"]
                .eq("STRONG PULLBACK")
                .sum()
            )

            normal_count = (
                result_df["signal"]
                .eq("PULLBACK")
                .sum()
            )

            highest_score = (
                result_df["pullback_score"]
                .max()
            )

            average_score = (
                result_df["pullback_score"]
                .mean()
            )

        else:

            strong_count = 0
            normal_count = 0
            highest_score = 0
            average_score = 0

        # ----------------------------------------------------
        # Log summary
        # ----------------------------------------------------

        logger.info(
            "Pullback opportunities found: %s",
            len(result_df),
        )

        logger.info(
            "Strong pullbacks: %s",
            strong_count,
        )

        logger.info(
            "Normal pullbacks: %s",
            normal_count,
        )

        if not result_df.empty:

            logger.info(
                "Highest signal score: %.2f",
                highest_score,
            )

            logger.info(
                "Average signal score: %.2f",
                average_score,
            )

        # ----------------------------------------------------
        # Display
        # ----------------------------------------------------

        display_results(result_df)

        elapsed = (
            time.perf_counter()
            - start_time
        )

        logger.info(
            "Scanner execution time: %.2f seconds",
            elapsed,
        )

        logger.info("=" * 70)
        logger.info("PULLBACK SCANNER COMPLETED")
        logger.info(
            "Opportunities: %s",
            len(result_df),
        )
        logger.info("=" * 70)

    except Exception as exc:

        logger.exception(
            "PULLBACK SCANNER FAILED: %s",
            exc,
        )

        raise


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()