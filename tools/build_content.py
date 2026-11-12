#!/usr/bin/env python3
"""Builds Vast Star, a content mod for Horizon: the long climb's last craft. Five cores, each the best of one mod
of the Vast family (Vast Depths, Vast Ores, Vast Compressed, Vast Adventures) or of the game itself, a Star Seed,
and the Vast Star they make, with a block of nine.

The chain, its names and its art are this mod's own; the sprites are drawn below pixel by pixel. It needs Vast
Depths, Vast Ores, Vast Compressed and Vast Adventures for the cores' recipes.
Usage: build_content.py <output dir>   (writes <output dir>/vaststar)
"""
import json
import math
import shutil
import struct
import sys
import zlib
from pathlib import Path

NS = "vaststar"
VERSION = "0.1.0"

# ---- the chain ----------------------------------------------------------------------

# name, english, portuguese, rarity, (lore en, lore pt), pattern, key
CORES = [
    ("deep_core", "Core of the Deep", "Núcleo das Profundezas", "rare",
     ("Stellarite, Infernium and Voidium, pressed into one.", "Estelarita, Infernium e Voidium, prensados em um só."),
     ["SXS", "IVI", "SZS"],
     {"S": "vastdepths:stellarite_block", "I": "vastdepths:infernium_block", "V": "vastdepths:voidium_block",
      "X": "vastdepths:infernium_stellarite_alloy_block", "Z": "vastdepths:voidium_infernium_alloy_block"}),
    ("alloy_core", "Core of Alloys", "Núcleo das Ligas", "rare",
     ("Every alloy the furnace knows.", "Todas as ligas que a fornalha conhece."),
     ["ABC", "DEF", "GHI"],
     {"A": "vastores:bronze_block", "B": "vastores:brass_block", "C": "vastores:constantan_block",
      "D": "vastores:electrum_block", "E": "vastores:enderium_block", "F": "vastores:invar_block",
      "G": "vastores:steel_block", "H": "vastores:lumium_block", "I": "vastores:signalum_block"}),
    ("pressure_core", "Core of Pressure", "Núcleo da Pressão", "rare",
     ("Millions of blocks, and the weight of them.", "Milhões de blocos, e o peso deles."),
     ["CNC", "EDE", "CNC"],
     {"C": "vastcompressed:cobblestone_6", "N": "vastcompressed:netherrack_6", "E": "vastcompressed:end_stone_5",
      "D": "vastcompressed:diamond_block_1"}),
    ("valor_core", "Core of Valor", "Núcleo da Bravura", "rare",
     ("Taken from the strongest, one fight at a time.", "Tirado dos mais fortes, uma luta de cada vez."),
     ["ASB", "EPX", "CRD"],
     {"A": "vastadventures:gem_solar", "B": "vastadventures:gem_lunar", "C": "vastadventures:gem_royalty",
      "D": "vastadventures:gem_warlord", "S": "vastadventures:seal_of_sockets", "E": "vastadventures:seal_of_extraction",
      "X": "vastadventures:seal_of_erasure", "R": "vastadventures:starsand", "P": "vastadventures:titan_pearl"}),
    ("wild_core", "Core of the Wild", "Núcleo da Natureza", "rare",
     ("A piece of every corner of the world.", "Um pedaço de cada canto do mundo."),
     ["TWD", "SHR", "UGB"],
     {"T": "minecraft:totem_of_undying", "W": "minecraft:wither_skeleton_skull", "D": "minecraft:dragon_head",
      "S": "minecraft:sniffer_egg", "H": "minecraft:heart_of_the_sea", "R": "minecraft:trident",
      "U": "minecraft:turtle_scute", "G": "minecraft:enchanted_golden_apple", "B": "minecraft:breeze_rod"}),
]
SEED = ("star_seed", "Star Seed", "Semente Estelar", "epic",
        ("Four stars of the Nether around a heart that won't break.", "Quatro estrelas do Nether ao redor de um coração que não quebra."),
        ["ENE", "NHN", "ENE"],
        {"E": "minecraft:echo_shard", "N": "minecraft:nether_star", "H": "minecraft:heavy_core"})
STAR = ("vast_star", "Vast Star", "Estrela Vasta", "epic",
        ("The end of the climb.", "O fim da escalada."),
        ["CDC", "ASP", "CVW"],
        {"C": "minecraft:end_crystal", "D": f"{NS}:deep_core", "A": f"{NS}:alloy_core", "S": f"{NS}:star_seed",
         "P": f"{NS}:pressure_core", "V": f"{NS}:valor_core", "W": f"{NS}:wild_core"})

# ---- the art (drawn here) ----------------------------------------------------------------

CLEAR = (0, 0, 0, 0)


def rgb(h):
    return ((h >> 16) & 255, (h >> 8) & 255, h & 255)


def mix(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def orb(inner, outer, ring):
    """A core: a lit sphere (inner colour at its highlight, outer at its rim) held in a thin ring of `ring`."""
    px = [[CLEAR] * 16 for _ in range(16)]
    cx = cy = 7.5
    for y in range(16):
        for x in range(16):
            d = math.hypot(x - cx, y - cy)
            if d <= 5.6:
                # Light from the top left.
                lx, ly = x - (cx - 2.2), y - (cy - 2.2)
                t = min(1.0, math.hypot(lx, ly) / 8.0)
                c = mix(inner, outer, t)
                if d > 4.8:
                    c = mix(c, (0, 0, 0), 0.35)
                px[y][x] = (*c, 255)
            elif 6.2 <= d <= 7.3 and (x + y) % 2 == 0:
                px[y][x] = (*ring, 255)
    # The highlight.
    for x, y in ((5, 4), (4, 5), (5, 5)):
        px[y][x] = (255, 255, 255, 255)
    return px


def seed():
    px = [[CLEAR] * 16 for _ in range(16)]
    shell, glow, core = rgb(0x3B2A55), rgb(0x9C6BFF), rgb(0xFFF2C0)
    for y in range(16):
        for x in range(16):
            # A seed: an egg shape, taller than wide.
            d = math.hypot((x - 7.5) / 4.6, (y - 8.2) / 6.2)
            if d <= 1.0:
                c = mix(glow, shell, d)
                px[y][x] = (*c, 255)
    for x, y in ((7, 7), (8, 7), (7, 8), (8, 8), (7, 9), (8, 6)):
        px[y][x] = (*core, 255)
    for x, y in ((6, 4), (6, 5)):
        px[y][x] = (255, 255, 255, 255)
    # A sprout on top.
    for x, y in ((8, 1), (9, 0), (8, 2), (7, 1)):
        px[y][x] = (*rgb(0x7CE06A), 255)
    return px


STAR_COLOURS = [rgb(0xF0B33A), rgb(0xE0562A), rgb(0xC23CE6), rgb(0x4FD8F0)]


def star(phase=0.0, size=16):
    """An eight-pointed star in the Vast metals' colours, white at its heart; `phase` turns its colours."""
    px = [[CLEAR] * size for _ in range(size)]
    c = (size - 1) / 2
    for y in range(size):
        for x in range(size):
            dx, dy = x - c, y - c
            r = math.hypot(dx, dy) / (size / 16)
            a = math.atan2(dy, dx)
            # Long points on the axes, short ones on the diagonals.
            spike = 3.2 + 4.6 * abs(math.cos(2 * a)) ** 4 + 2.8 * abs(math.sin(2 * a)) ** 4
            if r <= spike:
                t = (a / (2 * math.pi) + phase) % 1.0
                i = int(t * 4)
                col = mix(STAR_COLOURS[i], STAR_COLOURS[(i + 1) % 4], t * 4 - i)
                col = mix((255, 255, 255), col, min(1.0, r / 4.0))
                if r > spike - 1.0:
                    col = mix(col, (40, 20, 60), 0.45)
                px[y][x] = (*col, 255)
    return px


def star_block():
    px = [[(*rgb(0x161022), 255)] * 16 for _ in range(16)]
    # A frame of the three Vast metals, then the star.
    for i in range(16):
        for x, y in ((i, 0), (i, 15), (0, i), (15, i)):
            px[y][x] = (*rgb(0x2A1638), 255)
    for i in range(1, 15):
        px[1][i] = px[i][1] = (*rgb(0xF0B33A), 255)
        px[14][i] = px[i][14] = (*rgb(0x8A2FB0), 255)
    s = star(0.0, 12)
    for y in range(12):
        for x in range(12):
            if s[y][x][3]:
                px[y + 2][x + 2] = s[y][x]
    return px


def png(pixels):
    raw = b"".join(b"\x00" + bytes(c for px in row for c in px) for row in pixels)

    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", len(pixels[0]), len(pixels), 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


SPRITES = {
    "deep_core": lambda: orb(rgb(0xFFD27A), rgb(0x7A1FA0), rgb(0xE0562A)),
    "alloy_core": lambda: orb(rgb(0xFFE9A8), rgb(0x9A5A1E), rgb(0x6F767D)),
    "pressure_core": lambda: orb(rgb(0xE6EBF0), rgb(0x2B2F36), rgb(0xB862E8)),
    "valor_core": lambda: orb(rgb(0xFFB0B0), rgb(0x8A0E1E), rgb(0xF5D13B)),
    "wild_core": lambda: orb(rgb(0xC8FFD8), rgb(0x0E6A5A), rgb(0x7CE06A)),
    "star_seed": seed,
}
STAR_FRAMES = 8

# ---- the mod ------------------------------------------------------------------------------


def build(out):
    files, tags, items = {}, {}, []
    lang_en, lang_pt = {}, {}

    def item(name, en, pt, rarity, lore, glint):
        files[f"data/{NS}/horizon/item/{name}.json"] = {
            "template": "minecraft:nether_star", "rarity": rarity,
            "components": {"minecraft:enchantment_glint_override": glint,
                           "minecraft:lore": [{"translate": f"item.{NS}.{name}.lore", "color": "gray", "italic": True}]}}
        files[f"assets/{NS}/models/item/{name}.json"] = {"parent": "minecraft:item/generated",
                                                          "textures": {"layer0": f"{NS}:item/{name}"}}
        files[f"assets/{NS}/items/{name}.json"] = {"model": {"type": "minecraft:model", "model": f"{NS}:item/{name}"}}
        lang_en[f"item.{NS}.{name}"], lang_pt[f"item.{NS}.{name}"] = en, pt
        lang_en[f"item.{NS}.{name}.lore"], lang_pt[f"item.{NS}.{name}.lore"] = lore
        items.append(f"{NS}:{name}")

    def shaped(name, pattern, key, result, count=1):
        files[f"data/{NS}/recipe/{name}.json"] = {"type": "minecraft:crafting_shaped", "category": "misc",
                                                  "key": key, "pattern": pattern, "result": {"id": result, "count": count}}

    for name, en, pt, rarity, lore, pattern, key in CORES + [SEED]:
        item(name, en, pt, rarity, lore, name == "star_seed")
        files[f"assets/{NS}/textures/item/{name}.png"] = png(SPRITES[name]())
        shaped(name, pattern, key, f"{NS}:{name}")
    name, en, pt, rarity, lore, pattern, key = STAR
    item(name, en, pt, rarity, lore, True)
    # The star shimmers: its colours turn round it, a frame every 3 ticks.
    frames = [row for f in range(STAR_FRAMES) for row in star(f / STAR_FRAMES)]
    files[f"assets/{NS}/textures/item/{name}.png"] = png(frames)
    files[f"assets/{NS}/textures/item/{name}.png.mcmeta"] = {"animation": {"frametime": 3, "interpolate": True}}
    shaped(name, pattern, key, f"{NS}:{name}")

    # The block of nine.
    block = "vast_star_block"
    files[f"data/{NS}/horizon/block/{block}.json"] = {
        "template": "minecraft:diamond_block", "item": True,
        "properties": {"hardness": 50.0, "explosion_resistance": 1200.0, "light": 15, "requires_tool": True}}
    files[f"assets/{NS}/blockstates/{block}.json"] = {"variants": {"": {"model": f"{NS}:block/{block}"}}}
    files[f"assets/{NS}/models/block/{block}.json"] = {"parent": "minecraft:block/cube_all", "textures": {"all": f"{NS}:block/{block}"}}
    files[f"assets/{NS}/items/{block}.json"] = {"model": {"type": "minecraft:model", "model": f"{NS}:block/{block}"}}
    files[f"assets/{NS}/textures/block/{block}.png"] = png(star_block())
    files[f"data/{NS}/loot_table/blocks/{block}.json"] = {
        "type": "minecraft:block", "random_sequence": f"{NS}:blocks/{block}",
        "pools": [{"bonus_rolls": 0.0, "rolls": 1.0, "entries": [{"type": "minecraft:item", "name": f"{NS}:{block}"}],
                   "conditions": [{"condition": "minecraft:survives_explosion"}]}]}
    shaped(block, ["###", "###", "###"], {"#": f"{NS}:vast_star"}, f"{NS}:{block}")
    files[f"data/{NS}/recipe/vast_star_from_block.json"] = {
        "type": "minecraft:crafting_shapeless", "category": "misc", "ingredients": [f"{NS}:{block}"],
        "result": {"id": f"{NS}:vast_star", "count": 9}}
    lang_en[f"block.{NS}.{block}"], lang_pt[f"block.{NS}.{block}"] = "Block of Vast Star", "Bloco de Estrela Vasta"
    for t in ("minecraft:mineable/pickaxe", "minecraft:needs_diamond_tool", "minecraft:beacon_base_blocks"):
        tags.setdefault(("block", t), []).append(f"{NS}:{block}")
    items.append(f"{NS}:{block}")

    for (registry, tname), values in tags.items():
        tns, path = tname.split(":")
        files[f"data/{tns}/tags/{registry}/{path}.json"] = {"values": sorted(set(values))}
    files[f"data/{NS}/horizon/creative_tab/main.json"] = {"title": "Vast Star", "icon": f"{NS}:vast_star", "items": items}
    files[f"assets/{NS}/lang/en_us.json"] = dict(sorted(lang_en.items()))
    files[f"assets/{NS}/lang/pt_br.json"] = dict(sorted(lang_pt.items()))

    out = Path(out) / NS
    if out.exists():
        shutil.rmtree(out)
    for path, value in files.items():
        target = out / path
        target.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(value, bytes):
            target.write_bytes(value)
        else:
            target.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    (out / "horizon-mod.toml").write_text(
        f'id = "{NS}"\nname = "Vast Star"\nversion = "{VERSION}"\n'
        'description = "The last craft of the Vast family: five cores, a Star Seed and the Vast Star. Needs Vast Depths, Vast Ores, Vast Compressed and Vast Adventures."\n'
        'authors = ["voltzz900"]\napi = "0.2"\nside = "both"\ncapabilities = ["registries"]\n')
    print(f"{NS}: {len(items)} items, {len(files) + 1} files")


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "build")
