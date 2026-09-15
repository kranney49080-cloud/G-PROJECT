# ASTRA 6 — COMBAT / ANIMATION START HERE

## Current authoritative workflow
The combat/animation implementation is being rebuilt around the owner-selected reference tutorial:

**Evans Bohl — How to Make a Combat System in UE5**
https://youtu.be/4omEu9N9WIE

The detailed Astra package is currently stored in the owner’s `MyProject2` coordination repository:

1. `ASTRA_EVANS_BOHL_COMBAT_REBUILD.md` — authoritative implementation directive
2. `EVANS_BOHL_REFERENCE_LEDGER.md` — mandatory timestamp/frame/Blueprint study ledger
3. `EVANS_BOHL_PARITY_MATRIX.md` — chapter-by-chapter implementation/test gate
4. `HANDSOME_SWORD_ASSET_MAP.md` — repository-confirmed HandsomeSwordV1/V2 source map
5. `ASTRA_HANDSOME_SWORD_START_HERE.txt` — updated entry point

## Critical correction
The older animation process must not be continued blindly.

For this project, **omnidirectional locomotion means normal third-person movement/animation in all directions including diagonals**. It does not by itself require lock-on, enemy-facing locomotion, a special duel architecture, or a special recovery-direction framework.

## Required method
`study tutorial → log exact visible Blueprint work → understand rationale → reproduce a single vertical slice → PIE test → adapt to HandsomeSwordV1/V2 → PIE test → expand → automate repetitive work → regression test`

Do not replace the tutorial’s proven process with speculative architecture. Do not guess unreadable Blueprint values. Mark unknown visual details and verify them.

## Sword-only source families
Use:
- `HandsomeSwordV1`
- `HandsomeSwordV2`

Do not silently substitute:
- `HandsomeSwordShield`

## Blocking
Do not derail tutorial parity to invent blocking. The currently confirmed V1/V2 inventory does not expose obvious dedicated sword-only block clips. If valid sword-only block assets are discovered later, document them and handle blocking as a separately verified feature.

## Stop point
Do not scale to other Combat Master weapon families until the owner reviews the complete tutorial-derived Handsome Sword implementation.
