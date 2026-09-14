# Validation history

Current locally built patched JAR SHA-256:

`d578fbcbae6b4b47f799f73b92b6d70caf3a1c3ed51bd724e37dd8e8388994cf`

Original uploaded EMF 3.3.5 JAR SHA-256 used during development:

`68d185eeadb63f6669f2040cc35c4d2abaae7619c311d7b541d31628785e45db`

Static checks performed during development:

- restored class `EMFAnimationEntityContext` exists in the patched JAR,
- exact legacy `getEmfState()` descriptor exists,
- exact legacy `isEntityAnimPaused()Z` method exists,
- `entitiesPaused` has the expected `Set` field descriptor,
- Better Combat pause bridge targets current `EMFAnimationPauseHandler`,
- explicit current-EMF pause requests retain priority,
- bridge mixin is registered in EMF's mixin JSON,
- every EMF client mixin entry resolves to a class,
- JAR ZIP integrity passes.

Runtime testing still depends on launching the actual target modpack. Every runtime failure discovered later should be treated as a regression test for the next build.
