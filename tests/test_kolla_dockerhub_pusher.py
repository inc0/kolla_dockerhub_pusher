#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_kolla_dockerhub_pusher
----------------------------------

Tests for `kolla_dockerhub_pusher` module.
"""


import sys
import unittest
from contextlib import contextmanager
from click.testing import CliRunner

from kolla_dockerhub_pusher import kolla_dockerhub_pusher
from kolla_dockerhub_pusher import cli



class TestKolla_dockerhub_pusher(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_000_something(self):
        pass

    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'kolla_dockerhub_pusher.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output