from scipy.stats import kruskal
from scikit_posthocs import posthoc_dunn
import pandas as pd

def kruskal_test(data, names = None):
    statistic, p_value = kruskal(*data)
    print(f"p-value: {p_value}")
    if p_value < 0.05:
        if names:
            print(f"\n {names}")
        print(posthoc_dunn(data))
