#!/bin/sh
# Builds Vast Star and packs it as the .hmod the Horizon registry takes, into dist/.
set -e
here="$(cd "$(dirname "$0")" && pwd)"
python3 -I "$here/tools/build_content.py" "$here/build"
mkdir -p "$here/dist"
version="$(sed -n 's/^version = "\(.*\)"/\1/p' "$here/build/vaststar/horizon-mod.toml")"
file="$here/dist/vaststar-$version.hmod"
rm -f "$file"
# The MIT notice goes with every copy.
cp "$here/LICENSE" "$here/build/vaststar/LICENSE"
(cd "$here/build/vaststar" && zip -q -X -r -9 "$file" .)
echo "$file  $(shasum -a 256 "$file" | cut -d' ' -f1)"
