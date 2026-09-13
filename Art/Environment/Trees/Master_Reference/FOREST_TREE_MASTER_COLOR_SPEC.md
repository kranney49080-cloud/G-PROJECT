# Forest Tree Master Color Specification

**Status:** APPROVED COLOR AUTHORITY. The tree design/geometry itself is not yet approved.

## Master reference
The supplied Sword-in-the-Stone-inspired forest image is the color authority for trees, ground, atmospheric depth, lighting, and shadows.

## Core color language
**blue-black → dark teal → slate teal → blue-grey → pale cyan-grey**

Tree bark is fundamentally blue-grey / blue-brown. Do not use conventional warm brown as the base.

## Dominant sampled colors
| Role | HEX | RGB | Note |
|---|---|---|---|
| Dominant blue-teal | #081C23 | 8,28,35 | ~17.6% |
| Dominant blue-teal | #0C252C | 12,37,44 | ~14.0% |
| Deep blue-black | #061319 | 6,19,25 | ~12.1% |
| Dark teal | #083037 | 8,48,55 | ~9.7% |
| Deep teal | #0D3F47 | 13,63,71 | midtone |
| Blue-green midtone | #12505A | 18,80,90 | midtone |
| Slate teal | #2D565E | 45,86,94 | exposed/light-facing |
| Muted cyan-grey | #336973 | 51,105,115 | cool light |
| Blue-grey highlight | #457E89 | 69,126,137 | selective |
| Pale cyan highlight | #62949E | 98,148,158 | rare, ~1.9% |

The four darkest dominant families account for more than half the image. Bright colors must remain selective.

## Foreground trees
Main progression: `#08181E → #0A272F → #113841 → #194C57`

Selective accents: `#2F6673`, `#4A8594`

Target visual balance:
- 70–80% blue-grey / teal
- 10–20% muted earthy undertone
- small amount of brighter cyan-green moss/accent
- warm brown must never dominate

## Background / depth
`#0D272E → #183940 → #274D52 → #3A696E → #608D93`

Distance becomes lower-contrast, greyer, and slightly more cyan—not simply brighter. Unreal fog/lighting should push distant trees toward blue-grey/cyan.

## Ground
`#07191F → #0B2A33 → #143C47 → #214E5C`

Wet/mossy accents: `#3C666F`, `#588790`

Ground, rocks, roots, mud, and leaf litter stay within the cool forest family. Earth colors are restrained accents.

## Shadows
Extreme darkest sampled pixel: approximately `#000208`.

Practical production shadow floor: `#061319` to `#08181E`.

Use blue-black shadows, not neutral black.

## Highlights
Extreme light pixel: approximately `#8BBBBD`.

Representative practical high highlight: `#6B999A`.

Highlights remain muted cyan-grey. Avoid pure white on ordinary tree/ground materials.

## Bark value ladder
- Deep cavity: `#061319`
- Shadow bark: `#081C23`
- Base bark: `#0C252C` / `#083037`
- Exposed bark: `#1A323A` / `#25434B`
- Cool illuminated bark: `#2D565E` / `#336973`
- Rare highlight: `#457E89` / `#62949E`

Lighter bark should read like **weathered blue-grey stone mixed with wood**, not beige bark.

## Production authority
Use this specification for concept generation, 2.5D cards, hybrid trees, Blender materials, Unreal materials, foliage, forest ground, atmospheric fog, lighting, and color grading.

The forthcoming **50-foot hero tree** must use this specification and the master reference as its color authority. Its geometry and silhouette remain subject to separate visual approval.
