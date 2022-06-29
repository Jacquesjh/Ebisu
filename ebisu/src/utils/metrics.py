
import pandas as pd
import quantstats as qs


def get_metrics(qs_metrics: pd.DataFrame) -> pd.DataFrame:
    indicators = ["Sharpe", "Sortino", "Calmar", "Expected Shortfall (cVaR)","CAGR﹪", "Max Drawdown",
                  "Longest DD Days", "Avg. Drawdown Days", "Daily Value-at-Risk", "Volatility (ann.)",
                  "1Y", "3M"]

    metrics = pd.DataFrame(columns = ["Indicators"], index = indicators)

    for indicator in indicators:
        metrics.loc[indicator] = qs_metrics.loc[indicator][0]

    mdd_algarism = len(str(metrics.loc["Longest DD Days"][0]))
    metrics.loc["Longest DD Days"] = metrics.loc["Longest DD Days"][0]/pow(10, mdd_algarism)

    mdd_algarism = len(str(metrics.loc["Avg. Drawdown Days"][0]))
    metrics.loc["Avg. Drawdown Days"] = metrics.loc["Avg. Drawdown Days"][0]/pow(10, mdd_algarism)

    metrics.loc["Expected Shortfall (cVaR)"] = metrics.loc["Expected Shortfall (cVaR)"][0]
    metrics.loc["Max Drawdown"]              = metrics.loc["Max Drawdown"][0]
    metrics.loc["Daily Value-at-Risk"]       = metrics.loc["Daily Value-at-Risk"][0]
    metrics.loc["RoMad"]                     = (qs_metrics.loc["Cumulative Return"]/qs_metrics.loc["Max Drawdown"])[0]

    return metrics


def metrics_df(returns: pd.DataFrame) -> pd.DataFrame:
    qs_metrics = qs.reports.metrics(returns, mode = "full", display = False)
    metrics = get_metrics(qs_metrics = qs_metrics)

    return metrics