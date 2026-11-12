#!/bin/sh
# Rebuilds Vast Star and installs it into Horizon (a content mod: restart Horizon, no game rebuild).
set -e
here="$(cd "$(dirname "$0")" && pwd)"
mods="$HOME/Library/Application Support/horizon/horizon-mods"
python3 -I "$here/tools/build_content.py" "$here/build"
rm -rf "$mods/vaststar"
cp -R "$here/build/vaststar" "$mods/vaststar"
echo "Installed. Restart Horizon."
