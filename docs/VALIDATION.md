# Validation history

## Reproducible upstream input

The GitHub Actions build selected:

`3.3.5-neoforge-1.21 -> entity_model_features-3.3.5-1.21-neoforge.jar`

Upstream/original SHA-256:

`68d185eeadb63f6669f2040cc35c4d2abaae7619c311d7b541d31628785e45db`

That exactly matches the original EMF 3.3.5 JAR used during local development.

## Published GitHub Release

Published patched JAR SHA-256:

`91fc901e60d0a3c3a8c05fbc34adb2178f4a0705fe732000d6f39c3cd8b446aa`

Release asset:

`entity_model_features-3.3.5-1.21-neoforge.jar`

The GitHub Actions run completed successfully, including build, ZIP/JAR integrity validation, artifact upload, upstream-license retrieval, and GitHub Release publication.

## Local development build

Earlier locally built patched JAR SHA-256:

`d578fbcbae6b4b47f799f73b92b6d70caf3a1c3ed51bd724e37dd8e8388994cf`

The local and CI patched JAR hashes differ because the patched ZIP/JAR was rebuilt independently; the CI release is the canonical published build.

## Static checks

Checks performed during development and/or automated build:

- restored class `EMFAnimationEntityContext` exists in the patched JAR,
- exact legacy `getEmfState()` API exists,
- exact legacy `isEntityAnimPaused()Z` method exists,
- `entitiesPaused` exposes the expected `Set` field,
- Better Combat pause bridge targets current `EMFAnimationPauseHandler`,
- explicit current-EMF pause requests retain priority,
- bridge mixin is registered in EMF's mixin JSON,
- EMF version remains `3.3.5`,
- patched display name identifies the bridge build in logs,
- JAR ZIP integrity passes.

Runtime testing still depends on launching the actual target modpack. Every runtime failure discovered later should be treated as a regression test for the next build.
