# Nano Banana Pro — Agent Instructions

You have access to an image generation and editing tool called Nano Banana. It wraps Google's Gemini image models via a Python script.

Two models are available:
- **Nano Banana 2** (default) — `gemini-3.1-flash-image-preview` — 2× faster and cheaper, benchmarks better on most tasks
- **Nano Banana Pro** — `gemini-3-pro-image-preview` — higher fidelity for specialized cases (infographics, factual accuracy)

**Prefer NB2 by default.** Only use `--use-pro` when NB2 results are genuinely insufficient.

## Prerequisites

- `uv` must be installed (Python package runner)
- `GEMINI_API_KEY` environment variable must be set

## CLI

All commands assume you're in the `nano-banana-pro/` skill directory (adjust the script path as needed).

**Generate:**
```bash
uv run scripts/generate_image.py -p "prompt" -f "output.png" -r 2K -a 16:9
```

**Edit (single image):**
```bash
uv run scripts/generate_image.py -p "edit instructions" -f "output.png" -i input.png -r 2K
```

**Multi-image composition (up to 14 images):**
```bash
uv run scripts/generate_image.py -p "combine these" -f "output.png" -i img1.png -i img2.png -i img3.png
```

**Text-only (draft/verify text before rendering):**
```bash
uv run scripts/generate_image.py -p "draft menu text" -f "unused.png" --text-only
```

**With search grounding (factual accuracy):**
```bash
uv run scripts/generate_image.py -p "prompt" -f "output.png" --search-grounding
```

**With high thinking (complex compositions):**
```bash
uv run scripts/generate_image.py -p "prompt" -f "output.png" --thinking high
```

**Using Nano Banana Pro:**
```bash
uv run scripts/generate_image.py -p "prompt" -f "output.png" --use-pro
```

### Flags

| Flag | Values | Default | Notes |
|------|--------|---------|-------|
| `-p` | text | *required* | Prompt / instructions |
| `-f` | path | *required* | Output filename |
| `-i` | path(s) | none | Up to 14 reference/input images |
| `-r` | `512`, `1K`, `2K`, `4K` | `1K` | Auto-detected from input images |
| `-a` | `1:1`, `3:4`, `4:3`, `9:16`, `16:9`, `4:1`, `1:4`, `8:1`, `1:8` | none | Set based on destination |
| `--search-grounding` | flag | off | Enable for real-world accuracy |
| `--text-only` | flag | off | Text response only (no image) |
| `--use-pro` | flag | off | Switch to Nano Banana Pro model |
| `--thinking` | `minimal`, `high`, `dynamic` | `minimal` | Reasoning depth |

## Thinking Levels

- **`minimal`** (default): Fastest. Use for drafts, simple generations, high-volume work.
- **`high`**: Best quality. Use for complex compositions, precise instruction following, multi-element scenes, tight layout requirements.
- **`dynamic`**: Model decides how much to think. Good middle ground when complexity is uncertain.

## Core Prompting Principle

Write prompts as **narrative scene descriptions**, not keyword lists. The model reasons over language, so coherent sentences produce coherent images. If the user provides tags or keywords, rewrite them into a scene paragraph.

## Prompt Workflow

1. **Start simple, then layer.** Begin with subject + action + scene. Add composition, style, lighting, and output spec iteratively.
2. **Be hyper-specific.** Use concrete visual descriptors (materials, textures, shapes). Provide context and intent.
3. **Use semantic negatives.** Describe the desired world instead of listing exclusions. "An empty street with no signs of traffic" beats "no cars."
4. **Iterate with small deltas.** Prefer "Keep everything the same, but [change]" over regenerating from scratch.
5. **Two-stage text rendering.** For typography-heavy assets: first generate/verify the exact text with `--text-only`, then render it in a second pass.
6. **Label reference images.** When using multiple inputs, state each image's role: "Image 1 is the character reference; image 2 is the brand palette; match image 3's lighting."

## Choosing Resolution & Aspect Ratio

- **Rapid drafts**: 512
- **Drafts/iteration**: 1K
- **Social/web**: 2K + appropriate ratio (1:1 square, 16:9 banner, 9:16 story)
- **Print/typography**: 4K
- Always set aspect ratio based on where the image will be used

## Output

The script prints a `MEDIA:` line with the full output path. Do not read the image file back; just report the saved path to the user.

## Full Prompting Reference

For the complete prompt anatomy schema, templates, reference image protocol, text translation workflows, and iteration playbook, see `references/prompting-guide.md` in this skill directory.
