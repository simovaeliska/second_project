import pandas as pd
from scipy.stats import norm

def two_proportion_z_test(p1, p2, n1, n2):
    P = (p1 * n1 + p2 * n2) / (n1 + n2)
    SE = (P * (1 - P) * (1 / n1 + 1 / n2)) ** 0.5
    z = (p1 - p2) / SE
    p_value = 2 * (1 - norm.cdf(abs(z)))  # Two-tailed test
    return z, p_value