#!/bin/sh
# Neue Versionsnummer für daten.js in index.html, damit Browser neue Daten sofort laden.
cd "$(dirname "$0")/.." && sed -i -E "s|daten\.js(\?v=[0-9]+)?\"|daten.js?v=$(TZ=Europe/Berlin date +%Y%m%d%H%M)\"|" index.html && grep -o 'daten.js?v=[0-9]*' index.html
