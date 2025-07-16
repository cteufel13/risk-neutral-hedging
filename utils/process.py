import pandas as pd
import numpy as np


def process_option_row(
    option_type="C",
    option_strike=None,
    option_expiration_date=None,
):
    return None


def process_options(data, option_expiration_date, option_type, option_strike):

    option_history = data.loc[
        (data["expiration_date"] == option_expiration_date)
        & (data["option_type"] == option_type)
        & (data["strike"] == option_strike)
    ].sort_index()

    beginning_timestamp = option_history.index[0]
    end_timestamp = option_history.index[-1]
    daily_index = pd.date_range(start=beginning_timestamp, end=end_timestamp, freq="D")
    option_history = option_history.reindex(daily_index, method="ffill")

    return option_history


def process_underlying(data, expiration_date, beginning_timestamp, end_timestamp):
    future_history = data.loc[data["expiration_date"] == expiration_date].sort_index()

    daily_index = pd.date_range(start=beginning_timestamp, end=end_timestamp, freq="D")

    future_history = future_history.reindex(daily_index, method="ffill")

    return future_history


def process_rf(data):
    annualized_r = 12 * np.log(1 + data["rate"] / 1200)
    annualized_r = annualized_r.to_frame()
    annualized_r.index = data.index
    annualized_r = annualized_r.sort_index()

    return annualized_r
