# Complete Studio — Master Specification

## Purpose
Complete Studio is a standalone local visual asset-production application for the Game Project. Astra 6 writes/builds it once; after that, the studio should run independently without requiring Astra for normal use.

It is not the Tree Production Dashboard. The Tree Production Dashboard tracks approvals/status. Complete Studio is the actual visual working environment used to create, isolate, compose, organize, compare, and prepare art assets for the game.

## Core principle
The studio should feel like a comfortable, simple, visual workspace rather than a developer tool. The user should be able to perform common image-production tasks without hunting through folders or repeatedly asking an AI to do basic operations.

## Primary capabilities

### 1. Image workspace / canvas composition
Provide a central canvas where images can be:
- imported by drag/drop or file picker;
- positioned freely;
- scaled;
- rotated;
- duplicated;
- layered front/back;
- hidden/shown;
- locked/unlocked;
- grouped;
- aligned;
- cropped;
- composed into reference boards, tree sheets, environment sheets, or card atlases.

Canvas should support:
- zoom and pan;
- fit-to-screen;
- selectable background color including pure white, transparent checkerboard, and dark neutral;
- export at user-selected resolution;
- quick presets for square, portrait, landscape, ultrawide, and custom dimensions.

### 2. Remove Background integration
A dedicated Remove Background action should operate on selected images.

Requirements:
- one-click background removal;
- preserve original image untouched;
- create a derived transparent-background version;
- before/after preview;
- edge refinement controls where practical;
- ability to restore original;
- save result as PNG with transparency;
- no need to manually leave the studio for routine background removal.

The implementation may use an existing local/rembg-style model/tool or another reliable offline/local method selected by Astra 6, but the user-facing workflow should stay simple.

### 3. Asset library
Provide a visual asset browser for all studio outputs.

Each asset should be able to store:
- name;
- category;
- source/original file;
- derived files;
- notes;
- tags;
- approval/save status;
- creation timestamp;
- last-edited timestamp;
- project-relative path when saved into the Game Project.

Useful categories include:
- Trees
- Trunks
- Branches
- Canopy
- Foliage
- Ground
- Rocks
- Graveyard
- Architecture
- Characters
- References
- Cards / 2.5D
- UI / Misc

### 4. Temporary workspace and cleanup lifecycle
The studio should distinguish between temporary/generated work and explicitly saved production assets.

Agreed cleanup behavior:
- Newly created/imported/generated working items may begin in a temporary area.
- If an item is not explicitly selected/marked for Save within **12 hours**, it moves to a **Delete Bin**.
- Items in the Delete Bin remain recoverable for **7 days**.
- After 7 days in the Delete Bin, they are automatically permanently deleted.
- Provide **Restore** for individual items.
- Provide **Delete Now** for individual items.
- Provide **Empty Delete Bin Now** for all items.
- Clearly show time remaining before permanent deletion.
- Saved/approved production assets must never be auto-deleted.

### 5. Reference board workflow
The studio should make it easy to create visual reference sheets like the tree-reference boards used in this project.

Capabilities:
- import multiple images;
- tile them automatically;
- reorder them;
- label them;
- crop/split a collage into separate reference images;
- save the original board and the split images;
- maintain links between board and source images;
- compare a new asset side-by-side against the master reference.

### 6. Color analysis tools
Selected images should support palette extraction and image statistics.

At minimum provide:
- dominant colors;
- HEX;
- RGB;
- HSL/HSV when useful;
- linear RGB suitable for Unreal material constants;
- lightest color;
- darkest color;
- most common colors;
- least common / rare highlight colors;
- percentage/share of dominant palette colors;
- brightness/luminance statistics;
- optional region sampling for foreground, background, ground, shadow, highlight, etc.

The studio should be able to export:
- palette image/chart;
- CSV/JSON palette data;
- human-readable Markdown spec.

### 7. 2.5D card preparation
The studio is intended to support the game's optimized 2.5D environment pipeline.

Provide tools/workflow for preparing:
- trunk cards;
- branch cards;
- leaf/foliage cards;
- overhead canopy cards;
- distant forest cards;
- alpha-masked transparent PNGs;
- atlases where helpful.

Useful functions:
- trim transparent margins;
- add/remove padding;
- set pivot marker/reference point;
- preview card on light/dark backgrounds;
- preview approximate in-game angle;
- export with transparent background.

### 8. Tree production support
For Tree 01 and future trees, Complete Studio should support producing and organizing:
- standing hero tree;
- oblique/side reference;
- felled/cut tree;
- stump;
- cut surface;
- tree-local canopy pieces;
- shared canopy artwork;
- harvested logs/resource pieces;
- damage/chop mark textures;
- variants.

It should preserve the separation between structural trunk/major branches and canopy artwork so harvesting mechanics can remove local canopy without requiring every shared canopy element to belong to one tree.

### 9. Versioning and approval
Every important asset should support versions such as:
- v01
- v02
- v03

User should be able to mark:
- Draft
- Keep
- Needs Revision
- Approved
- Production Ready

Do not overwrite approved versions silently.

### 10. Project save/export
Complete Studio should be able to save approved outputs into organized project folders without requiring the user to hunt through the filesystem.

Target integration should support the G-PROJECT repository and project-relative paths.

Examples:
`Art/Environment/Trees/...`
`Art/Environment/Canopy/...`
`Art/References/...`

The tool should make the destination understandable and visible before saving.

## UX direction
- Comfortable dark UI.
- Dark teal / blue-grey visual language fits the forest project.
- Large visual previews.
- Minimal clutter.
- Clear left asset browser, central canvas, right properties/operations panel is acceptable.
- Drag-and-drop should be preferred where practical.
- Common actions should be obvious and one-click.
- The user should not need terminal knowledge for normal operation.

## Standalone requirement
After Astra 6 finishes building and validating Complete Studio:
- normal use must not require Astra 6;
- normal use must not require OpenCode;
- normal use should not require a terminal;
- the user should have a simple launcher or executable/shortcut;
- the studio should run locally on the user's PC;
- failures should be shown in-app with understandable messages.

## Safety / stability requirements
- Never recursively spawn terminals/processes.
- Never start repeated launcher instances.
- Use a single-instance lock where practical.
- Never mass-delete outside the studio-managed temporary/delete-bin directories.
- Destructive actions require clear confirmation.
- Auto-cleanup rules apply only to studio-managed temporary assets.
- Preserve originals by default when running transformations.

## Relationship to other project tools

### Complete Studio
Actual visual production workspace.

### Tree Production Dashboard
Tracks status, approval, dependencies, harvesting readiness, and Unreal verification.

### Astra 6
Builds/extends Complete Studio and handles difficult architecture/development work. It should not be required for ordinary day-to-day studio usage once the tool is complete.

## Current priority
Build Complete Studio around the environment/tree pipeline first rather than attempting to become a general-purpose Photoshop replacement.

First production proof should support:
1. import master forest/tree references;
2. isolate/remove background from a tree;
3. compose and resize tree artwork on canvas;
4. compare against master reference;
5. extract/save palette data;
6. export transparent tree/card art;
7. organize/save approved results into the project;
8. recover/delete temporary work according to the 12-hour → Delete Bin → 7-day cleanup policy.

Once this complete loop is stable, extend the same studio architecture to other environment assets.
