#!/bin/sh


exec poetry run waitress-serve --host=0.0.0.0 --port=8080 wsgi:application