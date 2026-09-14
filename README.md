# EMF 3.3.5 + Legacy EMF Compat Bridge

Compatibility work for **Entity Model Features (EMF) 3.3.5**, **Minecraft 1.21.1**, and **NeoForge 21.1.248**.

This repository contains the source and release files for the compatibility bridge built to keep older `emf-compat` addons working after EMF removed the legacy `EMFAnimationEntityContext` API.

## Current build

The current release is a patched EMF 3.3.5 JAR that restores the legacy API inside EMF itself and adds a modern pause bridge for Better Combat compatibility.

Release file:

`release/entity_model_features-3.3.5-1.21-neoforge.jar`

The mod still reports version **3.3.5** to NeoForge so existing dependency ranges continue to work. Its display name is changed to **Entity Model Features + Legacy Compat Bridge** so logs clearly show when this build is loaded.

## What the bridge restores

The compatibility class:

`traben.entity_model_features.models.animation.EMFAnimationEntityContext`

restores these old members expected by older compatibility addons:

- `getEmfState()`
- `entitiesPaused`
- `isEntityAnimPaused()`

They delegate to the current EMF 3.3.5 APIs:

- `EMFState.state()`
- `EMFAnimationPauseHandler.entitiesPaused`
- `EMFAnimationPauseHandler.shouldAnimationsPause(...)`

The project also includes `MixinLegacyEMFCompatPauseBridge`, which bridges old Better Combat compatibility behavior onto EMF 3.3.5's current pause handler.

## Repository layout

- `src/main/java/` — bridge source code that is injected into EMF 3.3.5
- `src/compile-stubs/` — minimal compile-only stubs used when compiling the bridge classes outside the full upstream workspace
- `release/` — current patched JAR
- `docs/` — technical notes, compatibility details, and validation history
- `LICENSE-EMF.txt` — upstream EMF LGPL-3.0 license
- `THIRD_PARTY.md` — upstream attribution and source links

## Installation

Use the patched EMF JAR in place of the standard `entity_model_features-3.3.5-1.21-neoforge.jar`. Keep the existing five EMF Compat addon JARs installed.

Do not install both the standard EMF 3.3.5 JAR and this patched JAR at the same time because they use the same NeoForge mod ID.

## Upstream projects

- Entity Model Features: https://github.com/Traben-0/Entity_Model_Features
- EMF Compatibility: https://github.com/victorkozhokin/emf-compat

This repository is a compatibility project and is not an official upstream EMF release.
