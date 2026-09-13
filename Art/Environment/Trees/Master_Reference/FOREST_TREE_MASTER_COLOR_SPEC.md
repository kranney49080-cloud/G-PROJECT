# Forest Tree Master Color Specification

**Status:** APPROVED COLOR AUTHORITY. The tree design/geometry itself is not yet approved.

## Master reference
The supplied master forest image is the color authority for trees, ground, atmospheric depth, lighting, shadows, highlights, and palette relationships.

Image dimensions: **297 × 170 px**  
Total pixels analyzed: **50,490**  
Unique RGB colors: **18,199**

## Core color language
**blue-black → dark teal → slate teal → blue-grey → pale cyan-grey**

Tree bark is fundamentally blue-grey / blue-brown. Do not use conventional warm brown as the base.

## Global color statistics
- Mean RGB: approximately **(19, 53, 61)**
- Median RGB: approximately **(13, 46, 53)**
- Darkest sampled pixel: **#000208** / RGB **(0, 2, 8)**
- Lightest sampled pixel: **#8BBBBD** / RGB **(139, 187, 189)**
- Mean perceptual luma: **48.28 / 255**
- Median perceptual luma: **40.19 / 255**
- Luma standard deviation: **29.04**
- Pixels below luma 64: **76.02%**
- Pixels from luma 64–127: **22.34%**
- Pixels at luma 128 or higher: **1.63%**

### Luma percentiles
- 1st: **12.30**
- 5th: **16.59**
- 10th: **19.54**
- 25th: **25.68**
- 50th: **40.19**
- 75th: **62.86**
- 90th: **91.69**
- 95th: **111.11**
- 99th: **134.45**
- Maximum: **176.94**

This confirms that the image is intentionally very dark. High-value highlights are rare and therefore visually powerful.

## Hue statistics
For pixels with meaningful saturation/value, the weighted mean hue is approximately **191.5°**, placing the overall image firmly in the cyan/teal family.

Approximate hue-family distribution:
- Cyan/teal: **88.44%**
- Cyan-green: **6.71%**
- Blue: **4.37%**
- Green: **0.25%**
- Indigo: **0.18%**
- Violet: **0.05%**
- Red: **0.01%**
- Orange/yellow/magenta: effectively **0%**

This is the strongest statistical reason not to use normal brown as the dominant tree color.

## Dominant 16-color clustered palette
|Rank|HEX|RGB|Share %|HSL|HSV|Linear RGB|Luma|
|---:|---|---|---:|---|---|---|---:|
|1|#08191F|(8,25,31)|13.166|(195.7°,59.0%,7.6%)|(195.7°,74.2%,12.2%)|(0.00243,0.00972,0.01370)|21.82|
|2|#081F27|(8,31,39)|11.298|(195.5°,66.0%,9.2%)|(195.5°,79.5%,15.3%)|(0.00243,0.01370,0.02029)|26.69|
|3|#082B32|(8,43,50)|8.370|(190.0°,72.4%,11.4%)|(190.0°,84.0%,19.6%)|(0.00243,0.02416,0.03190)|36.06|
|4|#0C343D|(12,52,61)|7.493|(191.0°,67.1%,14.3%)|(191.0°,80.3%,23.9%)|(0.00368,0.03434,0.04667)|44.15|
|5|#071218|(7,18,24)|7.398|(201.2°,54.8%,6.1%)|(201.2°,70.8%,9.4%)|(0.00212,0.00605,0.00913)|16.09|
|6|#11242C|(17,36,44)|7.221|(197.8°,44.3%,12.0%)|(197.8°,61.4%,17.3%)|(0.00561,0.01764,0.02519)|32.54|
|7|#192F37|(25,47,55)|5.829|(196.0°,37.5%,15.7%)|(196.0°,54.5%,21.6%)|(0.00972,0.02843,0.03820)|42.90|
|8|#0D4047|(13,64,71)|5.774|(187.2°,69.0%,16.5%)|(187.2°,81.7%,27.8%)|(0.00402,0.05127,0.06301)|53.66|
|9|#134A55|(19,74,85)|5.768|(190.0°,63.5%,20.4%)|(190.0°,77.6%,33.3%)|(0.00651,0.06848,0.09084)|63.10|
|10|#223D44|(34,61,68)|4.899|(192.4°,33.3%,20.0%)|(192.4°,50.0%,26.7%)|(0.01600,0.04667,0.05781)|55.77|
|11|#2A4D53|(42,77,83)|4.522|(188.8°,32.8%,24.5%)|(188.8°,49.4%,32.5%)|(0.02315,0.07421,0.08650)|69.99|
|12|#467D89|(70,125,137)|3.869|(190.7°,32.4%,40.6%)|(190.7°,48.9%,53.7%)|(0.06125,0.20508,0.25016)|114.17|
|13|#336F78|(51,111,120)|3.642|(187.8°,40.4%,33.5%)|(187.8°,57.5%,47.1%)|(0.03310,0.15896,0.18782)|98.89|
|14|#335D66|(51,93,102)|3.472|(190.6°,33.3%,30.0%)|(190.6°,50.0%,40.0%)|(0.03310,0.10946,0.13287)|84.72|
|15|#1C5A64|(28,90,100)|3.029|(188.3°,56.2%,25.1%)|(188.3°,72.0%,39.2%)|(0.01161,0.10224,0.12744)|77.54|
|16|#60929D|(96,146,157)|3.022|(190.8°,26.5%,49.6%)|(190.8°,38.9%,61.6%)|(0.11697,0.28744,0.33716)|136.16|

## Spatial / material-region statistics
These are heuristic rectangular samples from the image, used to preserve the relationship between foreground trees, depth, canopy, and ground.

| Region | Mean HEX / RGB | Median HEX / RGB | Mean Luma | 10th–90th Luma |
|---|---|---|---:|---:|
| Upper-left foreground tree | #153B42 / (21,59,66) | #0B3238 / (11,50,56) | 51.38 | 20.67–101.89 |
| Upper-right foreground tree | #133039 / (19,48,57) | #0F2A33 / (15,42,51) | 42.52 | 17.24–73.83 |
| Central depth/opening | #18363C / (24,54,60) | #102E34 / (16,46,52) | 47.94 | 21.04–87.85 |
| Ground lower band | #183943 / (24,57,67) | #0E3039 / (14,48,57) | 50.78 | 19.67–100.15 |
| Upper canopy band | #12353A / (18,53,58) | #0D3036 / (13,48,54) | 45.89 | 20.40–77.81 |

## Foreground trees
Primary progression:
`#08181E → #0A272F → #113841 → #194C57`

Selective edge/bark accents:
`#2F6673`, `#4A8594`

Target visual balance:
- approximately **70–80% blue-grey / teal** visual read
- approximately **10–20% muted earthy undertone**
- only a small amount of brighter cyan-green moss/accent
- warm brown must never dominate

The trunks should read as weathered blue-grey wood with a stone-like coolness. Brown is an undertone, not the visible identity of the bark.

## Background / atmospheric depth
Representative progression:
`#0D272E → #183940 → #274D52 → #3A696E → #608D93`

Distance should become:
- lower contrast
- greyer
- slightly more cyan
- not simply brighter

Use Unreal atmospheric fog and lighting to shift distant trees toward blue-grey/cyan and reduce contrast rather than merely raising exposure.

## Ground
Representative progression:
`#07191F → #0B2A33 → #143C47 → #214E5C`

Wet/mossy accents:
`#3C666F`, `#588790`

Ground, rocks, roots, mud, and leaf litter should remain integrated with the same cool family. Conventional dirt-brown should not take over the scene.

## Shadows
- Extreme darkest sampled pixel: **#000208**
- Practical production shadow floor: **#061319** to **#08181E**

Shadows are blue-black, not neutral black.

## Highlights
- Extreme lightest sampled pixel: **#8BBBBD**
- Representative practical high highlight: approximately **#6B999A**

Highlights remain muted cyan-grey. Avoid pure white on normal tree and ground materials.

## Bark value ladder
- Deep bark cavity: `#061319`
- Shadow bark: `#081C23`
- Base bark: `#0C252C` / `#083037`
- Exposed bark: `#1A323A` / `#25434B`
- Cool illuminated bark: `#2D565E` / `#336973`
- Rare highlight: `#457E89` / `#62949E`

## Production rules for future trees
1. Start the tree in blue-grey/teal, not brown.
2. Keep the majority of the trunk in the dark-to-mid teal range.
3. Use warm/earth tones as restrained undertones only.
4. Keep highlights rare; the master image has only **1.63%** of pixels at luma 128+.
5. Use blue-black cavities and contact shadows.
6. Let distant trees lose contrast and drift toward cyan-grey.
7. Keep the ground within the same cool family so tree, soil, fog, and lighting feel unified.
8. Treat this master as a relationship system, not just a list of swatches.

## Production authority
Use this specification for:
- AI concept generation
- 2.5D tree cards
- hybrid 2.5D/3D trees
- Blender materials
- Unreal materials
- foliage
- forest ground
- atmospheric fog
- lighting
- color grading

The forthcoming **50-foot hero tree** must use this specification and master reference as its color authority. Its geometry/silhouette remains subject to separate approval.

## Statistical data file
The machine-readable clustered-palette data is stored alongside this document in:
`FOREST_TREE_MASTER_COLOR_STATS.csv`
