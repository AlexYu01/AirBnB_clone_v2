#!/usr/bin/python3
"""
    Starts a Flash web application
"""
from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """
        Prints `Hello HBNB!` when accessing root of website
    """
    return 'Hello HBNB!'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
