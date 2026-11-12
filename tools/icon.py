#!/usr/bin/env python3
"""Draws icons/vaststar.png (256x256): the Vast Star on the night it is made in."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_content import png, star  # noqa: E402

SIZE = 64


def main():
    sky = (0x14, 0x0E, 0x22, 255)
    px = [[sky] * SIZE for _ in range(SIZE)]
    for x, y in ((6, 9), (51, 7), (57, 40), (9, 52), (44, 56), (20, 4), (60, 22), (3, 30)):
        px[y][x] = (0xE8, 0xE0, 0xFF, 255)
    s = star(0.0, 48)
    for y in range(48):
        for x in range(48):
            if s[y][x][3]:
                px[y + 8][x + 8] = s[y][x]
    big = [[px[y // 4][x // 4] for x in range(SIZE * 4)] for y in range(SIZE * 4)]
    out = Path(__file__).resolve().parent.parent / "icons/vaststar.png"
    out.write_bytes(png(big))
    print(out)


if __name__ == "__main__":
    main()
