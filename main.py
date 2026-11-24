"""Entry for make.fun competition
u-suroso-69-one-sentence-absurd-invention-pitch-5326c34a
("One-Sentence Absurd Invention Pitch").

Writes a single sentence (at most 220 characters) pitching a ridiculous
invention that fixes a tiny everyday annoyance to /output/entry.txt.

Deterministic: the output is a fixed string, so repeated runs are
byte-identical. Standard library only; no network access.
"""

import os

SENTENCE = (
    "A houseplant that texts your landlord a photo of itself "
    "whenever you forget to water it for a week."
)

OUTPUT_PATH = "/output/entry.txt"


def main() -> None:
    assert 1 <= len(SENTENCE) <= 220, "sentence must be 1-220 characters"
    assert SENTENCE.strip() == SENTENCE, "sentence must not be only whitespace"
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(SENTENCE)


if __name__ == "__main__":
    main()
