#!/bin/sh
# Start the AEGIS Sky Map (macOS / Linux / ChromeOS Linux):  sh start_sky_map.sh   [--lan]
cd "$(dirname "$0")" && exec python3 serve.py "$@"
