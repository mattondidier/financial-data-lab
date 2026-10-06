# PCA of the US Treasury Yield Curve vs Nelson-Siegel, 1982–2026

🇫🇷 [Version française](README.fr.md)

**Without being told anything about finance, a PCA finds the same three forces as the Nelson-Siegel formula: level, slope and curvature.**

![PCA loadings vs Nelson-Siegel loadings](assets/figure1_loadings_vs_ns.png)

## What this project does

The notebook runs a principal component analysis on eight US Treasury yields over **537 months (January 1982 to September 2026)**. It compares the principal components with the Nelson-Siegel factors estimated in [project 02](../02-nelson-siegel-yield-curve-factors/), both in shape and over time, then repeats the analysis on monthly yield changes, the standard approach in risk management.

## Key findings

| # | Finding | Evidence |
|---|---------|----------|
| 1 | **The data alone recover the Nelson-Siegel shapes** | Cosine similarity between PCA and Nelson-Siegel loadings: level 1.000, slope 0.994, curvature 0.971; the PC3 hump peaks around 2.5 years, exactly where the Nelson-Siegel curvature peaks with λ = 0.7308 |
| 2 | **Three factors explain almost everything** | 99.98% of the variance of yield levels and 99.05% of monthly yield changes |
| 3 | **Yield levels overstate the level factor** | PC1 explains 97.68% of levels but 84.41% of monthly changes; slope and curvature account for about 15% of monthly moves, so a duration-only hedge leaves about 15% of monthly curve moves unhedged |
| 4 | **The slope is the most robust factor** | PC2 and −β₁ correlate at 0.993 over 44 years |
| 5 | **Two different notions of "level"** | PC1 (average level) and β₀ (very long-term level) correlate at 0.933; their gaps in 2009–2015 and 2022–2025 reflect the slope |
| 6 | **Curvature is the fragile factor** | PC3 explains only 0.12% of levels and correlates at 0.656 with β₂; its loading falls faster at the long end than the Nelson-Siegel one, the limitation that led Svensson to add a second hump |
| 7 | **The short end lives its own life** | On monthly changes, the 3-month yield has the lowest level loading (0.29) and the strongest slope loading (−0.61) |

![PCA loadings on yield levels vs monthly changes](assets/figure3_levels_vs_changes.png)

## Method

| Item | Detail |
|------|--------|
| Data | FRED: `DGS3MO`, `DGS6MO`, `DGS1`, `DGS2`, `DGS3`, `DGS5`, `DGS7`, `DGS10`, monthly averages |
| PCA | Standardized yields, eigendecomposition of the covariance matrix with `numpy.linalg.eigh` (designed for symmetric matrices) |
| Sign convention | PC1 rises when all yields rise, PC2 when the curve steepens, PC3 when a hump appears in the middle |
| Shape comparison | Nelson-Siegel loadings rescaled to unit length (slope and curvature centred), compared by cosine similarity |
| Time comparison | Correlation between each component and its Nelson-Siegel factor (PC2 with −β₁) |
| Changes | Same PCA on month-to-month yield changes |

## Run it yourself

1. From the repository root: `pip install -r requirements.txt`
2. Put your free FRED API key in a `.env` file at the repository root: `FRED_API_KEY=your_key_here`
3. Open `pca_yield_curve_factors.ipynb` and run all cells.

## Limitations

- The analysis is descriptive and in-sample: it does not test whether the factors help to forecast yields. [Project 04](../04-yield-curve-forecasting/) addresses this question.
- Monthly averages smooth volatility and create artificial autocorrelation in monthly changes; end-of-month values would be preferable for the PCA on changes.
- FRED constant-maturity yields are yields on coupon bonds, while Nelson-Siegel is in principle a model of the zero-coupon curve.
- Yields are standardized, which gives every maturity the same weight; a PCA on the raw covariance of changes (in basis points) would weight maturities by their actual volatility.
- Only maturities up to 10 years are used, so the long end discussed by Svensson is not directly observed.

## References

- Diebold, F. X. & Li, C. (2006). *Forecasting the Term Structure of Government Bond Yields*. Journal of Econometrics, 130(2), 337–364. [Free working paper (NBER)](https://www.nber.org/papers/w10048)
- Litterman, R. & Scheinkman, J. (1991). *Common Factors Affecting Bond Returns*. Journal of Fixed Income, 1(1), 54–61.
- Nelson, C. R. & Siegel, A. F. (1987). *Parsimonious Modeling of Yield Curves*. Journal of Business, 60(4), 473–489.

## Related projects

- [01 · US Treasury Yield Curve animation](../01-us-yield-curve-animation/)
- [02 · Nelson-Siegel factors of the US yield curve](../02-nelson-siegel-yield-curve-factors/)

## Author

**Didier Matton** | Financial Engineer | Full-Stack Data Scientist | Python, Django, VBA, BI & LLMs | Quantitative Finance