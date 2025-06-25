# src/regression_diagnostics.py

import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

def plot_residuals(residuals):
    """
    Erstellt Histogramm und QQ-Plot der Residuen zur Beurteilung der Normalverteilung.
    
    Args:
        residuals (array-like): Residuen aus Regressionsmodell (results.resid)
    """
    # Histogramm
    plt.figure(figsize=(8, 4))
    sns.histplot(residuals, kde=True, bins=50, color='steelblue')
    plt.title("Histogramm der Residuen")
    plt.xlabel("Residuen")
    plt.ylabel("Häufigkeit")
    plt.tight_layout()
    plt.show()

    # QQ-Plot
    sm.qqplot(residuals, line='s')
    plt.title("QQ-Plot der Residuen")
    plt.tight_layout()
    plt.show()
