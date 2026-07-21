"""
Install full mbedTLS client libraries into the Tasmota Arduino framework.

Tasmota's hybrid `custom_sdkconfig` rebuild compiles real SSL objects under
esp-idf/mbedtls/mbedtls/library/, but only copies the stub
esp-idf/mbedtls/libmbedtls.a into esp32-arduino-libs. This pre-script overlays
vendored full archives so NetworkClientSecure can link.
"""

Import("env")  # noqa: F821 — PlatformIO injects env

from pathlib import Path
import shutil

FRAMEWORK = Path(env.PioPlatform().get_package_dir("framework-arduinoespressif32"))
DST = FRAMEWORK / "tools" / "esp32-arduino-libs" / "esp32s3" / "lib"
SRC = Path(env["PROJECT_DIR"]) / "lib" / "mbedtls_esp32s3"

LIBS = ("libmbedtls.a", "libmbedx509.a", "libmbedcrypto.a")

if not SRC.is_dir():
    print(f"*** mbedtls TLS: missing vendored libs at {SRC}")
else:
    for name in LIBS:
        src = SRC / name
        dst = DST / name
        if not src.is_file():
            print(f"*** mbedtls TLS: missing {src}")
            continue
        DST.mkdir(parents=True, exist_ok=True)
        if (not dst.is_file()) or src.stat().st_size != dst.stat().st_size:
            shutil.copy2(src, dst)
            print(f"*** mbedtls TLS: installed {name} ({src.stat().st_size} bytes)")
        else:
            print(f"*** mbedtls TLS: {name} already installed")
