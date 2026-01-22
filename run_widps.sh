#!/usr/bin/env bash
set -euo pipefail

echo "=============================="
echo "   WIDPS FULL SYSTEM BOOTSTRAP "
echo "=============================="

# -------- CONFIG --------
INTERFACE="wlp0s20f3"
DATA_DIR="$(pwd)/data"
AIRODUMP_PREFIX="$DATA_DIR/widps_capture"
CPP_BUILD_DIR="cpp_sniffer/build"
CPP_BINARY="$CPP_BUILD_DIR/sniffer"
FASTAPI_URL="http://127.0.0.1:8000/ingest"
# ------------------------

AIRODUMP_PID=""
SNIFFER_PID=""

cleanup() {
  echo ""
  echo "[CLEANUP] Shutting down WIDPS..."

  if [[ -n "$AIRODUMP_PID" ]]; then
    echo "[CLEANUP] Killing airodump-ng (PID $AIRODUMP_PID)"
    sudo kill "$AIRODUMP_PID" 2>/dev/null || true
  fi

  if [[ -n "$SNIFFER_PID" ]]; then
    echo "[CLEANUP] Killing sniffer (PID $SNIFFER_PID)"
    sudo kill "$SNIFFER_PID" 2>/dev/null || true
  fi

  echo "[CLEANUP] Stopping monitor mode"
  sudo airmon-ng stop "${INTERFACE}mon" >/dev/null 2>&1 || true

  echo "[CLEANUP] Done."
}
trap cleanup EXIT INT TERM

# STEP 1: Enable monitor mode
echo "[1/4] Enabling monitor mode on $INTERFACE"
sudo airmon-ng start "$INTERFACE" >/dev/null

MON_IFACE="${INTERFACE}mon"

if ! iw dev | grep -q "$MON_IFACE"; then
  echo "[ERROR] Monitor mode interface not found"
  exit 1
fi

echo "[OK] Monitor mode active on $MON_IFACE"

# STEP 2: Start airodump-ng
echo "[2/4] Starting airodump-ng"
mkdir -p "$DATA_DIR"

sudo airodump-ng \
  --write "$AIRODUMP_PREFIX" \
  --output-format csv \
  "$MON_IFACE" \
  > /dev/null 2>&1 &
  AIRODUMP_PID=$!


echo "[OK] Airodump PID: $AIRODUMP_PID"
sleep 5

# ------------------------
# STEP 3: Build & run C++ sniffer
# ------------------------
echo "[3/4] Building C++ sniffer"

mkdir -p "$CPP_BUILD_DIR"
cd "$CPP_BUILD_DIR"
cmake ..
make -j"$(nproc)"
cd ../..

# auto-detect latest CSV
CSV_FILE="$(ls -t "$DATA_DIR"/widps_capture-*.csv | head -n 1)"

if [[ ! -f "$CSV_FILE" ]]; then
  echo "[ERROR] No airodump CSV found"
  exit 1
fi

echo "[INFO] Using CSV: $CSV_FILE"
echo "[INFO] Starting sniffer (READ_EXISTING=1)"

sudo READ_EXISTING=1 \
  "./$CPP_BINARY" \
  "$CSV_FILE" \
  "$FASTAPI_URL" &
SNIFFER_PID=$!

echo "[OK] Sniffer PID: $SNIFFER_PID"

# block until sniffer exits
wait "$SNIFFER_PID"
