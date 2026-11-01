


import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


def metrics(r):
    capital = (1 + r).cumprod()
    n = len(r)
    return pd.Series({
        "Rendement annuel": capital.iloc[-1] ** (252 / n) - 1,
        "Volatilité annuelle": r.std() * (252 ** 0.5),
        "Sharpe": r.mean() / r.std() * (252 ** 0.5),
        "Max Drawdown": (capital / capital.cummax() - 1).min(),
    })


def backtest(prices, short_window, long_window, cost):
    returns = prices.pct_change()
    sma_short = prices.rolling(short_window).mean()
    sma_long = prices.rolling(long_window).mean()
    signal = (sma_short > sma_long).astype(int)
    position = signal.shift(1).fillna(0)
    change = position.diff().abs().fillna(0)
    strategie = position * returns - change * cost

    start = sma_long.dropna().index[0]
    result = pd.DataFrame()
    result["buy_hold"] = returns.loc[returns.index > start]
    result["strategie"] = strategie.loc[strategie.index > start]
    return result


def analyse(ticker, short_window=20, long_window=100, cost=0.001):
    #Les données
    df = yf.download(ticker, start="2014-01-01", auto_adjust=True, progress=False)
    prices = df["Close"].squeeze().dropna()

    # Le backtest
    res = backtest(prices, short_window, long_window, cost)
    capital_bh = (1 + res["buy_hold"]).cumprod()
    capital_st = (1 + res["strategie"]).cumprod()

    #  Graphique du capital
    plt.figure(figsize=(10, 4))
    capital_bh.plot(label="Buy & hold")
    capital_st.plot(label="Stratégie nette")
    plt.legend()
    plt.title(f"{ticker} : évolution de 1 € (SMA {short_window}/{long_window})")
    plt.show()

    # Graphique du drawdown
    plt.figure(figsize=(10, 3))
    (capital_bh / capital_bh.cummax() - 1).plot(label="Buy & hold")
    (capital_st / capital_st.cummax() - 1).plot(label="Stratégie nette")
    plt.legend()
    plt.title("Drawdown : chute depuis le plus haut")
    plt.show()

    # Tableau des métriques
    table = pd.DataFrame()
    table["Buy & hold"] = metrics(res["buy_hold"])
    table["Stratégie"] = metrics(res["strategie"])
    print(table.round(3))

    # Verdict
    if table.loc["Sharpe", "Stratégie"] > table.loc["Sharpe", "Buy & hold"]:
        print("La stratégie a fait mieux que le buy & hold (sur le passé).")
    else:
        print("La stratégie a fait moins bien que le buy & hold (sur le passé).")