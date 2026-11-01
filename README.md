# Backtest d'une stratégie SMA Crossover

Projet personnel en Python : tester une strategie de croisement de moyennes mobiles et la comparer au buy & hold, en gain et en risque.

## Question
Une stratégie de moyennes mobiles (SMA 20/100) fait-elle mieux que d'acheter et garder le CAC 40, entre 2014 et 2026 ?

## Méthode
- **Signal** : investi si la moyenne 20 jours est au-dessus de la moyenne 100 jours sinon hors du marché.
- **Règle anti-triche** : le signal est calculé le soir et appliqué le lendemain (pas de biais d'anticipation).
- **Frais** : 0,1 % par achat ou vente.
- **Comparaison équitable** : les deux approches démarrent le même jour.
- **Mesures** : rendement annuel, volatilité, Sharpe, Max Drawdown, courbe du drawdown, stress test (10 pires et 10 meilleur jours).

## Résultats (CAC 40)

| | Buy & hold | Stratégie |
|---|---|---|
| Rendement annuel | +4,6 % | −2,8 % |
| Volatilité | 18,2 % | 11,9 % |
| Sharpe | 0,34 | -0,18 |
| Max Drawdown | -38,6 % | -37,0 % |

- La stratégie évite 7 des 10 pires jour, mais rate 9 des 10 meilleurs : les rebonds arrivent en pleine crise.
- Elle ne retrouve jamais son plus haut de 2015
- Sur 4 autres actifs (S&P 500, Apple, LVMH, or), la stratégie ne bat jamais le buy & hold. Elle fait presque jeu égal seulement sur l'or
- **Conclusion : la stratégie ne bat pas le buy & hold, ni en gain, ni en risque.**

## Contenu du projet
- `notebooks/analyse.ipynb` : l'étude complète sur le CAC 40, étape par étape.
- `notebooks/outil.ipynb` : tester la stratégie sur n'importe quel actif en une ligne, par exemple `analyse("AAPL", 50, 100)`.
- `src/backtest_tool.py` : le moteur de backtest.


## Lancer le projet
pip install -r requirements.txt
Puis ouvrir les notebooks dans le dossier `notebooks`.

## Limites
Un seul actif étudié en détail, frais simplifiés, dividendes non inclus. Un backtest décrit le passé et ne garantit pas le futur.