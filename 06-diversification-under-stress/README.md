# Does sector diversification survive market crises?

[Français](README.fr.md)

An equal-weight portfolio of the nine original S&P 500 sector ETFs spreads its risk across the whole economy. This project tests whether that diversification still works when the market falls: how sector correlations and volatilities change in crises, how much of the change is a volatility effect, whether stress-test correlation matrices remain usable for simulation, and what it all means for portfolio losses.

**Short answer: it depends on the crisis, and sector diversification does not protect against the market itself.** In a sector-driven bust (2000–2002), correlations fell and diversification worked. In systemic crises (2007–2009, 2020), correlations rose to 0.73–0.88 and one factor absorbed up to 90% of sector variance. And in a Monte Carlo simulation, the volatility shock matters far more than the rise in correlations.

## Key findings

| | Result |
|:---|:---|
| Average sector correlation | 0.59 in calm periods; **0.44** in 2000–2002, **0.73** in 2007–2009, **0.88** in 2020, 0.62 in 2022 |
| Volatility vs correlation (simulated) | P(one-year loss > 20%): 1.8% calm → 2.9% with crisis correlations → **22.7%** with crisis correlations and volatilities |
| Diversification ratio | 1.25 in calm markets → **1.05** under a worst-case stress matrix |
| Forbes & Rigobon (2002) correction | Crisis correlations fall to 0.32–0.48, below the calm level: "no contagion, only interdependence" (probably an overcorrection) |
| Worst-case stress matrix | Highest correlation per pair across crises: **not positive definite** (smallest eigenvalue −0.045), Cholesky fails; Higham's nearest correlation matrix repairs it with a largest change of 0.015 |
| Absorption ratio | First eigenvalue: 64% of sector variance in calm periods, **90%** during the 2020 crash |

![Sector correlations: calm vs crises](assets/correlation_calm_vs_crisis.png)

![Monte Carlo: one-year portfolio returns under four scenarios](assets/monte_carlo_one_year.png)

## Data

| | |
|:---|:---|
| Assets | Nine SPDR sector ETFs (XLB, XLE, XLF, XLI, XLK, XLP, XLU, XLV, XLY) and SPY as market benchmark — Yahoo Finance via `yfinance`, adjusted closes (dividends reinvested) |
| Excluded | XLRE (real estate, launched 2015) and XLC (communication services, launched 2018): too recent |
| Period | 5 January 1999 – 30 September 2026: 6,977 common trading days |
| Treatment | Common trading days kept before computing returns; log returns for covariances, correlations and eigenvalues; simple returns for drawdowns and the Monte Carlo |
| Crises | SPY total-return drawdowns of at least 20%, peak to trough, detected from the data: 2000–2002 (637 days), 2007–2009 (355), 2020 (23), 2022 (195) |
| Portfolio | Equal weights across the nine sectors, rebalanced daily |

**Tools:** Python, pandas, NumPy, matplotlib, yfinance.

## Methodology

| Step | Content |
|:---|:---|
| 1. Data | Download with explicit checks on failed tickers; common trading days; sanity checks |
| 2. Crisis detection | Peak-to-trough SPY drawdowns of at least 20%; all other days are calm |
| 3. Covariance and correlation | Calm vs crisis matrices; conversion Σ = DRD checked both ways; symmetry; positive (semi-)definiteness tested with eigenvalues |
| 4. Volatility correction | Forbes & Rigobon (2002) adjustment of crisis correlations, with δ from the SPY variance |
| 5. Absorption ratio | Eigenvalue decomposition R = BΛBᵀ by regime and on rolling 500-day and 63-day windows (Kritzman et al., 2011) |
| 6. Stress matrices | Worst-case and inconsistent expert matrices that break Cholesky; repair by eigenvalue clipping (Rebonato & Jäckel, 2000) and by Higham's (2002) nearest correlation matrix |
| 7. Monte Carlo | Cholesky simulation X = μ + diag(σ)LZ, 10,000 one-year paths per scenario, same mean everywhere: calm, crisis correlations, crisis correlations and volatilities, worst-case stress |

## Other results

| Regime | Days | Avg sector volatility | Avg correlation | Smallest eigenvalue | Absorption ratio (n = 2) |
|:---|:---|:---|:---|:---|:---|
| Calm | 5,767 | 18.8% | 0.59 | 0.141 | 72.9% |
| 2000–2002 | 637 | 28.4% | 0.44 | 0.185 | 65.7% |
| 2007–2009 | 355 | 41.1% | 0.73 | 0.106 | 82.9% |
| 2020 | 23 | 86.4% | 0.88 | 0.008 | 96.5% |
| 2022 | 195 | 26.0% | 0.62 | 0.069 | 78.1% |

| Monte Carlo scenario (simulated) | Portfolio volatility | Diversification ratio | P(loss > 20%), 1 year |
|:---|:---|:---|:---|
| 1. Calm | 15.1% | 1.25 | 1.75% |
| 2. Crisis correlations | 16.5% | 1.14 | 2.91% |
| 3. Crisis correlations + volatilities | 35.9% | 1.15 | 22.67% |
| 4. Worst-case stress (Higham) | 39.1% | 1.05 | 25.47% |

![S&P 500 drawdown and crisis windows](assets/spy_drawdown_crises.png)

![Forbes & Rigobon correction of crisis correlations](assets/forbes_rigobon_correction.png)

![Rolling absorption ratio](assets/absorption_ratio.png)

## Limitations

- Crises are defined by SPY declines, which selects days of falling markets and inflates correlations. The 20% threshold is a convention: 2018 and 2025 came close and are treated as calm.
- The 2020 crisis has only 23 observations: its correlations are noisy and its matrix is close to singular.
- The Forbes & Rigobon correction assumes a single common shock and constant sector-specific variance, and tends to overcorrect (Corsetti, Pericoli & Sbracia, 2005).
- Equal-weighted rolling windows create step changes when extreme days leave the window; the absorption ratio is computed on correlations and is not tested as an early-warning signal.
- The Monte Carlo is Gaussian and i.i.d.: no fat tails and no volatility clustering. It gives a 0% probability of a one-day loss above 10%, although the SPY lost 10.9% on 16 March 2020. A multivariate Student t would be the natural extension. Crisis volatility is assumed to last a full year, and the same positive mean is used in every scenario.
- The nine sectors are US large caps exposed to the same market factor; the result concerns sector diversification, not diversification across asset classes. Daily rebalancing ignores transaction costs.

## How to run

```bash
git clone https://github.com/mattondidier/financial-data-lab.git
cd financial-data-lab
python -m venv venv
venv\Scripts\activate            # Windows  |  source venv/bin/activate on macOS/Linux
pip install -r requirements.txt
```

Then open `06-diversification-under-stress/diversification_under_stress.ipynb` and run all cells. No API key is needed. Charts are saved to `assets/`.

## References

- Corsetti, G., Pericoli, M., & Sbracia, M. (2005). "Some contagion, some interdependence": More pitfalls in tests of financial contagion. *Journal of International Money and Finance*, 24(8), 1177–1199.
- Forbes, K. J., & Rigobon, R. (2002). No contagion, only interdependence: Measuring stock market comovements. *Journal of Finance*, 57(5), 2223–2261.
- Higham, N. J. (2002). Computing the nearest correlation matrix — a problem from finance. *IMA Journal of Numerical Analysis*, 22(3), 329–343.
- Kritzman, M., Li, Y., Page, S., & Rigobon, R. (2011). Principal components as a measure of systemic risk. *Journal of Portfolio Management*, 37(4), 112–126.
- Rebonato, R., & Jäckel, P. (2000). The most general methodology for creating a valid correlation matrix for risk management and option pricing purposes. *Journal of Risk*, 2(2), 17–27.

---

**Didier Matton** | Financial Engineer | Full-Stack Data Scientist | Python, Django, VBA, BI & LLMs | Quantitative Finance
