package traben.entity_model_features.models.animation;

import java.util.Set;
import java.util.UUID;
import traben.entity_model_features.models.animation.state.EMFEntityRenderState;
import traben.entity_model_features.models.animation.state.EMFState;
import traben.entity_model_features.utils.EMFAnimationPauseHandler;

/** Compatibility shim for addons compiled against EMF <= 3.3.3. */
@Deprecated
public abstract class EMFAnimationEntityContext {
    public static final Set<UUID> entitiesPaused = EMFAnimationPauseHandler.entitiesPaused;

    public static EMFEntityRenderState getEmfState() {
        return EMFState.state();
    }

    public static boolean isEntityAnimPaused() {
        return EMFAnimationPauseHandler.shouldAnimationsPause(EMFState.state());
    }
}
