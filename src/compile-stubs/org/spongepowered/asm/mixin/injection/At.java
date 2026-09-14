package org.spongepowered.asm.mixin.injection;
import java.lang.annotation.*;
@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.METHOD, ElementType.ANNOTATION_TYPE})
public @interface At {
    String value();
    String target() default "";
    String[] args() default {};
    int ordinal() default -1;
    int opcode() default -1;
    boolean remap() default true;
}
