# Vast Star

A content mod for [Horizon](https://playhorizon.dev) (Minecraft 26.3 rewritten in Rust): the last craft of the
Vast family. Five cores, each the best of one mod or of the game itself, a Star Seed, and the **Vast Star** they
make.

| Item | Made from |
| --- | --- |
| **Core of the Deep** | blocks of Stellarite, Infernium, Voidium and two of their alloys (Vast Depths) |
| **Core of Alloys** | a block of each of the nine alloys (Vast Ores) |
| **Core of Pressure** | Compressed Cobblestone VI, Compressed Netherrack VI, Compressed End Stone V and Compressed Diamond I (Vast Compressed) |
| **Core of Valor** | four gems, the three seals, Starsand and a Titan Pearl (Vast Adventures) |
| **Core of the Wild** | a totem of undying, a wither skeleton skull, a dragon head, a sniffer egg, a heart of the sea, a trident, a turtle scute, an enchanted golden apple and a breeze rod |
| **Star Seed** | four nether stars, four echo shards and a heavy core |
| **Vast Star** | the five cores, the Star Seed and four end crystals |
| **Block of Vast Star** | nine Vast Stars (and back); it shines and serves a beacon |

Names and tooltips in English and Brazilian Portuguese. JEI shows every recipe.

**Needs** Vast Depths, Vast Ores, Vast Compressed and Vast Adventures for the cores (the Core of the Wild and the
Star Seed need only the game).

## Install

Put `vaststar-<version>.hmod` in Horizon's mods (or install it from the launcher) with the four mods above, and
restart. Data only: nothing to build.

## Building

`python3 tools/build_content.py build` writes the mod into `build/vaststar`; `./release.sh` packs
`dist/vaststar-<version>.hmod`; `./apply.sh` installs it locally. `tools/icon.py` draws the icon.

## Art and credits

Every sprite (the cores, the seed, the star with its shimmer and the block) is drawn pixel by pixel in
`tools/build_content.py`. The idea of a modpack's last star comes from the All The Mods packs' ATM Star; nothing
of it is used (its recipe, names and art are not), and this mod is not affiliated with or endorsed by All The Mods.

## License

MIT, see [LICENSE](LICENSE).
