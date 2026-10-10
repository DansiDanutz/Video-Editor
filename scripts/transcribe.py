"""Transcribe one clip with WhisperX and write word-level timings to transcript/words.json.

Run with the project venv:
  ~/.cache/video-editor/whisperx-venv/bin/python scripts/transcribe.py raw/<clip> [--model large-v3-turbo]
"""
import argparse
import json
import sys
from pathlib import Path

import whisperx

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = REPO_ROOT / "transcript" / "words.json"
DEFAULT_MODEL = "large-v3-turbo"
BATCH_SIZE = 8
# ctranslate2 has no Metal backend; int8 on CPU is the fast option on Apple Silicon.
DEVICE = "cpu"
COMPUTE_TYPE = "int8"


def transcribe(clip: Path, model_name: str, language: str | None) -> dict:
    audio = whisperx.load_audio(str(clip))
    model = whisperx.load_model(model_name, DEVICE, compute_type=COMPUTE_TYPE, language=language)
    result = model.transcribe(audio, batch_size=BATCH_SIZE)
    align_model, metadata = whisperx.load_align_model(language_code=result["language"], device=DEVICE)
    aligned = whisperx.align(result["segments"], align_model, metadata, audio, DEVICE, return_char_alignments=False)
    words = [
        {"word": w["word"], "start": w.get("start"), "end": w.get("end"), "score": w.get("score")}
        for seg in aligned["segments"]
        for w in seg.get("words", [])
    ]
    segments = [{"start": s["start"], "end": s["end"], "text": s["text"].strip()} for s in aligned["segments"]]
    return {"source": str(clip.relative_to(REPO_ROOT)), "model": model_name, "language": result["language"],
            "segments": segments, "words": words}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("clip", type=Path)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--language", default=None, help="e.g. en, ro; auto-detected when omitted")
    args = parser.parse_args()

    clip = args.clip.resolve()
    if not clip.is_file():
        print(f"clip not found: {args.clip}", file=sys.stderr)
        return 1

    data = transcribe(clip, args.model, args.language)
    OUTPUT_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"{len(data['words'])} words, {len(data['segments'])} segments, language={data['language']} -> {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
