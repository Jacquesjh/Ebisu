
import pandas as pd
import plotly.express as px
from quantstats import plots, reports


def pie_plot(portfolio: pd.DataFrame) -> None:
    tickers = pd.DataFrame(portfolio.columns, columns = ["Tickers"])
    weights = pd.DataFrame(portfolio.values[:, :].reshape((len(tickers), 1)), columns = ["Weights"])

    df = pd.concat([tickers, weights], axis = 1)

    fig = px.pie(df, values = "Weights", names = "Tickers")
    fig.show()


def make_snapshot(returns: pd.Series, title: str = "Portfolio Performance") -> None:
    plots.snapshot(returns, title = title)


def make_html(returns: pd.Series, benchmark: str = "^BVSP", title: str = "Portfolio Performance") -> None:
    reports.html(returns, benchmark = benchmark, title = title)
