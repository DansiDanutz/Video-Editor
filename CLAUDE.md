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
