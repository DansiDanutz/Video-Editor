"""Draft transcript/cuts.json from transcript/words.json by tightening long pauses.

Every pause between words longer than MAX_PAUSE is shortened to KEEP_PAUSE (split evenly
around the gap). Leading/trailing non-speech is kept unless --trim-ends is given.
The output is a draft for approval; nothing is rendered.

  python3 scripts/draft_cuts.py --fps 30 --duration 119 [--trim-ends]
"""
import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WORDS_PATH = REPO_ROOT / "transcript" / "words.json"
CUTS_PATH = REPO_ROOT / "transcript" / "cuts.json"
MAX_PAUSE = 0.6  # seconds; pauses longer than this get tightened
KEEP_PAUSE = 0.35  # seconds of pause left after tightening
END_PAD = 0.25  # seconds kept before the first / after the last word with --trim-ends


def to_frame(seconds: float, fps: int) -> int:
    return round(seconds * fps)


def find_removals(words: list[dict], fps: int) -> list[dict]:
    timed = [w for w in words if w.get("start") is not None and w.get("end") is not None]
    removals = []
    for before, after in zip(timed, timed[1:]):
        gap = after["start"] - before["end"]
        if gap <= MAX_PAUSE:
            continue
        half = KEEP_PAUSE / 2
        start, end = to_frame(before["end"] + half, fps), to_frame(after["start"] - half, fps)
        if end > start:
            removals.append({"start_frame": start, "end_frame": end, "type": "pause",
                             "reason": f"{gap:.2f}s pause after '{before['word']}' tightened to {KEEP_PAUSE}s"})
    return removals


def end_removals(words: list[dict], fps: int, total_frames: int) -> list[dict]:
    timed = [w for w in words if w.get("start") is not None]
    head_end = to_frame(max(0.0, timed[0]["start"] - END_PAD), fps)
    tail_start = to_frame(timed[-1]["end"] + END_PAD, fps)
    cuts = []
    if head_end > 0:
        cuts.append({"start_frame": 0, "end_frame": head_end, "type": "intro", "reason": "no speech before first word"})
    if tail_start < total_frames:
        cuts.append({"start_frame": tail_start, "end_frame": total_frames, "type": "outro", "reason": "no speech after last word"})
    return cuts


def keep_ranges(removals: list[dict], total_frames: int) -> list[dict]:
    keeps, cursor = [], 0
    for cut in sorted(removals, key=lambda c: c["start_frame"]):
        if cut["start_frame"] > cursor:
            keeps.append({"start_frame": cursor, "end_frame": cut["start_frame"]})
        cursor = max(cursor, cut["end_frame"])
    if cursor < total_frames:
        keeps.append({"start_frame": cursor, "end_frame": total_frames})
    return keeps


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--fps", type=int, required=True)
    parser.add_argument("--duration", type=float, required=True, help="source duration in seconds")
    parser.add_argument("--trim-ends", action="store_true")
    args = parser.parse_args()

    data = json.loads(WORDS_PATH.read_text())
    total = to_frame(args.duration, args.fps)
    removals = find_removals(data["words"], args.fps)
    if args.trim_ends:
        removals = removals + end_removals(data["words"], args.fps, total)
    keeps = keep_ranges(removals, total)
    kept = sum(k["end_frame"] - k["start_frame"] for k in keeps)
    cuts = {
        "status": "draft",
        "source": data["source"],
        "fps": args.fps,
        "source_frames": total,
        "output_frames": kept,
        "removed_seconds": round((total - kept) / args.fps, 2),
        "removals": sorted(removals, key=lambda c: c["start_frame"]),
        "keep": [{**k, "start_s": round(k["start_frame"] / args.fps, 3), "end_s": round(k["end_frame"] / args.fps, 3)}
                 for k in keeps],
    }
    CUTS_PATH.write_text(json.dumps(cuts, indent=2) + "\n")
    print(f"{len(removals)} removals, {len(keeps)} keep ranges, {total}->{kept} frames "
          f"({cuts['removed_seconds']}s removed) -> {CUTS_PATH}")


if __name__ == "__main__":
    main()
