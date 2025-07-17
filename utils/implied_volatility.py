from scipy.stats import norm
from scipy.optimize import brentq, newton
import numpy as np


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
