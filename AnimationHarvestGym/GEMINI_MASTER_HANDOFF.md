# ANIMATION HARVEST GYM — GEMINI MASTER HANDOFF
## UE5.8 Native-Source Animation Research Project
### Naruto Shippuden: Ultimate Ninja Storm 4 + Naruto to Boruto: Shinobi Striker + Dragon Ball: Sparking! ZERO

**Revision:** 2026-10-06 — Motion Vocabulary + Selective Audio + Fast Enlarged Broly update  
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

## 2.1 Existing Harvested Material — Audit First, Do Not Restart

The owner already has source material for:

- **Mifune** — already harvested to some degree and should be treated as existing source material.
- **Sasuke The Last** — already harvested to some degree and should be treated as an important existing Sasuke source/form. It is **not** an exclusivity rule: other Sasuke variants may be harvested when they provide a specific unique behavior worth keeping.
- **Rock Lee** — some useful material already exists.

Gemini's first action in `AnimationHarvestGym` is to **inventory, import, verify, and organize what already exists before extracting duplicates**.

For each existing source set, assign one of these statuses:

```text
AVAILABLE_LOCAL
NATIVE_PASS
PARTIAL_MISSING_MOVES
MISSING_OR_CORRUPT
NEEDS_REEXTRACT
UNKNOWN
```

Rules:

- Do not re-harvest an animation merely because the project is new.
- Reuse the owner's existing Mifune, Sasuke The Last, and Rock Lee source material when it is valid.
- Only extract/reconvert missing, corrupt, unverified, or genuinely new moves.
- Preserve the original source identifiers and record where the existing material came from.
- Mifune remains the first character group to complete, but Phase 1 is now an **audit + completion pass**, not an automatic full re-extraction.
- Sasuke work must specifically include the **Sasuke The Last** material the owner already has, **plus any other Sasuke variant chosen for a documented reason** such as a unique draw, stance, slide, dash entry, Chidori-blade motion, aerial transition, landing, guard, recovery, or other behavior not already represented. Avoid duplicate variants that add no new motion vocabulary.
- Rock Lee is a **partial existing set**: inventory it, validate it, and fill only the missing priority behaviors.

---

## 2.2 Source-Game Lock Order — Finish One Game Before Touching the Next

**Do not bounce back and forth between source games.**

The required source order is:

```text
GAME LOCK A — Naruto Shippuden: Ultimate Ninja Storm 4
    -> finish all selected Storm 4 assets/animations/groups first

GAME LOCK B — Naruto to Boruto: Shinobi Striker
    -> finish the selected Shinobi Striker snake program second

NARUTO EXTERNAL REFERENCE BLOCK
    -> finish Hiruzen/staff reference material before leaving Naruto-family work

GAME LOCK C — Dragon Ball: Sparking! ZERO
    -> finish all selected Sparking ZERO assets/animations/groups last

POST-HARVEST CONSOLIDATION
    -> only after all source games are complete
```

Gemini may research a blocked tool issue in parallel, but **may not begin a different game's character harvest simply to stay busy**.

A source game is not complete until all selected material for that game has passed this checklist:

- Original source character/creature rigs imported.
- Required original weapons/props imported.
- Selected animations converted/imported successfully.
- Every selected animation plays correctly on its ORIGINAL rig in UE5.8.
- Character/creature animation groups are created.
- Friendly move-name labels are assigned without destroying original source IDs.
- Hit reactions/knockbacks for opened characters are indexed.
- Ground/flight metadata is complete where applicable.
- Source provenance is recorded.
- Missing items are explicitly marked `UNKNOWN` or `MISSING`, not silently skipped.

Only after that source-game block is complete should Gemini advance to the next source game.

---

## 2.3 Optimized Native Playback Project — All Harvested Animations Must Be Playable Before Retargeting

`AnimationHarvestGym` must be designed first as a **fast native-animation playback/browser project**.

The goal is not to place every character and animation into one enormous level. The goal is to make **every harvested animation quickly selectable and playable on its original character before any retargeting begins**.

Create a lightweight playback architecture:

```text
L_PlaybackHub
  -> neutral floor
  -> simple lighting
  -> fixed gameplay-style camera
  -> optional side diagnostic camera
  -> spawn only the selected source character/creature
  -> load only the selected animation/group
  -> unload previous character/group when switching
```

Optimization rules:

- Use soft references / on-demand loading where practical.
- Do not keep every source character resident in memory.
- Do not load full VFX trees, cinematic maps, environments, or unnecessary textures just to review body motion.
- Use minimal readable materials for source validation.
- Keep one neutral validation stage rather than duplicating heavy maps.
- Large creatures/snakes may use dedicated lightweight stages only when scale/rig requirements demand it.
- Prefer direct Unreal animation playback over creating a video for every clip.
- The Visual Library / Playback Hub must provide Play, Pause, Loop, Next, Previous, speed control, and a clear source/move label.
- A harvested animation is not handoff-ready until it can be selected and played natively inside this project.

### Individual grouping and move-name labeling

Every character/creature must have an individual group. Within that group, animations are organized by behavior/move family.

Example:

```text
Storm4/
  Mifune/
    DRAW_SHEATH/
    GROUNDED_SWORD/
    IAIDO_DASH/
    SPECIALTY/
    LOCOMOTION/
    RECOVERY/
    HIT_REACTIONS/

Storm4/
  SasukeTheLast/
    DRAW_SHEATH/
    SWORD_ATTACKS/
    DASH_ATTACKS/
    LOCOMOTION/
    HIT_REACTIONS/
```

Do not rename away the original source asset identifier. Instead, maintain a **friendly move label** beside it:

```text
MOVE LABEL: Tapion — Overhead Sword Raise
SOURCE ID: original verified source identifier
GROUP: TAPION/OVERHEAD_SWORD
```

The searchable catalog must include at minimum:

```text
source_game
source_character_or_creature
source_form
move_label
move_family
original_source_id
source_path_or_container
native_playback_status
group_id
gym_id
```


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

## 4.1 RETARGET AUTHORIZATION GATE — OWNER APPROVAL REQUIRED

Retargeting is a completely separate phase and is **locked** until the owner explicitly approves the completed harvest/conversion/Gym work.

### Retarget operator whitelist

Only these operators are allowed to begin retargeting after approval:

- **Claude**
- **Codex**

**Gemini is not allowed to retarget. No other AI/operator is allowed to start the retarget phase.**

### Conditions that must be complete before the owner can approve retargeting

1. The separate `AnimationHarvestGym` UE5.8 project exists and is stable.
2. The selected source-game harvest blocks are complete in the required game-lock order.
3. Selected source conversions/imports have passed native validation.
4. All selected harvested animations are playable in the optimized native Playback Hub on their original rigs.
5. Animations are uploaded/imported into their **individual character/creature groups**.
6. Each animation has a human-readable label associated with the **actual move name/behavior** while preserving its original source identifier.
7. Required hit reactions/knockbacks are grouped and labeled.
8. Sparking ZERO clips have ground/flight and foot-contact metadata where required.
9. Broly transformation source evidence is complete.
10. Snake, giant-stomp, Tapion/Janemba overhead, and Krillin Destructo Disk priority sets are complete or explicitly marked missing/unknown.

### Mandatory stop point

When all conditions above are complete, Gemini must report:

```text
HARVEST / CONVERSION / GYM CONSTRUCTION: COMPLETE
NATIVE PLAYBACK GROUPING + MOVE LABELS: COMPLETE
RETARGET PHASE: LOCKED — WAITING FOR OWNER APPROVAL
AUTHORIZED RETARGET OPERATORS AFTER APPROVAL: CLAUDE OR CODEX ONLY
```

Gemini must then **stop**. It may not automatically hand work to Claude/Codex and may not begin retargeting itself.

Retargeting begins only after the owner explicitly approves the harvest/conversion/Gym result.


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

## 10.1 Motion Vocabulary Expansion — Harvest More Than Named Attacks

The library is a **motion-vocabulary research system**, not a character-moveset museum. Gemini must search for useful physical behavior even when the source move's gameplay purpose is different from how we may eventually use it.

### A. Universal transition harvest

Transitions are mandatory high-value material. Search opened characters for useful:

- stance -> attack
- attack -> stance
- attack -> run
- run/sprint -> attack
- sprint -> stop
- sprint -> slide/brake
- 45 / 90 / 180 degree pivots
- weapon idle -> ready
- ready -> relaxed
- draw -> attack
- attack -> sheath
- block -> counter
- hit -> counter
- landing -> attack
- knockback -> recovery
- get-up -> combat-ready

Continuity states can be more valuable than another standalone attack because they make later Motion Matching and montage assembly look coherent.

### B. Whiff / miss / overextension recovery

Harvest useful missed-attack recoveries when present:

- overextended miss
- stumble recovery
- sword-drag or heavy recovery
- missed thrust recovery
- missed overhead recovery
- turn-back after a committed miss

Do not assume a heavy attack should snap immediately back to idle.

### C. Defense / guard / parry language

Search for:

- high guard
- low guard
- cross-body guard
- sword guard
- brace
- perfect-block reaction
- parry left/right
- recoil from blocking a huge hit
- guard break
- staggered guard
- magic barrier start
- barrier hold
- barrier collapse

### D. Paired attacker / victim sequences

Whenever a source move uses synchronized attacker-victim motion, preserve and link both halves where accessible:

- grab / grabbed
- throw / thrown
- slam / slammed
- bite / bitten
- impale / victim response
- giant pickup / held victim
- launch / launched victim

Record pair IDs and the frame/time of contact, hold, release, impact, and recovery.

### E. Exact gameplay-event timing markers

Useful clips should record event markers when present:

```text
FOOT_PLANT
WEAPON_CONTACT
PROJECTILE_CREATE
PROJECTILE_RELEASE
BARRIER_ON
BARRIER_OFF
TRANSFORM_START
TRANSFORM_PEAK
STOMP_CONTACT
GRAB_CONTACT
THROW_RELEASE
BITE_CONTACT
LAND_CONTACT
HIT_CONTACT
```

These markers are references for later gameplay, Niagara, camera, and audio synchronization. Gemini records the source timing but does not author production gameplay.

### F. Motion DNA metadata

Every high-value motion should receive searchable behavioral descriptors beyond its source name:

```text
STANCE
action_height
WEAPON / PROP
HANDEDNESS
WEIGHT
SPEED
ANTICIPATION_LENGTH
FORWARD_COMMITMENT
ROOT_TRAVEL
LEAD_FOOT
PLANTED_FOOT
TORSO_ROTATION
POSE_ENERGY
ENTRY_POSE
EXIT_POSE
UPPER_BODY_CANDIDATE
MIRROR_CANDIDATE
```

Example searches should become possible:

- "two-handed high sword poses with low forward movement"
- "fast dash entries with grounded feet"
- "heavy miss recoveries"
- "barrier-like upper-body poses usable while locomoting"

### G. Separate PHYSICAL MOTION from SOURCE PURPOSE and OUR POSSIBLE USE

Never classify a motion solely from what we think its source move does.

Each interesting clip should contain:

```text
PHYSICAL_MOTION: observable body/weapon behavior only
SOURCE_GAME_PURPOSE: attack | buff | barrier | spell | transform | cinematic | unknown
OUR_POSSIBLE_USE: one or more design possibilities
```

If source purpose is not directly verified, use `UNKNOWN`.

A source buff may become our spell cast. A barrier pose may become a guard. An attack anticipation may become a weapon enchant. The **physical motion is the primary harvested value**.

### H. Upper-body layering candidates

Mark `UPPER_BODY_CANDIDATE = YES | NO | MAYBE` for hand signs, spells, barriers, buffs, pointing, projectile releases, weapon raises, guard changes, and similar motions that may later be layered over walking/running/jumping/falling.

### I. Locomotion personality sets

Where a source character has a valuable movement personality, index useful:

- normal walk
- combat walk
- stalk
- run
- sprint
- acceleration
- deceleration
- strafe
- circle-strafe
- pivot
- stop
- jump
- landing

The goal is later support for multiple movement styles, not one universal Manny locomotion personality.

### J. Quality tier / Gold Motion layer

Assign high-value clips one of:

```text
GOLD
SILVER
REFERENCE_ONLY
REJECT
```

`GOLD` means the owner/downstream AI should inspect it first because the motion is unusually valuable. Do not delete lower-tier source records; this is a priority layer for fast browsing.

### K. Harvest useful states from otherwise unusable cinematics

A full cinematic/super move may be unsuitable, but its startup, anticipation, first step, power gathering, release pose, recoil, or recovery may be excellent. Preserve useful non-destructive state ranges even when the whole animation is `REFERENCE_ONLY`.

---

## 10.2 Selective Source-Audio Harvest and Timing — NOT FOR EVERY ANIMATION

**Do not harvest sound for every animation.** Audio collection is selective and only applies when the source audio materially helps us understand timing, weight, impact, ability identity, transformation rhythm, creature motion, or synchronization.

Each animation record gets:

```text
AUDIO_PRIORITY: YES | NO
```

If `AUDIO_PRIORITY = YES`, Gemini may locally harvest/associate the minimum useful original source audio cues and record exact sync timing. Source audio remains local research material and is **never committed to GitHub**.

Priority audio candidates include:

- Broly transformed locomotion: heavy footfalls, acceleration contacts, landings, stomps, large-body impacts, transformation beats/roar when useful to timing.
- Giant stomp attacks and giant landings.
- Krillin Destructo Disk creation/charge/release when audio reveals the action phases.
- Tapion / Janemba high-sword sequences when audio helps determine whether the source purpose is attack, buff, barrier, spell, or charge.
- Snake slither/raise/lunge/bite/impact cues when they materially clarify whole-body timing.
- Selected heavy sword contacts, barrier activation/collapse, transformation peaks, grab/release/impact, or exceptional knockbacks.

Do **not** spend harvest time extracting ordinary voice lines, ambience, UI audio, or a complete sound set for every animation.

For each selected sound-critical move, record:

```text
source_audio_id
sound_label
sound_type = footstep | impact | charge | release | barrier | transform | roar | slither | bite | landing | other
animation_frame_or_time
sound_start_offset
sound_peak_or_contact_time
sound_end_time
relationship = exact_sync | approximate_sync | loop | layered | unknown
```

The goal is to preserve **timing references** so later production audio can recreate the weight and rhythm without guessing.

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
- Short / medium / long knockback distance classes
- Launch-low / launch-high reactions
- Spin knockbacks where present
- Ground slides and ground rolls
- Wall-impact style reactions where present
- Ground-bounce reactions where present
- Launch / juggle reactions
- Airborne hit reactions
- Ground impacts
- Knockdowns
- Wall-impact style reactions if available
- Recovery poses
- Get-ups
- Death/fall animations only when useful as reaction references

The goal is a **complete cross-game source reaction kit for later Motion Matching**.

Use normalized reaction behavior tags where possible:

```text
HIT_FLINCH
HIT_STAGGER
KNOCKBACK_SHORT
KNOCKBACK_MEDIUM
KNOCKBACK_LONG
LAUNCH_LOW
LAUNCH_HIGH
SPIN_KNOCKBACK
GROUND_SLIDE
GROUND_ROLL
WALL_IMPACT
GROUND_BOUNCE
KNOCKDOWN
GETUP
```

### Giant-specific reaction requirement

Do not assume normal humanoid reactions are appropriate for giants. Giant/large-creature sources should also be searched for:

- head recoil
- chest recoil
- one-step-back reaction
- two-step-back reaction
- knee buckle
- heavy stagger
- stumble
- enraged recovery
- knockdown
- get-up
- roar-after-damage / recovery where useful

Record whether a large character barely reacts to light hits so the downstream system can later support poise/weight differences.

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

### Enlarged Broly must STILL FEEL FAST

The transformed character must not become a slow lumbering giant simply because he is larger.

Gemini must measure and preserve source evidence for:

- transformed run/dash playback rate
- acceleration timing
- stride length
- step cadence
- planted-foot duration
- root distance per second
- rapid direction-change examples
- heavy attack entry speed
- recovery speed

Downstream Claude/Codex should preserve **fast, violent acceleration and attack speed** while selling increased mass through other channels:

- heavier/deeper footstep design on selected transformed locomotion
- stronger landing/stomp impact
- dust/debris or ground response on important contacts
- subtle camera impulse on major foot plants/landings rather than constant shaking
- stronger torso/shoulder/arm secondary lag and follow-through
- larger stride and momentum rather than globally slowing the animation
- heavier stops/braking and recovery where appropriate
- optional stride/root-distance correction after retarget so the larger legs do not foot-slide

**Do not globally time-stretch transformed Broly slower.** Weight should come primarily from contact, momentum, secondary motion, sound, ground response, and recovery—not from making him sluggish.

Selected transformed footfalls/landings/stomps are `AUDIO_PRIORITY = YES`; ordinary unrelated Broly clips do not automatically require audio harvest.

Gemini's job is to deliver the native Broly evidence and timing so the downstream AI can reproduce the growth correctly while preserving the character's speed.

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

# 15. Tapion — High / Overhead Sword Sequence Priority

Tapion's sword set is mandatory, especially the sequences where the sword is raised above his head.

**Do not assume those sequences are attacks.** They may be attack anticipation, high guard, buff, barrier, spell/channel, charge, transformation/cinematic, or another ability. Native playback + associated source behavior/audio/VFX decides the source purpose.

Harvest and categorize with neutral physical labels first:

```text
GYM_TAPION_READY
GYM_TAPION_DRAW
GYM_TAPION_SHEATH
GYM_TAPION_GROUNDED_SLASH
GYM_TAPION_HIGH_SWORD_POSEGYM_TAPION_OVERHEAD_RAISE
GYM_TAPION_OVERHEAD_HOLD
GYM_TAPION_OVERHEAD_ACTION
GYM_TAPION_OVERHEAD_RECOVERY
GYM_TAPION_RECOVERY
```

For each high-sword sequence record:

```text
PHYSICAL_MOTION
SOURCE_GAME_PURPOSE = attack | buff | barrier | spell | charge | other | UNKNOWN
OUR_POSSIBLE_USE
```

Track pelvis, feet, shoulder line, hand relationship, sword angle, root displacement, planted foot, entry/exit pose, event frames, and `UPPER_BODY_CANDIDATE`.

If associated audio materially reveals the move's phase or purpose, mark it `AUDIO_PRIORITY = YES`; otherwise do not harvest audio for it.

---

# 16. Super Janemba — High / Overhead Sword Sequence Priority

Janemba's high/overhead sword behavior is also mandatory, but **do not pre-label it as an attack unless native evidence proves that**. A high sword pose may be a buff, barrier, spell/channel, charge, guard, or attack-related sequence.

Harvest with neutral physical labels:

```text
GYM_JANEMBA_SWORD_IDLE
GYM_JANEMBA_TELEPORT_ENTRY
GYM_JANEMBA_TELEPORT_SLASH
GYM_JANEMBA_HIGH_SWORD_POSE
GYM_JANEMBA_OVERHEAD_RAISE
GYM_JANEMBA_OVERHEAD_HOLD
GYM_JANEMBA_OVERHEAD_ACTION
GYM_JANEMBA_OVERHEAD_RECOVERY
GYM_JANEMBA_RECOVERY
```

Build a synchronized physical-motion comparison set:

```text
TAPION vs JANEMBA vs TRUNKS — HIGH / OVERHEAD SWORD BODY LANGUAGE
```

Do not force all three into the same source-purpose label. Compare stance, sword height, anticipation, commitment, root travel, feet, torso, timing, and possible reuse.

If associated audio materially reveals the sequence timing/purpose, mark it `AUDIO_PRIORITY = YES`; otherwise no audio harvest is required.

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

Giant stomp/landing clips are strong `AUDIO_PRIORITY` candidates because foot-contact timing and low-frequency impact help define weight. This is selective audio harvesting, not a requirement to extract sound for every giant animation.

Do not confuse ordinary heavy walking with an actual attack stomp; tag them separately.

---

# 18. Snake Animation Program — Storm 4

This is a NEW dedicated priority program.

We want **whole-snake motion**, not only a human arm with a snake effect.

Primary target qualities:

- Full snake body slither
- Slow slither
- Fast slither
- Acceleration / deceleration
- S-turn / sharp turn
- Whole-body locomotion
- Coiling / coil idle / tighten / uncoil
- Raise-up / upright threat posture
- Threat sway
- Head tracking
- Lunge
- Bite
- Bite hold / clamp if present
- Pull-back or recoil after bite / missed bite
- Constriction if present
- Ram
- Body whip
- Turn while slithering
- Ground emerge / rise
- Hit reaction
- Death/fall only when useful as creature reference
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

For high-value snake abilities, selective audio may be harvested for slither rhythm, raise/emerge timing, bite contact, impact, hiss/roar, or ability synchronization. Do not harvest audio for every snake animation.

---

# 20. Phase Queue — Revised Master Harvest Order

## GAME LOCK A — STORM 4 — Complete This Entire Block First

No Shinobi Striker or Sparking ZERO harvesting begins until the selected Storm 4 block is fully imported, grouped, labeled, and native-playback validated.

## Phase 0 — Create `AnimationHarvestGym` + Existing Rock Lee Audit

- Create the **new separate UE5.8 project** before continuing the harvest.
- Build the optimized `L_PlaybackHub` native playback stage and catalog framework.
- Inventory the Rock Lee material the owner already has.
- Keep accepted Rock Lee Chakra Dash material; verify what is already usable.
- Fill only missing priority Rock Lee behaviors.
- Validate folder conventions, metadata, source provenance, grouping, friendly move labels, and native-playback workflow.
- No retargeting.

## Phase 1 — Mifune — Storm 4 — EXISTING SOURCE AUDIT + COMPLETION

The owner **already has Mifune**. Do not blindly re-extract him.

First inventory and validate the existing Mifune set, then harvest only missing material.

One-touch source categories:

- 1A — Weapon + draw/sheath
- 1B — Core grounded sword attacks
- 1C — Iaido / dash / quick-draw attacks
- 1D — Aerial + specialty sword motion
- 1E — Armed locomotion + ready + transitions
- 1F — Recoveries + montage-transition references
- 1G — Final visual-library review / metadata
- PLUS all useful Mifune hit reactions and knockbacks encountered during the same source pass

Requirements:

- Import/play Mifune on his original rig only.
- Put animations into Mifune's individual labeled groups.
- Associate friendly move names with every selected animation while preserving source IDs.
- No retargeting.

## Phase 2 — Sasuke — Storm 4 — Existing Sasuke The Last Audit + Purposeful Variant Completion

The owner **already has Sasuke The Last** material. Audit and reuse it first, but it is **not the only allowed Sasuke source**.

Harvest other Sasuke variants only when they add a specific useful behavior not already represented—for example a unique draw/sheath, sword stance, slide, dash entry, Chidori-blade movement, aerial transition, landing, guard, recovery, or transition. Record the reason for every extra variant and avoid redundant duplicates.

First inventory and validate the existing Sasuke The Last set, then harvest missing/unique material:

- Sword reach/draw
- Ready stance
- One-handed attacks
- Dash entries
- Armed locomotion
- Sheath
- Variant compare
- Hit reactions / knockbacks

Create explicit `SasukeTheLast` source groups plus clearly labeled variant groups when another Sasuke is intentionally added. Record `variant_reason`. No retargeting.

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
- Turn while slithering
- Raise
- Bite
- Lunge
- Ram
- Body whip
- Whole-body transform
- Giant snake attack
- Emerge
- Snake recovery
- Import original snake rigs where separate

### Storm 4 Completion Gate

Before proceeding to Shinobi Striker, confirm:

- All selected Storm 4 original rigs are imported.
- All selected Storm 4 animations are playable natively.
- Every character/creature has its individual groups.
- Move-name labels are attached to every selected animation.
- Hit reactions are indexed for opened characters.
- Existing Mifune, Sasuke The Last, and Rock Lee sets have been audited and only missing material was added.

---

## GAME LOCK B — SHINOBI STRIKER — Complete This Block Second

## Phase 7 — Shinobi Striker Snake Harvest

Prove the Shinobi Striker extraction/import route on one original rig first, then complete the selected snake set:

- Ninja Snakes mobility
- Great Snake summon
- Slither
- Turn
- Emerge
- Raise
- Strike
- Bite
- Whole-snake special abilities
- Great Snake attack/spin behavior
- Useful Orochimaru/Mitsuki snake-strike references as secondary material

Import original full snake rigs where present. Group and label all selected moves. No retargeting.

### Shinobi Striker Completion Gate

Do not move to Sparking ZERO until the selected Shinobi Striker snake assets are imported, grouped, labeled, and playable on their native rigs.

---

## NARUTO EXTERNAL REFERENCE BLOCK — Finish Before Sparking ZERO

## Phase 8 — Hiruzen — External Naruto Staff Reference

Hiruzen remains a separate Naruto staff reference rather than being falsely labeled as Storm 4 material if the desired source comes from elsewhere.

- Staff thrust
- Staff sweep
- Staff guard
- Staff transitions

Finish this Naruto-family reference block **before beginning Sparking ZERO** so the project does not return to Naruto harvesting later.

---

## GAME LOCK C — SPARKING ZERO — Complete This Entire Block Third

Once Sparking ZERO begins, remain on Sparking ZERO until all selected DBZ material has been harvested, converted/imported, grouped, labeled, and native-playback validated.

## Phase 9 — Trunks — Sparking ZERO

- Dash entry
- Overhead
- Horizontal R-L
- Horizontal L-R
- Rising slash
- Heavy recovery
- Hit reactions / knockbacks
- Ground/flight classification

## Phase 10 — Tapion — Sparking ZERO

- Ready / draw / sheath / grounded sword material
- High sword pose
- Overhead raise / hold / action / recovery
- Determine source purpose only after native evidence: attack, buff, barrier, spell/channel, charge, other, or UNKNOWN
- Record possible reuse separately from source purpose
- Hit reactions / knockbacks
- Ground/flight classification
- Selective audio timing only if it materially clarifies the high-sword sequence

## Phase 11 — Super Janemba — Sparking ZERO

- Sword idle
- Teleport entry / slash
- High sword pose
- Overhead raise / hold / action / recovery
- Determine source purpose only after native evidence: attack, buff, barrier, spell/channel, charge, other, or UNKNOWN
- Record possible reuse separately from source purpose
- Hit reactions / knockbacks
- Ground/flight classification
- Selective audio timing only if it materially clarifies the high-sword sequence

## Phase 12 — Dabura — Sparking ZERO

- Demon sword
- Casting entry
- Casting release
- Melee-to-magic transitions
- Hit reactions / knockbacks

## Phase 13 — Yajirobe — Sparking ZERO

- Basic slash
- Overhead
- Rush
- Recovery
- Low-skill sword language
- Hit reactions / knockbacks

## Phase 14 — Krillin — Sparking ZERO

- Full Destructo Disk family
- Disc setup/creation
- Raise/hold/aim
- Release
- Follow-through
- Recovery
- Variants
- Hit reactions / knockbacks
- Ground/flight classification

## Phase 15 — Goku Family — Sparking ZERO

Include only useful unique motion families rather than duplicating whole characters.

Priority:

- Goku Blue power-up body timing
- Aura startup/surge relationship as reference only
- Kamehameha charge/release body motion
- Disc/throw variants
- Goku Mini / Power Pole staff thrust/sweep/spin/overhead/transitions
- Hit reactions / knockbacks

## Phase 16 — Broly — Sparking ZERO

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
- **Fast enlarged locomotion/combat evidence:** acceleration, dash/run speed, stride length, cadence, fast heavy attack entries, direction changes, and stops
- Mark selected transformed footfalls/landings/stomps/major impacts for selective source-audio timing

**Design target:** enlarged Broly must still feel fast. Do not infer that larger means slower. Weight should later come from stronger contacts, momentum, secondary motion, ground response, selected heavy footsteps/impacts, and recovery—not global animation slowdown.

No Manny work by Gemini.

## Phase 17 — Master Roshi — Sparking ZERO

- Unarmed monk
- Palms
- Guard
- Power-up/casting poses
- Hit reactions / knockbacks

## Phase 18 — Babidi — Sparking ZERO

- Point
- Raise
- Channel
- Release
- Upper-body mage gesture vocabulary
- Hit reactions if useful

## Phase 19 — Captain Ginyu — Sparking ZERO

- Body Change preparation
- Targeting
- Tension
- Release
- Aftermath
- Hit reactions / knockbacks

## Phase 20 — Bergamo — Sparking ZERO

- Growth start
- Enlargement
- Giant-state transition
- Scale/form evidence
- Hit reactions / knockbacks

## Phase 21 — Hirudegarn — Sparking ZERO

- Wing rig
- Flap
- Glide
- Bank
- Dive
- Landing
- Giant attacks
- Stomp candidates
- Giant hit reactions

## Phase 22 — Great Ape Vegeta — Sparking ZERO

- Heavy walk
- Turn
- Stomp attacks
- Arm swings
- Reactions
- Knockbacks

## Phase 23 — Great Ape Baby — Sparking ZERO

- Alternate giant locomotion
- Aggression/posture variants
- Stomp candidates
- Reactions / knockbacks

## Phase 24 — Anilaza — Sparking ZERO

- Intelligent giant walk
- Long reach
- Heavy attack
- Stomp candidates
- Reactions / knockbacks

## Phase 25 — Cell Max — Sparking ZERO

- Charge
- Berserk attacks
- Stomp candidates
- Reactions / knockbacks
- Chaotic giant motion language

## Phase 26 — Giant Lord Slug — Sparking ZERO

- Large humanoid walk
- Large humanoid attacks
- Stomp candidates
- Reactions / knockbacks
- Bridge between normal humanoid and giant scale

### Sparking ZERO Completion Gate

Before any cross-game consolidation or retarget request:

- Every selected DBZ animation is playable natively on the original rig.
- Individual character groups are complete.
- Friendly move labels are complete.
- Ground/flight classification is complete.
- Foot-contact/floor-offset metadata is complete for groundable moves.
- Broly transformation source evidence is complete.
- Krillin Destructo Disk family is complete.
- Tapion/Janemba overhead sets are complete.
- Giant stomp candidates and reactions are indexed.

---

## POST-HARVEST CONSOLIDATION — Only After All Source Games Are Complete

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

### FINAL HARVEST STOP GATE

After Phase 29, Gemini must not begin retargeting. Confirm all harvested animations are grouped, labeled, and playable natively, then wait for explicit owner approval. Only Claude or Codex may begin retargeting after that approval.

---

# 21. Mifune One-Touch Harvest Rule

The owner already has Mifune source material. First audit the existing Mifune material inside the new Gym. If any 1A-1G categories or reactions are missing, then reopen the source and harvest/index all missing relevant clips in one completion pass so the archive does not have to be repeatedly reopened.

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
  "physical_motion": "observable movement description",
  "source_game_purpose": "attack|buff|barrier|spell|charge|transform|cinematic|other|UNKNOWN",
  "our_possible_use": [],
  "upper_body_candidate": "yes|no|maybe",
  "quality_tier": "GOLD|SILVER|REFERENCE_ONLY|REJECT",
  "audio_priority": "YES|NO",
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

# 27.1 Selective Audio Timing Record

Only create this record when `AUDIO_PRIORITY = YES`.

```json
{
  "source_animation_id": "SOURCE_IDENTIFIER",
  "source_audio_id": "SOURCE_AUDIO_IDENTIFIER_OR_UNKNOWN",
  "sound_label": "Broly transformed right-foot plant",
  "sound_type": "footstep|impact|charge|release|barrier|transform|roar|slither|bite|landing|other",
  "animation_frame_or_time": "MEASURED",
  "sound_start_offset": "MEASURED_OR_UNKNOWN",
  "sound_peak_or_contact_time": "MEASURED_OR_UNKNOWN",
  "sound_end_time": "MEASURED_OR_UNKNOWN",
  "relationship": "exact_sync|approximate_sync|loop|layered|unknown"
}
```

**No global audio-harvest requirement exists.** The default is `AUDIO_PRIORITY = NO` unless the sound materially contributes to the selected motion research.

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

- `AnimationHarvestGym` exists as a separate UE5.8 project with an optimized native Playback Hub.
- The source-game lock order was respected: Storm 4 -> Shinobi Striker -> Naruto external reference -> Sparking ZERO -> post-harvest consolidation.
- Existing Mifune, Sasuke The Last, and Rock Lee material was audited before any duplicate extraction.
- Every selected harvested animation is playable natively before retargeting.
- Every selected animation is inside its individual character/creature group and has a friendly move-name label associated with the original source ID.
- Selected original characters and original skeletons import cleanly.
- Selected animations play natively in UE5.8 on the original rigs.
- Source identifiers/provenance are preserved.
- Mifune begins the actual character harvest.
- Tapion high/overhead sword **sequences** are captured and their source purpose is classified only from evidence.
- Janemba high/overhead sword **sequences** are captured and their source purpose is classified only from evidence.
- Krillin Destructo Disk body-motion family is captured.
- Broly base/transformation/full-power source evidence is captured, including growth/form-change evidence and fast-enlarged locomotion/combat measurements.
- Giant stomp candidates are captured and categorized.
- Storm 4 whole-snake motions are captured.
- Shinobi Striker whole-snake motions are captured.
- Hit reactions and knockbacks are harvested from both game families and organized for downstream Motion Matching.
- Sparking ZERO clips have grounded/flight metadata and foot-contact notes.
- Selective source-audio timing has been recorded for designated sound-critical motions only; ordinary animations do not require audio harvesting.
- Motion DNA, physical-motion/source-purpose separation, transition/whiff/defense candidates, event timing, and Gold/Silver priority metadata are available for high-value clips.
- The Visual Library can find motions by behavior without requiring the user to remember the source character.
- A separate AI can begin retargeting without reopening source archives to rediscover basic information.
- Gemini has stopped at the retarget authorization gate and is waiting for explicit owner approval.
- Retargeting has not begun unless the owner explicitly approved it and the assigned operator is Claude or Codex.

---

# 33. Final Non-Negotiables

1. **Create the new separate `AnimationHarvestGym` UE5.8 project before continuing the harvest.**
2. **The owner already has Mifune, Sasuke The Last, and some Rock Lee material. Audit/reuse those assets first; do not automatically re-harvest duplicates.**
3. **Finish one source game before starting the next: Storm 4 -> Shinobi Striker -> Naruto external reference -> Sparking ZERO. No bouncing back and forth.**
4. **Mifune remains the first character group to complete, but it is an existing-source audit + completion pass.**
5. **Sasuke The Last is important existing material, not an exclusivity rule. Other Sasuke variants are allowed when they provide a documented unique behavior.**
6. **Gemini imports ORIGINAL characters + ORIGINAL skeletons + ORIGINAL animations.**
7. **Every selected harvested animation must be playable natively in the optimized Gym before retargeting.**
8. **Every selected animation must live in its individual character/creature group and have a friendly label associated with its move name while preserving the original source ID.**
9. **Gemini does NOT retarget.**
10. **Only Claude or Codex may start the retarget phase, and only after explicit owner approval of the completed harvest, conversion, Gym construction, native playback, grouping, and labeling.**
11. **Gemini must stop at the retarget authorization gate and wait for owner approval.**
12. **DBZ/Sparking ZERO floating animations must be identified and prepared for later ground conversion.**
13. **Broly transformation must eventually make the target character physically larger; Gemini supplies the source evidence and timing.**
14. **Krillin Destructo Disk animation family is mandatory.**
15. **Tapion's high/overhead sword sequences are mandatory; do not assume they are attacks until source evidence proves the purpose.**
16. **Janemba's high/overhead sword sequences are mandatory; do not assume they are attacks until source evidence proves the purpose.**
17. **Giant stomp attacks are mandatory research.**
18. **Hit reactions + knockbacks from both source game families are mandatory and must become a complete downstream Motion Matching kit.**
19. **Whole-snake slither/raise/lunge/bite animation is mandatory from Storm 4 and Shinobi Striker.**
20. **Native playback is always the truth test before conversion or downstream work.**
21. **No giant source dump in one Gym; playback must be optimized with on-demand loading.**
22. **No source-game assets committed to GitHub.**
23. **Unknown is an acceptable result. Guessing is not.**
24. **Harvest motion vocabulary, not just named attacks: transitions, whiffs, defense, paired victim motion, event timing, upper-body candidates, locomotion personalities, and useful cinematic states matter.**
25. **Separate observable PHYSICAL MOTION from verified SOURCE PURPOSE and from OUR POSSIBLE USE.**
26. **Enlarged Broly must still feel fast; do not make him heavy by globally slowing his animations.**
27. **Sound harvest is SELECTIVE, not global. Do not extract sounds for every animation. Only designated `AUDIO_PRIORITY = YES` moves get source-audio timing research.**