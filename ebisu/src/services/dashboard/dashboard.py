import os
import sys
from pathlib import Path

path = Path(os.getcwd())
sys.path.append(str(path))

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
from athena.src.services.backtest.backtest import Backtest
from athena.src.services.dashboard.configs import (
    DOMAINS_AVAILABLE,
    FILTERS_AVAILABLE,
    FILTERS_SECUNDARY_OPTIONS,
    OPTIMIZERS_AVAILABLE,
    OPTIMIZERS_SECUNDARY_OPTIONS,
    RULES_AVAILABLE,
    RULES_SECUNDARY_OPTIONS,
    SECTORS_AVAILABLE,
    TICKERS_AVAILABLE,
)
from dash import MATCH, Dash, Input, Output, State, dcc, html

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])

app.layout = html.Div(
    [
        # dbc.NavbarSimple(brand = f"Siga.Me", brand_href = "#", color = "white"),
        html.Label("Choose the domain/s you want to work with*"),
        dcc.Dropdown(DOMAINS_AVAILABLE, multi=True, id="domain-dropdown"),
        html.Div(children=[], id="rules-layout"),
        html.Br(),
        html.Label(
            "Do you want to add new a customized rule to your assets selection?",
            id="add-rule",
        ),
        html.Button("+", id="add-rule-button", n_clicks=0),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Br(),
                        html.Label("Select the filter you want.*", id="label-filter-0"),
                        dcc.Dropdown(
                            FILTERS_AVAILABLE,
                            id={"type": "filter-dropdown", "index": f"filter-0"},
                        ),
                    ],
                    id={"type": "filter-div", "index": f"filter-0"},
                )
            ],
            id="filters-layout",
        ),
        html.Br(),
        html.Label("Add another filter?", id="add-filter"),
        html.Button("+", id="add-filter-button", n_clicks=0),
        html.Div(
            children=[
                html.Br(),
                html.Label("Please add an optimizer.*", id="label-optimizer"),
                dcc.Dropdown(OPTIMIZERS_AVAILABLE, id=f"select-optimizer"),
            ],
            id="optimizer-layout",
        ),
        html.Br(),
        html.Label("How many years you want to backtest?*", id="label-period"),
        dcc.Input(type="number", min=1, step=1, id="input-period"),
        html.Br(),
        html.Button("RUN", id="run-button", n_clicks=0),
        html.Div(children=[], id="show-layout"),
    ],
    id="layout",
    style={"padding": 50, "flex": 1, "fontSize": 14},
)


@app.callback(
    Output("rules-layout", "children"),
    Input("add-rule-button", "n_clicks"),
    State("rules-layout", "children"),
    prevent_initial_call=True,
)
def add_rule(click: int, children: dict) -> dict:
    component = html.Div(
        children=[
            html.Br(),
            html.Label(
                "Select the rule you want in your asset selection.*",
                id=f"label-rule-{click}",
            ),
            dcc.Dropdown(
                RULES_AVAILABLE, id={"type": "rule-dropdown", "index": f"rule-{click}"}
            ),
        ],
        id={"type": "rule-div", "index": f"rule-{click}"},
    )

    children.append(component)
    return children


@app.callback(
    Output({"type": "rule-div", "index": MATCH}, "children"),
    Input({"type": "rule-dropdown", "index": MATCH}, "value"),
    State({"type": "rule-div", "index": MATCH}, "children"),
    prevent_initial_call=True,
)
def update_rules_options(value: str, children: dict) -> dict:
    if value is None:
        children = children[:3]

    else:
        children = children[:3]
        index = children[2]["props"]["id"]["index"][-1]
        rule_options = RULES_SECUNDARY_OPTIONS.get(value)

        for option in rule_options:
            if option.endswith("tickers"):
                drop_options = TICKERS_AVAILABLE

            else:
                drop_options = SECTORS_AVAILABLE

            name = value.replace("_", " the ")

            negation = "DON'T" if value.startswith("exclude") else ""

            br = html.Br()
            label = html.Label(
                f"{name} you {negation} want.*", id=f"label-rule-{index}-{option}"
            )
            option = dcc.Dropdown(
                drop_options, id=f"rule-options-{index}-{option}", multi=True
            )

            children += [br, label, option]

    return children


@app.callback(
    Output("filters-layout", "children"),
    Input("add-filter-button", "n_clicks"),
    State("filters-layout", "children"),
    prevent_initial_call=True,
)
def add_filter(click: int, children: dict) -> dict:
    component = html.Div(
        children=[
            html.Br(),
            html.Label("Select the filter you want.*", id=f"label-filter-{click}"),
            dcc.Dropdown(
                FILTERS_AVAILABLE,
                id={"type": "filter-dropdown", "index": f"filter-{click}"},
            ),
        ],
        id={"type": "filter-div", "index": f"filter-{click}"},
    )

    children.append(component)
    return children


@app.callback(
    Output({"type": "filter-div", "index": MATCH}, "children"),
    Input({"type": "filter-dropdown", "index": MATCH}, "value"),
    State({"type": "filter-div", "index": MATCH}, "children"),
    prevent_initial_call=True,
)
def update_filters_options(value: str, children: dict) -> dict:
    if value is None:
        children = children[:3]

    else:
        children = children[:3]
        index = children[2]["props"]["id"]["index"][-1]
        filter_options = FILTERS_SECUNDARY_OPTIONS.get(value)

        for option in filter_options:
            name = option.replace("_", " ")

            br = html.Br()
            label = html.Label(
                f"Select the {name} you want.*", id=f"label-filter-{index}-{option}"
            )
            option = dcc.Input(
                type="number", min=1, step=1, id=f"filter-options-{index}-{option}"
            )

            children += [br, label, option]

    return children


@app.callback(
    Output("optimizer-layout", "children"),
    [Input("select-optimizer", "value")],
    [State("optimizer-layout", "children")],
    prevent_initial_call=True,
)
def update_optimizer_options(value: str, children: dict) -> dict:
    if value is None:
        children = children[:3]

    else:
        children = children[:3]
        optimizer_options = OPTIMIZERS_SECUNDARY_OPTIONS.get(value)

        for option in optimizer_options:
            name = option.replace("_", " ")

            br = html.Br()
            label = html.Label(
                f"Select the {name} you want.", id=f"label-optimizer-{option}"
            )
            option = dcc.Dropdown(
                optimizer_options[option],
                id=f"optimizer-options-{option}",
                value=optimizer_options[option][0],
            )

            components = [br, label, option]
            children += components

    return children


@app.callback(
    Output("show-layout", "children"),
    Input("run-button", "n_clicks"),
    State("layout", "children"),
    prevent_initial_call=True,
)
def run(click: int, children: dict) -> dict:
    rules = get_rules(children)
    filters = get_filters(children)
    optimizer = get_optimizer(children)
    period = get_period(children)

    print("Backtesting...")
    backtest = Backtest(
        filters=filters, data_rules=rules, optimizer=optimizer, backtesting_years=period
    )
    backtest.backtest(plot_snapshot=False)

    fig = get_plot(backtest_returns=backtest.returns, period=period)
    graph = dcc.Graph(figure=fig)

    show_layout = children[-1]
    show_layout["props"]["children"] = [graph]

    return show_layout


def get_plot(backtest_returns: pd.DataFrame, period: int) -> go.Figure:
    data = yf.download("^BVSP", period=f"{period}y")

    new = pd.DataFrame(columns=["Portfolio", "Benchmark"])
    new["Portfolio"] = backtest_returns.astype(float)
    new["Benchmark"] = data["Close"].pct_change()

    new = new.dropna(how="any")
    fig = px.line(new.cumsum())
    fig.update_yaxes(tickformat="0.2%")

    return fig


def get_rules(children: dict) -> dict:
    rules = dict()

    domains = children[1]["props"].get("value", None)
    rules["domains"] = domains

    rules_layout = [
        child for child in children if child["props"].get("id", "") == "rules-layout"
    ][0]

    for rule_div in rules_layout["props"]["children"]:
        rule_type = rule_div["props"]["children"][2]["props"].get("value", None)
        chosen = rule_div["props"]["children"][5]["props"].get("value", None)

        rules[rule_type] = chosen

    return rules


def get_filters(children: dict) -> dict:
    filters = dict()

    filters_layout = [
        child for child in children if child["props"].get("id", "") == "filters-layout"
    ][0]

    for filter_div in filters_layout["props"]["children"]:
        filter_type = filter_div["props"]["children"][2]["props"].get("value", None)
        filters[filter_type] = dict()

        for filter_comp in filter_div["props"]["children"]:
            try:
                if filter_comp["props"]["id"].startswith("filter"):
                    option = filter_comp["props"]["id"].split("-")[-1]
                    value = filter_comp["props"].get("value", None)

                    filters[filter_type][option] = value
            except:
                pass

    return filters


def get_optimizer(children: dict) -> dict:
    optimizer = dict()

    opt_layout = [
        child
        for child in children
        if child["props"].get("id", "") == "optimizer-layout"
    ][0]
    opt_selected = opt_layout["props"]["children"][2]["props"].get("value", None)

    optimizer[opt_selected] = dict()

    for opt_comp in opt_layout["props"]["children"]:
        try:
            if opt_comp["props"]["id"].startswith("optimizer"):
                option = opt_comp["props"]["id"].split("-")[-1]
                value = opt_comp["props"].get("value", None)

                optimizer[opt_selected][option] = value

        except:
            pass

    return optimizer


def get_period(children: dict) -> int:
    period_comp = [
        child for child in children if child["props"].get("id", "") == "input-period"
    ][0]
    period = period_comp["props"].get("value", None)

    return period


if __name__ == "__main__":
    app.run_server(debug=True)
