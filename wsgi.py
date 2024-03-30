"""
WSGI config for sentiment project.

To test locally, simply run `flask run` in the root directory of this project.
To deploy to production, use your preferred WSGI server.
"""
import os
import sys

# make sure the `python` dir is in the path for importing modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'python'))

# import the WSGI app from the server module
from server import app
