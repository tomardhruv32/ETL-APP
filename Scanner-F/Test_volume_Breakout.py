"""
============================================================
VOLUME BREAKOUT SCANNER
============================================================

PURPOSE
-------
Find stocks where an unusually large increase in volume is
accompanied by a REAL PRICE BREAKOUT above the previous
20-day high.

The scanner uses ONLY completed daily OHLCV candles.

DATA SOURCE
-----------
ohlcv.csv

The scanner does NOT call:

    - Upstox API
    - Live market data
    - WebSocket
    - Redis
    - Stage 1 historical data manager


============================================================
INPUT CSV
============================================================

Expected columns:

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

Used columns:

    instrument_key
    name
    open
    high
    low
    close
    volume
    Date

Mapping:

    name -> stock_name
    Date -> date


============================================================
VOLUME BREAKOUT LOGIC
============================================================

A stock MUST satisfy ALL of the following:

1. REAL PRICE BREAKOUT

       Latest close > previous 20-day high

2. HIGH VOLUME

       Latest volume >= 2.0 × previous 20-day
       average volume

3. BULLISH EMA STRUCTURE

       EMA20 > EMA50


============================================================
STRONG VOLUME BREAKOUT
============================================================

All normal conditions PLUS:

    Volume ratio >= 3.0
    Price change >= 5.0%
    Breakout percentage >= 2.0%


============================================================
SCORING
============================================================

Maximum score = 100.

Volume strength       = 30 points
Price breakout        = 30 points
EMA trend             = 20 points
Price momentum        = 20 points

The score NEVER overrides mandatory conditions.


============================================================
OUTPUT
============================================================

    instrument_key
    stock_name
    date
    close
    volume_ratio
    avg_volume_20d
    price_change_percentage
    previous_20d_high
    breakout_percentage
    ema_20
    ema_50
    signal_score
    signal
"""

from __future__ import annotations

import logging
import time
from pathlib import Path

import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

INPUT_FILE = PROJECT_ROOT / "ohlcv.csv"

OUTPUT_FILE = PROJECT_ROOT / "volume_breakout_results.csv"


# ============================================================
# SCANNER SETTINGS
# ============================================================

# Minimum candles required.
#
# EMA50 needs 50 candles.
# Previous 20-day reference needs 20 candles.
#
# 51 is therefore the minimum required to evaluate the
# latest candle correctly.

MIN_CANDLES = 51


# EMA periods

EMA_FAST = 20
EMA_SLOW = 50


# Previous high and volume reference period

LOOKBACK_PERIOD = 20


# ============================================================
# VOLUME REQUIREMENTS
# ============================================================

# Minimum volume ratio required for any breakout.

MIN_VOLUME_RATIO = 2.0


# Minimum volume ratio for a strong breakout.

STRONG_VOLUME_RATIO = 3.0


# ============================================================
# STRONG BREAKOUT REQUIREMENTS
# ============================================================

STRONG_PRICE_CHANGE = 5.0

STRONG_BREAKOUT_PERCENTAGE = 2.0


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# ============================================================
# LOAD AND VALIDATE DATA
# ============================================================

def load_historical_data() -> pd.DataFrame:
    """
    Load and validate OHLCV data from ohlcv.csv.
    """

    logger.info("=" * 70)
    logger.info("READING HISTORICAL DATA")
    logger.info("=" * 70)

    logger.info(
        "Input file: %s",
        INPUT_FILE,
    )

    # --------------------------------------------------------
    # Check input file.
    # --------------------------------------------------------

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
        )

    # --------------------------------------------------------
    # Read CSV.
    #
    # Your CSV uses semicolon as separator.
    # --------------------------------------------------------

    df = pd.read_csv(
        INPUT_FILE,
        sep=";",
    )

    rows_loaded = len(df)

    logger.info(
        "Rows loaded: %d",
        rows_loaded,
    )

    # --------------------------------------------------------
    # Required input columns.
    # --------------------------------------------------------

    required_columns = {
        "instrument_key",
        "name",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "Date",
    }

    missing_columns = (
        required_columns - set(df.columns)
    )

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            f"{sorted(missing_columns)}"
        )

    # --------------------------------------------------------
    # Rename columns to internal scanner names.
    # --------------------------------------------------------

    df = df.rename(
        columns={
            "name": "stock_name",
            "Date": "date",
        }
    )

    # --------------------------------------------------------
    # Convert date.
    # --------------------------------------------------------

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce",
    )

    # --------------------------------------------------------
    # Convert numeric columns.
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
    # Remove rows with missing required values.
    # --------------------------------------------------------

    before_dropna = len(df)

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

    removed_missing = (
        before_dropna - len(df)
    )

    if removed_missing > 0:
        logger.warning(
            "Removed %d rows with missing/invalid values.",
            removed_missing,
        )

    # --------------------------------------------------------
    # Validate OHLCV values.
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

    df = df.loc[
        valid_ohlcv
    ].copy()

    removed_invalid = (
        before_validation - len(df)
    )

    if removed_invalid > 0:
        logger.warning(
            "Removed %d invalid OHLCV rows.",
            removed_invalid,
        )

    # --------------------------------------------------------
    # Sort by instrument and date.
    # --------------------------------------------------------

    df = df.sort_values(
        [
            "instrument_key",
            "date",
        ]
    )

    # --------------------------------------------------------
    # Remove duplicate candles.
    #
    # Only one candle should exist for an instrument/date.
    # --------------------------------------------------------

    before_duplicates = len(df)

    df = df.drop_duplicates(
        subset=[
            "instrument_key",
            "date",
        ],
        keep="last",
    )

    removed_duplicates = (
        before_duplicates - len(df)
    )

    if removed_duplicates > 0:
        logger.warning(
            "Removed %d duplicate candles.",
            removed_duplicates,
        )

    # --------------------------------------------------------
    # Reset index.
    # --------------------------------------------------------

    df = df.reset_index(
        drop=True
    )

    # --------------------------------------------------------
    # Final statistics.
    # --------------------------------------------------------

    logger.info(
        "Valid rows        : %d",
        len(df),
    )

    logger.info(
        "Unique instruments: %d",
        df["instrument_key"].nunique(),
    )

    if not df.empty:

        logger.info(
            "First date        : %s",
            df["date"].min().date(),
        )

        logger.info(
            "Latest date       : %s",
            df["date"].max().date(),
        )

    logger.info(
        "Historical data successfully loaded."
    )

    return df


# ============================================================
# SIGNAL SCORE
# ============================================================

def calculate_signal_score(
    volume_ratio: float,
    breakout_percentage: float,
    ema_20: float,
    ema_50: float,
    close: float,
    previous_close: float,
) -> float:
    """
    Calculate a 0-100 volume breakout quality score.

    IMPORTANT:

    This score is calculated ONLY after all mandatory
    conditions have passed.

    The score does NOT decide whether a stock is returned.
    """

    score = 0.0

    # ========================================================
    # 1. VOLUME STRENGTH
    # Maximum = 30 points
    # ========================================================

    if volume_ratio >= 5.0:
        score += 30

    elif volume_ratio >= 3.0:
        score += 25

    elif volume_ratio >= 2.5:
        score += 20

    elif volume_ratio >= 2.0:
        score += 15

    # ========================================================
    # 2. PRICE BREAKOUT
    # Maximum = 30 points
    # ========================================================

    if breakout_percentage >= 5.0:
        score += 30

    elif breakout_percentage >= 3.0:
        score += 25

    elif breakout_percentage >= 2.0:
        score += 20

    elif breakout_percentage >= 1.0:
        score += 15

    elif breakout_percentage > 0:
        score += 10

    # ========================================================
    # 3. EMA TREND
    # Maximum = 20 points
    # ========================================================

    if ema_20 > ema_50:
        score += 20

    # ========================================================
    # 4. PRICE MOMENTUM
    # Maximum = 20 points
    # ========================================================

    if previous_close > 0:

        price_change_percentage = (
            (
                close - previous_close
            )
            / previous_close
            * 100
        )

        if price_change_percentage >= 10:
            score += 20

        elif price_change_percentage >= 5:
            score += 15

        elif price_change_percentage >= 2:
            score += 10

        elif price_change_percentage > 0:
            score += 5

    # --------------------------------------------------------
    # Ensure score never exceeds 100.
    # --------------------------------------------------------

    return round(
        min(score, 100.0),
        2,
    )


# ============================================================
# ANALYZE ONE INSTRUMENT
# ============================================================

def analyze_instrument(
    group: pd.DataFrame,
):
    """
    Analyze the latest completed candle of one instrument.

    Returns:
        dict if breakout found
        None otherwise
    """

    # --------------------------------------------------------
    # Always sort chronologically.
    # --------------------------------------------------------

    group = group.sort_values(
        "date"
    ).copy()

    # --------------------------------------------------------
    # Check minimum history.
    # --------------------------------------------------------

    if len(group) < MIN_CANDLES:
        return None

    # ========================================================
    # EMA20
    # ========================================================

    group["ema_20"] = (
        group["close"]
        .ewm(
            span=EMA_FAST,
            adjust=False,
            min_periods=EMA_FAST,
        )
        .mean()
    )

    # ========================================================
    # EMA50
    # ========================================================

    group["ema_50"] = (
        group["close"]
        .ewm(
            span=EMA_SLOW,
            adjust=False,
            min_periods=EMA_SLOW,
        )
        .mean()
    )

    # ========================================================
    # PREVIOUS 20-DAY HIGH
    # ========================================================

    # rolling(20) calculates the previous 20 candles.
    #
    # shift(1) ensures the current/latest candle is NOT
    # included in its own breakout reference.

    group["previous_20d_high"] = (
        group["high"]
        .rolling(
            window=LOOKBACK_PERIOD,
            min_periods=LOOKBACK_PERIOD,
        )
        .max()
        .shift(1)
    )

    # ========================================================
    # PREVIOUS 20-DAY AVERAGE VOLUME
    # ========================================================

    # The current candle's volume is excluded.

    group["avg_volume_20d"] = (
        group["volume"]
        .rolling(
            window=LOOKBACK_PERIOD,
            min_periods=LOOKBACK_PERIOD,
        )
        .mean()
        .shift(1)
    )

    # ========================================================
    # VOLUME RATIO
    # ========================================================

    group["volume_ratio"] = (
        group["volume"]
        / group["avg_volume_20d"]
    )

    # ========================================================
    # PREVIOUS CLOSE
    # ========================================================

    group["previous_close"] = (
        group["close"].shift(1)
    )

    # ========================================================
    # PRICE CHANGE %
    # ========================================================

    group["price_change_percentage"] = (
        (
            group["close"]
            - group["previous_close"]
        )
        / group["previous_close"]
        * 100
    )

    # ========================================================
    # BREAKOUT %
    # ========================================================

    group["breakout_percentage"] = (
        (
            group["close"]
            - group["previous_20d_high"]
        )
        / group["previous_20d_high"]
        * 100
    )

    # ========================================================
    # LATEST COMPLETED CANDLE
    # ========================================================

    latest = group.iloc[-1]

    # ========================================================
    # VALIDATE CALCULATED VALUES
    # ========================================================

    calculated_values = [
        latest["ema_20"],
        latest["ema_50"],
        latest["previous_20d_high"],
        latest["avg_volume_20d"],
        latest["volume_ratio"],
        latest["previous_close"],
        latest["price_change_percentage"],
        latest["breakout_percentage"],
    ]

    if not all(
        pd.notna(value)
        for value in calculated_values
    ):
        return None

    # ========================================================
    # EXTRACT VALUES
    # ========================================================

    close_price = float(
        latest["close"]
    )

    current_volume = float(
        latest["volume"]
    )

    ema_20 = float(
        latest["ema_20"]
    )

    ema_50 = float(
        latest["ema_50"]
    )

    previous_20d_high = float(
        latest["previous_20d_high"]
    )

    avg_volume_20d = float(
        latest["avg_volume_20d"]
    )

    volume_ratio = float(
        latest["volume_ratio"]
    )

    previous_close = float(
        latest["previous_close"]
    )

    price_change_percentage = float(
        latest["price_change_percentage"]
    )

    breakout_percentage = float(
        latest["breakout_percentage"]
    )

    # ========================================================
    # MANDATORY CONDITION 1
    # REAL PRICE BREAKOUT
    # ========================================================

    # IMPORTANT:
    #
    # Latest close MUST be greater than the previous
    # 20-day high.
    #
    # Equal is NOT enough.
    #
    # Below is NOT enough.
    #
    # Only:
    #
    # close > previous_20d_high
    #
    # qualifies.

    real_price_breakout = (
        close_price
        > previous_20d_high
    )

    if not real_price_breakout:
        return None

    # ========================================================
    # MANDATORY CONDITION 2
    # HIGH VOLUME
    # ========================================================

    high_volume = (
        volume_ratio
        >= MIN_VOLUME_RATIO
    )

    if not high_volume:
        return None

    # ========================================================
    # MANDATORY CONDITION 3
    # BULLISH EMA STRUCTURE
    # ========================================================

    bullish_ema = (
        ema_20
        > ema_50
    )

    if not bullish_ema:
        return None

    # ========================================================
    # STRONG VOLUME BREAKOUT
    # ========================================================

    strong_breakout = (
        volume_ratio
        >= STRONG_VOLUME_RATIO
        and price_change_percentage
        >= STRONG_PRICE_CHANGE
        and breakout_percentage
        >= STRONG_BREAKOUT_PERCENTAGE
    )

    if strong_breakout:
        signal = "STRONG VOLUME BREAKOUT"

    else:
        signal = "VOLUME BREAKOUT"

    # ========================================================
    # SIGNAL SCORE
    # ========================================================

    signal_score = calculate_signal_score(
        volume_ratio=volume_ratio,
        breakout_percentage=breakout_percentage,
        ema_20=ema_20,
        ema_50=ema_50,
        close=close_price,
        previous_close=previous_close,
    )

    # ========================================================
    # RETURN RESULT
    # ========================================================

    return {
        "instrument_key": latest[
            "instrument_key"
        ],

        "stock_name": latest[
            "stock_name"
        ],

        "date": latest[
            "date"
        ].date(),

        "close": round(
            close_price,
            2,
        ),

        "volume_ratio": round(
            volume_ratio,
            2,
        ),

        "avg_volume_20d": round(
            avg_volume_20d,
            2,
        ),

        "price_change_percentage": round(
            price_change_percentage,
            2,
        ),

        "previous_20d_high": round(
            previous_20d_high,
            2,
        ),

        "breakout_percentage": round(
            breakout_percentage,
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

        "signal_score": signal_score,

        "signal": signal,
    }


# ============================================================
# RUN SCANNER
# ============================================================

def run_scanner(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Run the volume breakout scanner across all instruments.
    """

    logger.info("=" * 70)
    logger.info(
        "RUNNING VOLUME BREAKOUT ANALYSIS"
    )
    logger.info("=" * 70)

    opportunities = []

    grouped = df.groupby(
        "instrument_key",
        sort=False,
    )

    total_instruments = len(
        grouped
    )

    processed = 0

    # --------------------------------------------------------
    # Analyze every instrument.
    # --------------------------------------------------------

    for _, group in grouped:

        result = analyze_instrument(
            group
        )

        if result is not None:
            opportunities.append(
                result
            )

        processed += 1

    logger.info(
        "Processed %d/%d instruments.",
        processed,
        total_instruments,
    )

    # ========================================================
    # NO RESULTS
    # ========================================================

    if not opportunities:

        logger.info(
            "No volume breakout opportunities found."
        )

        return pd.DataFrame()

    # ========================================================
    # CREATE RESULT DATAFRAME
    # ========================================================

    result_df = pd.DataFrame(
        opportunities
    )

    # ========================================================
    # SIGNAL SORTING
    # ========================================================

    signal_order = {
        "STRONG VOLUME BREAKOUT": 0,
        "VOLUME BREAKOUT": 1,
    }

    result_df["_signal_order"] = (
        result_df["signal"]
        .map(signal_order)
    )

    # --------------------------------------------------------
    # Sort:
    #
    # 1. Strong signals first
    # 2. Highest score
    # 3. Highest volume ratio
    # --------------------------------------------------------

    result_df = result_df.sort_values(
        [
            "_signal_order",
            "signal_score",
            "volume_ratio",
        ],
        ascending=[
            True,
            False,
            False,
        ],
    )

    result_df = result_df.drop(
        columns="_signal_order"
    )

    return result_df.reset_index(
        drop=True
    )


# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(
    result_df: pd.DataFrame,
) -> None:
    """
    Save scanner results to CSV.

    If there are no results, an old output file is removed
    to prevent stale data from being used.
    """

    # --------------------------------------------------------
    # Remove stale output if no opportunities exist.
    # --------------------------------------------------------

    if result_df.empty:

        if OUTPUT_FILE.exists():

            OUTPUT_FILE.unlink()

            logger.info(
                "Removed stale output file: %s",
                OUTPUT_FILE,
            )

        return

    # --------------------------------------------------------
    # Save results.
    # --------------------------------------------------------

    result_df.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    logger.info(
        "Results saved: %s",
        OUTPUT_FILE,
    )

    logger.info(
        "Rows written: %d",
        len(result_df),
    )


# ============================================================
# DISPLAY RESULTS
# ============================================================

def display_results(
    result_df: pd.DataFrame,
) -> None:
    """
    Display scanner results.
    """

    print()

    print("=" * 150)
    print("VOLUME BREAKOUT OPPORTUNITIES")
    print("=" * 150)

    # --------------------------------------------------------
    # No results.
    # --------------------------------------------------------

    if result_df.empty:

        print(
            "No volume breakout opportunities found."
        )

        print("=" * 150)

        return

    # --------------------------------------------------------
    # Columns to display.
    # --------------------------------------------------------

    display_columns = [
        "instrument_key",
        "stock_name",
        "date",
        "close",
        "volume_ratio",
        "avg_volume_20d",
        "price_change_percentage",
        "previous_20d_high",
        "breakout_percentage",
        "ema_20",
        "ema_50",
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

    # ========================================================
    # SUMMARY
    # ========================================================

    strong_count = (
        result_df["signal"]
        .eq(
            "STRONG VOLUME BREAKOUT"
        )
        .sum()
    )

    normal_count = (
        result_df["signal"]
        .eq(
            "VOLUME BREAKOUT"
        )
        .sum()
    )

    highest_score = (
        result_df["signal_score"]
        .max()
    )

    average_score = (
        result_df["signal_score"]
        .mean()
    )

    highest_volume_ratio = (
        result_df["volume_ratio"]
        .max()
    )

    print()

    print("=" * 70)
    print("VOLUME BREAKOUT SUMMARY")
    print("=" * 70)

    print(
        f"STRONG VOLUME BREAKOUT : "
        f"{strong_count}"
    )

    print(
        f"VOLUME BREAKOUT        : "
        f"{normal_count}"
    )

    print("-" * 70)

    print(
        f"Total opportunities     : "
        f"{len(result_df)}"
    )

    print(
        f"Highest signal score    : "
        f"{highest_score:.2f}"
    )

    print(
        f"Average signal score    : "
        f"{average_score:.2f}"
    )

    print(
        f"Highest volume ratio    : "
        f"{highest_volume_ratio:.2f}x"
    )

    print("=" * 70)


# ============================================================
# MAIN
# ============================================================

def main() -> None:
    """
    Main scanner entry point.
    """

    start_time = time.perf_counter()

    logger.info("=" * 70)
    logger.info(
        "VOLUME BREAKOUT SCANNER STARTED"
    )
    logger.info("=" * 70)

    try:

        # ====================================================
        # STEP 1
        # LOAD DATA
        # ====================================================

        historical_data = (
            load_historical_data()
        )

        # ====================================================
        # STEP 2
        # RUN SCANNER
        # ====================================================

        results = run_scanner(
            historical_data
        )

        # ====================================================
        # STEP 3
        # SAVE RESULTS
        # ====================================================

        save_results(
            results
        )

        # ====================================================
        # STEP 4
        # DISPLAY RESULTS
        # ====================================================

        display_results(
            results
        )

        # ====================================================
        # EXECUTION TIME
        # ====================================================

        elapsed = (
            time.perf_counter()
            - start_time
        )

        logger.info("=" * 70)
        logger.info(
            "VOLUME BREAKOUT SCANNER COMPLETED"
        )
        logger.info(
            "Opportunities: %d",
            len(results),
        )
        logger.info(
            "Execution time: %.2f seconds",
            elapsed,
        )
        logger.info("=" * 70)

    except Exception:

        logger.exception(
            "VOLUME BREAKOUT SCANNER FAILED"
        )

        raise


# ============================================================
# PROGRAM ENTRY
# ============================================================

if __name__ == "__main__":
    main()
