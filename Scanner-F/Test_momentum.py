

from __future__ import annotations

import logging
import sys
import time
from pathlib import Path

import pandas as pd
import pandas_ta as ta


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# ============================================================
# PROJECT PATH
# ============================================================

# IMPORTANT:
#
# This file is:
#
# Scanner/
#     Test_momentum.py
#
# Therefore .parent points directly to Scanner.
#
# DO NOT use .parent.parent here.
#

PROJECT_ROOT = Path(__file__).resolve().parent


# ============================================================
# FILE PATHS
# ============================================================

HISTORICAL_DATA_FILE = (
    PROJECT_ROOT / "ohlcv.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT / "momentum_results.csv"
)


# ============================================================
# MOMENTUM CONFIGURATION
# ============================================================

MOMENTUM_PERIOD = 20

MIN_MOMENTUM_PERCENTAGE = 5.0

VOLUME_PERIOD = 20

EMA_FAST_PERIOD = 20

EMA_SLOW_PERIOD = 50

RSI_PERIOD = 14

MIN_RSI = 60.0

MIN_VOLUME_RATIO = 1.20

ADX_PERIOD = 14


# ============================================================
# SCORE CONFIGURATION
# ============================================================

PRICE_MOMENTUM_SCORE_MAX = 25.0

RSI_SCORE_MAX = 20.0

EMA_SCORE_MAX = 20.0

ADX_SCORE_MAX = 20.0

VOLUME_SCORE_MAX = 15.0


# ============================================================
# SCORE SCALING LIMITS
# ============================================================

MAX_MOMENTUM_FOR_SCORE = 20.0

MAX_RSI_FOR_SCORE = 80.0

MAX_EMA_SPREAD_FOR_SCORE = 10.0

MAX_ADX_FOR_SCORE = 50.0

MAX_VOLUME_RATIO_FOR_SCORE = 3.0


# ============================================================
# INPUT COLUMNS
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
# FUNCTION 1
# READ HISTORICAL DATA
# ============================================================

def read_historical_data() -> pd.DataFrame:

    logger.info("=" * 70)
    logger.info("READING HISTORICAL DATA FROM CSV")
    logger.info("=" * 70)

    # ========================================================
    # CHECK FILE
    # ========================================================

    if not HISTORICAL_DATA_FILE.exists():

        raise FileNotFoundError(
            "Historical data file not found:\n"
            f"{HISTORICAL_DATA_FILE}"
        )

    logger.info(
        "Historical data file: %s",
        HISTORICAL_DATA_FILE,
    )

    # ========================================================
    # READ CSV
    # ========================================================

    try:

        df = pd.read_csv(
            HISTORICAL_DATA_FILE,
            sep=";",
            low_memory=False,
        )

    except Exception as exc:

        raise RuntimeError(
            "Failed to read ohlcv.csv."
        ) from exc

    # ========================================================
    # CHECK EMPTY
    # ========================================================

    if df.empty:

        raise RuntimeError(
            "ohlcv.csv is empty."
        )

    logger.info(
        "Rows loaded: %d",
        len(df),
    )

    logger.info(
        "CSV columns: %s",
        list(df.columns),
    )

    # ========================================================
    # CHECK REQUIRED COLUMNS
    # ========================================================

    missing_columns = [
        column
        for column in REQUIRED_INPUT_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            "ohlcv.csv is missing required columns: "
            f"{missing_columns}"
        )

    # ========================================================
    # COPY
    # ========================================================

    df = df.copy()

    # ========================================================
    # RENAME COLUMNS
    # ========================================================

    df = df.rename(
        columns={
            "name": "stock_name",
            "Date": "date",
        }
    )

    # ========================================================
    # KEEP ONLY REQUIRED COLUMNS
    # ========================================================

    df = df[
        [
            "instrument_key",
            "stock_name",
            "date",
            "open",
            "high",
            "low",
            "close",
            "volume",
        ]
    ].copy()

    # ========================================================
    # CLEAN TEXT
    # ========================================================

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

    # ========================================================
    # CONVERT DATE
    # ========================================================

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce",
    ).dt.normalize()

    # ========================================================
    # CONVERT NUMERIC VALUES
    # ========================================================

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

    # ========================================================
    # REMOVE INVALID REQUIRED VALUES
    # ========================================================

    before_count = len(df)

    df = df.dropna(
        subset=REQUIRED_COLUMNS
    )

    removed_count = (
        before_count - len(df)
    )

    if removed_count > 0:

        logger.warning(
            "Removed %d rows with missing/invalid required values",
            removed_count,
        )

    # ========================================================
    # REMOVE INVALID OHLCV VALUES
    # ========================================================

    before_count = len(df)

    valid_values = (
        (df["open"] > 0)
        & (df["high"] > 0)
        & (df["low"] > 0)
        & (df["close"] > 0)
        & (df["volume"] >= 0)
    )

    df = df[valid_values]

    removed_count = (
        before_count - len(df)
    )

    if removed_count > 0:

        logger.warning(
            "Removed %d rows with invalid OHLCV values",
            removed_count,
        )

    # ========================================================
    # VALIDATE OHLC RELATIONSHIPS
    # ========================================================

    before_count = len(df)

    valid_ohlc = (
        (df["high"] >= df["open"])
        & (df["high"] >= df["close"])
        & (df["high"] >= df["low"])
        & (df["low"] <= df["open"])
        & (df["low"] <= df["close"])
    )

    df = df[valid_ohlc]

    removed_count = (
        before_count - len(df)
    )

    if removed_count > 0:

        logger.warning(
            "Removed %d rows with invalid OHLC relationships",
            removed_count,
        )

    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    before_count = len(df)

    df = df.drop_duplicates(
        subset=[
            "instrument_key",
            "date",
        ],
        keep="last",
    )

    duplicate_count = (
        before_count - len(df)
    )

    if duplicate_count > 0:

        logger.warning(
            "Removed %d duplicate candles",
            duplicate_count,
        )

    # ========================================================
    # SORT
    # ========================================================

    df = df.sort_values(
        [
            "instrument_key",
            "date",
        ]
    ).reset_index(
        drop=True
    )

    # ========================================================
    # FINAL CHECK
    # ========================================================

    if df.empty:

        raise RuntimeError(
            "No valid historical data remains."
        )

    # ========================================================
    # INFORMATION
    # ========================================================

    logger.info(
        "Valid rows: %d",
        len(df),
    )

    logger.info(
        "Unique instruments: %d",
        df["instrument_key"].nunique(),
    )

    logger.info(
        "First date: %s",
        df["date"].min().strftime("%Y-%m-%d"),
    )

    logger.info(
        "Latest date: %s",
        df["date"].max().strftime("%Y-%m-%d"),
    )

    logger.info(
        "Historical data successfully loaded."
    )

    return df


# ============================================================
# FUNCTION 2
# CALCULATE MOMENTUM INDICATORS
# ============================================================

def calculate_momentum_indicators(
    stock_df: pd.DataFrame,
) -> pd.DataFrame:

    stock_df = stock_df.copy()

    # ========================================================
    # SORT
    # ========================================================

    stock_df = stock_df.sort_values(
        "date"
    ).reset_index(
        drop=True
    )

    # ========================================================
    # CLOSE 20 DAYS AGO
    # ========================================================

    stock_df[
        "close_20_days_ago"
    ] = (
        stock_df["close"]
        .shift(MOMENTUM_PERIOD)
    )

    # ========================================================
    # MOMENTUM %
    # ========================================================

    stock_df[
        "momentum_percentage"
    ] = (
        (
            stock_df["close"]
            - stock_df["close_20_days_ago"]
        )
        / stock_df["close_20_days_ago"]
    ) * 100

    # ========================================================
    # PREVIOUS 20-DAY AVERAGE VOLUME
    # ========================================================

    # IMPORTANT:
    #
    # shift(1) excludes the current candle.
    #

    stock_df[
        "previous_volume_average_20"
    ] = (
        stock_df["volume"]
        .rolling(
            window=VOLUME_PERIOD,
            min_periods=VOLUME_PERIOD,
        )
        .mean()
        .shift(1)
    )

    # ========================================================
    # VOLUME RATIO
    # ========================================================

    stock_df["volume_ratio"] = (
        stock_df["volume"]
        / stock_df[
            "previous_volume_average_20"
        ]
    )

    # ========================================================
    # EMA 20
    # ========================================================

    stock_df["ema_20"] = ta.ema(
        stock_df["close"],
        length=EMA_FAST_PERIOD,
    )

    # ========================================================
    # EMA 50
    # ========================================================

    stock_df["ema_50"] = ta.ema(
        stock_df["close"],
        length=EMA_SLOW_PERIOD,
    )

    # ========================================================
    # EMA SPREAD %
    # ========================================================

    stock_df[
        "ema_spread_percentage"
    ] = (
        (
            stock_df["ema_20"]
            - stock_df["ema_50"]
        )
        / stock_df["ema_50"]
    ) * 100

    # ========================================================
    # RSI 14
    # ========================================================

    stock_df["rsi"] = ta.rsi(
        stock_df["close"],
        length=RSI_PERIOD,
    )

    # ========================================================
    # ADX 14
    # ========================================================

    adx = ta.adx(
        high=stock_df["high"],
        low=stock_df["low"],
        close=stock_df["close"],
        length=ADX_PERIOD,
    )

    # ========================================================
    # ADX FAILED
    # ========================================================

    if adx is None:

        stock_df["adx"] = pd.NA

        return stock_df

    # ========================================================
    # FIND ADX COLUMN
    # ========================================================

    adx_columns = [
        column
        for column in adx.columns
        if str(column)
        .upper()
        .startswith(
            f"ADX_{ADX_PERIOD}"
        )
    ]

    # ========================================================
    # FALLBACK
    # ========================================================

    if not adx_columns:

        adx_columns = [
            column
            for column in adx.columns
            if str(column)
            .upper()
            .startswith("ADX_")
        ]

    # ========================================================
    # ADX COLUMN NOT FOUND
    # ========================================================

    if not adx_columns:

        stock_df["adx"] = pd.NA

        return stock_df

    # ========================================================
    # STORE ADX
    # ========================================================

    stock_df["adx"] = (
        adx[adx_columns[0]]
        .to_numpy()
    )

    return stock_df


# ============================================================
# FUNCTION 3
# SIGNAL SCORE
# ============================================================

def calculate_signal_score(
    momentum_percentage: float,
    rsi_value: float,
    ema_spread_percentage: float,
    adx_value: float,
    volume_ratio: float,
) -> dict:

    # ========================================================
    # PRICE MOMENTUM
    # ========================================================

    momentum_strength = max(
        0.0,
        min(
            momentum_percentage,
            MAX_MOMENTUM_FOR_SCORE,
        ),
    )

    price_momentum_score = (
        momentum_strength
        / MAX_MOMENTUM_FOR_SCORE
    ) * PRICE_MOMENTUM_SCORE_MAX

    # ========================================================
    # RSI
    # ========================================================

    rsi_strength = max(
        0.0,
        min(
            rsi_value,
            MAX_RSI_FOR_SCORE,
        ),
    )

    rsi_score = (
        rsi_strength
        / MAX_RSI_FOR_SCORE
    ) * RSI_SCORE_MAX

    # ========================================================
    # EMA
    # ========================================================

    ema_strength = max(
        0.0,
        min(
            ema_spread_percentage,
            MAX_EMA_SPREAD_FOR_SCORE,
        ),
    )

    ema_score = (
        ema_strength
        / MAX_EMA_SPREAD_FOR_SCORE
    ) * EMA_SCORE_MAX

    # ========================================================
    # ADX
    # ========================================================

    adx_strength = max(
        0.0,
        min(
            adx_value,
            MAX_ADX_FOR_SCORE,
        ),
    )

    adx_score = (
        adx_strength
        / MAX_ADX_FOR_SCORE
    ) * ADX_SCORE_MAX

    # ========================================================
    # VOLUME
    # ========================================================

    volume_strength = max(
        0.0,
        min(
            volume_ratio,
            MAX_VOLUME_RATIO_FOR_SCORE,
        ),
    )

    volume_score = (
        volume_strength
        / MAX_VOLUME_RATIO_FOR_SCORE
    ) * VOLUME_SCORE_MAX

    # ========================================================
    # TOTAL
    # ========================================================

    signal_score = (
        price_momentum_score
        + rsi_score
        + ema_score
        + adx_score
        + volume_score
    )

    # ========================================================
    # SAFETY
    # ========================================================

    signal_score = max(
        0.0,
        min(
            signal_score,
            100.0,
        ),
    )

    return {
        "price_momentum_score":
            price_momentum_score,

        "rsi_score":
            rsi_score,

        "ema_score":
            ema_score,

        "adx_score":
            adx_score,

        "volume_score":
            volume_score,

        "signal_score":
            signal_score,
    }


# ============================================================
# FUNCTION 4
# ANALYZE MOMENTUM
# ============================================================

def analyze_momentum(
    historical_data: pd.DataFrame,
) -> pd.DataFrame:

    logger.info("=" * 70)
    logger.info("RUNNING MOMENTUM ANALYSIS")
    logger.info("=" * 70)

    # ========================================================
    # VALIDATE INPUT
    # ========================================================

    if historical_data is None:

        raise ValueError(
            "historical_data cannot be None."
        )

    if not isinstance(
        historical_data,
        pd.DataFrame,
    ):

        raise TypeError(
            "historical_data must be a pandas DataFrame."
        )

    if historical_data.empty:

        logger.warning(
            "Historical DataFrame is empty."
        )

        return pd.DataFrame()

    # ========================================================
    # COPY
    # ========================================================

    df = historical_data.copy()

    # ========================================================
    # NORMALIZE DATE
    # ========================================================

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce",
    ).dt.normalize()

    # ========================================================
    # NUMERIC COLUMNS
    # ========================================================

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

    # ========================================================
    # REMOVE INVALID ROWS
    # ========================================================

    df = df.dropna(
        subset=REQUIRED_COLUMNS
    )

    if df.empty:

        logger.warning(
            "No valid data available."
        )

        return pd.DataFrame()

    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    df = df.drop_duplicates(
        subset=[
            "instrument_key",
            "date",
        ],
        keep="last",
    )

    # ========================================================
    # SORT
    # ========================================================

    df = df.sort_values(
        [
            "instrument_key",
            "date",
        ]
    ).reset_index(
        drop=True
    )

    # ========================================================
    # MINIMUM HISTORY
    # ========================================================

    minimum_required_rows = (
        max(
            MOMENTUM_PERIOD,
            VOLUME_PERIOD,
            EMA_SLOW_PERIOD,
            RSI_PERIOD,
            ADX_PERIOD,
        )
        + 5
    )

    # ========================================================
    # RESULT STORAGE
    # ========================================================

    opportunities = []

    # ========================================================
    # TOTAL INSTRUMENTS
    # ========================================================

    total_instruments = (
        df["instrument_key"]
        .nunique()
    )

    processed_instruments = 0

    # ========================================================
    # PROCESS EACH INSTRUMENT
    # ========================================================

    for instrument_key, stock_df in df.groupby(
        "instrument_key",
        sort=False,
    ):

        processed_instruments += 1

        # ====================================================
        # MINIMUM HISTORY
        # ====================================================

        if len(stock_df) < minimum_required_rows:

            continue

        # ====================================================
        # CALCULATE INDICATORS
        # ====================================================

        stock_df = calculate_momentum_indicators(
            stock_df
        )

        # ====================================================
        # LATEST COMPLETED CANDLE
        # ====================================================

        latest = stock_df.iloc[-1]

        # ====================================================
        # BASIC DATA
        # ====================================================

        current_instrument_key = str(
            latest["instrument_key"]
        )

        stock_name = str(
            latest["stock_name"]
        )

        latest_date = latest["date"]

        open_price = float(
            latest["open"]
        )

        high_price = float(
            latest["high"]
        )

        low_price = float(
            latest["low"]
        )

        close_price = float(
            latest["close"]
        )

        volume = float(
            latest["volume"]
        )

        # ====================================================
        # INDICATORS
        # ====================================================

        close_20_days_ago = latest[
            "close_20_days_ago"
        ]

        momentum_percentage = latest[
            "momentum_percentage"
        ]

        average_volume = latest[
            "previous_volume_average_20"
        ]

        volume_ratio = latest[
            "volume_ratio"
        ]

        ema_20 = latest[
            "ema_20"
        ]

        ema_50 = latest[
            "ema_50"
        ]

        ema_spread_percentage = latest[
            "ema_spread_percentage"
        ]

        rsi_value = latest[
            "rsi"
        ]

        adx_value = latest[
            "adx"
        ]

        # ====================================================
        # VALIDATE INDICATORS
        # ====================================================

        indicator_values = [
            close_20_days_ago,
            momentum_percentage,
            average_volume,
            volume_ratio,
            ema_20,
            ema_50,
            ema_spread_percentage,
            rsi_value,
            adx_value,
        ]

        if any(
            pd.isna(value)
            for value in indicator_values
        ):

            continue

        # ====================================================
        # VALIDATE POSITIVE VALUES
        # ====================================================

        if close_20_days_ago <= 0:

            continue

        if average_volume <= 0:

            continue

        if ema_50 <= 0:

            continue

        # ====================================================
        # CONDITION 1
        # 20-DAY RETURN >= 5%
        # ====================================================

        price_momentum = (
            momentum_percentage
            >= MIN_MOMENTUM_PERCENTAGE
        )

        # ====================================================
        # CONDITION 2
        # CLOSE > EMA20
        # ====================================================

        short_term_trend = (
            close_price
            > ema_20
        )

        # ====================================================
        # CONDITION 3
        # EMA20 > EMA50
        # ====================================================

        medium_term_trend = (
            ema_20
            > ema_50
        )

        # ====================================================
        # CONDITION 4
        # RSI >= 60
        # ====================================================

        momentum_strength = (
            rsi_value
            >= MIN_RSI
        )

        # ====================================================
        # CONDITION 5
        # VOLUME >= 1.2x
        # ====================================================

        volume_confirmation = (
            volume_ratio
            >= MIN_VOLUME_RATIO
        )

        # ====================================================
        # FINAL SIGNAL
        # ====================================================

        momentum_signal = (
            price_momentum
            and short_term_trend
            and medium_term_trend
            and momentum_strength
            and volume_confirmation
        )

        # ====================================================
        # SKIP NON-MOMENTUM STOCKS
        # ====================================================

        if not momentum_signal:

            continue

        # ====================================================
        # CALCULATE SCORE
        # ====================================================

        score = calculate_signal_score(
            momentum_percentage=float(
                momentum_percentage
            ),
            rsi_value=float(
                rsi_value
            ),
            ema_spread_percentage=float(
                ema_spread_percentage
            ),
            adx_value=float(
                adx_value
            ),
            volume_ratio=float(
                volume_ratio
            ),
        )

        # ====================================================
        # STORE RESULT
        # ====================================================

        opportunities.append(
            {
                "instrument_key":
                    current_instrument_key,

                "stock_name":
                    stock_name,

                "date":
                    latest_date,

                "open":
                    open_price,

                "high":
                    high_price,

                "low":
                    low_price,

                "close":
                    close_price,

                "volume":
                    volume,

                "close_20_days_ago":
                    float(close_20_days_ago),

                "momentum_percentage":
                    float(momentum_percentage),

                "volume_average_20":
                    float(average_volume),

                "volume_ratio":
                    float(volume_ratio),

                "ema_20":
                    float(ema_20),

                "ema_50":
                    float(ema_50),

                "ema_spread_percentage":
                    float(ema_spread_percentage),

                "rsi":
                    float(rsi_value),

                "adx":
                    float(adx_value),

                "price_momentum_score":
                    score[
                        "price_momentum_score"
                    ],

                "rsi_score":
                    score[
                        "rsi_score"
                    ],

                "ema_score":
                    score[
                        "ema_score"
                    ],

                "adx_score":
                    score[
                        "adx_score"
                    ],

                "volume_score":
                    score[
                        "volume_score"
                    ],

                "signal_score":
                    score[
                        "signal_score"
                    ],

                "signal":
                    "MOMENTUM",
            }
        )

    # ========================================================
    # PROCESSING COMPLETE
    # ========================================================

    logger.info(
        "Processed %d/%d instruments.",
        processed_instruments,
        total_instruments,
    )

    # ========================================================
    # NO RESULTS
    # ========================================================

    if not opportunities:

        logger.info(
            "No momentum opportunities found."
        )

        return pd.DataFrame()

    # ========================================================
    # CREATE RESULT DATAFRAME
    # ========================================================

    result = pd.DataFrame(
        opportunities
    )

    # ========================================================
    # SORT
    # ========================================================

    result = result.sort_values(
        [
            "signal_score",
            "momentum_percentage",
            "rsi",
            "volume_ratio",
        ],
        ascending=[
            False,
            False,
            False,
            False,
        ],
    ).reset_index(
        drop=True
    )

    # ========================================================
    # ROUND VALUES
    # ========================================================

    decimal_columns = [
        "close",
        "close_20_days_ago",
        "momentum_percentage",
        "volume_average_20",
        "volume_ratio",
        "ema_20",
        "ema_50",
        "ema_spread_percentage",
        "rsi",
        "adx",
        "price_momentum_score",
        "rsi_score",
        "ema_score",
        "adx_score",
        "volume_score",
        "signal_score",
    ]

    for column in decimal_columns:

        if column in result.columns:

            result[column] = (
                pd.to_numeric(
                    result[column],
                    errors="coerce",
                )
                .round(2)
            )

    # ========================================================
    # LOG RESULTS
    # ========================================================

    logger.info(
        "Momentum opportunities found: %d",
        len(result),
    )

    logger.info(
        "Highest signal score: %.2f",
        result["signal_score"].max(),
    )

    logger.info(
        "Average signal score: %.2f",
        result["signal_score"].mean(),
    )

    return result


# ============================================================
# FUNCTION 5
# SAVE RESULTS
# ============================================================

def save_results(
    results: pd.DataFrame,
) -> None:

    # ========================================================
    # NO RESULTS
    # ========================================================

    if results.empty:

        if OUTPUT_FILE.exists():

            OUTPUT_FILE.unlink()

            logger.info(
                "Removed old result file: %s",
                OUTPUT_FILE,
            )

        logger.info(
            "No results to save."
        )

        return

    # ========================================================
    # SAVE
    # ========================================================

    try:

        results.to_csv(
            OUTPUT_FILE,
            index=False,
        )

    except Exception as exc:

        raise RuntimeError(
            f"Failed to save results to: {OUTPUT_FILE}"
        ) from exc

    logger.info(
        "Results saved to: %s",
        OUTPUT_FILE,
    )


# ============================================================
# FUNCTION 6
# DISPLAY RESULTS
# ============================================================

def display_results(
    results: pd.DataFrame,
) -> None:

    print()

    print("=" * 150)

    print(
        "MOMENTUM OPPORTUNITIES"
    )

    print("=" * 150)

    # ========================================================
    # NO RESULTS
    # ========================================================

    if results.empty:

        print(
            "No momentum opportunities found."
        )

        print("=" * 150)

        return

    # ========================================================
    # COLUMNS
    # ========================================================

    display_columns = [
        "instrument_key",
        "stock_name",
        "date",
        "close",
        "momentum_percentage",
        "volume_ratio",
        "ema_20",
        "ema_50",
        "ema_spread_percentage",
        "rsi",
        "adx",
        "signal_score",
        "signal",
    ]

    available_columns = [
        column
        for column in display_columns
        if column in results.columns
    ]

    # ========================================================
    # DISPLAY
    # ========================================================

    print(
        results[
            available_columns
        ].to_string(
            index=False
        )
    )

    # ========================================================
    # SUMMARY
    # ========================================================

    print("=" * 150)

    print(
        f"Total opportunities: {len(results)}"
    )

    print(
        f"Highest signal score: "
        f"{results['signal_score'].max():.2f}"
    )

    print(
        f"Average signal score: "
        f"{results['signal_score'].mean():.2f}"
    )

    print("=" * 150)


# ============================================================
# FUNCTION 7
# COMPLETE SCANNER
# ============================================================

def run_momentum_scanner() -> pd.DataFrame:

    logger.info("=" * 70)
    logger.info("MOMENTUM SCANNER STARTED")
    logger.info("=" * 70)

    scanner_start_time = time.perf_counter()

    # ========================================================
    # STEP 1
    # READ CSV
    # ========================================================

    historical_data = (
        read_historical_data()
    )

    # ========================================================
    # STEP 2
    # ANALYZE
    # ========================================================

    results = analyze_momentum(
        historical_data
    )

    # ========================================================
    # STEP 3
    # SAVE
    # ========================================================

    save_results(
        results
    )

    # ========================================================
    # EXECUTION TIME
    # ========================================================

    execution_time = (
        time.perf_counter()
        - scanner_start_time
    )

    logger.info(
        "Scanner execution time: %.2f seconds",
        execution_time,
    )

    # ========================================================
    # FINAL
    # ========================================================

    logger.info("=" * 70)

    logger.info(
        "MOMENTUM SCANNER COMPLETED"
    )

    logger.info(
        "Opportunities: %d",
        len(results),
    )

    logger.info("=" * 70)

    return results


# ============================================================
# MAIN
# ============================================================

def main() -> None:

    total_start_time = time.perf_counter()

    try:

        results = (
            run_momentum_scanner()
        )

        display_results(
            results
        )

        total_execution_time = (
            time.perf_counter()
            - total_start_time
        )

        logger.info(
            "Total execution time: %.2f seconds",
            total_execution_time,
        )

    except Exception as exc:

        logger.exception(
            "Momentum Scanner failed: %s",
            exc,
        )

        sys.exit(1)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()

