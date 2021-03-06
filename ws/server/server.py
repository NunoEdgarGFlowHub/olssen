#!/usr/bin/env python

import time, sys, cherrypy
from paste.translogger import TransLogger
from api import create_app
from pyspark import SparkContext, SparkConf


def init_spark_context():
    # load spark context
    conf = SparkConf().setAppName("spectral-search-server")
    #  .set("spark.executor.memory", "6g")
    sc = SparkContext(conf=conf, pyFiles=['engine.py', 'api.py'])

    return sc


def run_server(app):

    # Enable WSGI access logging via Paste
    app_logged = TransLogger(app)

    # Mount the WSGI callable object (app) on the root directory
    cherrypy.tree.graft(app_logged, '/')

    # Set the configuration of the web server
    cherrypy.config.update({
        'engine.autoreload.on': True,
        'log.screen': True,
        'server.socket_port': 5432,
        'server.socket_host': '0.0.0.0'
    })

    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == "__main__":
    # Init spark context and load libraries
    sc = init_spark_context()
    api_app = create_app(sc)

    # start web server
    run_server(api_app)
