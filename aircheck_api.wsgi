#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/AirCheck/rest/")

from server import app as application
application.secret_key = 'barry_allen'
