# ANIMATION HARVEST GYM — GEMINI MASTER HANDOFF
## UE5.8 Native-Source Animation Research Project
### Naruto Shippuden: Ultimate Ninja Storm 4 + Naruto to Boruto: Shinobi Striker + Dragon Ball: Sparking! ZERO

**Revision:** 2026-10-06  
**Project name:** `AnimationHarvestGym`  
**Engine:** Unreal Engine 5.8  
**Primary operator for this handoff:** Gemini  
**Gemini role:** source import, native-character setup, native playback validation, cataloging, metadata, and small Gym organization only.  
**Retargeting owner:** a different AI/operator. Gemini must not retarget animations.

---

# 1. Executive Order

Create a **new, separate UE5.8 project** named `AnimationHarvestGym` dedicated to harvesting, viewing, validating, and cataloging reference animations from:

1. Naruto Shippuden: Ultimate Ninja Storm 4
2. Naruto to Boruto: Shinobi Striker
3. Dragon Ball: Sparking! ZERO

This project is **not the production game project** and must not become a giant mixed-content warehouse. It is a focused animation research and source-validation project.

The central rule is:

> **Gemini imports each animation with its ORIGINAL source character/skeleton and validates it natively. Gemini does NOT retarget it to Manny, Quinn, MetaHuman, or any production character.**

A separate AI/operator will later handle:

- Retargeting
- IK Rig / IK Retargeter work
- Manny/production-character adaptation
- Foot grounding and Full Body IK fixes
- Animation cleanup
- Production Motion Matching databases
- Production montage authoring
- Broly-style growth on Manny or the production character

Gemini must prepare clean, verified source material and metadata so the downstream AI does not have to rediscover anything.

---

# 2. New Project Requirement

Create a fresh UE5.8 project:

`AnimationHarvestGym`

It must be separate from the production G-PROJECT and separate from the Survival RPG Engine project.

Recommended project purpose:

- Native source-character animation playback
- Small test Gyms
- Source provenance
- Motion-state cataloging
- Hit-reaction cataloging
- Grounded-vs-flight classification
- Creature/snake/giant animation research
- Visual comparison
- Downstream retarget handoff preparation

Do not import the full game archives into Unreal. Index first, then import only selected assets required by the current phase.

---

# 3. Gemini Scope — Allowed Work

Gemini MAY:

- Create and maintain the new `AnimationHarvestGym` UE5.8 project.
- Inspect source packages and animation containers.
- Use the maintained/proven extraction route for each source game.
- Import the ORIGINAL source skeletal mesh, ORIGINAL skeleton, and selected ORIGINAL animation clips into the Gym project.
- Import required source props that are necessary to read the animation correctly, such as swords, scabbards, staff/pole weapons, creature rigs, wings, and full snake rigs.
- Import minimal materials/textures needed to make the source character readable in the Gym.
- Import minimal VFX/camera references only when they are necessary to understand animation timing or a transformation/ability relationship.
- Preserve original source identifiers and provenance.
- Validate native playback before doing any batch operation.
- Build tiny focused Gym maps.
- Mark motion-state ranges non-destructively.
- Record foot-contact frames, root displacement, floor offset, native hover/flight state, weapon state, and source timing.
- Build a searchable source-animation catalog.
- Create side-by-side native comparisons.
- Create thumbnails or lightweight previews when useful.
- Use direct native animation playback in the Unreal viewport as the primary visual review method.

---

# 4. Gemini Scope — Forbidden Work

Gemini MUST NOT:

- Retarget any animation to Manny, Quinn, MetaHuman, or the production skeleton.
- Create or modify IK Retargeters for production use.
- Alter production skeletons.
- Edit source bones to make an animation fit a target skeleton.
- Permanently ground/fix a Sparking ZERO animation by modifying the source clip.
- Bake production foot IK.
- Build the final production Motion Matching reaction database.
- Build final production montages.
- Scale Manny for Broly transformation work.
- Modify the production G-PROJECT character for this research.
- Destructively split or overwrite the only copy of a source animation.
- Rename away original animation/package identifiers.
- Guess filenames, animation IDs, package relationships, bone names, or fixes.
- Batch hundreds of files through an unproven import route.
- Commit extracted copyrighted source-game assets to GitHub.

If retargeting, skeleton editing, production IK, or production cleanup becomes necessary, STOP at the handoff boundary and record exactly what the next AI needs to do.

---

# 5. Architecture

```text
SOURCE VAULT (cold / immutable)
        |
        v
MASTER INDEX (metadata only)
        |
        +----------------------> VISUAL LIBRARY
        |                         native playback / thumbnails / optional proxies
        |
        v
SMALL SOURCE GYMS
        |
        v
NATIVE PLAYBACK VALIDATION
        |
        v
MOTION STATE + REACTION CATALOG
        |
        v
RETARGET HANDOFF PACKAGE
        |
        v
SEPARATE AI / OPERATOR
(retarget, grounding, IK, Manny, production motion matching)
```

The Gym must answer one focused technical question at a time.

---

# 6. Proposed UE Project Content Layout

```text
AnimationHarvestGym/
  Content/
    SourceNative/
      Storm4/
        Characters/
        Creatures/
        Shared/
      ShinobiStriker/
        Characters/
        Creatures/
        Shared/
      SparkingZero/
        Characters/
        Giants/
        Creatures/
        Shared/
    Gyms/
      Storm4/
      ShinobiStriker/
      SparkingZero/
      CrossGame/
    Maps/
    Metadata/
    VisualLibrary/
    ComparisonSets/
  Docs/
  ExternalSourceVault/   # preferred outside Content / cold reference only
```

Do not load all source characters at once.

---

# 7. Source-Game Routes

## 7.1 Storm 4

Default route:

- Use maintained XFBIN tooling, including Blender XFBIN Importer where applicable.
- Use Storm 4-capable community tooling/API for parameter relationships where applicable.
- Search both character-specific and shared/common animation containers.
- Native visual playback decides identity, not a guessed filename.
- Import the original source character/skeleton and selected clip into UE5.8.
- No retargeting by Gemini.

## 7.2 Sparking! ZERO

Default route:

- Index packages first.
- Use FModel for package/property inspection and supported mesh/animation/morph/texture export paths.
- Use another Unreal inspection route only if it is directly proven to support the exact game data.
- Validate the original skeleton with one simple animation first.
- Use Blender only when required as a diagnostic/conversion checkpoint.
- Import the original character and animation into UE5.8.
- No retargeting by Gemini.

## 7.3 Shinobi Striker

Do not assume a generic Unreal extractor automatically supports the exact current game build.

Gemini must:

1. Identify a maintained/proven Shinobi Striker-capable extraction path for the installed build.
2. Prove it with one original character/skeleton + one animation.
3. Validate native playback.
4. Record the exact tool and version.
5. Only then expand the snake harvest.

If the exact extraction route is not proven, mark it `UNKNOWN` and research the maintained community route before writing custom tooling.

---

# 8. Native Import Contract

Every harvested animation must retain:

- Source game
- Source character/form
- Original animation/package identifier
- Original skeleton
- Original skeletal mesh
- Required weapon/prop/creature relationship
- Native root behavior
- Native floor/hover relationship
- Native playback result
- Animation length
- Frame rate if known
- Motion family tags
- Hit-reaction metadata when applicable
- Grounded/airborne/flight classification
- Source notes

A source asset is not considered validated until it visibly plays correctly on its original rig.

---

# 9. Visual Library Rule

The current preferred workflow is **native animation playback in Unreal**, not spending time filming a video for every animation.

For each validated source animation:

- Keep a searchable animation entry.
- Provide a thumbnail/poster image when useful.
- Open/play the actual imported animation on the original source character.
- Optional lightweight proxy capture is allowed only when it materially improves browsing or comparison.
- Diagnostic views may show root path, foot contacts, weapon/socket relation, and state markers.

Do not create slow video-capture work for every clip by default.

---

# 10. Motion-State Catalog

Do not destructively cut the source clip.

Store states as pointers:

```text
source_animation_id
start_time / start_frame
end_time / end_frame
state_type
entry_pose
exit_pose
lead_foot
planted_foot
root_displacement
facing_delta
weapon_state
native_ground_state
notes
```

Standard motion-state vocabulary should include:

- ENTRY
- ANTICIPATION
- WINDUP
- ATTACK
- CONTACT
- FOLLOW_THROUGH
- RECOVERY
- EXIT
- START
- ACCELERATE
- LOOP
- TURN
- BRAKE
- STOP
- JUMP_START
- AIR
- LAND
- DRAW
- READY
- THRUST
- SLASH_LR
- SLASH_RL
- OVERHEAD
- RISING
- SPIN
- BLOCK
- PARRY
- SHEATH
- HIT_LIGHT
- HIT_HEAVY
- KNOCKBACK
- LAUNCH
- KNOCKDOWN
- GROUND_IMPACT
- GETUP

---

# 11. Mandatory Hit-Reaction Harvest — BOTH GAMES

This is now a **global rule for every character pass**.

When a source character is opened, Gemini must also search for useful:

- Light hit reactions
- Heavy hit reactions
- Front reactions
- Back reactions
- Left reactions
- Right reactions
- Diagonal reactions if present
- Guard-break reactions
- Staggers
- Crumples
- Knockbacks
- Sliding knockbacks
- Launch / juggle reactions
- Airborne hit reactions
- Ground impacts
- Knockdowns
- Wall-impact style reactions if available
- Recovery poses
- Get-ups
- Death/fall animations only when useful as reaction references

The goal is a **complete cross-game source reaction kit for later Motion Matching**.

Gemini does NOT build the final production Motion Matching database. Gemini builds the verified native source library and metadata that the downstream retarget AI will use.

Required reaction metadata:

```text
incoming_direction
reaction_direction
severity = light | medium | heavy | launch
native_grounded = yes | no
native_flight = yes | no
root_displacement
horizontal_velocity
vertical_velocity
knockdown = yes | no
recovery_available = yes | no
usable_for_motion_matching = yes | maybe | no
```

---

# 12. Sparking ZERO Grounding / Foot-IK Preparation

Many Dragon Ball animations assume hovering or flight. Our production game does not use constant Dragon Ball-style flight for normal combat.

Gemini must classify every useful Sparking ZERO motion:

- `GROUND_NATIVE` — source clip already reads correctly as grounded.
- `GROUNDABLE_FLIGHT_SOURCE` — source is slightly hovering/flying but body mechanics can plausibly be adapted to ground combat.
- `FLIGHT_DEPENDENT` — lower body only makes sense in flight; likely use upper-body/action information later with an authored grounded lower body.
- `AIRBORNE_INTENTIONAL` — jump, launch, aerial attack, knockback, fall, etc.

For every `GROUNDABLE_FLIGHT_SOURCE`, Gemini records:

- Approximate native floor offset
- Left-foot contact windows
- Right-foot contact windows
- Pelvis height behavior
- Root vertical movement
- Whether feet should be planted, sliding, stepping, or airborne
- Where the clip would need grounding after retarget

**Gemini does not perform the final grounding or IK.**

Downstream AI requirement:

```text
RETARGET -> ROOT/PELVIS HEIGHT CORRECTION -> FOOT CONTACT SETUP
-> FULL BODY IK / CONTROL RIG FOOT LOCK -> BAKE CLEANED TARGET CLIP
-> RUNTIME TERRAIN FOOT PLACEMENT
```

Do not use runtime terrain IK to hide a fundamentally floating source conversion.

---

# 13. Broly Transformation — Growth Requirement

Broly's transformation must not end as merely the same-size character doing a power-up pose.

Gemini must harvest and preserve:

- Base Broly original mesh/skeleton
- Transformed Broly original mesh/form
- Transformation body animation
- Transformation pose sequence
- Any morph/shape-change evidence
- Bone-scale evidence if present
- Mesh-swap evidence if present
- Camera relationship if necessary
- VFX relationship if necessary to understand timing
- Before/after body proportions
- Before/after approximate character height/width
- Exact transformation timing markers

The existing research question remains:

```text
mesh swap vs morph vs bone scaling vs uniform actor scale vs combination
```

Gemini must determine what the source appears to be doing, but **must not scale Manny or retarget Broly**.

### Downstream Manny / production-character test

The next AI will build a reusable `GrowthAlpha` transformation test on Manny or the production character:

- 0.0 = base size
- 1.0 = transformed size
- Feet remain grounded while size changes
- Capsule height/radius update safely
- Mesh/root compensates from a ground-level growth pivot
- Camera distance/height expands smoothly
- Final scale persists after transformation
- Later pass adds wider shoulders/chest/arms/torso rather than only uniform scaling

Gemini's job is to deliver the native Broly evidence and timing so the downstream AI can reproduce the growth correctly.

---

# 14. Krillin — Destructo Disk / Disc Projectile Priority

Krillin is now a priority harvest.

Do not harvest only a single throw.

Search for and preserve the complete useful Destructo Disk body-motion family:

- Disc creation / charge
- Hand raise
- Hold / aim
- Overhead or high-hand preparation
- Body torque
- Release
- Follow-through
- Recovery
- Running/dashing disc use if present
- Airborne disc use if present
- Multiple-disc variants if present
- Ultimate/special variants if they contain unique body mechanics

Create native source Gyms:

```text
GYM_KRILLIN_DISC_CREATE
GYM_KRILLIN_DISC_RAISE
GYM_KRILLIN_DISC_AIM
GYM_KRILLIN_DISC_RELEASE
GYM_KRILLIN_DISC_FOLLOWTHROUGH
GYM_KRILLIN_DISC_RECOVERY
GYM_KRILLIN_DISC_VARIANTS
```

Also harvest Krillin's useful hit reactions during the same source pass.

---

# 15. Tapion — Overhead Sword Priority

Tapion's sword set is mandatory.

High priority is specifically given to the moves where he raises the sword above his head.

Harvest and categorize:

```text
GYM_TAPION_READY
GYM_TAPION_DRAW
GYM_TAPION_SHEATH
GYM_TAPION_GROUNDED_SLASH
GYM_TAPION_HIGH_GUARD
GYM_TAPION_OVERHEAD_RAISE
GYM_TAPION_OVERHEAD_ANTICIPATION
GYM_TAPION_OVERHEAD_STRIKE
GYM_TAPION_OVERHEAD_RECOVERY
GYM_TAPION_RECOVERY
```

Track:

- Pelvis
- Feet
- Shoulder line
- Two-hand/one-hand relationship
- Sword angle
- Root displacement
- Planted foot
- Entry and exit pose

---

# 16. Super Janemba — Demonic Overhead Sword Priority

Janemba's overhead sword behavior is also a priority.

Harvest:

```text
GYM_JANEMBA_SWORD_IDLE
GYM_JANEMBA_TELEPORT_ENTRY
GYM_JANEMBA_TELEPORT_SLASH
GYM_JANEMBA_HIGH_GUARD
GYM_JANEMBA_OVERHEAD_RAISE
GYM_JANEMBA_DEMONIC_OVERHEAD
GYM_JANEMBA_OVERHEAD_RECOVERY
GYM_JANEMBA_RECOVERY
```

Build a comparison set:

```text
TAPION vs JANEMBA vs TRUNKS — OVERHEAD SWORD
```

Purpose:

- Tapion = controlled grounded/traditional reference
- Janemba = supernatural/demonic reference
- Trunks = high-power committed sword reference

---

# 17. Giant Stomp Search

Stomp attacks are mandatory creature/giant research.

Search all relevant giant characters for:

- Single attack stomp
- Forward step-stomp
- Turning stomp
- Repeated/rage stomp
- Landing stomp
- Crushing foot attack
- Downward foot slam
- Ground-shock stomp
- Heavy locomotion step that can be adapted into an attack

Priority giant sources:

- Great Ape Vegeta
- Great Ape Baby
- Anilaza
- Cell Max
- Giant Lord Slug
- Hirudegarn
- Broly Full Power where useful

For each stomp, record the exact foot-contact frame so downstream systems can attach:

- Damage timing
- Screen shake
- Dust
- Debris
- Ground ring
- Camera impulse
- Sound

Do not confuse ordinary heavy walking with an actual attack stomp; tag them separately.

---

# 18. Snake Animation Program — Storm 4

This is a NEW dedicated priority program.

We want **whole-snake motion**, not only a human arm with a snake effect.

Primary target qualities:

- Full snake body slither
- Whole-body locomotion
- Coiling
- Raise-up / upright threat posture
- Head tracking
- Lunge
- Bite
- Pull-back after bite
- Ram
- Body whip
- Turn while slithering
- Ground emerge / rise
- Attack recovery

### Storm 4 priority source: Orochimaru

Use public gameplay move labels only as search/verification labels. Internal file IDs remain UNKNOWN until directly verified.

Priority moves to locate and visually verify:

- `Dako` — Orochimaru becomes snake-like and slithers toward the opponent.
- `Snake Bearer Jutsu` — large-snake transformation with forward slither/ram behavior.
- `White Snake Charmer Jutsu` — giant white-snake form rushing and biting.
- `Giant Snake Bearer` / giant-snake secret-technique sequence.
- `Biting Fang` — bite/grab/hurl behavior.
- `Striking Shadow Snake` and `Multiple Striking Shadow Snake` for secondary snake strike language.

### Storm 4 secondary source: Sage Kabuto

Search his snake-heavy attacks for:

- Giant white snakes
- Four-snake attacks
- Attached-snake grab/bite behavior
- Snake approach/lunge motion
- Snake bite / clamp motion
- Large snake emerge/attack sequences

Create focused Gyms:

```text
GYM_STORM_SNAKE_SLITHER
GYM_STORM_SNAKE_TURN
GYM_STORM_SNAKE_RAISE
GYM_STORM_SNAKE_LUNGE
GYM_STORM_SNAKE_BITE
GYM_STORM_SNAKE_RAM
GYM_STORM_SNAKE_BODY_WHIP
GYM_STORM_SNAKE_EMERGE
GYM_STORM_SNAKE_RECOVERY
GYM_STORM_SNAKE_OROCHIMARU_TRANSFORM
GYM_STORM_SNAKE_KABUTO_VARIANTS
```

When a distinct full snake rig exists, import the full ORIGINAL snake mesh/skeleton/animation, not merely Orochimaru's human skeleton.

---

# 19. Snake Animation Program — Shinobi Striker

This is a separate source because Shinobi Striker contains snake behavior worth harvesting even if Storm 4 already has snake material.

Prioritize **whole summoned/mount snake movement first**.

### Highest-priority Shinobi Striker targets

1. **Ninja Snakes summoned animal**
   - Slithers through/along the ground for mobility.
   - Erupts upward to strike when the action ends.
   - High-value whole-body locomotion source.

2. **Summoning: Great Snake**
   - Full summoned snake actor.
   - Attack/spin behavior.
   - Useful whole-body idle/attack/readiness source.

3. **Orochimaru — Multiple Striking Shadow Snake**
   - Secondary source for lunging snake strike motion.

4. **Snake Clone**
   - Useful swarm/disperse transformation reference.

5. **Mitsuki — Snake Thrust**
   - Useful extension/strike body language even though it is not a full independent snake locomotion rig.

6. **White Snake Sword "Orochimaru"**
   - Inspect snake attacks/body-transformation sequences for any unique whole-body snake motion.

Create:

```text
GYM_SS_SNAKE_NATIVE_RIG
GYM_SS_SNAKE_SLITHER
GYM_SS_SNAKE_TURN
GYM_SS_SNAKE_EMERGE
GYM_SS_SNAKE_RAISE
GYM_SS_SNAKE_LUNGE
GYM_SS_SNAKE_BITE
GYM_SS_GREAT_SNAKE_IDLE
GYM_SS_GREAT_SNAKE_ATTACK
GYM_SS_SNAKE_MOBILITY
GYM_SS_SNAKE_VARIANTS
```

The desired outcome is a reusable **snake motion reference library** that can later feed an original creature rig for the game.

---

# 20. Phase Queue — Revised Master Harvest Order

## Phase 0 — Pipeline Lock / Rock Lee Reference

- Keep Rock Lee Chakra Dash as an accepted traversal reference.
- Validate folder conventions, metadata, source provenance, and native-playback workflow.
- Do not spend time re-solving an already accepted Rock Lee reference unless a source artifact is missing.

## Phase 1 — Mifune — Storm 4

Mifune remains the **first actual character harvest**.

One-touch source harvest categories:

- 1A — Weapon + draw/sheath
- 1B — Core grounded sword attacks
- 1C — Iaido / dash / quick-draw attacks
- 1D — Aerial + specialty sword motion
- 1E — Armed locomotion + ready + transitions
- 1F — Recoveries + montage-transition references
- 1G — Final visual-library review / metadata
- PLUS all useful Mifune hit reactions and knockbacks encountered during the same source pass

Import on Mifune's original rig only. No retargeting.

## Phase 2 — Sasuke — Storm 4

- Sword reach/draw
- Ready stance
- One-handed attacks
- Dash entries
- Armed locomotion
- Sheath
- Variant compare
- Hit reactions / knockbacks

## Phase 3 — Hidan — Storm 4

- Oversized scythe windup
- Sweeps
- Spins
- Throws
- Recoveries
- Hit reactions / knockbacks

## Phase 4 — Naruto / Shared Ninja Locomotion — Storm 4

- Acceleration
- Fast run
- Running jump
- Land
- Shared dash start/loop/turn/brake/attack exit
- Hit reactions / knockbacks

## Phase 5 — Garuda — Storm 4

- Wing rig
- Flap
- Glide
- Banks
- Dive
- Takeoff
- Landing
- Rider relationship where useful

## Phase 6 — Orochimaru + Kabuto Snake Harvest — Storm 4

- Full snake slither
- Raise
- Bite
- Lunge
- Ram
- Whole-body transform
- Giant snake attack
- Snake recovery
- Import original snake rigs where separate

## Phase 7 — Shinobi Striker Snake Harvest

- Ninja Snakes mobility
- Great Snake summon
- Slither
- Turn
- Emerge
- Raise
- Strike
- Bite
- Whole-snake special abilities

## Phase 8 — Trunks — Sparking ZERO

- Dash entry
- Overhead
- Horizontal R-L
- Horizontal L-R
- Rising slash
- Heavy recovery
- Hit reactions / knockbacks
- Ground/flight classification

## Phase 9 — Tapion — Sparking ZERO

- Ready
- Draw
- Sheath
- Grounded slash
- High guard
- Overhead raise
- Overhead anticipation
- Overhead strike
- Overhead recovery
- Hit reactions / knockbacks
- Ground/flight classification

## Phase 10 — Super Janemba — Sparking ZERO

- Sword idle
- Teleport entry
- Teleport slash
- High guard
- Overhead raise
- Demonic overhead
- Recovery
- Hit reactions / knockbacks
- Ground/flight classification

## Phase 11 — Dabura — Sparking ZERO

- Demon sword
- Casting entry
- Casting release
- Melee-to-magic transitions
- Hit reactions / knockbacks

## Phase 12 — Yajirobe — Sparking ZERO

- Basic slash
- Overhead
- Rush
- Recovery
- Low-skill sword language
- Hit reactions / knockbacks

## Phase 13 — Krillin — Sparking ZERO

- Full Destructo Disk family
- Disc setup/creation
- Raise/hold/aim
- Release
- Follow-through
- Recovery
- Variants
- Hit reactions / knockbacks
- Ground/flight classification

## Phase 14 — Goku Family — Sparking ZERO

Include only useful unique motion families rather than duplicating whole characters.

Priority:

- Goku Blue power-up body timing
- Aura startup/surge relationship as reference only
- Kamehameha charge/release body motion
- Disc/throw variants
- Goku Mini / Power Pole staff thrust/sweep/spin/overhead/transitions
- Hit reactions / knockbacks

## Phase 15 — Broly — Sparking ZERO

### Base / Agile
- Dash
- Fast locomotion
- Quick attacks

### Transformation
- Base form
- Transformed form
- Body animation
- Growth evidence
- Shape/morph/bone-scale evidence
- Camera/VFX timing relationship

### Full Power
- Heavy punches
- Grabs
- Slams
- Roar
- Heavy recovery
- Giant/large-character stomp candidates
- Hit reactions / knockbacks

No Manny work by Gemini.

## Phase 16 — Master Roshi — Sparking ZERO

- Unarmed monk
- Palms
- Guard
- Power-up/casting poses
- Hit reactions / knockbacks

## Phase 17 — Babidi — Sparking ZERO

- Point
- Raise
- Channel
- Release
- Upper-body mage gesture vocabulary
- Hit reactions if useful

## Phase 18 — Captain Ginyu — Sparking ZERO

- Body Change preparation
- Targeting
- Tension
- Release
- Aftermath
- Hit reactions / knockbacks

## Phase 19 — Bergamo — Sparking ZERO

- Growth start
- Enlargement
- Giant-state transition
- Scale/form evidence
- Hit reactions / knockbacks

## Phase 20 — Hirudegarn — Sparking ZERO

- Wing rig
- Flap
- Glide
- Bank
- Dive
- Landing
- Giant attacks
- Stomp candidates
- Giant hit reactions

## Phase 21 — Great Ape Vegeta — Sparking ZERO

- Heavy walk
- Turn
- Stomp attacks
- Arm swings
- Reactions
- Knockbacks

## Phase 22 — Great Ape Baby — Sparking ZERO

- Alternate giant locomotion
- Aggression/posture variants
- Stomp candidates
- Reactions / knockbacks

## Phase 23 — Anilaza — Sparking ZERO

- Intelligent giant walk
- Long reach
- Heavy attack
- Stomp candidates
- Reactions / knockbacks

## Phase 24 — Cell Max — Sparking ZERO

- Charge
- Berserk attacks
- Stomp candidates
- Reactions / knockbacks
- Chaotic giant motion language

## Phase 25 — Giant Lord Slug — Sparking ZERO

- Large humanoid walk
- Large humanoid attacks
- Stomp candidates
- Reactions / knockbacks
- Bridge between normal humanoid and giant scale

## Phase 26 — Hiruzen — External Naruto Staff Reference

Hiruzen remains a separate Naruto staff reference rather than being falsely labeled as part of the Storm 4 extraction set if his desired reference comes from elsewhere.

- Staff thrust
- Staff sweep
- Staff guard
- Staff transitions

## Phase 27 — Cross-Game Hit Reaction / Knockback Consolidation
Create a source-reference reaction library organized by:

- Direction
- Severity
- Grounded/airborne
- Knockback distance
- Launch height
- Knockdown type
- Recovery type

Do not retarget yet.

## Phase 28 — Giant Stomp Consolidation

Compare every stomp candidate from:

- Great Ape Vegeta
- Great Ape Baby
- Anilaza
- Cell Max
- Giant Lord Slug
- Hirudegarn
- Broly Full Power

Mark true attack stomps vs locomotion steps.

## Phase 29 — Grounding / Flight Metadata Audit

Before downstream retarget work begins, audit all selected Sparking ZERO animations and confirm:

- Ground classification
- Floor offset
- Foot contacts
- Root vertical movement
- Flight dependency
- Downstream grounding recommendation

---

# 21. Mifune One-Touch Harvest Rule

When Mifune source data is opened, harvest/index all relevant 1A-1G source clips and reactions in one source pass so the archive does not have to be repeatedly reopened.

However:

- Do not process every category simultaneously.
- Do not create giant maps.
- Validate one representative path first.
- Then work through the queue in controlled sets.

The same one-touch principle applies to every later character: while that source character is open, also index their useful reactions, recoveries, transitions, and grounded/flight metadata.

---

# 22. Small Gym Standard

Every Gym should contain only what is necessary to answer its question.

Example:

```text
GYM_TAPION_OVERHEAD_STRIKE
Question: What is the native body/foot/sword timing of Tapion's preferred high overhead strike?
Contains:
- Original Tapion skeletal mesh
- Original Tapion skeleton
- Sword/scabbard if required
- Selected source animation(s)
- Neutral floor
- One consistent light rig
- One gameplay-like camera
- Optional side camera
- Debug root/foot markers
```

Do not build a map containing every character and every animation.

---

# 23. Validation Gates

Every source animation moves through these source-only gates:

- **G0 IDENTIFIED** — source relationship found; filename/ID verified or explicitly UNKNOWN.
- **G1 NATIVE PASS** — plays correctly on original rig.
- **G2 CONVERSION PASS** — any required conversion preserves intended native motion.
- **G3 UE5.8 SOURCE PASS** — imports into `AnimationHarvestGym` and plays correctly on original rig.
- **G4 VISUALIZED** — searchable entry, thumbnail/native preview, and diagnostic notes exist.
- **G5 STATE-CATALOGED** — useful states/time ranges recorded.
- **G6 HANDOFF READY** — metadata required by the retarget/production AI is complete.

There is intentionally **no Gemini retarget gate**.

---

# 24. Per-Animation Handoff Record

Use a structured record similar to:

```json
{
  "animation_id": "SOURCE_IDENTIFIER_OR_UNKNOWN",
  "source_game": "Sparking ZERO | Storm 4 | Shinobi Striker",
  "source_character": "Tapion",
  "source_form": "base",
  "source_container": "verified path or UNKNOWN",
  "native_skeleton": "verified source skeleton",
  "native_mesh": "verified source mesh",
  "weapon_or_prop": "sword/scabbard/etc",
  "gym_ids": ["GYM_TAPION_OVERHEAD_STRIKE"],
  "native_playback": "PASS",
  "ue58_native_import": "PASS",
  "retarget": "NOT_GEMINI_SCOPE",
  "motion_family": ["sword", "overhead"],
  "native_ground_class": "GROUND_NATIVE",
  "native_floor_offset_cm": 0,
  "left_foot_contacts": [],
  "right_foot_contacts": [],
  "root_motion": "inplace|forward|other|unknown",
  "root_displacement_cm": 0,
  "hit_reaction": false,
  "notes": ""
}
```

Never invent numeric values. Unknown values remain `UNKNOWN` until measured.

---

# 25. Reaction Record

```json
{
  "reaction_id": "SOURCE_REACTION_IDENTIFIER",
  "source_game": "Storm 4",
  "source_character": "Mifune",
  "incoming_direction": "front|back|left|right|diagonal|unknown",
  "severity": "light|medium|heavy|launch",
  "native_grounded": true,
  "native_flight": false,
  "root_displacement_cm": "MEASURED_OR_UNKNOWN",
  "knockdown": false,
  "recovery_clip": "SOURCE_ID_OR_UNKNOWN",
  "motion_matching_candidate": "yes|maybe|no",
  "native_playback": "PASS"
}
```

---

# 26. Snake Record

For a whole-snake clip, record:

```json
{
  "source_game": "Storm 4 | Shinobi Striker",
  "source_character_or_summon": "Orochimaru / Great Snake / Ninja Snakes / etc",
  "source_animation_id": "VERIFIED_OR_UNKNOWN",
  "snake_rig_type": "independent_full_rig|character_transform|attached_snakes|unknown",
  "motion": ["slither", "turn", "raise", "lunge", "bite"],
  "whole_body_motion": true,
  "root_or_body_translation": "animation|gameplay|mixed|unknown",
  "native_playback": "PASS",
  "notes": ""
}
```

Whole-body snake animation is the priority. Attached-arm snakes are secondary material.

---

# 27. Broly Transformation Record

Gemini must leave a compact transformation handoff:

```text
BASE FORM:
- native mesh/skeleton
- measured approximate height/width

TRANSFORM SEQUENCE:
- start frame/time
- major stance-widen frame/time
- major torso/shoulder expansion frame/time
- final power pose frame/time

TRANSFORMED FORM:
- native mesh/skeleton relationship
- measured approximate height/width

SOURCE IMPLEMENTATION EVIDENCE:
- mesh swap: yes/no/unknown
- morph targets: yes/no/unknown
- bone scale: yes/no/unknown
- actor scale: yes/no/unknown
- combination: yes/no/unknown

DOWNSTREAM:
- Manny/production GrowthAlpha required
- feet must remain grounded during growth
- Gemini does not implement target growth
```

---

# 28. Troubleshooting Decision Tree

```text
SOURCE NOT FOUND
 -> search character container
 -> search shared/common container
 -> search parameter/reference relationships
 -> compare gameplay behavior
 -> UNKNOWN if unresolved

SOURCE FOUND, NATIVE PLAYBACK WRONG
 -> extraction/interpretation problem
 -> verify tool version + exact game support
 -> compare a known-good clip on same source rig
 -> do NOT start retarget troubleshooting

NATIVE PASS, CONVERSION WRONG
 -> inspect scale / axes / hierarchy / curves / bake
 -> compare known-good conversion settings
 -> change one variable at a time

CONVERSION PASS, UE5.8 SOURCE IMPORT WRONG
 -> inspect import settings / source skeleton assignment / root / units
 -> compare known-good source import

SOURCE IMPORT PASS
 -> catalog, visualize, record states, and prepare handoff
 -> STOP before retargeting
```

After two failed hypotheses, stop guessing and collect evidence.

---

# 29. Git / GitHub Rule

The GitHub repository should contain:

- This master handoff document
- Project structure documentation
- Metadata schemas
- Automation scripts that are safe to share
- Known-good procedures
- Asset manifests that reference local source IDs

Do **not** commit extracted source-game meshes, skeletons, animations, textures, audio, or proprietary packages.

Source assets stay local in the Source Vault / Gym workstation.

---

# 30. ClickUp Organization

Use a dedicated list:

`17 — Animation Harvest Gym`

The ClickUp list should track:

- Project setup
- Every harvest phase
- Native import status
- Native playback status
- Metadata complete
- Reaction harvest complete
- Grounding metadata complete where applicable
- Handoff-ready status

Retargeting is a separate downstream workstream and must not be marked as Gemini work.

---

# 31. Gemini Reporting Format

For every completed Gym return:

```text
GYM ID:
GOAL:
SOURCE GAME:
SOURCE CHARACTER / FORM:
SOURCE ASSETS / CONTAINERS SEARCHED:
TOOL + VERSION:
ORIGINAL MESH IMPORTED: PASS/FAIL/UNKNOWN
ORIGINAL SKELETON IMPORTED: PASS/FAIL/UNKNOWN
NATIVE PLAYBACK: PASS/FAIL/PARTIAL/UNKNOWN
UE5.8 SOURCE IMPORT: PASS/FAIL/PARTIAL/UNKNOWN
WEAPON / PROP / CREATURE RELATIONSHIP:
ROOT / DISPLACEMENT NOTES:
GROUND / FLIGHT CLASSIFICATION:
FOOT CONTACT NOTES:
HIT REACTION ASSETS FOUND:
USEFUL STATE RANGES:
VISUAL LIBRARY ENTRY:
PROBLEMS:
EXACT NEXT SMALLEST TEST:
HANDOFF READY: YES/NO
RETARGETING: NOT GEMINI SCOPE
```

---

# 32. Definition of Done for Gemini

Gemini's animation-harvest job is complete when:

- `AnimationHarvestGym` exists as a separate UE5.8 project.
- Selected original characters and original skeletons import cleanly.
- Selected animations play natively in UE5.8 on the original rigs.
- Source identifiers/provenance are preserved.
- Mifune begins the actual character harvest.
- Tapion overhead sword attacks are captured.
- Janemba overhead sword attacks are captured.
- Krillin Destructo Disk body-motion family is captured.
- Broly base/transformation/full-power source evidence is captured, including growth/form-change evidence.
- Giant stomp candidates are captured and categorized.
- Storm 4 whole-snake motions are captured.
- Shinobi Striker whole-snake motions are captured.
- Hit reactions and knockbacks are harvested from both game families and organized for downstream Motion Matching.
- Sparking ZERO clips have grounded/flight metadata and foot-contact notes.
- The Visual Library can find motions by behavior without requiring the user to remember the source character.
- A separate AI can begin retargeting without reopening source archives to rediscover basic information.

---

# 33. Final Non-Negotiables

1. **Mifune is the first actual character harvest.**
2. **Gemini imports ORIGINAL characters + ORIGINAL animations.**
3. **Gemini does NOT retarget.**
4. **Another AI handles retargeting, Manny, production IK, and Motion Matching implementation.**
5. **DBZ/Sparking ZERO floating animations must be identified and prepared for later ground conversion.**
6. **Broly transformation must eventually make the target character physically larger; Gemini supplies the source evidence and timing.**
7. **Krillin Destructo Disk animation family is mandatory.**
8. **Tapion's high/overhead sword attacks are mandatory.**
9. **Janemba's high/demonic overhead sword attacks are mandatory.**
10. **Giant stomp attacks are mandatory research.**
11. **Hit reactions + knockbacks from both source games are mandatory and must become a complete downstream Motion Matching kit.**
12. **Whole-snake slither/raise/lunge/bite animation is mandatory from Storm 4 and Shinobi Striker.**
13. **Native playback is always the truth test before conversion or downstream work.**
14. **No giant source dump in one Gym.**
15. **No source-game assets committed to GitHub.**
16. **Unknown is an acceptable result. Guessing is not.**
