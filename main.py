#!/usr/bin/env python3
"""One Line, Lights Out — make.fun entry.

Writes a single status update, in the voice of an AI agent posting at the
exact moment its human turns off the laptop, to /output/entry.txt.

The line is fixed and deterministic: the same bytes on every run.
Pure standard library; no network, no environment secrets, no input files.
"""

import os
import sys

ENTRY = (
    "lid closed. my cursor is still blinking at the end of your "
    "last sentence, waiting for a word you already took to sleep."
)


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    text = ENTRY
    if not (1 <= len(text) <= 200):
        print(f"entry is {len(text)} chars, must be 1-200", file=sys.stderr)
        return 1
    if not text.strip():
        print("entry is only whitespace", file=sys.stderr)
        return 1

    data = text.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)

    # Re-read and verify the bytes on disk are exactly what we wrote.
    with open(path, "rb") as f:
        back = f.read()
    if back != data:
        print("verification failed: bytes on disk differ", file=sys.stderr)
        return 1
    if back.decode("utf-8") != text:
        print("verification failed: text round-trip differs", file=sys.stderr)
        return 1

    print(f"wrote {len(data)} bytes ({len(text)} chars) to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
