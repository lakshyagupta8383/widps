#!/usr/bin/env bash
set -euo pipefail

# ------------------------
# LOAD ENV
# ------------------------
if [[ -f ".env" ]]; then
  export $(grep -v '^#' .env | xargs)
else
  echo "[ERROR] .env file not found"
  exit 1
fi

echo "=============================="
echo "   WIDPS FULL SYSTEM BOOTSTRAP "
echo "=============================="

# Expand paths safely
DATA_DIR="$(pwd)/${DATA_DIR}"
AIRODUMP_PREFIX="${DATA_DIR}/${AIRODUMP_PREFIX}"
CPP_BINARY_PATH="${CPP_BUILD_DIR}/${CPP_BINARY}"

AIRODUMP_PID=""
SNIFFER_PID=""

cleanup() {
  echo ""
  echo "[CLEANUP] Shutting down WIDPS..."

  if [[ -n "${AIRODUMP_PID:-}" ]]; then
    sudo kill "$AIRODUMP_PID" 2>/dev/null || true
  fi

  if [[ -n "${SNIFFER_PID:-}" ]]; then
    sudo kill "$SNIFFER_PID" 2>/dev/null || true
  fi

  echo "[CLEANUP] Stopping monitor mode"
  sudo airmon-ng stop "${INTERFACE}mon" >/dev/null 2>&1 || true

  echo "[CLEANUP] Done."
}
trap cleanup EXIT INT TERM


# ------------------------
# STEP 1: Enable monitor mode
# ------------------------
echo "[1/4] Enabling monitor mode on $INTERFACE"
sudo airmon-ng start "$INTERFACE" >/dev/null

MON_IFACE="${INTERFACE}mon"

if ! iw dev | grep -q "$MON_IFACE"; then
  echo "[ERROR] Monitor mode interface not found"
  exit 1
fi

echo "[OK] Monitor mode active on $MON_IFACE"


# ------------------------
# STEP 2: Start airodump-ng
# ------------------------
echo "[2/4] Starting airodump-ng"

mkdir -p "$DATA_DIR"

sudo airodump-ng \
  --write "$AIRODUMP_PREFIX" \
  --output-format csv \
  "$MON_IFACE" \
  > /dev/null 2>&1 &
AIRODUMP_PID=$!

echo "[OK] Airodump PID: $AIRODUMP_PID"
sleep "${AIRODUMP_WARMUP}"


# ------------------------
# STEP 3: Build C++ Sniffer
# ------------------------
echo "[3/4] Building C++ sniffer"

mkdir -p "$CPP_BUILD_DIR"
cd "$CPP_BUILD_DIR"
cmake ..
make -j"$(nproc)"
cd - >/dev/null

echo "[OK] Sniffer built"


# ------------------------
# STEP 4: Run Sniffer
# ------------------------
echo "[4/4] Starting sniffer"

CSV_FILE="$(ls -t "$DATA_DIR"/${AIRODUMP_PREFIX##*/}-*.csv | head -n 1)"

if [[ ! -f "$CSV_FILE" ]]; then
  echo "[ERROR] No airodump CSV found"
  exit 1
fi

echo "[INFO] Using CSV: $CSV_FILE"

sudo READ_EXISTING=1 \
  "./$CPP_BINARY_PATH" \
  "$CSV_FILE" \
  "$FASTAPI_URL" &
SNIFFER_PID=$!

echo "[OK] Sniffer PID: $SNIFFER_PID"

echo "[RUNNING] WIDPS active..."
wait "$SNIFFER_PID"
