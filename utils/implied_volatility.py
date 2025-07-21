from scipy.stats import norm
from scipy.optimize import brentq, newton
from scipy.interpolate import griddata
import math
import plotly.graph_objects as go

import numpy as np

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def bs_call_price(S, K, T, r, sigma):
    """Black-Scholes call option price."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)


def implied_volatility(S, K, T, r, market_price):
    """Calculate the implied volatility using the Black-Scholes model."""
    print(f"Calculating IV for S={S}, K={K}, T={T}, r={r}, market_price={market_price}")

    lower = np.exp(-r * T) * (F - K)
    if market_price < lower:
        return None  # No solution if market price is below the lower bound

    def objective_function(sigma):
        return bs_call_price(S, K, T, r, sigma) - market_price

    return brentq(objective_function, 1e-6, 5.0, xtol=1e-6)


def b76_call_price(F, K, T, r, sigma):
    """Black-76 call option price on futures."""
    d1 = (np.log(F / K) + 0.5 * sigma**2 * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return np.exp(-r * T) * (F * norm.cdf(d1) - K * norm.cdf(d2))


def b76_put_price(F, K, T, r, sigma):
    """Black-76 put option price on futures."""
    d1 = (np.log(F / K) + 0.5 * sigma**2 * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return np.exp(-r * T) * (K * norm.cdf(-d2) - F * norm.cdf(-d1))


def implied_vol_b76(F, K, T, r, market_price, option_type="C"):
    """Implied vol solving Black-76."""

    if option_type == "P":
        # For put options, we use the put price formula
        def objective(sigma):
            return b76_put_price(F, K, T, r, sigma) - market_price

    else:

        def objective(sigma):
            return b76_call_price(F, K, T, r, sigma) - market_price

    try:
        # Use Brent's method for root finding
        return brentq(objective, 1e-6, 5.0, xtol=1e-6)
    except:
        return np.nan


def _make_surface(df):
    pts = df[["strike", "T"]].values
    vals = df["IV"].values

    def surf(K, tau):
        try:
            v = griddata(pts, vals, (K, tau), method="linear")
            if np.isnan(v):
                raise ValueError
        except Exception:
            v = griddata(pts, vals, (K, tau), method="nearest")
        return float(v)

    return surf


def fill_missing_iv(df):
    for (ts, ot), grp in df.groupby(["ts_event", "option_type"]):
        known = grp[grp["IV"].notna()]
        if len(known) > 3:
            surf = _make_surface(known)
            missing_idx = grp["IV"].isna()
            idx = grp.index[missing_idx]
            strikes = grp.loc[missing_idx, "strike"]
            Ts = grp.loc[missing_idx, "T"]
            df.loc[idx, "IV"] = [surf(k, t) for k, t in zip(strikes, Ts)]
    return df


def plot_vol_surface(surf, T_min, T_max, K_min, K_max, n_T=50, n_K=50):
    T = np.linspace(T_min, T_max, n_T)
    K = np.linspace(K_min, K_max, n_K)
    TT, KK = np.meshgrid(T, K)
    IV = surf(TT, KK)
    fig = go.Figure(data=[go.Surface(x=TT, y=KK, z=IV)])
    fig.update_layout(
        scene=dict(
            xaxis_title="Time to expiry (yrs)",
            yaxis_title="Strike",
            zaxis_title="Implied Vol",
        )
    )
    return fig


def price_future_option(F, K, T, sigma, r, option_type="C"):
    """Black-76 pricing for an option on a futures contract."""
    if T <= 0 or sigma <= 0:
        # immediate expiry or zero vol → intrinsic
        intrinsic = max(0.0, (F - K) if option_type == "call" else (K - F))
        return intrinsic * math.exp(-r * T)
    sqrtT = math.sqrt(T)
    d1 = (math.log(F / K) + 0.5 * sigma * sigma * T) / (sigma * sqrtT)
    d2 = d1 - sigma * sqrtT
    df = math.exp(-r * T)

    if "C":
        return df * (F * norm.cdf(d1) - K * norm.cdf(d2))
    else:
        return df * (K * norm.cdf(-d2) - F * norm.cdf(-d1))
