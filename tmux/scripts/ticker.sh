#!/usr/bin/env bash
# Usage: ticker.sh SYMBOL [LABEL]
# Examples: ticker.sh VGT | ticker.sh %5EGSPC S&P500
SYMBOL="${1:-VGT}"
export LABEL="${2:-$SYMBOL}"
CACHE_DIR="/tmp/tmux-ticker"
CACHE_FILE="$CACHE_DIR/$SYMBOL.cache"
CACHE_TTL=300 # 5 minutes

mkdir -p "$CACHE_DIR"

# Use cache if fresh enough
if [ -f "$CACHE_FILE" ]; then
  age=$(( $(date +%s) - $(stat -f %m "$CACHE_FILE") ))
  if [ "$age" -lt "$CACHE_TTL" ]; then
    cat "$CACHE_FILE"
    exit 0
  fi
fi

result=$(curl -s -A "Mozilla/5.0" "https://query1.finance.yahoo.com/v8/finance/chart/${SYMBOL}?range=1d&interval=1d" | python3 -c "
import sys,json,os
label=os.environ['LABEL']
d=json.load(sys.stdin)
r=d['chart']['result'][0]['meta']
price=r['regularMarketPrice']
prev=r['chartPreviousClose']
pct=((price-prev)/prev)*100
color='#[fg=green]' if pct >= 0 else '#[fg=red]'
print(f\"{color} {label}: {price:,.2f} ({pct:+.2f}%)\")
" 2>/dev/null)

if [ -n "$result" ]; then
  echo -n "$result" | tee "$CACHE_FILE"
else
  [ -f "$CACHE_FILE" ] && cat "$CACHE_FILE" || echo -n "$LABEL: --"
fi
