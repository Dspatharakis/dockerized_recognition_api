#!/bin/bash

gunicorn edge_server.edge_server:app -w $(( 2 * `cat /proc/cpuinfo | grep 'core id'| wc -l` + 1 )) -b 0.0.0.0:8000
