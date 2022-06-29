
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
from typing import Dict, List, Set

from inari.main import DataIngestion
import pandas as pd
import yfinance as yf

from athena.src.utils import utils


class Data:

    """


            This is the data aquisition module of the backtest and pipeline. It give many choices in how 
        to select the data you want to work with. This uses the same way of parsing rules of the other modules.
        
        This module works only to select the universe of assets to be passed to the pipeline and/or backtest.
        You must give a dictionary as an input, with all the rules you want to be applied to the assets selection processing.

        This module work in the following way:

            1. Specify the domain of the assets you want. You specify it through a key "domains", which contains a list of the domains
            you want;

            2.1 Verify INCLUSIVE rules, if they are provided;

            2.2 If they are not provided, every ticker of every sector of the domains you specified will be used;

            3. Build the tickers universe;

                Example:
                    rules = {
                        "domains": ["stocks", "bdrs"],
                        "include_sectors": ["Technology", "Healthcare"],
                        "include_tickers": ["VALE3.SA"]
                    }

                    In this example, I want to work with stocks and BDRs. But I only want the one that are part of the Technology and Healthcare
                sectors. Also, for any reason, I want to include VALE3.SA, which is not part of any of the sectors I selected.

                Example 2:
                    rules = {
                        "domains": ["fiis", "variable etfs"]
                    }

                    In this case, I want the work with FIIs and variable income ETFs, and as I didn't specified any inclusive rule,
                every ticker available of these two domains will be used.
                
            4. Verify EXCLUSIONARY rules.

                Example 3:
                    rules = {
                        "domains": ["stocks"]
                        "exclude_sectors": ["Technology", "Healthcare"]
                        "exclude_tickers": ["PETR4"]
                    }

                    In this example I want to use only stocks. As there are no inclusive rules, the data wants to use every ticker of every
                sector of stocks. But I can tell it that out of every sector available, I do NOT want the Technology and Healthcare sectors. Also, I 
                can tell it that I don't want to consider the PETR4.SA ticker, for whatever reason.


        You must always, at least, inform the domains you want to use. If none is given, the default if to use "stocks" only. You do this by using
        the "domains" dictionary key, which must contain a LIST of domains, even you want only one domain.

        The rules that you can use are separeted into two categories:

            1. INCLUSIVE rules: rules that will the selection system to ONLY use what you tell it to use. They are applied BEFORE the universe is difined.

                1.1 "include_tickers": this rule will specify which tickers you want to use. The selector will ONLY use these tickers;
                1.2 "include_sectors": here you will specify the ONLY sectors that you want to use.

            2. EXCLUSIONARY rules: rules that will tell the system what NOT to use. They are applied AFTER the universe is difined.

                2.1 "exclude_tickers": this will exclude the tickers you selected, and leave the rest of the universe;
                2.2 "exclude_sectors": this will exclude the tickers that belong to the specified sectors, across the domains;

        You can use the following domains: "stocks", "bdrs", "variable etfs", "fixed etfs", "fiis".

        You can use the following sectors: "Financial Services", "Consumer Defensive", "Industrials", "Consumer Cyclical", "Real Estate", "Basic Materials",
        "Communication Services", "Utilities", "Technology", "Energy", "Healthcare", "Financial", "Fixed ETF" and "Variable ETF". These sector are the consistent
        across the domains.


    """


    rules      : dict
    tickers    : Set[str]
    domains    : Set[str]
    start_date : datetime
    sectors_map: Dict[str, Set[str]]                                        # I don't use this now, but maybe I will


    def __init__(self, start_date: datetime, rules: dict) -> None:
        default_rules = {"domains": ["stocks"]}

        self.rules       = rules if rules is not None else default_rules
        self.tickers     = set()
        self.start_date  = start_date
        self.domains     = set()
        self.sectors_map = dict()

        self._get_tickers()


    def _get_tickers(self) -> None:
        self._get_domains()
        
        self._inclusive_rules()

        if len(self.tickers) == 0:                                          # Means that that were no inclusive rules
            self._get_domains_full_tickers()

        self._exclusionary_rules()


    def _get_domains(self) -> None:
        domains = self.rules.get("domains", None)
        utils.validate_domains(domains = domains)
        self.domains = set(domains)


    def _get_domains_full_tickers(self) -> None:
        path_dir = Path(__file__).parent.resolve()

        for domain in self.domains:
            domain_paths = {
                "stocks"       : "stock_sectors",
                "bdrs"         : "bdr_sectors",
                "fixed etfs"   : "fixed_etfs",
                "fiis"         : "fii_sectors",
                "variable etfs": "variable_etfs"
            }

            path = domain_paths.get(domain, None)

            with open(os.path.join(path_dir, f"{path}.json")) as f:
                domain_sectors = json.load(f)

            for sector in domain_sectors:
                tickers = domain_sectors[sector]

                if sector not in self.sectors_map:
                    self.sectors_map[sector] = set()
                
                self.sectors_map[sector] = self.sectors_map[sector].union(tickers)
                self.tickers             = self.tickers.union(tickers)
                

    def _inclusive_rules(self) -> None:
        rules_table = {
            "include_sectors": self._include_sectors,
            "include_tickers": self._include_tickers
        }

        for rule in self.rules:
            rule_function = rules_table.get(rule, None)

            if rule_function is not None:
                rule_function(args = self.rules[rule])


    def _include_tickers(self, args: List[str]) -> None:
        tickers = [ticker if ticker.endswith(".SA") else f"{ticker}.SA" for ticker in args]
        self.tickers = self.tickers.union(tickers)


    def _include_sectors(self, args: List[str]) -> None:
        path_dir = Path(__file__).parent.resolve()

        for domain in self.domains:
            utils.validate_domain_sectors(sectors = args)

            domain_paths = {
                "stocks"       : "stock_sectors",
                "bdrs"         : "bdr_sectors",
                "fixed etfs"   : "fixed_etfs",
                "fiis"         : "fii_sectors",
                "variable etfs": "variable_etfs"
            }
            
            path = domain_paths.get(domain, None)

            with open(os.path.join(path_dir, f"{path}.json")) as f:
                domain_sectors = json.load(f)

            for sector in args:
                tickers = domain_sectors.get(sector, None)

                if tickers is None:
                    pass

                else:
                    if sector not in self.sectors_map:
                        self.sectors_map[sector] = set()

                    self.sectors_map[sector] = self.sectors_map[sector].union(tickers)
                    self.tickers             = self.tickers.union(tickers)


    def _exclusionary_rules(self) -> None:
        rules_table = {
            "exclude_tickers": self._exclude_tickers,
            "exclude_sectors": self._exclude_sectors
        }

        for rule in self.rules:
            rule_function = rules_table.get(rule)

            if rule_function is not None:
                rule_function(args = self.rules.get(rule))


    def _exclude_tickers(self, args: List[str]) -> None:
        tickers = [ticker if ticker.endswith(".SA") else f"{ticker}.SA" for ticker in args]

        for ticker in tickers:
            self.tickers.remove(ticker)


    def _exclude_sectors(self, args: List[str]) -> None:
        path_dir = Path(__file__).parent.resolve()

        for domain in self.domains:
            utils.validate_domain_sectors(sectors = args)

            domain_paths = {
                "stocks"       : "stock_sectors",
                "bdrs"         : "bdr_sectors",
                "fixed etfs"   : "fixed_etfs",
                "fiis"         : "fii_sectors",
                "variable etfs": "variable_etfs"
            }

            path = domain_paths.get(domain, None)

            with open(os.path.join(path_dir, f"{path}.json")) as f:
                domain_sectors = json.load(f)

            for sector in args:
                tickers = domain_sectors.get(sector, None)

                if tickers is None:
                    raise ValueError(f"The domain {domain} domain doesn't have {sector} sector. Only {list(domain_sectors.keys())}.")

                else:
                    del self.sectors_map[sector]

                    for ticker in tickers:
                        self.tickers.remove(ticker)


    def _download_data(self, yahoo: bool) -> None:
        if yahoo:
            ydata = yf.download(self.tickers, start = self.start_date)
            ydata = ydata.astype(float).interpolate("ffill")

            data = dict()

            for column in ydata.columns.levels[0]:
                df = ydata[column].copy()
                df.columns = [ticker.split(".")[0] for ticker in df.columns]
                data[column] = df

            data = pd.concat(data, axis = 1)
            data.index.name = None

        else:
            start_date = self.start_date

            dataingestion = DataIngestion()

            needed_info = {
                "domains"   : ["stocks", "variable etfs", "fixed etfs"],
                # "tickers"   : tickers,
                "info_types": ["Close", "Volume", "Open"]
            }

            data = dataingestion.get_data(needed_info = needed_info, start_date = start_date)
        
        data = data.astype(float) #.interpolate(method = "ffill")

        return data


    def get_data(self, yahoo: bool = False) -> pd.DataFrame:
        data = self._download_data(yahoo)

        return data