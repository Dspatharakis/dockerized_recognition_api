#!/bin/bash

gunicorn edge_server.edge_server:app -w $((2*$CPU_LIMIT+1)) --threads=2  --max-requests=30 -b 0.0.0.0:8000
