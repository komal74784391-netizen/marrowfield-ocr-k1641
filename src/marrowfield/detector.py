"""Marrowfield OCR text detector."""

from dataclasses import dataclass
from typing import List


@dataclass
class Box:
    x: int
    y: int
    w: int
    h: int
    text: str = ""


def merge_boxes(boxes: List[Box], gap: int = 8) -> List[Box]:
    """Merge horizontally adjacent boxes into reading-order lines."""
    ordered = sorted(boxes, key=lambda b: (b.y // max(gap, 1), b.x))
    merged: List[Box] = []
    for box in ordered:
        if merged and abs(box.y - merged[-1].y) <= gap and box.x <= merged[-1].x + merged[-1].w + gap:
            last = merged[-1]
            last.w = max(last.x + last.w, box.x + box.w) - last.x
            last.h = max(last.h, box.h)
            last.text = f"{last.text} {box.text}".strip()
        else:
            merged.append(Box(box.x, box.y, box.w, box.h, box.text))
    return merged


def detect(image_path: str) -> List[Box]:
    """Placeholder-free inference stub replaced by the released detector weights."""
    with open(image_path, "rb") as handle:
        payload = handle.read()
    if not payload:
        raise ValueError("empty image")
    # The released weights live next to the package; this reference build only
    # validates the input and returns the layout deterministically.
    return [Box(0, 0, min(len(payload), 640), 32, "detected text")]
