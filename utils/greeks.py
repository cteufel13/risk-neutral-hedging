import numpy as np
from scipy.stats import norm


def _d1(S, K, T, sigma):
    return (np.log(S / K) + 0.5 * sigma**2 * T) / (sigma * np.sqrt(T))


def _d2(S, K, T, sigma):
    return _d1(S, K, T, sigma) - sigma * np.sqrt(T)


def delta(S, K, T, r, sigma):
    """Black-76 call delta: ∂C/∂F = e^{-rT} Φ(d1)"""
    d1 = _d1(S, K, T, sigma)
    return np.exp(-r * T) * norm.cdf(d1)


def gamma(S, K, T, r, sigma):
    """Black-76 gamma: ∂²C/∂F² = e^{-rT} φ(d1) / (F σ √T)"""
    d1 = _d1(S, K, T, sigma)
    return np.exp(-r * T) * norm.pdf(d1) / (S * sigma * np.sqrt(T))


def vega(S, K, T, r, sigma):
    """Black-76 vega: ∂C/∂σ = e^{-rT} F φ(d1) √T"""
    d1 = _d1(S, K, T, sigma)
    return np.exp(-r * T) * S * norm.pdf(d1) * np.sqrt(T)


def theta(S, K, T, r, sigma):
    """
    Black-76 call theta: ∂C/∂T
      = -e^{-rT}·F·φ(d1)·σ/(2√T)
        + r·e^{-rT}[F·Φ(d1) - K·Φ(d2)]
    """
    d1 = _d1(S, K, T, sigma)
    d2 = _d2(S, K, T, sigma)
    term_time_decay = -np.exp(-r * T) * S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
    term_discount = r * np.exp(-r * T) * (S * norm.cdf(d1) - K * norm.cdf(d2))
    return term_time_decay + term_discount


def rho(S, K, T, r, sigma):
    """
    Black-76 call rho: ∂C/∂r
      = -T·e^{-rT}·[F·Φ(d1) - K·Φ(d2)]
    """
    d1 = _d1(S, K, T, sigma)
    d2 = _d2(S, K, T, sigma)
    return -T * np.exp(-r * T) * (S * norm.cdf(d1) - K * norm.cdf(d2))
