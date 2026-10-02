# Nelson-Siegel Factors of the US Yield Curve, 1982–2026

🇫🇷 [Version française](README.fr.md)

**Three numbers to describe 44 years of the US yield curve: level, slope and curvature.**

![Nelson-Siegel factors over time](assets/figure2_factors.png)

## What this project does

The notebook fits the Nelson-Siegel model to the US Treasury yield curve **every month from January 1982 to September 2026 (537 months)**. It tracks the three factors over time, checks that they carry their economic meaning, and shows where the model fits well and where it struggles.

## Key findings

| # | Finding | Evidence |
|---|---------|----------|
| 1 | **Three factors describe 44 years of the US yield curve** | Median fit error of 4.4 bp (0.044%) over 537 months; 75% of months below 6.4 bp (0.064%) |
| 2 | **The factors mean what they claim** | Correlation with observed measures: level 0.988, slope 0.992, curvature 0.998 |
| 3 | **Inversions are rare** | The curve is inverted (β₁ > 0) in only 11.5% of months, about one month in nine |
| 4 | **Inversions came before recessions** | Inverted slope in 2000, 2006–2007 and 2019, ahead of the 2001, 2008 and 2020 recessions; the deepest inversion (2022–2024) was not followed by a recession |
| 5 | **Four decades of falling rates, then a rebound** | The level fell from 14.14% (1982) to 0.84% (2020), then rose back to 5.03% in September 2026 |
| 6 | **The model's weak spot is the short end** | Clean shapes fit very well (3.6 bp in November 2000), but sudden kinks between 3 months and 1 year do not: 26.8 bp in September 1982, 20.1 bp in November 2008, 10.7 bp in June 2012 |

![Observed vs fitted curves at key dates](assets/figure5_key_dates.png)

## Method

| Item | Detail |
|------|--------|
| Data | FRED: `DGS3MO`, `DGS6MO`, `DGS1`, `DGS2`, `DGS3`, `DGS5`, `DGS7`, `DGS10`, converted to monthly averages |
| Model | Nelson-Siegel with a fixed decay rate λ = 0.7308 per year (Diebold & Li, 2006) |
| Estimation | One least-squares regression per month (`nelson_siegel_svensson`) |
| Fit quality | Root mean squared error (RMSE), in basis points |
| Validation | Factors compared with the 10-year yield, the 10Y − 3M spread and the butterfly (2 × 2Y − 3M − 10Y) |
| Recessions | NBER business cycle dates |

**Why a fixed λ?** Estimating λ every month makes the factors unstable and hard to compare over time, and the optimisation can fail. With λ fixed, each fit becomes a simple linear regression, and the three factors stay comparable over 44 years.

## Run it yourself

1. From the repository root: `pip install -r requirements.txt`
2. Put your free FRED API key in a `.env` file at the repository root: `FRED_API_KEY=your_key_here`
3. Open `nelson_siegel_factors.ipynb` and run all cells.

## Limitations

- With a fixed λ, the model cannot follow sudden kinks at the short end, nor the zero lower bound.
- High correlations with the observed measures are partly mechanical: both are linear combinations of the same yields.
- The yield curve is a leading indicator, not a forecast: not every inversion is followed by a recession.

## Related project

[01 · US Treasury Yield Curve animation](../01-us-yield-curve-animation/): the same curve, animated month by month.

## Author

**Didier Matton** | Financial Engineer | Full-Stack Data Scientist