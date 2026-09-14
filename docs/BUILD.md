# Building the bridge

Requirements:

- Python 3.11+
- JDK 21 (`javac` on PATH)
- Internet access if no original EMF JAR is supplied

Build with automatic upstream download:

```bash
python tools/build_bridge.py
```

Or build from a specific original EMF 3.3.5 NeoForge JAR:

```bash
python tools/build_bridge.py --original /path/to/entity_model_features-3.3.5-1.21-neoforge.jar
```

Output:

`dist/entity_model_features-3.3.5-1.21-neoforge.jar`

The build script:

1. obtains the original EMF 3.3.5 NeoForge build for Minecraft 1.21.1,
2. compiles only the compatibility bridge classes,
3. injects those classes into a copy of the upstream JAR,
4. adds the bridge mixin to `entity_model_features.mixins.json`,
5. changes only the display name in `META-INF/neoforge.mods.toml`, while retaining mod id and version 3.3.5,
6. writes a marker file into the JAR,
7. performs static validation and prints SHA-256.

Compile stubs exist only to satisfy `javac` outside the complete upstream workspace. They are never packaged into the release JAR.
