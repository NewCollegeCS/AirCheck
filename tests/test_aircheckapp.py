#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from aircheck.aircheckapp import AircheckApp

class TestAircheckApp(unittest.TestCase):
    """TestCase for Aircheck.
    """
    def setUp(self):
        self.app = AircheckApp()

    def test_name(self):
        self.assertEqual(self.app.name, 'aircheck')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
