# mbedTLS (ESP32-C3) for online_lookup HTTPS

Full client TLS archives for the Tasmota Arduino-ESP32 framework, built with
SECP384R1/SECP521R1 elliptic curve support in addition to the default
SECP256R1. Modern CAs increasingly issue with P-384 (e.g. Google's GTS Root
R4) — without it, `mbedtls_x509_crt_parse_der()` fails with
`MBEDTLS_ERR_PK_UNKNOWN_NAMED_CURVE` (-0x3A00) on any certificate chain that
includes a P-384 cert, aborting the handshake even under `setInsecure()`
(mbedTLS still has to structurally parse every cert the server sends).

Stock Tasmota `libmbedtls.a` is a stub (~120KB) even when
`CONFIG_MBEDTLS_TLS_CLIENT_ONLY=y`. These archives come from the hybrid IDF
rebuild path `esp-idf/mbedtls/mbedtls/library/` and are installed before each
build by `scripts/install_mbedtls_tls_c3.py`.

Extracted from a one-time `custom_sdkconfig`-triggered build of
`esp32c3dev` (which produces these correctly, but also — for reasons
unrelated to mbedTLS — breaks compilation of WLED's own `wled00/` source;
see kanbus-2c3584/kanbus-3d5ae7 in the WLED-project Kanbus tracker).
Vendoring these once and dropping `custom_sdkconfig` from the env avoids
that breakage entirely while still getting full TLS support.

Note: `CONFIG_MBEDTLS_CERTIFICATE_BUNDLE` (needed for `seengreat_rgb_matrix_s3`'s
mutual-TLS AWS IoT connection) was left OFF for this extraction — enabling it
implicitly restricted the curve set back to SECP256R1-only, and online_lookup
doesn't need it anyway since it uses `setInsecure()` rather than chain
verification against a bundled root set.
