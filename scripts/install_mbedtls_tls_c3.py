"""
Install full mbedTLS client libraries AND a matching sdkconfig.h into the
Tasmota Arduino framework for ESP32-C3.

Tasmota's stock libmbedtls.a is a stub (~120KB, built against a sdkconfig.h
with CONFIG_MBEDTLS_TLS_DISABLED=1 — no real SSL/TLS implementation at all).
Overlaying only the real .a files (built with CONFIG_MBEDTLS_TLS_CLIENT_ONLY=y)
while our own code still compiles against the stock TLS_DISABLED sdkconfig.h
is an ABI mismatch: mbedtls struct layouts differ between the two configs,
corrupting the TLS handshake at runtime (garbled ClientHello / fatal alerts)
even though everything links fine. So this script overlays BOTH: the real
.a archives, and the sdkconfig.h they were actually compiled against
(extracted once from a custom_sdkconfig hybrid rebuild — see
lib/mbedtls_esp32c3/README.md) — so our code and the .a files agree on
mbedtls's struct layout. Avoids needing custom_sdkconfig on every build,
which breaks wled00/ source compilation on this chip (see kanbus-2c3584).
"""

Import("env")  # noqa: F821 — PlatformIO injects env

from pathlib import Path
import shutil

FRAMEWORK = Path(env.PioPlatform().get_package_dir("framework-arduinoespressif32"))
LIBS_DST = FRAMEWORK / "tools" / "esp32-arduino-libs" / "esp32c3" / "lib"
SRC = Path(env["PROJECT_DIR"]) / "lib" / "mbedtls_esp32c3"

LIBS = ("libmbedtls.a", "libmbedx509.a", "libmbedcrypto.a")
# Both board variants -- flash_mode selects one of these at build time; overlay both.
SDKCONFIG_DST_DIRS = (
    FRAMEWORK / "tools" / "esp32-arduino-libs" / "esp32c3" / "dio_qspi" / "include",
    FRAMEWORK / "tools" / "esp32-arduino-libs" / "esp32c3" / "qio_qspi" / "include",
)


def overlay(src, dst):
    if not src.is_file():
        print(f"*** mbedtls TLS (C3): missing {src}")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if (not dst.is_file()) or src.stat().st_size != dst.stat().st_size:
        shutil.copy2(src, dst)
        print(f"*** mbedtls TLS (C3): installed {dst.name} -> {dst.parent} ({src.stat().st_size} bytes)")
    else:
        print(f"*** mbedtls TLS (C3): {dst.name} already installed at {dst.parent}")


if not SRC.is_dir():
    print(f"*** mbedtls TLS (C3): missing vendored libs at {SRC}")
else:
    for name in LIBS:
        overlay(SRC / name, LIBS_DST / name)
    for d in SDKCONFIG_DST_DIRS:
        overlay(SRC / "sdkconfig.h", d / "sdkconfig.h")
