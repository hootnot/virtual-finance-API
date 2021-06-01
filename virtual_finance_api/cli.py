#!/usr/bin/env python
"""Console script for virtual_finance_api."""

import pandas as pd
import yachain
import typer
import logging
from typing import List

import virtual_finance_api as fa
import virtual_finance_api.compat.yfinance.endpoints as yf
import virtual_finance_api.endpoints.yahoo.types as types


app = typer.Typer()
logger = logging.getLogger(__name__)


client = fa.Client()
PERIODS = [t.value for t in types.Period]
INTERVALS = [t.value for t in types.Interval]


def do_rep(r, repcats: List[str]) -> str:  # pragma: no cover
    if repcats.count(None) == len(repcats):
        typer.echo("missing info flag parameter")
        raise typer.Exit()

    client.request(r)
    for repcat in repcats:
        if repcat:
            yield getattr(r, repcat)


@app.command()
def profile(
    info: str = typer.Option(
        False, "--info", "-i", flag_value="info", help="JSON info data"
    ),
    calendar: str = typer.Option(
        False, "--calendar", "-c", flag_value="calendar", help="calendar"
    ),
    sustainability: str = typer.Option(
        False,
        "--sustainability",
        "-s",
        flag_value="sustainability",
        help="sustainability",
    ),
    recommendations: str = typer.Option(
        False,
        "--recommentations",
        "-r",
        flag_value="recommendations",
        help="recommendations",
    ),
    ticker: str = typer.Argument(...),
) -> None:  # pragma: no cover
    """Profile."""
    repcats = [info, calendar, sustainability, recommendations]
    if repcats.count(None) == len(repcats):
        typer.echo("missing info flag parameter")
        raise typer.Exit()

    for _ in do_rep(yf.Profile(ticker), repcats):
        print(_)


@app.command()
def financials(
    balancesheet: str = typer.Option(
        False, "--balancesheet", "-b", flag_value="balancesheet", help="Balance sheet"
    ),
    earnings: str = typer.Option(
        False, "--earnings", "-e", flag_value="earnings", help="Earnings"
    ),
    cashflow: str = typer.Option(
        False, "--cashflow", "-c", flag_value="cashflow", help="Cashflow"
    ),
    financials: str = typer.Option(
        False, "--financials", "-f", flag_value="financials", help="Financials"
    ),
    reportperiod: types.ReportPeriod = typer.Option(
        types.ReportPeriod.y, help="Report period"
    ),
    ticker: str = typer.Argument(...),
) -> None:  # pragma: no cover
    """Financials."""
    repcats = [balancesheet, earnings, cashflow, financials]
    if repcats.count(None) == len(repcats):
        typer.echo("missing info flag parameter")
        raise typer.Exit()

    rp = "yearly" if reportperiod == "y" else "quarterly"
    for _ in do_rep(yf.Financials(ticker), repcats):
        print(_[rp])


@app.command()
def holders(
    major: str = typer.Option(False, "--major", "-m", flag_value="major", help="major"),
    mutualfund: str = typer.Option(
        False, "--mutualfund", "-f", flag_value="mutualfund", help="mutual fund"
    ),
    institutional: str = typer.Option(
        False, "--institutional", "-i", flag_value="institutional", help="institutional"
    ),
    ticker: str = typer.Argument(...),
) -> None:  # pragma: no cover
    """Holders."""
    repcats = [major, mutualfund, institutional]
    if repcats.count(None) == len(repcats):
        typer.echo("missing info flag parameter")
        raise typer.Exit()

    for _ in do_rep(yf.Holders(ticker), repcats):
        print(_)


@app.command()
def history(
    period: types.Period = typer.Option(
        types.Period.p_1mo, "--period", "-p", help="Period"
    ),
    interval: types.Interval = typer.Option(
        types.Interval.i_1d, "--interval", "-i", help="Interval"
    ),
    adjust: types.AdjustType = typer.Option(None, "--adjust", "-a", help="Adjust"),
    csv: bool = typer.Option(False, help="CSV format"),
    ticker: str = typer.Argument(...),
) -> None:  # pragma: no cover
    """History."""
    params = {"period": period, "interval": interval}
    params.update({"auto_adjust": False})
    params.update({"back_adjust": False})
    if adjust:
        if adjust.value == types.AdjustType.auto:
            params.update({"auto_adjust": True})
        elif adjust.value == types.AdjustType.back:
            params.update({"back_adjust": True})

    r = yf.History(ticker, params=params)
    client.request(r)
    print(r.history.to_csv() if csv is True else r.history)


if __name__ == "__main__":  # pragma: no cover
    import sys
    import os

    pd.set_option("display.max_rows", None)
    VFA = os.getenv("VFA")
    if VFA is not None:
        cfg = yachain.Config().load(f"{VFA}/etc/vfa.cfg")
        logging.basicConfig(
            filename=f"{VFA}/" + cfg["vfa::logging::logfile"],
            level=getattr(logging, cfg["vfa::logging::loglevel"]),
            format=cfg["vfa::logging::format"],
        )

    else:
        logging.basicConfig(stream=sys.stderr, level=logging.INFO)
        logger.info("VFA not configured, using defaults")

    app()
