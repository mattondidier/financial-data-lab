# Bitcoin contre S&P 500 : la différence de Sharpe est-elle réelle ?

[English](README.md)

Sur 2015-2026, le ratio de Sharpe du Bitcoin (1,02) dépasse nettement celui du S&P 500 (0,70). Ce projet vérifie si cet écart se distingue statistiquement du hasard, une fois prises en compte les queues épaisses, la corrélation entre actifs et l'instabilité dans le temps. L'or sert d'actif de référence.

**Réponse courte : non.** Avec 12 ans de données quotidiennes, la différence ne se distingue pas du bruit, et le classement s'inverse quand l'échantillon démarre en 2018 au lieu de 2015.

## Résultats clés

| | Résultat |
|:---|:---|
| Différence de Sharpe, Bitcoin − S&P 500 | 0,32, erreur-type ≈ 0,34, **p ≈ 0,35**, intervalle à 95 % [−0,35 ; 0,97] |
| Départ en janvier 2018 au lieu de janvier 2015 | Le Sharpe du Bitcoin passe de 1,02 à 0,59 : **de la première à la dernière place**, derrière le S&P 500 (0,67) et l'or (0,69) |
| Données nécessaires pour détecter un écart de 0,32 | Environ **57 ans** de données quotidiennes (corrélation de 0,24) |
| Queues épaisses | Degrés de liberté de la loi de Student entre 2,3 et 3,7 : aplatissement théorique infini ; le pire jour de chaque actif se situe 10,5 à 11 écarts-types sous sa moyenne |
| Corrélation avec les actions | Changement de régime en 2020 : Bitcoin de 0,02 à 0,39, or de −0,17 à +0,15 |

![Distribution bootstrap de la différence de Sharpe](assets/sharpe_diff_bootstrap.png)

![Sharpe glissant sur 2 ans](assets/rolling_sharpe.png)

## Données

| | |
|:---|:---|
| Actifs | SPY (ETF du S&P 500, dividendes réinvestis), BTC-USD (Bitcoin), GLD (ETF or) — Yahoo Finance via `yfinance`, cours de clôture ajustés |
| Taux sans risque | Bon du Trésor américain à 3 mois, série FRED `DTB3`, converti en taux quotidien et décalé d'un jour |
| Période | Du 2 janvier 2015 au 30 septembre 2026 : 2 953 jours de bourse communs, 2 952 rendements quotidiens |
| Traitement | Seuls les jours où les trois actifs cotent (jours de bourse américains) sont conservés avant le calcul des rendements ; rendements simples pour le Sharpe et le Sortino, rendements logarithmiques pour la volatilité, la corrélation et l'analyse des distributions |

**Outils :** Python, pandas, NumPy, SciPy, matplotlib, yfinance, fredapi, python-dotenv.

## Méthodologie

| Étape | Contenu |
|:---|:---|
| 1. Données et rendements | Téléchargement avec contrôle explicite des tickers en échec ; rendements simples et logarithmiques, frein de la volatilité σ²/2 |
| 2. Volatilité | Volatilité annualisée ; volatilité mobile sur 50 jours avec les périodes de crise grisées |
| 3. Corrélation | Matrice de corrélation ; corrélations décalées et correction de Dimson (1979) pour les heures de clôture différentes ; rendements hebdomadaires ; test z de Fisher sur le changement de 2020 ; corrélations mobiles |
| 4. Sharpe et Sortino | Rendements simples excédentaires ; écart à la baisse de Sortino & Price (1994) ; effet du passage aux rendements logarithmiques |
| 5. Normalité | Asymétrie, excès d'aplatissement, tests de Jarque-Bera et de D'Agostino-Pearson ; jours au-delà de ±3σ avec un test binomial ; pire jour sous une loi normale |
| 6. Loi de Student | Ajustement par maximum de vraisemblance, comparaison par AIC, QQ-plots, existence des moments |
| 7. Intervalles de confiance des Sharpe | Erreurs-types de Lo (2002) et de Mertens (2002) |
| 8. Test de la différence de Sharpe | Test de Jobson-Korkie corrigé par Memmel (2003) ; bootstrap par blocs circulaire apparié (10 000 tirages, blocs de 5, 20 et 50 jours) |
| 9. Stabilité | 2015-2019 contre 2020 et après ; départ après le sommet du Bitcoin de 2017 ; Sharpe glissant sur 2 ans |

## Autres résultats

| Actif | Volatilité | Sharpe | Sortino | ν de Student | IC à 95 % du Sharpe |
|:---|:---|:---|:---|:---|:---|
| S&P 500 | 17,6 % | 0,70 | 0,99 | 2,76 | [0,13 ; 1,28] |
| Bitcoin | 66,0 % | 1,02 | 1,54 | 2,30 | [0,45 ; 1,60] |
| Or | 16,3 % | 0,59 | 0,83 | 3,73 | [0,01 ; 1,17] |

![Ratios de Sharpe et intervalles de confiance](assets/sharpe_ci.png)

![QQ-plots : loi normale contre loi de Student](assets/qq_plots.png)

![Volatilité mobile sur 50 jours](assets/rolling_volatility.png)

![Corrélation mobile avec le S&P 500](assets/rolling_correlation.png)

## Limites

- Le test binomial, le test de Fisher, les erreurs-types de Mertens et de Memmel et l'annualisation par √252 supposent des rendements indépendants et identiquement distribués ; les grappes de volatilité les rendent un peu trop optimistes. Le bootstrap par blocs corrige en partie ce problème.
- Le bootstrap par blocs par percentiles est une version simplifiée du bootstrap studentisé de Ledoit & Wolf (2008).
- Le rendement du lundi du Bitcoin couvre trois jours calendaires ; aucun effet significatif lié aux heures de clôture différentes n'a été trouvé.
- Les frais des ETF (SPY environ 0,09 % par an, GLD environ 0,40 %) sont déjà déduits des prix.
- `DTB3` est coté sur une base d'escompte ; le convertir en rendement actuariel modifie le taux d'environ 0,04 point par an en moyenne, et les ratios de Sharpe de moins de 0,003.
- La loi de Student est ajustée avec une volatilité constante ; la volatilité variable dans le temps (GARCH) n'est pas modélisée.
- Une seule source de données et une seule fenêtre de 12 ans : les résultats dépendent de la période, comme le montre l'étape 9.

## Exécution

```bash
git clone https://github.com/mattondidier/financial-data-lab.git
cd financial-data-lab
python -m venv venv
venv\Scripts\activate            # Windows  |  source venv/bin/activate sous macOS/Linux
pip install -r requirements.txt
copy .env.example .env           # Windows  |  cp .env.example .env sous macOS/Linux
```

Ajoutez une clé API FRED gratuite dans `.env` (`FRED_API_KEY=...`), puis ouvrez `05-asset-risk-beyond-volatility/asset_risk.ipynb` et exécutez toutes les cellules. Les graphiques sont enregistrés dans `assets/`.

## Références

- Dimson, E. (1979). Risk measurement when shares are subject to infrequent trading. *Journal of Financial Economics*, 7(2), 197–226.
- Jobson, J. D. & Korkie, B. M. (1981). Performance hypothesis testing with the Sharpe and Treynor measures. *Journal of Finance*, 36(4), 889–908.
- Ledoit, O. & Wolf, M. (2008). Robust performance hypothesis testing with the Sharpe ratio. *Journal of Empirical Finance*, 15(5), 850–859.
- Lo, A. W. (2002). The statistics of Sharpe ratios. *Financial Analysts Journal*, 58(4), 36–52.
- Memmel, C. (2003). Performance hypothesis testing with the Sharpe ratio. *Finance Letters*, 1, 21–23.
- Mertens, E. (2002). Comments on variance of the IID estimator in Lo (2002). Document de travail, Université de Bâle.
- Sortino, F. A. & Price, L. N. (1994). Performance measurement in a downside risk framework. *Journal of Investing*, 3(3), 59–64.

La liste complète figure dans le notebook.

---

**Didier Matton** | Ingénieur financier | Data Scientist Full Stack | Python, Django, VBA, BI & LLMs | Finance quantitative
