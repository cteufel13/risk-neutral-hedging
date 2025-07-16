import numpy as np
from scipy.stats import norm


def delta(S, K, T, r, sigma):
    return norm.cdf((np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T)))


def gamma(S, K, T, r, sigma):
    return norm.pdf(
        (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    ) / (S * sigma * np.sqrt(T))


def vega(S, K, T, r, sigma):
    return (
        S
        * norm.pdf((np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T)))
        * np.sqrt(T)
    )


def theta(S, K, T, r, sigma):
    return -S * norm.pdf(
        (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    ) * sigma / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(
        (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        - sigma * np.sqrt(T)
    )


def rho(S, K, T, r, sigma):
    return (
        K
        * T
        * np.exp(-r * T)
        * norm.cdf(
            (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
            - sigma * np.sqrt(T)
        )
    )
