# Master Tree 01 — Blender / 3D + 2.5D Instructions

OpenCode should use this file as the entry point for all Master Tree 01 Blender work.

## Authoritative local source folder

`D:\UNREAL GAME PROJECT FOLDER\MASTER TREE`

The approved Tree 01 source images in that folder are the visual authority. Preserve the originals and do not redesign the tree.

## Authoritative GitHub references

Read these before doing Blender/tree work:

1. `Art/Environment/Trees/Master_Reference/FOREST_TREE_MASTER_COLOR_SPEC.md`
   - approved color language and bark/lighting rules

2. `Art/Environment/Trees/Master_Reference/FOREST_TREE_MASTER_COLOR_STATS.csv`
   - machine-readable palette statistics

3. `Design/Environment/Trees/TREE_HARVESTING_AND_2_5D_CANOPY_ARCHITECTURE.md`
   - harvesting compatibility and local/shared canopy architecture

4. This file
   - production routing and Blender efficiency rules

## Core production rule

**BUILD ONCE IN BLENDER → DERIVE BOTH 3D AND 2.5D.**

Do not independently redraw or regenerate a separate 2.5D tree when the needed asset can be derived from the Blender master.

The Blender master should contain, where practical:

- rootball
- major roots
- trunk
- primary branches
- useful secondary branches
- harvest cut region
- stump state
- felled-tree state
- log pieces only if gameplay requires them

From that same Blender source derive:

### 3D outputs
- near structural tree
- simplified geometry/LODs
- collision proxy
- stump mesh
- felled-tree mesh
- logs if needed

### 2.5D outputs
- front card
- back card
- useful side/oblique cards
- structural branch cards
- root/base cards
- stump card
- felled-tree card
- near/mid/far distance cards
- alpha/opacity masks
- supporting depth/normal passes only if useful

## Dedicated 2.5D-only art

Create separate 2.5D artwork only where geometry provides little benefit:

- fine twig clusters
- leaves
- tree-local canopy
- shared overhead canopy
- very distant silhouettes/background layers
- decorative foliage

## Visual constraints

Preserve:

- approved trunk width
- approved branch architecture
- approved root character
- asymmetry
- painterly/cel-shaded treatment
- major negative spaces
- approved cool palette

Do not:

- widen the trunk unless explicitly instructed
- replace branches with generic oak branches
- recolor the tree conventional brown
- add foliage to the structural master without approval
- replace painted bark with photographic/procedural realism
- use planning/contact sheets as authoritative source artwork

## Color authority

Use the approved progression:

`blue-black → dark teal → slate teal → blue-grey → pale cyan-grey`

Warm brown is an undertone only.

## Distance strategy

- Near: 3D/hybrid
- Medium: simplified 3D + cards
- Far: 2.5D card derived from Blender master
- Very far: silhouette/background representation

## Harvest compatibility

Standing, stump, felled, and logs should come from the same Blender structure wherever possible.

Keep tree-local canopy separate from shared forest canopy so harvesting one tree does not remove a giant forest-ceiling section.

Initial visual target:

- local canopy influence: ~20–30%
- shared canopy influence: ~70–80%

These are editable starting targets, not hard constants.

## Required manifest

Create/update a machine-readable Tree 01 manifest recording:

- source images
- Blender master path
- exported meshes
- textures
- materials
- cards
- resolutions
- pivots
- dimensions/world scale
- LOD classification
- harvesting relationship
- canopy relationship
- approval status
- notes

## OpenCode instruction

Before doing any Tree 01 Blender work:

1. Read this file.
2. Read the three authoritative GitHub references listed above.
3. Inspect `D:\UNREAL GAME PROJECT FOLDER\MASTER TREE`.
4. Identify the approved source images.
5. Preserve originals.
6. Use Blender as the shared structural source.
7. Derive reusable 2.5D outputs from Blender instead of independently inventing replacements.
8. Stop and flag any asset that cannot be faithfully derived from approved references instead of fabricating it.
