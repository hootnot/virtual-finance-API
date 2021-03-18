#!/usr/bin/env python

"""Tests for `virtual_finance_api` package."""


import unittest
from click.testing import CliRunner

from virtual_finance_api import virtual_finance_api
from virtual_finance_api import cli


class TestVirtual_finance_api(unittest.TestCase):
    """Tests for `virtual_finance_api` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'virtual_finance_api.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
