#!/bin/sh

if [ -z "$PORT" ]; then
    PORT=8080 
fi

exec poetry run waitress-serve --host=0.0.0.0 --port=$PORT wsgi:application