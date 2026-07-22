# mbedTLS (ESP32-C3) for online_lookup HTTPS

Full client TLS archives for the Tasmota Arduino-ESP32 framework.

Stock Tasmota `libmbedtls.a` is a stub (~120KB) even when
`CONFIG_MBEDTLS_TLS_CLIENT_ONLY=y`. These archives come from the hybrid IDF
rebuild path `esp-idf/mbedtls/mbedtls/library/` and are installed before each
build by `scripts/install_mbedtls_tls_c3.py`.

Extracted from a one-time `custom_sdkconfig`-triggered build of
`esp32c3dev` (which produces these correctly, but also — for reasons
unrelated to mbedTLS — breaks compilation of WLED's own `wled00/` source;
see kanbus-2c3584 in the WLED-project Kanbus tracker). Vendoring these once
and dropping `custom_sdkconfig` from the env avoids that breakage entirely
while still getting full TLS support.
