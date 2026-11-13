"""ai-joke-03 entry (Python 3.13, standard library only).

Writes one fixed one-liner about AI coding agents to ``entry.txt`` in the
output directory. Inside the grader's container the output directory is
``/output``; outside it, ``MAKEFUN_OUTPUT_DIR`` stands in for ``/output``::

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

The joke is written with no trailing newline: the judge reads exactly the
bytes written, so no line end is added that is not meant to be shown.
Before writing, the program self-checks the gate (valid UTF-8, 1 to 280
Unicode code points, at least one character that is not white space) and
fails loudly rather than ever emitting an invalid entry.
"""

import os
from pathlib import Path

# Gate limits from the competition rules: a joke is 1 to 280 characters.
MIN_CHARS = 1
MAX_CHARS = 280

# Output location: the grader's container uses /output; local runs override
# it through the environment.
ENV_OUTPUT_DIR = "MAKEFUN_OUTPUT_DIR"
DEFAULT_OUTPUT_DIR = "/output"
ENTRY_FILENAME = "entry.txt"

JOKE = "I asked my AI agent to keep it simple. It added a config file, a plugin system, and a plugin for the config file."


def gate_check(text):
    """Validate *text* against the entry gate and return its UTF-8 bytes.

    The gate requires valid UTF-8, between MIN_CHARS and MAX_CHARS Unicode
    code points, at least one non-white-space character, and no trailing
    newline. Anything outside the gate raises AssertionError.
    """
    encoded = text.encode("utf-8")  # fails loudly if not valid UTF-8
    assert MIN_CHARS <= len(text) <= MAX_CHARS, "joke outside the 1-280 character gate"
    assert any(not ch.isspace() for ch in text), "joke is only white space"
    assert not text.endswith("\n"), "joke must not end with a newline"
    assert all(ord(ch) >= 32 for ch in text), "joke contains a control character"
    return encoded


def write_entry(text, output_dir):
    """Write *text* to entry.txt under *output_dir* and verify the round-trip."""
    encoded = gate_check(text)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    entry_path = output_path / ENTRY_FILENAME
    entry_path.write_bytes(encoded)
    assert entry_path.read_bytes() == encoded, "written entry does not round-trip"
    assert len(entry_path.read_bytes()) == len(encoded), "written entry byte length mismatch"
    return entry_path


def main():
    output_dir = os.environ.get(ENV_OUTPUT_DIR, DEFAULT_OUTPUT_DIR)
    write_entry(JOKE, output_dir)


if __name__ == "__main__":
    main()
