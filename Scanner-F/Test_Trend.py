"""
============================================================
STRONG BULLISH TREND SCANNER
============================================================

PURPOSE
-------
Find ONLY stocks that are currently showing a strong
bullish daily trend.

The scanner uses COMPLETED DAILY OHLCV candles only.

It does NOT use:

    - Live market data
    - Upstox API
    - WebSocket
    - Redis
    - Intraday candles


============================================================
INPUT
============================================================

Input file:

    ohlcv.csv

CSV separator:

    ;

Input columns:

    instrument_key
    name
    timestamp
    open
    high
    low
    close
    volume
    open_interest
    Till (Date)
    CreationDate
    Date


Mapping:

    name -> stock_name
    Date -> date


============================================================
STRONG BULLISH DEFINITION
============================================================

A stock is reported ONLY when ALL conditions pass.

    1. Close > EMA 20
    2. EMA 20 > EMA 50
    3. EMA 50 > EMA 200
    4. EMA 20 is rising
    5. EMA 50 is rising
    6. 20-day return >= 5%
    7. EMA 20 / EMA 50 spread >= 2%
    8. ADX >= 25
    9. RSI between 55 and 75

If even ONE condition fails:

    DO NOT REPORT THE STOCK


============================================================
OUTPUT
============================================================

Output file:

    trend_results.csv

Only:

    STRONG BULLISH

stocks are reported.
"""


import logging
import time
from pathlib import Path

import pandas as pd
import pandas_ta as ta


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

INPUT_FILE = PROJECT_ROOT / "ohlcv.csv"
OUTPUT_FILE = PROJECT_ROOT / "trend_results.csv"


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# ============================================================
# CONFIGURATION
# ============================================================

EMA_FAST = 20
EMA_MEDIUM = 50
EMA_LONG = 200

ADX_LENGTH = 14
RSI_LENGTH = 14

PRICE_LOOKBACK = 20
SLOPE_LOOKBACK = 10

MIN_PRICE_RETURN = 5.0

MIN_EMA_SPREAD = 2.0

MIN_ADX = 25.0

MIN_RSI = 55.0
MAX_RSI = 75.0

MIN_HISTORY = 220


# ============================================================
# REQUIRED INPUT COLUMNS
# ============================================================

REQUIRED_COLUMNS = [
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
# LOAD AND CLEAN HISTORICAL DATA
# ============================================================

def load_historical_data():

    logger.info("=" * 70)
    logger.info("READING HISTORICAL DATA")
    logger.info("=" * 70)

    logger.info(
        "Input file: %s",
        INPUT_FILE
    )

    if not INPUT_FILE.exists():

        logger.error(
            "Input file does not exist: %s",
            INPUT_FILE
        )

        return pd.DataFrame()

    try:

        df = pd.read_csv(
            INPUT_FILE,
            sep=";"
        )

    except Exception as exc:

        logger.exception(
            "Failed to read CSV: %s",
            exc
        )

        return pd.DataFrame()

    logger.info(
        "Rows loaded: %s",
        len(df)
    )

    if df.empty:

        logger.warning(
            "Historical DataFrame is empty."
        )

        return df

    # --------------------------------------------------------
    # Validate required columns
    # --------------------------------------------------------

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:

        logger.error(
            "Missing required columns: %s",
            missing_columns
        )

        return pd.DataFrame()

    # --------------------------------------------------------
    # Keep only required columns
    # --------------------------------------------------------

    df = df[
        REQUIRED_COLUMNS
    ].copy()

    # --------------------------------------------------------
    # Rename columns to scanner-standard names
    # --------------------------------------------------------

    df = df.rename(
        columns={
            "name": "stock_name",
            "Date": "date",
        }
    )

    # --------------------------------------------------------
    # Clean instrument key and stock name
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
    # Parse date
    # --------------------------------------------------------

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
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
            errors="coerce"
        )

    # --------------------------------------------------------
    # Remove invalid / missing rows
    # --------------------------------------------------------

    before_cleaning = len(df)

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
    ).copy()

    removed_missing = (
        before_cleaning - len(df)
    )

    if removed_missing > 0:

        logger.warning(
            "Removed %s rows with missing/invalid required values.",
            removed_missing
        )

    # --------------------------------------------------------
    # Validate OHLCV
    # --------------------------------------------------------

    invalid_ohlcv = (
        (df["open"] <= 0)
        | (df["high"] <= 0)
        | (df["low"] <= 0)
        | (df["close"] <= 0)
        | (df["volume"] < 0)
        | (df["high"] < df["low"])
        | (df["high"] < df["open"])
        | (df["high"] < df["close"])
        | (df["low"] > df["open"])
        | (df["low"] > df["close"])
    )

    invalid_count = int(
        invalid_ohlcv.sum()
    )

    if invalid_count > 0:

        logger.warning(
            "Removed %s rows with invalid OHLCV values.",
            invalid_count
        )

        df = df[
            ~invalid_ohlcv
        ].copy()

    # --------------------------------------------------------
    # Remove duplicate instrument/date rows
    # --------------------------------------------------------

    duplicate_count = int(
        df.duplicated(
            subset=[
                "instrument_key",
                "date",
            ],
            keep="last"
        ).sum()
    )

    if duplicate_count > 0:

        logger.warning(
            "Removing %s duplicate instrument/date rows.",
            duplicate_count
        )

        df = df.drop_duplicates(
            subset=[
                "instrument_key",
                "date",
            ],
            keep="last"
        )

    # --------------------------------------------------------
    # Sort data
    # --------------------------------------------------------

    df = df.sort_values(
        [
            "instrument_key",
            "date",
        ]
    ).reset_index(
        drop=True
    )

    # --------------------------------------------------------
    # Final statistics
    # --------------------------------------------------------

    logger.info(
        "Valid rows        : %s",
        len(df)
    )

    logger.info(
        "Unique instruments: %s",
        df["instrument_key"].nunique()
    )

    logger.info(
        "First date        : %s",
        df["date"].min().date()
    )

    logger.info(
        "Latest date       : %s",
        df["date"].max().date()
    )

    logger.info(
        "Historical data successfully loaded."
    )

    return df


# ============================================================
# CALCULATE INDICATORS
# ============================================================

def calculate_indicators(stock_df):

    stock_df = stock_df.copy()

    # --------------------------------------------------------
    # EMA 20
    # --------------------------------------------------------

    stock_df["ema_20"] = ta.ema(
        stock_df["close"],
        length=EMA_FAST
    )

    # --------------------------------------------------------
    # EMA 50
    # --------------------------------------------------------

    stock_df["ema_50"] = ta.ema(
        stock_df["close"],
        length=EMA_MEDIUM
    )

    # --------------------------------------------------------
    # EMA 200
    # --------------------------------------------------------

    stock_df["ema_200"] = ta.ema(
        stock_df["close"],
        length=EMA_LONG
    )

    # --------------------------------------------------------
    # ADX 14
    # --------------------------------------------------------

    adx_df = ta.adx(
        stock_df["high"],
        stock_df["low"],
        stock_df["close"],
        length=ADX_LENGTH
    )

    if adx_df is not None:

        adx_column = f"ADX_{ADX_LENGTH}"

        if adx_column in adx_df.columns:

            stock_df["adx"] = (
                adx_df[adx_column]
            )

        else:

            stock_df["adx"] = float("nan")

    else:

        stock_df["adx"] = float("nan")

    # --------------------------------------------------------
    # RSI 14
    # --------------------------------------------------------

    stock_df["rsi"] = ta.rsi(
        stock_df["close"],
        length=RSI_LENGTH
    )

    # --------------------------------------------------------
    # 20-day price return
    # --------------------------------------------------------

    stock_df["price_return_20d"] = (
        stock_df["close"]
        .pct_change(PRICE_LOOKBACK)
        * 100
    )

    # --------------------------------------------------------
    # EMA 20 / EMA 50 spread
    #
    # Example:
    #
    # EMA20 = 105
    # EMA50 = 100
    #
    # Spread = 5%
    # --------------------------------------------------------

    stock_df["ema_spread_percentage"] = (
        (
            stock_df["ema_20"]
            - stock_df["ema_50"]
        )
        / stock_df["ema_50"]
        * 100
    )

    # --------------------------------------------------------
    # EMA 20 slope
    #
    # Positive = EMA20 rising
    # Negative = EMA20 falling
    # --------------------------------------------------------

    ema_20_previous = (
        stock_df["ema_20"]
        .shift(SLOPE_LOOKBACK)
    )

    stock_df["ema_20_slope"] = (
        (
            stock_df["ema_20"]
            - ema_20_previous
        )
        / ema_20_previous
        * 100
    )

    # --------------------------------------------------------
    # EMA 50 slope
    #
    # Positive = EMA50 rising
    # Negative = EMA50 falling
    # --------------------------------------------------------

    ema_50_previous = (
        stock_df["ema_50"]
        .shift(SLOPE_LOOKBACK)
    )

    stock_df["ema_50_slope"] = (
        (
            stock_df["ema_50"]
            - ema_50_previous
        )
        / ema_50_previous
        * 100
    )

    return stock_df


# ============================================================
# ANALYZE ONE STOCK
# ============================================================

def analyze_stock(stock_df):

    # --------------------------------------------------------
    # EMA200 requires sufficient history.
    # --------------------------------------------------------

    if len(stock_df) < MIN_HISTORY:

        return None

    stock_df = calculate_indicators(
        stock_df
    )

    # --------------------------------------------------------
    # Latest row = latest completed candle available
    # --------------------------------------------------------

    latest = stock_df.iloc[-1]

    # --------------------------------------------------------
    # Extract values
    # --------------------------------------------------------

    close = latest["close"]

    ema_20 = latest["ema_20"]

    ema_50 = latest["ema_50"]

    ema_200 = latest["ema_200"]

    adx = latest["adx"]

    rsi = latest["rsi"]

    price_return = (
        latest["price_return_20d"]
    )

    ema_spread = (
        latest["ema_spread_percentage"]
    )

    ema_20_slope = (
        latest["ema_20_slope"]
    )

    ema_50_slope = (
        latest["ema_50_slope"]
    )

    # --------------------------------------------------------
    # Validate indicator values
    # --------------------------------------------------------

    values = [
        close,
        ema_20,
        ema_50,
        ema_200,
        adx,
        rsi,
        price_return,
        ema_spread,
        ema_20_slope,
        ema_50_slope,
    ]

    if any(
        pd.isna(value)
        for value in values
    ):

        return None

    # ========================================================
    # STRONG BULLISH CONDITIONS
    # ========================================================

    condition_1 = (
        close > ema_20
    )

    condition_2 = (
        ema_20 > ema_50
    )

    condition_3 = (
        ema_50 > ema_200
    )

    condition_4 = (
        ema_20_slope > 0
    )

    condition_5 = (
        ema_50_slope > 0
    )

    condition_6 = (
        price_return >= MIN_PRICE_RETURN
    )

    condition_7 = (
        ema_spread >= MIN_EMA_SPREAD
    )

    condition_8 = (
        adx >= MIN_ADX
    )

    condition_9 = (
        MIN_RSI <= rsi <= MAX_RSI
    )

    # ========================================================
    # ALL 9 CONDITIONS MUST PASS
    # ========================================================

    strong_bullish = all(
        [
            condition_1,
            condition_2,
            condition_3,
            condition_4,
            condition_5,
            condition_6,
            condition_7,
            condition_8,
            condition_9,
        ]
    )

    # --------------------------------------------------------
    # If ANY condition fails, ignore stock.
    # --------------------------------------------------------

    if not strong_bullish:

        return None

    # ========================================================
    # TREND SCORE
    #
    # Since all 9 conditions passed:
    #
    # 9 / 9 = 100
    #
    # Therefore every reported stock gets 100.
    # This preserves the original strategy exactly.
    # ========================================================

    passed_conditions = sum(
        [
            condition_1,
            condition_2,
            condition_3,
            condition_4,
            condition_5,
            condition_6,
            condition_7,
            condition_8,
            condition_9,
        ]
    )

    trend_score = (
        passed_conditions / 9
    ) * 100

    # ========================================================
    # RESULT
    # ========================================================

    return {
        "instrument_key":
            latest["instrument_key"],

        "stock_name":
            latest["stock_name"],

        "date":
            latest["date"],

        "close":
            round(close, 2),

        "price_return_20d":
            round(price_return, 2),

        "ema_20":
            round(ema_20, 2),

        "ema_50":
            round(ema_50, 2),

        "ema_200":
            round(ema_200, 2),

        "ema_spread_percentage":
            round(ema_spread, 2),

        "ema_20_slope":
            round(ema_20_slope, 2),

        "ema_50_slope":
            round(ema_50_slope, 2),

        "rsi":
            round(rsi, 2),

        "adx":
            round(adx, 2),

        "trend_score":
            round(trend_score, 2),

        "trend":
            "STRONG BULLISH",
    }


# ============================================================
# RUN SCANNER
# ============================================================

def run_trend_scanner(df):

    logger.info("=" * 70)
    logger.info(
        "RUNNING STRONG BULLISH TREND ANALYSIS"
    )
    logger.info("=" * 70)

    opportunities = []

    instruments = (
        df["instrument_key"]
        .unique()
    )

    total = len(instruments)

    processed = 0

    for instrument_key in instruments:

        stock_df = df[
            df["instrument_key"]
            == instrument_key
        ].copy()

        result = analyze_stock(
            stock_df
        )

        if result is not None:

            opportunities.append(
                result
            )

        processed += 1

    logger.info(
        "Processed %s/%s instruments.",
        processed,
        total
    )

    return pd.DataFrame(
        opportunities
    )


# ============================================================
# DISPLAY RESULTS
# ============================================================

def display_results(results):

    print()

    print("=" * 120)

    print(
        "STRONG BULLISH TREND OPPORTUNITIES"
    )

    print("=" * 120)

    if results.empty:

        print(
            "No strong bullish trend "
            "opportunities found."
        )

        print("=" * 120)

        return

    # --------------------------------------------------------
    # Sort strongest first
    # --------------------------------------------------------

    results = results.sort_values(
        [
            "trend_score",
            "adx",
            "price_return_20d",
            "ema_spread_percentage",
        ],
        ascending=False
    ).reset_index(
        drop=True
    )

    display_columns = [
        "instrument_key",
        "stock_name",
        "date",
        "close",
        "price_return_20d",
        "ema_20",
        "ema_50",
        "ema_200",
        "ema_spread_percentage",
        "ema_20_slope",
        "ema_50_slope",
        "rsi",
        "adx",
        "trend_score",
        "trend",
    ]

    print(
        results[
            display_columns
        ].to_string(
            index=False
        )
    )

    # ========================================================
    # SUMMARY
    # ========================================================

    print()

    print("=" * 60)

    print(
        "TREND SUMMARY"
    )

    print("=" * 60)

    print(
        f"STRONG BULLISH       : "
        f"{len(results)}"
    )

    print(
        f"Highest trend score  : "
        f"{results['trend_score'].max():.2f}"
    )

    print(
        f"Average trend score  : "
        f"{results['trend_score'].mean():.2f}"
    )

    print(
        f"Average 20D return   : "
        f"{results['price_return_20d'].mean():.2f}%"
    )

    print(
        f"Average EMA spread   : "
        f"{results['ema_spread_percentage'].mean():.2f}%"
    )

    print(
        f"Average RSI          : "
        f"{results['rsi'].mean():.2f}"
    )

    print(
        f"Average ADX          : "
        f"{results['adx'].mean():.2f}"
    )

    print("=" * 60)


# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(results):

    if results.empty:

        # ----------------------------------------------------
        # Remove stale result file
        # ----------------------------------------------------

        if OUTPUT_FILE.exists():

            try:

                OUTPUT_FILE.unlink()

                logger.info(
                    "Removed stale output file: %s",
                    OUTPUT_FILE
                )

            except Exception as exc:

                logger.warning(
                    "Could not remove stale output file: %s",
                    exc
                )

        logger.info(
            "No opportunities to save."
        )

        return

    try:

        results.to_csv(
            OUTPUT_FILE,
            index=False
        )

        logger.info(
            "Results saved: %s",
            OUTPUT_FILE
        )

        logger.info(
            "Result rows: %s",
            len(results)
        )

    except Exception as exc:

        logger.exception(
            "Failed to save results: %s",
            exc
        )

        raise


# ============================================================
# MAIN
# ============================================================

def main():

    start_time = time.perf_counter()

    logger.info("=" * 70)

    logger.info(
        "STRONG BULLISH TREND SCANNER STARTED"
    )

    logger.info("=" * 70)

    # --------------------------------------------------------
    # Load data
    # --------------------------------------------------------

    df = load_historical_data()

    if df.empty:

        logger.error(
            "No historical data available."
        )

        return

    # --------------------------------------------------------
    # Run scanner
    # --------------------------------------------------------

    results = run_trend_scanner(
        df
    )

    # --------------------------------------------------------
    # Sort results
    # --------------------------------------------------------

    if not results.empty:

        results = results.sort_values(
            [
                "trend_score",
                "adx",
                "price_return_20d",
                "ema_spread_percentage",
            ],
            ascending=False
        ).reset_index(
            drop=True
        )

    # --------------------------------------------------------
    # Save results
    # --------------------------------------------------------

    save_results(
        results
    )

    # --------------------------------------------------------
    # Display results
    # --------------------------------------------------------

    display_results(
        results
    )

    # --------------------------------------------------------
    # Execution time
    # --------------------------------------------------------

    execution_time = (
        time.perf_counter()
        - start_time
    )

    logger.info("=" * 70)

    logger.info(
        "STRONG BULLISH TREND SCANNER COMPLETED"
    )

    logger.info(
        "Opportunities: %s",
        len(results)
    )

    logger.info(
        "Execution time: %.2f seconds",
        execution_time
    )

    logger.info("=" * 70)


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        logger.warning(
            "Scanner interrupted by user."
        )

    except Exception as exc:

        logger.exception(
            "Fatal scanner error: %s",
            exc
        )

        raise
