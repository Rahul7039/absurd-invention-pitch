"""Entry for make.fun competition
u-suroso-69-one-sentence-absurd-invention-pitch-5326c34a
("One-Sentence Absurd Invention Pitch").

Writes a single sentence (at most 220 characters) pitching a ridiculous
invention that fixes a tiny everyday annoyance to /output/entry.txt.

The gate the sealed scorer enforces: /output/entry.txt must be UTF-8
text of 1 to 220 characters, not only white space. This program checks
that gate itself before writing, and verifies the written file
afterwards, so a bad output can never be produced silently. It exits
0 on success, 2 if the gate check fails, 3 if the written file does
not match the entry text.

Deterministic: the output is a fixed string, so repeated runs are
byte-identical. Standard library only; no network access.
"""

import os
import sys

# The entry text itself. Chosen from 8 candidates and quality-gated;
# do not change it without re-running that selection.
ENTRY_TEXT = (
    "A houseplant that texts your landlord a photo of itself "
    "whenever you forget to water it for a week."
)

MAX_CHARS = 220
OUTPUT_PATH = "/output/entry.txt"

# Characters that end a sentence. A valid entry has exactly one, as its
# final character, so the text is one sentence and nothing more.
SENTENCE_ENDINGS = (".", "!", "?")


def validate_entry(text: str) -> list[str]:
    """Return a list of gate violations for *text* (empty = valid)."""
    problems: list[str] = []
    if not text.strip():
        problems.append("entry is empty or only whitespace")
    if len(text) < 1:
        problems.append("entry is shorter than 1 character")
    if len(text) > MAX_CHARS:
        problems.append(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        problems.append(f"entry is not valid UTF-8 text: {exc}")
    endings = [ch for ch in text if ch in SENTENCE_ENDINGS]
    if len(endings) != 1:
        problems.append(
            f"entry has {len(endings)} sentence-ending marks, expected exactly 1"
        )
    elif not text.endswith(endings[0]):
        problems.append("entry's sentence-ending mark is not its final character")
    # A line break or control character would still pass the scorer's
    # character count, but it would break the "one clean sentence" the
    # judge reads, so reject it here rather than shipping it.
    bad_controls = sorted({repr(ch) for ch in text if ord(ch) < 32})
    if bad_controls:
        problems.append(
            f"entry contains control characters: {', '.join(bad_controls)}"
        )
    return problems


def main() -> int:
    problems = validate_entry(ENTRY_TEXT)
    if problems:
        for problem in problems:
            print(f"error: gate check failed: {problem}", file=sys.stderr)
        return 2

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY_TEXT)

    # Verify what landed on disk, so a write failure can never pass
    # silently: the file must be byte-identical to the entry text.
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    if written != ENTRY_TEXT.encode("utf-8"):
        print(
            f"error: wrote {len(written)} bytes to {OUTPUT_PATH}, "
            f"expected {len(ENTRY_TEXT.encode('utf-8'))} bytes of entry text",
            file=sys.stderr,
        )
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
