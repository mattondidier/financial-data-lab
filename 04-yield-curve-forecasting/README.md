# Forecasting the US Treasury Yield Curve: Diebold-Li vs Random Walk, 1982–2026

🇫🇷 [Version française](README.fr.md)

**Can the three Nelson-Siegel factors forecast the yield curve better than assuming that yields do not move? Over 2000–2026, the answer is no, and this project shows why.**

![Out-of-sample RMSE ratio by horizon and maturity](assets/figure1_ratio_heatmap.png)

## What this project does

The notebook applies the method of Diebold and Li (2006): the US yield curve is summarised every month by the three Nelson-Siegel factors (level, slope, curvature), each factor is forecast with an AR(1) model, and the forecast curve is rebuilt 1, 6 and 12 months ahead. The forecasts are evaluated **out of sample from 2000 to 2026**, against the random walk ("yields do not move"), with a Diebold-Mariano test, an analysis by period and a robustness check with a rolling window.

## Key findings

| # | Finding | Evidence |
|---|---------|----------|
| 1 | **The random walk beats Diebold-Li out of sample** | RMSE ratio above 1 for all 24 horizon-maturity pairs over 2000–2026, from 1.03 to 1.20 |
| 2 | **The difference is statistically significant** | Diebold-Mariano statistic positive in 24 of 24 cases and significant at 5% in 18; Diebold-Li is never significantly better |
| 3 | **Forecasting one year ahead is hard for everyone** | RMSE of about 25 bp at 1 month, but 80 to 160 bp at 12 months for both methods |
| 4 | **The model's weakness is mean reversion in trending regimes** | Mean error at 12 months: +68 bp in 2000–2007 and +114 bp in 2008–2015 (forecasts too high while rates fell or sat at zero), −121 bp in 2022–2026 (forecasts too low during the hiking cycle) |
| 5 | **It wins when rates revert to their mean** | 2016–2021 is the only regime where Diebold-Li beats the random walk: RMSE ratio 0.93 at 6 months and 0.85 at 12 months |
| 6 | **No simple model anticipates turning points** | Both forecasts follow the 10-year yield with a one-year lag and miss 2008, 2020 and 2022 |
| 7 | **The problem is mean reversion itself, not the choice of mean** | A 10-year rolling window does worse than the expanding window (ratios up to 1.30, 24 of 24 Diebold-Mariano tests significant at 5%) |

![Forecast accuracy by period](assets/figure3_ratio_by_period.png)

**Takeaway:** the forecasting success reported by Diebold and Li on data up to 2000 does not hold over 2000–2026. The problem is not *which* mean the model reverts to, but mean reversion itself: the more the model pulls yields back toward a historical mean, the worse it forecasts. The random walk amounts to assuming no mean reversion at all; over 2000–2026, yields behaved almost like a random walk, which is why it wins.

![10-year yield: actual vs forecasts made 12 months earlier](assets/figure2_forecasts_vs_actual.png)

## Method

| Item | Detail |
|------|--------|
| Data | FRED: `DGS3MO`, `DGS6MO`, `DGS1`, `DGS2`, `DGS3`, `DGS5`, `DGS7`, `DGS10`, **end-of-month** values, January 1982 to September 2026 |
| Factors | Nelson-Siegel fitted every month with a fixed λ = 0.7308 per year |
| Model | Direct h-step AR(1) for each factor, as in Diebold & Li (2006): factor(t+h) = c + φ × factor(t) |
| Benchmark | Random walk: yields h months ahead equal today's yields |
| Out-of-sample design | Expanding window: at each month from December 1999, the model is re-estimated with past data only, then the curve is forecast 1, 6 and 12 months ahead |
| Evaluation | RMSE in basis points, RMSE ratio, Diebold-Mariano test with Newey-West variance and the Harvey-Leybourne-Newbold correction |
| Robustness | Same test with a 10-year rolling window |

## Run it yourself

1. From the repository root: `pip install -r requirements.txt`
2. Put your free FRED API key in a `.env` file at the repository root: `FRED_API_KEY=your_key_here`
3. Open `yield_curve_forecasting.ipynb` and run all cells.

## Limitations

- Only one model class is tested (an AR(1) on each factor). A VAR, a model with macroeconomic variables or a regime-switching model could behave differently.
- The test is run on 24 horizon-maturity pairs: with many tests, a few could be significant by chance, although all 24 statistics point in the same direction.
- FRED constant-maturity yields are yields on coupon bonds, while Nelson-Siegel is in principle a model of the zero-coupon curve.
- The evaluation covers point forecasts only, not forecast intervals.

## References

- Diebold, F. X. & Li, C. (2006). *Forecasting the Term Structure of Government Bond Yields*. Journal of Econometrics, 130(2), 337–364. [Free working paper (NBER)](https://www.nber.org/papers/w10048)
- Diebold, F. X. & Mariano, R. S. (1995). *Comparing Predictive Accuracy*. Journal of Business & Economic Statistics, 13(3), 253–263.
- Harvey, D., Leybourne, S. & Newbold, P. (1997). *Testing the Equality of Prediction Mean Squared Errors*. International Journal of Forecasting, 13(2), 281–291.
- Newey, W. K. & West, K. D. (1987). *A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix*. Econometrica, 55(3), 703–708.

## Related projects

- [01 · US Treasury Yield Curve animation](../01-us-yield-curve-animation/)
- [02 · Nelson-Siegel factors of the US yield curve](../02-nelson-siegel-yield-curve-factors/)
- [03 · PCA of the US yield curve vs Nelson-Siegel](../03-pca-yield-curve-factors/)

## Author

**Didier Matton** | Financial Engineer | Full-Stack Data Scientist