# Financial Data Lab

A series of small, self-contained projects exploring financial and economic data with Python: yield curves, interest rates, portfolios and market data...

Each project lives in its own folder, with its code, a short write-up and instructions to reproduce the results.

## Projects

| # | Project | What it shows | Stack |
|---|---------|---------------|-------|
| 01 | [US Treasury Yield Curve, 1982 to today](01-us-yield-curve-animation/) | An animated history of the US yield curve and its inversions before recessions | Python, pandas, matplotlib, FRED API |
| 02 | [Nelson-Siegel factors of the US yield curve, 1982–2026](02-nelson-siegel-yield-curve-factors/) | Level, slope and curvature of the curve over 44 years, and where the model struggles | Python, pandas, matplotlib, Nelson-Siegel, FRED API |
| 03 | [PCA of the US yield curve vs Nelson-Siegel, 1982–2026](03-pca-yield-curve-factors/) | Whether a purely statistical method recovers the level, slope and curvature of Nelson-Siegel, on levels and monthly changes | Python, NumPy, pandas, PCA, FRED API |


More projects coming soon.

## Getting started

```bash
git clone https://github.com/mattondidier/financial-data-lab.git
cd financial-data-lab
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
```

Then follow the instructions in each project folder.

## Author

**Didier Matton** | Financial Engineer | Full Stack Data Scientist

[LinkedIn](https://www.linkedin.com/in/didier-matton-8819b52a1/) · [YouTube](https://www.youtube.com/channel/UCQ_AZUFrhvHRLfTUvMzFUrw)