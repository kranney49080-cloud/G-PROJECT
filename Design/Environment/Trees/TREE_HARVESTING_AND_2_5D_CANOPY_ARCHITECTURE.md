# Tree Harvesting and 2.5D Canopy Architecture

**Status:** Design direction / implementation constraint. Tree art is still being developed.

## Project context
The game is a **third-person 2.5D game**. Forests should use dimensional structure only where it materially improves the player's view while using painterly cards for expensive visual complexity.

## Proposed forest construction
Each forest tree/cluster is separated into visual layers:

1. **Structural trunk/root asset** — dimensional enough for close third-person viewing, collision, interaction, and harvesting.
2. **Major structural branches** — simplified geometry/hybrid art where depth and silhouette matter.
3. **Tree-local 2.5D canopy cards** — branch/leaf artwork associated with an individual harvestable tree and removable when that tree disappears.
4. **Shared overhead canopy cards** — large overlapping painterly branch/leaf layers spanning groups of trees. These form most of the forest ceiling and do not disappear when a single tree is harvested.
5. **Distant forest cards/layers** — increasingly inexpensive painterly representations where close geometry is unnecessary.

The overhead canopy should be a shallow layered volume rather than one perfectly flat horizontal plane. Cards can sit at multiple heights/angles to provide parallax, sky gaps, fog penetration, and believable views when the third-person player looks upward or sees the canopy from a distance.

## Harvestable Tree Actor
A harvestable tree should have a gameplay actor/state independent from the shared forest canopy. Conceptually:

- structural trunk/root visual
- collision
- health / resource quantity
- harvesting interaction
- hit effects
- standing / falling / stump state
- reference to tree-local canopy pieces
- optional regeneration state

## Harvest sequence
1. Player strikes/chops the harvestable trunk.
2. Tree Actor receives damage and plays hit feedback.
3. At zero health, standing tree transitions to a simplified falling-tree representation.
4. Tree-local branch/canopy cards associated with that tree fade, hide, or swap.
5. Shared forest canopy remains so removing one tree never causes a giant rectangular hole in the forest ceiling.
6. Falling tree resolves into stump and/or harvestable log/resource pieces.

The falling representation does not need to contain every detail of the standing painterly tree. A simplified trunk + major branches can be used during the fall.

## Canopy ownership
Recommended starting design:

- **~70–80% shared canopy coverage**: belongs to the forest/cluster and survives removal of individual trees.
- **~20–30% tree-local canopy coverage**: visually tied to specific harvestable trees and removed with them.

These numbers are starting targets, not hard requirements. They should be tuned visually.

## Canopy response to harvesting
Removing one tree should create a **small believable opening** rather than deleting a large canopy sheet. The new opening can allow additional sky, sunlight/moonlight, fog, and atmospheric shafts into the forest.

For larger-scale harvesting, shared canopy coverage can respond to remaining tree density. Possible thresholds:

- 100–75% trees remaining: dense shared canopy
- 75–50%: scattered openings
- 50–25%: substantial sky exposure
- below 25%: mostly open canopy

This provides visible environmental consequences without simulating thousands of individual leaves.

## Regrowth
A possible regeneration progression:

`stump → sapling → young tree → mature tree`

At maturity the structural asset changes and its local canopy cards fade back in. Shared canopy density can also recover as local tree density increases.

## Critical art/engineering interface
**Art and harvesting mechanics should be developed separately, but against a shared interface contract.**

Do NOT fully finish all tree art first and later ask engineering to make arbitrary finished assets harvestable. Also do NOT couple the art pipeline tightly to unfinished harvesting code.

Before producing the full tree library, lock these interface requirements:

- consistent pivot/origin at the trunk/root base
- known world scale and tree height classes
- trunk collision zone
- chop/hit region
- separation between structural trunk/major branches and foliage canopy artwork
- explicit local-canopy ownership hooks/IDs
- stump/falling replacement convention
- clear asset naming
- material slots that remain compatible with forest palette/material systems
- optional attachment points for local canopy pieces
- predictable bounding boxes for placement/PCG

Then the two tracks can proceed largely in parallel:

### Art track
Develop master tree silhouette, trunk/roots, major branches, painterly materials, local canopy cards, shared canopy cards, variants, LOD/card strategy, and forest composition.

### Gameplay track
Develop Tree Actor, health/resource data, chopping interaction, state transitions, falling representation, stump/resource spawning, local-canopy visibility control, regeneration, and eventual density-driven shared-canopy changes.

## Recommended prototype order
1. Approve one master tree's visual design and color language.
2. Define the interface contract above.
3. Build one inexpensive prototype Tree Actor using placeholder geometry if necessary.
4. Insert the approved/master trunk asset into that actor.
5. Attach one local canopy card and one shared canopy card.
6. Prove the complete loop: standing → chopped → falling → local canopy opening → stump/resources.
7. Only after that proof, mass-produce tree variants and canopy artwork.

This avoids expensive art rework while keeping gameplay implementation from dictating the visual style prematurely.
