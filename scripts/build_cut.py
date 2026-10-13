"""Build the approved cut from transcript/cuts.json with one ffmpeg filtergraph.

Each keep range becomes its own trim/atrim pair, then all pairs are concatenated, so the
cut stays frame-accurate to cuts.json. Output goes to out/ (gitignored).

  python3 scripts/build_cut.py [--dry-run]
"""
import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CUTS_PATH = REPO_ROOT / "transcript" / "cuts.json"
OUT_DIR = REPO_ROOT / "out"
VIDEO_CODEC = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p"]
AUDIO_CODEC = ["-c:a", "aac", "-b:a", "192k"]


def filtergraph(keeps: list[dict], fps: int) -> str:
    parts, labels = [], []
    for i, k in enumerate(keeps):
        start_s, end_s = k["start_frame"] / fps, k["end_frame"] / fps
        parts.append(f"[0:v]trim=start_frame={k['start_frame']}:end_frame={k['end_frame']},setpts=PTS-STARTPTS[v{i}]")
        parts.append(f"[0:a]atrim=start={start_s:.6f}:end={end_s:.6f},asetpts=PTS-STARTPTS[a{i}]")
        labels.append(f"[v{i}][a{i}]")
    parts.append(f"{''.join(labels)}concat=n={len(keeps)}:v=1:a=1[outv][outa]")
    return ";".join(parts)


def build_command(cuts: dict) -> tuple[list[str], Path]:
    source = REPO_ROOT / cuts["source"]
    output = OUT_DIR / f"{source.stem}-cut.mp4"
    command = ["ffmpeg", "-hide_banner", "-y", "-i", str(source),
               "-filter_complex", filtergraph(cuts["keep"], cuts["fps"]),
               "-map", "[outv]", "-map", "[outa]", "-fps_mode", "passthrough",
               *VIDEO_CODEC, *AUDIO_CODEC, "-movflags", "+faststart", str(output)]
    return command, output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dry-run", action="store_true", help="print the ffmpeg command only")
    args = parser.parse_args()

    cuts = json.loads(CUTS_PATH.read_text())
    if cuts.get("status") != "approved":
        print(f"cuts.json status is '{cuts.get('status')}', not 'approved'; refusing to build", file=sys.stderr)
        return 1
    command, output = build_command(cuts)
    print(shlex.join(command))
    if args.dry_run:
        return 0
    OUT_DIR.mkdir(exist_ok=True)
    subprocess.run(command, check=True)
    print(f"built {output} (expect {cuts['output_frames']} frames)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
