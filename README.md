# tg-custom-skills

A collection of standalone AI agent skills. Each skill is a self-contained directory with instructions, scripts, and references that work with any agent harness — or no harness at all.

## Available Skills

| Skill | Description |
|-------|-------------|
| [nano-banana-pro](./nano-banana-pro/) | Image generation and editing via Google's Gemini image models |

## How to Use

Each skill directory contains:

- **`README.md`** — Human-readable docs: what it does, how to install, how to use
- **`AGENTS.md`** — Agent-facing instructions: paste into your agent's context, point a custom agent at it, or wire it into your harness config
- **`scripts/`** — Standalone scripts that do the actual work
- **`references/`** — Supplementary guides and references

### With any agent

Copy the contents of `AGENTS.md` into your agent's system prompt or instructions file. The agent will know how to call the scripts and follow the workflows.

### Quick start examples

**OpenAI Codex CLI** — Add as a custom agent:
```bash
# In your Codex agents config, point to the AGENTS.md as instructions
```

**Claude Code** — Drop into your project's `CLAUDE.md`:
```bash
cat nano-banana-pro/AGENTS.md >> CLAUDE.md
```

**Cursor** — Add to `.cursor/rules`:
```bash
cat nano-banana-pro/AGENTS.md >> .cursor/rules
```

**OpenClaw** — Copy the skill directory into your skills folder:
```bash
cp -r nano-banana-pro ~/.openclaw/skills/
```

### Without any agent

Every script runs standalone. Check the skill's README for direct CLI usage.

## Contributing

Have a skill that works well with AI agents? PRs welcome. Each skill should:

1. Be fully self-contained in its own directory
2. Have a `README.md` for humans and an `AGENTS.md` for agents
3. Work without any specific harness dependency
4. Include clear install/setup instructions

## License

MIT
