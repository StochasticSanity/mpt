# Makefile for Rust binary
PROJECT_NAME=rce-poc
RELEASE_BINARY=target/release/$(PROJECT_NAME)

.PHONY: all build release strip compress clean

all: release strip compress

# Build the project in debug mode
build:
	cargo build

# Build the project in release mode
release:
	cargo build --release

# Strip unnecessary symbols from the binary
strip: release
	strip $(RELEASE_BINARY)

# Compress the binary using UPX
compress: strip
	upx --best $(RELEASE_BINARY)

# Clean build artifacts
clean:
	cargo clean