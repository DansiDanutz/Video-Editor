# Video-Editor

Video editing workspace (GitHub: DansiDanutz/Video-Editor). Machine-wide rules in `~/CLAUDE.md` and `~/.claude/rules/` still apply; this file adds only project rules.

## Claude setup in this repo
- `.claude/settings.json` — enabled plugins (official, community, `danslab-mods`) and project permissions.
- `.claude/skills/` — video skills: `video-editing`, `general-video`, `media-use`, `scene-division`, `product-launch-video`, `hyperframes*`. Personal skills with the same name take precedence, so these are a portable copy for cloud/other machines.
- `.claude/agents/` — reviewers: code, security, TypeScript, Python, planner, TDD guide.

## Working rules
- Paid media generation (Higgsfield, fal, etc.) only when David starts it. Reuse existing assets; prepare prompts for David to generate.
- Run `danslab-workflow check` before renders, installs or large downloads; the disk is tight.
- Keep raw footage, renders and large media out of Git (see `.gitignore`). Commit sources, timelines, scripts and docs.
- Check outputs with `ffprobe` (duration, streams, A/V sync) before calling a render done.
- Conventional commits (`feat:`, `fix:`, ...). No secrets in the repo; use `.env` (gitignored).

## Starter AI editor (from Jason Cooper's free Claude Video Editor blueprint)
Layout: `raw/` input clip, `transcript/` words.json + cuts.json, `scripts/` our scripts, `vendor/` cloned connectors (gitignored).
Flow: pick app -> connect -> WhisperX transcribe (venv `~/.cache/video-editor/whisperx-venv`, create once, never recreate; 3-5 GB, run `danslab-workflow check` first) -> write `transcript/cuts.json` -> user approves -> build cut as real trimmable clips (never one flat clip) -> verify frame counts vs cuts.json.
Premiere connector: clone hetpatel-11/Adobe_Premiere_Pro_MCP at v1.2.3 (12684e3) into `vendor/premiere-mcp`; never `npm install -g adobe-premiere-pro-mcp`. Resolve Studio 21.1+: File > Setup AI Assistants. Final Cut: FCPXML. CapCut/no app: single ffmpeg filtergraph, `-fps_mode passthrough`.
Not covered by the starter: audio polish, grade, graphics, SFX, music, locked-spec export.
Machine status (2026-10-10): ffmpeg, uv, git, Node 26, Python 3.11 present. Connector + WhisperX are installed by `scripts/setup-premiere-whisperx.sh` (David runs it; disk-floor blocks agents).
MCP: `premiere-pro` registered at local scope (`node vendor/premiere-mcp/dist/cli.js`, `PREMIERE_MCP_TELEMETRY=0`). The CEP bridge (`--install-cep`) is a separate step: it edits Adobe CEP debug settings and Claude Desktop config.
