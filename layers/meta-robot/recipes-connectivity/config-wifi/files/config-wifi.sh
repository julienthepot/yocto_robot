#!/bin/bash

set -eu

# Runtime WiFi configuration file. Keep this file out of git and protect it with 0600 permissions.
ENV_FILE="${CONFIG_WIFI_ENV_FILE:-/etc/default/config-wifi}"

if [ -f "$ENV_FILE" ]; then
	# shellcheck disable=SC1090
	. "$ENV_FILE"
fi

WIFI_ID="${WIFI_ID:-}"
WIFI_NAME="${WIFI_NAME:-}"
WIFI_SSID_HEX="${WIFI_SSID_HEX:-}"
WIFI_FREQUENCY="${WIFI_FREQUENCY:-2412}"
WIFI_PASSPHRASE="${WIFI_PASSPHRASE:-}"
WIFI_PASSPHRASE_FILE="${WIFI_PASSPHRASE_FILE:-}"

if [ -n "$WIFI_PASSPHRASE_FILE" ] && [ -f "$WIFI_PASSPHRASE_FILE" ]; then
	WIFI_PASSPHRASE="$(head -n 1 "$WIFI_PASSPHRASE_FILE")"
fi

if [ -z "$WIFI_ID" ] || [ -z "$WIFI_NAME" ] || [ -z "$WIFI_SSID_HEX" ] || [ -z "$WIFI_PASSPHRASE" ]; then
	echo "Missing WiFi configuration in $ENV_FILE. Required: WIFI_ID, WIFI_NAME, WIFI_SSID_HEX, WIFI_PASSPHRASE (or WIFI_PASSPHRASE_FILE)." >&2
	exit 1
fi

echo "Configuring WiFi settings..."
ip link | grep -q wlan0 || echo "wlan0 interface not found."

CONFIG_DIR="/data/connman/${WIFI_ID}_managed_psk"
CONFIG_FILE="${CONFIG_DIR}/settings"

mkdir -p "$CONFIG_DIR"
umask 077
cat > "$CONFIG_FILE" <<EOF
[${WIFI_ID}_managed_psk]
Name=${WIFI_NAME}
SSID=${WIFI_SSID_HEX}
Frequency=${WIFI_FREQUENCY}
Favorite=true
AutoConnect=true
Passphrase=${WIFI_PASSPHRASE}
IPv4.method=dhcp
EOF

systemctl restart connman
connmanctl enable wifi
connmanctl scan wifi
connmanctl services
