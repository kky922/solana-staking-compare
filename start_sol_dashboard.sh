#!/bin/bash
cd "$(dirname "$0")"
echo "🪙 SOL 스테이킹 비교 대시보드 시작..."
streamlit run sol_dashboard.py --server.port 8555 --server.address 0.0.0.0