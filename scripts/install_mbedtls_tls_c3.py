"""
Install full mbedTLS client libraries into the Tasmota Arduino framework
for ESP32-C3.

Tasmota's stock libmbedtls.a is a stub (~120KB) with no real SSL/TLS
implementation. This pre-script overlays vendored full archives (extracted
once from a custom_sdkconfig hybrid rebuild — see lib/mbedtls_esp32c3/README.md)
so WiFiClientSecure/NetworkClientSecure can link, without needing
custom_sdkconfig on every build (which breaks wled00/ source compilation
on this chip — see kanbus-2c3584).
"""

Import("env")  # noqa: F821 — PlatformIO injects env

from pathlib import Path
import shutil

FRAMEWORK = Path(env.PioPlatform().get_package_dir("framework-arduinoespressif32"))
DST = FRAMEWORK / "tools" / "esp32-arduino-libs" / "esp32c3" / "lib"
SRC = Path(env["PROJECT_DIR"]) / "lib" / "mbedtls_esp32c3"

LIBS = ("libmbedtls.a", "libmbedx509.a", "libmbedcrypto.a")

if not SRC.is_dir():
    print(f"*** mbedtls TLS (C3): missing vendored libs at {SRC}")
else:
    for name in LIBS:
        src = SRC / name
        dst = DST / name
        if not src.is_file():
            print(f"*** mbedtls TLS (C3): missing {src}")
            continue
        DST.mkdir(parents=True, exist_ok=True)
        if (not dst.is_file()) or src.stat().st_size != dst.stat().st_size:
            shutil.copy2(src, dst)
            print(f"*** mbedtls TLS (C3): installed {name} ({src.stat().st_size} bytes)")
        else:
            print(f"*** mbedtls TLS (C3): {name} already installed")
