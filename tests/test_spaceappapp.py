#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from spaceapp.spaceappapp import SpaceappApp


class TestSpaceappApp(unittest.TestCase):
    """TestCase for SpaceappApp.
    """
    def setUp(self):
        self.app = SpaceappApp()

    def test_name(self):
        self.assertEqual(self.app.name, 'spaceapp')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
