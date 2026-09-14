package traben.entity_model_features.mixin.mixins.compat;

import java.lang.reflect.Method;
import java.util.UUID;

import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

import traben.entity_model_features.models.animation.state.EMFEntityRenderState;
import traben.entity_model_features.utils.EMFAnimationPauseHandler;

/**
 * Runtime bridge for legacy emf-compat Better Combat builds that were compiled
 * against the pre-3.3.5 animation context API.
 */
@Mixin(value = EMFAnimationPauseHandler.class, remap = false)
public abstract class MixinLegacyEMFCompatPauseBridge {
    private static volatile boolean emfcompat$reflectionResolved;
    private static Method emfcompat$isBetterCombatEnabled;
    private static Method emfcompat$isAttackUnpaused;
    private static Method emfcompat$getSavedPoses;

    @Inject(method = "shouldAnimationsPause", at = @At("RETURN"), cancellable = true, remap = false)
    private static void emfcompat$legacyBetterCombatPauseBridge(
            EMFEntityRenderState state,
            CallbackInfoReturnable<Boolean> cir) {
        if (!cir.getReturnValueZ() || state == null) return;

        UUID uuid = emfcompat$uuid(state);
        if (uuid == null) return;

        // Preserve an explicit pause requested through EMF's current API.
        if (EMFAnimationPauseHandler.entitiesPaused.contains(uuid)) return;

        if (emfcompat$legacyBetterCombatWantsAnimations(uuid)) {
            cir.setReturnValue(Boolean.FALSE);
        }
    }

    private static UUID emfcompat$uuid(EMFEntityRenderState state) {
        try {
            return state.uuid();
        } catch (Throwable ignored) {
            return null;
        }
    }

    private static boolean emfcompat$legacyBetterCombatWantsAnimations(UUID uuid) {
        emfcompat$resolveReflection();
        if (emfcompat$isBetterCombatEnabled == null) return false;
        try {
            Object enabled = emfcompat$isBetterCombatEnabled.invoke(null);
            if (!(enabled instanceof Boolean) || !((Boolean) enabled)) return false;

            if (emfcompat$isAttackUnpaused != null) {
                Object unpaused = emfcompat$isAttackUnpaused.invoke(null, uuid);
                if (Boolean.TRUE.equals(unpaused)) return true;
            }

            if (emfcompat$getSavedPoses != null) {
                if (emfcompat$getSavedPoses.invoke(null, uuid, "better_combat") != null) return true;
                if (emfcompat$getSavedPoses.invoke(null, uuid, "playeranim_base") != null) return true;
            }
        } catch (Throwable ignored) {
            // Compatibility must never be allowed to break EMF startup/rendering.
        }
        return false;
    }

    private static void emfcompat$resolveReflection() {
        if (emfcompat$reflectionResolved) return;
        synchronized (MixinLegacyEMFCompatPauseBridge.class) {
            if (emfcompat$reflectionResolved) return;
            try {
                Class<?> mod = Class.forName("strm.emfcompat.bettercombat.EMFCompatBetterCombatMod");
                emfcompat$isBetterCombatEnabled = mod.getMethod("isEnabled");
            } catch (Throwable ignored) {}
            try {
                Class<?> pause = Class.forName("strm.emfcompat.bettercombat.compat.AttackPauseOverride");
                emfcompat$isAttackUnpaused = pause.getMethod("isUnpaused", UUID.class);
            } catch (Throwable ignored) {}
            try {
                Class<?> pose = Class.forName("strm.emfcompat.core.PoseManager");
                emfcompat$getSavedPoses = pose.getMethod("getSavedPoses", UUID.class, String.class);
            } catch (Throwable ignored) {}
            emfcompat$reflectionResolved = true;
        }
    }
}
