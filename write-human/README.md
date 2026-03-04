# Write Human ✍️

An anti-AI-slop writing directive for AI agents. Load it before writing anything and the agent avoids the telltale patterns that make AI-generated text obvious: inflated significance, synonym cycling, stacked single-sentence paragraphs, the "AI essay skeleton," and 28 more specific patterns.

Based on Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) guide (WikiProject AI Cleanup), plus a framework for "semantic turbulence" — the meta-pattern behind most AI writing tells.

## What it does

1. **Prevents slop at the source.** Rather than generating AI-typical text and cleaning it up, this directive teaches the agent not to produce it in the first place.
2. **31 specific antipatterns** with concrete examples and fixes.
3. **Voice and craft guidance:** semantic turbulence, single purpose, truth over ornament, tone calibration by document type.
4. **Post-hoc audit process** for cleaning up existing AI-generated text.

## What it covers

- Content patterns (inflated significance, notability hammering, promotional language)
- Language patterns (AI vocabulary, copula avoidance, negative parallelisms, synonym cycling)
- Style patterns (em dash overuse, boldface overuse, emoji decoration)
- Communication artifacts (chatbot residue, sycophancy, knowledge-cutoff disclaimers)
- Structural tells (punchy fragment combos, bolded lead-ins)
- Macro-structural templates (the AI essay skeleton, stacked single-sentence paragraphs)
- Filler and hedging patterns

## Usage

Paste the contents of [`AGENTS.md`](./AGENTS.md) into your agent's system prompt, instructions file, or rules. It works with any AI agent or harness.

### Quick start

**Claude Code:**
```bash
cat write-human/AGENTS.md >> CLAUDE.md
```

**Cursor:**
```bash
cat write-human/AGENTS.md >> .cursor/rules
```

**OpenAI Codex CLI:** Add as custom agent instructions.

**OpenClaw:** Copy to skills directory:
```bash
cp -r write-human ~/.openclaw/skills/
```

## The test

Read your agent's output aloud. If it sounds like a press release, a Wikipedia article, or a LinkedIn post, and nobody asked for one, the agent needs this skill.
