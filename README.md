# EMF 3.3.5 + Legacy EMF Compat Bridge

Compatibility work for **Entity Model Features (EMF) 3.3.5**, **Minecraft 1.21.1**, and **NeoForge 21.1.248**.

This repository contains the source, build tooling, metadata patches, documentation, and published release for the compatibility bridge built to keep older `emf-compat` addons working after EMF removed the legacy `EMFAnimationEntityContext` API.

## Current build

The current release is a patched EMF 3.3.5 JAR that restores the legacy API inside EMF itself and adds a modern pause bridge for Better Combat compatibility.

**Release:** https://github.com/17rexfordd-glitch/EMF-and-EMF-Compaibilty-/releases/tag/emf-3.3.5-legacy-compat-bridge

Release asset:

`entity_model_features-3.3.5-1.21-neoforge.jar`

The mod still reports version **3.3.5** to NeoForge so existing dependency ranges continue to work. Its display name is changed to **Entity Model Features + Legacy Compat Bridge** so logs clearly show when this build is loaded.

The GitHub Actions build automatically downloads the official upstream EMF 3.3.5 NeoForge build for Minecraft 1.21.1, compiles the bridge with Java 21, patches the JAR, validates it, uploads a workflow artifact, and publishes the JAR plus the upstream EMF license to the GitHub Release.

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

- `src/main/java/` — bridge source code injected into EMF 3.3.5
- `src/compile-stubs/` — minimal compile-only stubs used outside the full upstream workspace
- `tools/build_bridge.py` — reproducible build/patch/validation script
- `patch/` — resulting EMF metadata/mixin configuration for reference
- `.github/workflows/build-release.yml` — automatic Java 21 build and GitHub Release publisher
- `docs/` — build, compatibility, and validation notes
- `archive/` — history notes for the superseded FIX1–FIX5 approach
- `THIRD_PARTY.md` — upstream attribution and licensing notes

## Installation

Download `entity_model_features-3.3.5-1.21-neoforge.jar` from the GitHub Release and use it **in place of** the standard EMF 3.3.5 JAR. Keep the existing five EMF Compat addon JARs installed.

Do not install both the standard EMF 3.3.5 JAR and this patched JAR at the same time because they use the same NeoForge mod ID.

## Building it yourself

With JDK 21 and Python 3 installed:

```bash
python tools/build_bridge.py
```

The script can also patch a specific original JAR:

```bash
python tools/build_bridge.py --original /path/to/entity_model_features-3.3.5-1.21-neoforge.jar
```

## Upstream projects

- Entity Model Features: https://github.com/Traben-0/Entity_Model_Features
- EMF Compatibility: https://github.com/victorkozhokin/emf-compat

This repository is a compatibility project and is not an official upstream EMF release.
