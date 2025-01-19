from math import exp, log, sqrt

from scipy.stats import norm


def calculate_black_scholes(
    S: float, X: float, T: float, r: float, q: float, v: float
) -> dict:
    """
    Calculate Black-Scholes option prices

    Args:
        S (float): Stock price
        X (float): Strike price
        T (float): Time to maturity
        r (float): Risk-free rate
        q (float): Dividend yield
        v (float): Volatility
    """
    try:
        d1 = (log(S / X) + (r - q + (v**2) / 2) * T) / (v * sqrt(T))
        d2 = d1 - v * sqrt(T)

        call_price = S * exp(-q * T) * norm.cdf(d1) - X * exp(-r * T) * norm.cdf(d2)
        put_price = X * exp(-r * T) * norm.cdf(-d2) - S * exp(-q * T) * norm.cdf(-d1)

        return {
            "call_option_price": round(call_price, 4),
            "put_option_price": round(put_price, 4),
        }
    except Exception as e:
        raise Exception(f"Black-Scholes calculation failed: {str(e)}")
