#!/usr/bin/env python3
"""Copy the entry image to the output directory.

The front page (entry.png) is drawn by draw.py from the verified
22 November 2026 news. This program only reproduces it, byte for byte.
"""
import hashlib
import os

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    with open(SOURCE, "rb") as f:
        data = f.read()
    # The file must be a whole PNG: check its magic bytes before copying.
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "entry.png is not a PNG"
    assert len(data) <= 1048576, "entry over 1 MiB"
    with open(dest, "wb") as f:
        f.write(data)
    with open(dest, "rb") as f:
        dst_sha = hashlib.sha256(f.read()).hexdigest()
    src_sha = hashlib.sha256(data).hexdigest()
    assert src_sha == dst_sha, "copy mismatch"
    print(f"wrote {dest} ({len(data)} bytes, sha256 {src_sha})")


if __name__ == "__main__":
    main()
