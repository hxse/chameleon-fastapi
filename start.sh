#!/bin/sh
uv run python ./src/plot/bokeh_server.py /app/src/fig_data 15000 & uv run python ./src/fast_api_demo.py /app/src/fig_data
