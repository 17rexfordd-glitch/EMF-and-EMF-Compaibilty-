# Compatibility notes

Target environment:

- Minecraft 1.21.1
- NeoForge 21.1.248
- Java 21
- Entity Model Features 3.3.5
- Entity Texture Features 7.2.x

Legacy EMF Compat modules being preserved:

- EMF Compat Core 1.1.2
- EMF Compat Better Combat 1.1.0
- EMF Compat Supplementaries 1.1.0
- EMF Compat Quark 1.1.0
- EMF Compat Not Enough Animations 1.2.0

## Root breakage

EMF 3.3.4 removed the deprecated class:

`traben.entity_model_features.models.animation.EMFAnimationEntityContext`

Older EMF Compat builds were compiled against that class and crash on EMF 3.3.5 with `ClassNotFoundException` / Mixin target errors.

The bridge restores that binary API inside EMF itself and delegates it to current EMF 3.3.5 state/pause APIs.

## Restored members

`EMFAnimationEntityContext.getEmfState()` delegates to `EMFState.state()`.

`EMFAnimationEntityContext.entitiesPaused` aliases `EMFAnimationPauseHandler.entitiesPaused`.

`EMFAnimationEntityContext.isEntityAnimPaused()` delegates to `EMFAnimationPauseHandler.shouldAnimationsPause(EMFState.state())`.

## Better Combat pause behavior

`MixinLegacyEMFCompatPauseBridge` injects at RETURN of `EMFAnimationPauseHandler.shouldAnimationsPause(EMFEntityRenderState)` and only lifts EMF's automatic pause when a legacy Better Combat compatibility source is actively holding an animation pose.

An explicit pause already present in `EMFAnimationPauseHandler.entitiesPaused` always wins.

Reflection is used deliberately so EMF does not gain a hard load-time dependency on Better Combat or emf-compat classes.
