#!/usr/bin/env python
"""Console script for virtual_finance_api."""

import sys
import click
from typing import List

import virtual_finance_api as fa
import virtual_finance_api.compat.yfinance.endpoints as yf
import virtual_finance_api.types as types


client = fa.Client()
PERIODS = [t.value for t in types.Period]
INTERVALS = [t.value for t in types.Interval]


@click.group()
def vfa():  # pragma: no cover
    """Virtual Finance API commandline app."""
    pass


@vfa.group()
def profile():  # pragma: no cover
    pass


@vfa.group()
def financials():  # pragma: no cover
    pass


@vfa.group()
def holders():  # pragma: no cover
    pass


@vfa.group()
def history():  # pragma: no cover
    pass


@profile.command("profile")
@click.option("--info", flag_value="info", help="JSON info data")
@click.option("--calendar", flag_value="calendar")
@click.option("--sustainability", flag_value="sustainability")
@click.option("--recommendations", flag_value="recommendations")
@click.argument("ticker")
def get_profile(
    info, calendar, sustainability, recommendations, ticker
) -> None:  # pragma: no cover
    """Profile."""
    repcats = [info, calendar, sustainability, recommendations]
    if repcats.count(None) == len(repcats):
        raise click.BadParameter("missing info flag parameter")

    for _ in do_rep(yf.Profile(ticker), repcats):
        print(_)


@financials.command("financials")
@click.option(
    "--reportperiod", type=click.Choice(["y", "q"], case_sensitive=False), default="y"
)  # pragma: no cover
@click.option("--balancesheet", flag_value="balancesheet")
@click.option("--earnings", flag_value="earnings")
@click.option("--cashflow", flag_value="cashflow")
@click.option("--financials", flag_value="financials")
@click.argument("ticker")
def get_financials(
    reportperiod, balancesheet, earnings, cashflow, financials, ticker
) -> None:  # pragma: no cover
    # """Financials."""
    repcats = [balancesheet, earnings, cashflow, financials]
    if repcats.count(None) == len(repcats):
        raise click.BadParameter("missing info flag parameter")

    rp = "yearly" if reportperiod == "y" else "quarterly"
    for _ in do_rep(yf.Financials(ticker), repcats):
        print(_[rp])


@holders.command("holders")
@click.option("--major", flag_value="major")
@click.option("--mutualfund", flag_value="mutualfund")
@click.option("--institutional", flag_value="institutional")
@click.argument("ticker")
def get_holders(major, mutualfund, institutional, ticker) -> None:  # pragma: no cover
    # """Holders."""
    repcats = [major, mutualfund, institutional]
    if repcats.count(None) == len(repcats):
        raise click.BadParameter("missing info flag parameter")

    for _ in do_rep(yf.Holders(ticker), repcats):
        print(_)


@holders.command("history")
@click.option(
    "--period", type=click.Choice(PERIODS, case_sensitive=False), default="1mo"
)
@click.option(
    "--interval", type=click.Choice(INTERVALS, case_sensitive=False), default="1d"
)
@click.option("--csv", flag_value="csv")
@click.argument("ticker")
def get_history(period, interval, csv, ticker) -> None:  # pragma: no cover
    # """History."""
    params = {"period": period, "interval": interval}
    r = yf.History(ticker, params=params)
    client.request(r)
    print(r.history.to_csv() if csv == "csv" else r.history)


def do_rep(r, repcats: List[str]) -> str:  # pragma: no cover
    if repcats.count(None) == len(repcats):
        raise click.BadParameter("missing info flag parameter")

    client.request(r)
    for repcat in repcats:
        if repcat:
            yield getattr(r, repcat)


def main() -> None:  # pragma: no cover
    vfa.add_command(get_profile)
    vfa.add_command(get_financials)
    vfa.add_command(get_holders)
    vfa.add_command(get_history)
    vfa()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
