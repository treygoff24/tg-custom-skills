# Nano Banana Pro 🍌

Image generation and editing powered by Google's Gemini image models. Two models available:

- **Nano Banana 2** (default) — `gemini-3.1-flash-image-preview` — Fast, cheap, great quality on most tasks
- **Nano Banana Pro** — `gemini-3-pro-image-preview` — Higher fidelity for specialized use cases

## Setup

**Requirements:**
- [uv](https://docs.astral.sh/uv/) (Python package runner)
- A [Google AI Studio](https://aistudio.google.com/) API key

**Install uv:**
```bash
# macOS
brew install uv

# Linux/Windows
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Set your API key:**
```bash
export GEMINI_API_KEY="your-key-here"
```

That's it. No virtual environments, no `pip install`. `uv` handles dependencies automatically on first run.

## Usage

### Generate an image
```bash
uv run scripts/generate_image.py -p "A golden retriever in a field of sunflowers at sunset" -f output.png
```

### Edit an existing image
```bash
uv run scripts/generate_image.py -p "Make the sky purple" -f edited.png -i original.png
```

### Combine multiple images
```bash
uv run scripts/generate_image.py -p "Combine these into a collage" -f collage.png -i img1.png -i img2.png -i img3.png
```

### Higher resolution
```bash
uv run scripts/generate_image.py -p "A detailed cityscape" -f city.png -r 4K -a 16:9
```

### Use Pro model
```bash
uv run scripts/generate_image.py -p "A detailed infographic" -f infographic.png --use-pro
```

### Enable thinking for complex scenes
```bash
uv run scripts/generate_image.py -p "A complex multi-element scene with specific layout requirements" -f scene.png --thinking high
```

### Text-only mode (draft text before rendering)
```bash
uv run scripts/generate_image.py -p "Draft a restaurant menu with 3 sections" -f unused.png --text-only
```

## CLI Reference

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `-p`, `--prompt` | text | *required* | Image description or edit instructions |
| `-f`, `--filename` | path | *required* | Output filename |
| `-i`, `--input-image` | path(s) | none | Input image(s) for editing (up to 14, repeat flag) |
| `-r`, `--resolution` | `512`, `1K`, `2K`, `4K` | `1K` | Output resolution (auto-detected from input) |
| `-a`, `--aspect-ratio` | `1:1`, `3:4`, `4:3`, `9:16`, `16:9`, `4:1`, `1:4`, `8:1`, `1:8` | none | Aspect ratio |
| `--search-grounding` | flag | off | Enable Google Search for factual accuracy |
| `--text-only` | flag | off | Text response only (no image) |
| `--use-pro` | flag | off | Use Nano Banana Pro model |
| `--thinking` | `minimal`, `high`, `dynamic` | `minimal` | Reasoning depth |
| `-k`, `--api-key` | key | env var | Override GEMINI_API_KEY |

## Use with AI Agents

See [`AGENTS.md`](./AGENTS.md) for instructions you can paste into any AI agent's context. See [`references/prompting-guide.md`](./references/prompting-guide.md) for the full prompting reference.

## Notes

- Outputs are watermarked with Google's SynthID
- Resolution auto-detects from input images when editing
- The script prints a `MEDIA:` line with the output path for easy integration with agent harnesses
