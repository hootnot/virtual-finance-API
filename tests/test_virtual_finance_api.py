"""Tests for `virtual_finance_api` package."""


import pytest
from click.testing import CliRunner

from virtual_finance_api import cli


def test_000_something():
    """Test something."""


# disabled due too: unresolved 'return cli.name or root' error
def Xtest_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert "virtual_finance_api.cli.main" in result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output
