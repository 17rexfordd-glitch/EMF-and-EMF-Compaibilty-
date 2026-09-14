#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "main" / "java"
STUBS = ROOT / "src" / "compile-stubs"
DIST = ROOT / "dist"
OUTPUT_NAME = "entity_model_features-3.3.5-1.21-neoforge.jar"
MODRINTH_PROJECT = "4I1XuqiY"
BRIDGE_MIXIN = "compat.MixinLegacyEMFCompatPauseBridge"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download_original(dest: Path) -> None:
    url = f"https://api.modrinth.com/v2/project/{MODRINTH_PROJECT}/version"
    req = urllib.request.Request(url, headers={"User-Agent": "emf-legacy-compat-bridge/1"})
    with urllib.request.urlopen(req) as response:
        versions = json.load(response)

    matches = []
    for version in versions:
        number = str(version.get("version_number", ""))
        loaders = version.get("loaders") or []
        games = version.get("game_versions") or []
        if number.startswith("3.3.5") and "neoforge" in loaders and "1.21.1" in games:
            matches.append(version)

    if not matches:
        raise RuntimeError("Could not find EMF 3.3.5 NeoForge for Minecraft 1.21.1 on Modrinth")

    matches.sort(key=lambda v: v.get("date_published", ""), reverse=True)
    version = matches[0]
    files = version.get("files") or []
    selected = next((f for f in files if f.get("primary")), files[0] if files else None)
    if not selected:
        raise RuntimeError("Matched Modrinth version has no downloadable files")

    print(f"Downloading upstream {version['version_number']} -> {selected['filename']}")
    urllib.request.urlretrieve(selected["url"], dest)


def compile_bridge(original: Path, classes: Path) -> None:
    javac = shutil.which("javac")
    if not javac:
        raise RuntimeError("javac was not found. Install/use JDK 21.")

    sources = sorted([*SRC.rglob("*.java"), *STUBS.rglob("*.java")])
    if not sources:
        raise RuntimeError("No bridge sources found")

    cmd = [
        javac,
        "--release", "21",
        "-classpath", str(original),
        "-d", str(classes),
        *map(str, sources),
    ]
    subprocess.run(cmd, check=True)


def patch_mixin_json(data: bytes) -> bytes:
    obj = json.loads(data.decode("utf-8"))
    client = obj.setdefault("client", [])
    if BRIDGE_MIXIN not in client:
        client.append(BRIDGE_MIXIN)
    return (json.dumps(obj, indent=2) + "\n").encode("utf-8")


def patch_mods_toml(data: bytes) -> bytes:
    text = data.decode("utf-8")
    old = 'displayName = "Entity Model Features"'
    new = 'displayName = "Entity Model Features + Legacy Compat Bridge"'
    if old in text:
        text = text.replace(old, new, 1)
    elif new not in text:
        raise RuntimeError("Could not find EMF displayName in neoforge.mods.toml")
    return text.encode("utf-8")


def write_patched_jar(original: Path, classes: Path, output: Path) -> None:
    replacements = {
        "entity_model_features.mixins.json": patch_mixin_json,
        "META-INF/neoforge.mods.toml": patch_mods_toml,
    }

    with zipfile.ZipFile(original, "r") as zin, zipfile.ZipFile(output, "w") as zout:
        seen = set()
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename in replacements:
                data = replacements[info.filename](data)
            zout.writestr(info, data)
            seen.add(info.filename)

        required_metadata = set(replacements)
        missing_metadata = required_metadata - seen
        if missing_metadata:
            raise RuntimeError(f"Original JAR missing required metadata: {sorted(missing_metadata)}")

        bridge_classes = [
            "traben/entity_model_features/models/animation/EMFAnimationEntityContext.class",
            "traben/entity_model_features/mixin/mixins/compat/MixinLegacyEMFCompatPauseBridge.class",
        ]
        for rel in bridge_classes:
            source = classes / rel
            if not source.is_file():
                raise RuntimeError(f"Compiled bridge class missing: {rel}")
            zout.write(source, rel)

        zout.writestr(
            "META-INF/emf-legacy-compat-bridge.txt",
            "EMF 3.3.5 legacy compatibility bridge\nMinecraft 1.21.1 / NeoForge 21.1.248 target\n",
        )


def validate(output: Path) -> None:
    with zipfile.ZipFile(output, "r") as jar:
        names = set(jar.namelist())
        required = {
            "traben/entity_model_features/models/animation/EMFAnimationEntityContext.class",
            "traben/entity_model_features/mixin/mixins/compat/MixinLegacyEMFCompatPauseBridge.class",
            "META-INF/emf-legacy-compat-bridge.txt",
        }
        missing = required - names
        if missing:
            raise RuntimeError(f"Patched JAR missing bridge files: {sorted(missing)}")

        mixins = json.loads(jar.read("entity_model_features.mixins.json"))
        if BRIDGE_MIXIN not in mixins.get("client", []):
            raise RuntimeError("Bridge mixin is not registered")

        toml = jar.read("META-INF/neoforge.mods.toml").decode("utf-8")
        if 'version = "3.3.5"' not in toml:
            raise RuntimeError("EMF version was not preserved as 3.3.5")
        if "Entity Model Features + Legacy Compat Bridge" not in toml:
            raise RuntimeError("Bridge display name is missing")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--original", type=Path, help="Path to original EMF 3.3.5 NeoForge JAR")
    args = parser.parse_args()

    DIST.mkdir(parents=True, exist_ok=True)
    output = DIST / OUTPUT_NAME

    with tempfile.TemporaryDirectory(prefix="emf-bridge-") as td:
        temp = Path(td)
        original = args.original.resolve() if args.original else temp / "original-emf.jar"
        if not args.original:
            download_original(original)
        if not original.is_file():
            raise FileNotFoundError(original)

        classes = temp / "classes"
        classes.mkdir()
        print(f"Original SHA-256: {sha256(original)}")
        compile_bridge(original, classes)
        write_patched_jar(original, classes, output)
        validate(output)

    print(f"Built: {output}")
    print(f"Patched SHA-256: {sha256(output)}")


if __name__ == "__main__":
    main()
