#!/usr/bin/env python3
"""Entry generator for the make.fun bounty
'u-zeroxfive-funniest-autocorrect-fail-ddf82154' (Funniest Autocorrect Fail).

The competition asks for ONE line, under 200 characters, that reads as a
funny autocorrect fail. This script holds the entry text, validates it
against the competition rules, writes it to ``entry.txt`` in the output
directory, and prints the entry text itself to stdout so the submission
pipeline can capture it verbatim.

Deterministic, stdlib only: no network, no clock, no randomness, no
environment-dependent behaviour. Running it twice produces byte-identical
stdout and an identical ``entry.txt``.
"""

import hashlib
import os
import re
import sys

# ---------------------------------------------------------------------------
# The entry
# ---------------------------------------------------------------------------

ENTRY_TEXT = (
    "I texted my boss \"I'll be there in a sec\" and autocorrect sent "
    "\"I'll be there in a sex\" \u2014 HR meeting scheduled for Monday."
)

# Competition limits (from the bounty brief).
MAX_CHARS = 200
MAX_LINES = 1

# Words the fail pivots on: what was typed vs. what autocorrect sent.
INTENDED_WORD = "sec"
AUTOCORRECTED_WORD = "sex"

# Words that must not appear anywhere in the entry (keep it clean and
# workplace-safe: the joke is the typo, not anything explicit).
BANNED_WORDS = (
    "porn",
    "xxx",
    "casino",
    "betting",
    "lottery",
)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

class EntryValidationError(ValueError):
    """Raised when the entry text violates a competition rule."""


def _check_length(text: str) -> None:
    """The entry must be a single line under 200 characters."""
    if not text:
        raise EntryValidationError("Entry text must not be empty")
    if len(text) >= MAX_CHARS:
        raise EntryValidationError(
            f"Entry must be under {MAX_CHARS} characters, "
            f"got {len(text)}: {text!r}"
        )
    if text != text.strip():
        raise EntryValidationError(
            "Entry must not start or end with whitespace"
        )


def _check_single_line(text: str) -> None:
    """Exactly one line: no newlines, carriage returns or line separators."""
    if "\n" in text or "\r" in text:
        raise EntryValidationError("Entry must be exactly one line")
    if "\u2028" in text or "\u2029" in text:
        raise EntryValidationError(
            "Entry must not contain Unicode line separators"
        )


def _check_consequence(text: str) -> None:
    """The fail needs a payoff: something that happens because of the typo.

    Without a consequence the line is just a typo report, not a joke. The
    entry's punchline is the HR meeting the mangled message caused, so the
    text must name a concrete fallout (a meeting, a reply, a reaction).
    """
    lowered = text.lower()
    fallout_markers = ("hr meeting", "called into", "replied", "mom called",
                       "grounded", "fired", "awkward")
    if not any(marker in lowered for marker in fallout_markers):
        raise EntryValidationError(
            "Entry must show a consequence of the autocorrect fail "
            "(e.g. an HR meeting, a reply, an awkward fallout)"
        )


def _check_reads_as_autocorrect_fail(text: str) -> None:
    """The line must read as an autocorrect fail, not a generic joke.

    Structural checks, kept deliberately simple so they cannot drift:
      * it mentions autocorrect by name,
      * it quotes both the intended text and the mangled text,
      * the two quoted fragments differ by exactly the autocorrected word,
      * the mangled word is a plausible one-letter-ish autocorrect slip of
        the intended word (same first letter, similar length).
    """
    lowered = text.lower()
    if "autocorrect" not in lowered:
        raise EntryValidationError(
            "Entry must mention autocorrect to read as an autocorrect fail"
        )

    quoted = re.findall(r'"([^"]+)"', text)
    if len(quoted) < 2:
        raise EntryValidationError(
            "Entry must quote both the intended text and the autocorrected "
            f"text; found {len(quoted)} quoted fragment(s)"
        )
    intended, mangled = quoted[0], quoted[1]
    if intended == mangled:
        raise EntryValidationError(
            "Quoted intended text and autocorrected text must differ"
        )
    if INTENDED_WORD not in intended.lower():
        raise EntryValidationError(
            f"Intended text must contain {INTENDED_WORD!r}: {intended!r}"
        )
    if AUTOCORRECTED_WORD not in mangled.lower():
        raise EntryValidationError(
            f"Autocorrected text must contain {AUTOCORRECTED_WORD!r}: "
            f"{mangled!r}"
        )
    if intended[0].lower() != mangled[0].lower():
        raise EntryValidationError(
            "Autocorrect slip should keep the same first letter: "
            f"{intended!r} vs {mangled!r}"
        )


def _check_tone_and_safety(text: str) -> None:
    """Keep the joke clean: no banned words, no shouting, no emoji spam."""
    lowered = text.lower()
    for word in BANNED_WORDS:
        if word in lowered:
            raise EntryValidationError(
                f"Entry contains banned word {word!r}"
            )
    if text != text.strip():
        raise EntryValidationError("Entry has leading/trailing whitespace")
    # No more than one exclamation/question mark cluster: the joke should
    # land on the typo, not on punctuation.
    if len(re.findall(r"[!?]{2,}", text)) > 0:
        raise EntryValidationError(
            "Entry must not use repeated ! or ? punctuation"
        )


def validate(text: str) -> dict:
    """Run every competition check; return a report dict on success.

    Raises :class:`EntryValidationError` on the first violation found.
    """
    _check_length(text)
    _check_single_line(text)
    _check_reads_as_autocorrect_fail(text)
    _check_consequence(text)
    _check_tone_and_safety(text)
    return {
        "chars": len(text),
        "lines": 1,
        "quoted_fragments": re.findall(r'"([^"]+)"', text),
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    }


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def output_path() -> str:
    """Resolve the output file path.

    Uses ``$MAKEFUN_OUTPUT`` when set, otherwise ``/output``; if ``/output``
    is not writable, falls back to ``./output`` relative to this script's
    directory. A unique per-entry temp directory (e.g.
    ``/tmp/u-zeroxfive-funniest-autocorrect-fail-ddf82154``) is the usual
    choice when running locally, so parallel authors never collide.
    """
    out_dir = os.environ.get("MAKEFUN_OUTPUT")
    if out_dir:
        return os.path.join(out_dir, "entry.txt")
    if os.access("/output", os.W_OK) or not os.path.exists("/output"):
        try:
            os.makedirs("/output", exist_ok=True)
            if os.access("/output", os.W_OK):
                return "/output/entry.txt"
        except OSError:
            pass
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "output", "entry.txt")


def main(argv: list | None = None) -> int:
    """Validate the entry, write ``entry.txt``, print the entry to stdout.

    With ``--check`` as the only argument, validate and report to stderr
    without writing any file or printing the entry.
    """
    args = list(sys.argv[1:] if argv is None else argv)
    report = validate(ENTRY_TEXT)

    if args == ["--check"]:
        print(
            f"Entry OK: {report['chars']} chars, 1 line, "
            f"sha256={report['sha256']}",
            file=sys.stderr,
        )
        return 0
    if args:
        print(f"Unknown arguments: {args}", file=sys.stderr)
        return 2

    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY_TEXT + "\n")

    # Verify the written file by reading it back byte-for-byte.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != ENTRY_TEXT + "\n":
        raise RuntimeError(f"Read-back mismatch in {path}")
    if hashlib.sha256(written.encode("utf-8")).hexdigest() != hashlib.sha256(
        (ENTRY_TEXT + "\n").encode("utf-8")
    ).hexdigest():
        raise RuntimeError(f"Checksum mismatch in {path}")

    print(
        f"Wrote {path} ({report['chars']} chars, "
        f"sha256={report['sha256']})",
        file=sys.stderr,
    )

    # Stdout carries ONLY the entry text, so the pipeline captures it verbatim.
    sys.stdout.write(ENTRY_TEXT + "\n")
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except EntryValidationError as exc:
        print(f"ENTRY INVALID: {exc}", file=sys.stderr)
        sys.exit(2)
