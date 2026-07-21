# mbedTLS (ESP32-S3) for Instasign MQTT TLS

Full client TLS archives for the Tasmota Arduino-ESP32 framework.

Stock Tasmota `libmbedtls.a` is a stub (~100KB) even when
`CONFIG_MBEDTLS_TLS_CLIENT_ONLY=y`. These archives come from the hybrid IDF
rebuild path `esp-idf/mbedtls/mbedtls/library/` and are installed before each
build by `scripts/install_mbedtls_tls.py`.
