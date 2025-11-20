#!/bin/bash
# 使用 conda 環境運行 GUI 程式
cd "$(dirname "$0")"
conda run -n base python tmdb_0583404.py

