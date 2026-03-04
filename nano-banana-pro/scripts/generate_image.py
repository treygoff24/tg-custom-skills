#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
#     "pillow>=10.0.0",
# ]
# ///
"""
Generate or edit images using Nano Banana 2 (Gemini 3.1 Flash Image) or Nano Banana Pro (Gemini 3 Pro Image).

Usage:
    uv run generate_image.py --prompt "description" --filename "out.png"
    uv run generate_image.py --prompt "edit" --filename "out.png" -i input.png
    uv run generate_image.py --prompt "combine" --filename "out.png" -i a.png -i b.png

Options:
    --resolution 512|1K|2K|4K   Output resolution (default: 1K; auto-detected from input)
    --aspect-ratio RATIO        Aspect ratio: 1:1, 3:4, 4:3, 9:16, 16:9, 4:1, 1:4, 8:1, 1:8
    --search-grounding          Enable Google Search grounding for factual accuracy
    --text-only                 Request TEXT only (no image) for draft/verify steps
    --use-pro                   Use Nano Banana Pro (gemini-3-pro-image-preview) instead of NB2
    --thinking LEVEL            Thinking level: minimal, high, dynamic (default: minimal)
"""

import argparse
import os
import sys
from pathlib import Path


ASPECT_RATIOS = ["1:1", "3:4", "4:3", "9:16", "16:9", "4:1", "1:4", "8:1", "1:8"]

MODEL_NB2 = "gemini-3.1-flash-image-preview"
MODEL_PRO = "gemini-3-pro-image-preview"


def get_api_key(provided_key: str | None) -> str | None:
    if provided_key:
        return provided_key
    return os.environ.get("GEMINI_API_KEY")


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Nano Banana 2 (Gemini 3.1 Flash Image)"
    )
    parser.add_argument(
        "--prompt", "-p", required=True,
        help="Image description or edit instructions"
    )
    parser.add_argument(
        "--filename", "-f", required=True,
        help="Output filename (e.g., 2026-02-07-sunset.png)"
    )
    parser.add_argument(
        "--input-image", "-i", action="append", dest="input_images", metavar="IMAGE",
        help="Input image(s) for editing/composition (up to 14). Repeat for multiple."
    )
    parser.add_argument(
        "--resolution", "-r", choices=["512", "1K", "2K", "4K"], default="1K",
        help="Output resolution (default: 1K; auto-detected from input images)"
    )
    parser.add_argument(
        "--aspect-ratio", "-a", choices=ASPECT_RATIOS, default=None,
        help="Aspect ratio: 1:1, 3:4, 4:3, 9:16, 16:9, 4:1, 1:4, 8:1, 1:8"
    )
    parser.add_argument(
        "--search-grounding", action="store_true",
        help="Enable Google Search grounding for factual/real-world accuracy"
    )
    parser.add_argument(
        "--text-only", action="store_true",
        help="Request TEXT response only (no image). Use for draft/verify text steps."
    )
    parser.add_argument(
        "--use-pro", action="store_true",
        help="Use Nano Banana Pro (gemini-3-pro-image-preview) instead of the default NB2 model"
    )
    parser.add_argument(
        "--thinking", choices=["minimal", "high", "dynamic"], default="minimal",
        help="Thinking level: minimal (fastest), high (best quality), dynamic (model decides)"
    )
    parser.add_argument(
        "--api-key", "-k",
        help="Gemini API key (overrides GEMINI_API_KEY env var)"
    )

    args = parser.parse_args()

    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: No API key. Set GEMINI_API_KEY or pass --api-key.", file=sys.stderr)
        sys.exit(1)

    from google import genai
    from google.genai import types
    from PIL import Image as PILImage

    client = genai.Client(api_key=api_key)

    # Select model
    model_id = MODEL_PRO if args.use_pro else MODEL_NB2
    model_label = "Nano Banana Pro" if args.use_pro else "Nano Banana 2"
    print(f"Model: {model_label} ({model_id})")

    if args.thinking != "minimal":
        print(f"Thinking: {args.thinking}")

    output_path = Path(args.filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Load input images
    input_images = []
    output_resolution = args.resolution
    if args.input_images:
        if len(args.input_images) > 14:
            print(f"Error: Too many input images ({len(args.input_images)}). Max is 14.", file=sys.stderr)
            sys.exit(1)

        max_input_dim = 0
        for img_path in args.input_images:
            try:
                img = PILImage.open(img_path)
                input_images.append(img)
                print(f"Loaded: {img_path}")
                width, height = img.size
                max_input_dim = max(max_input_dim, width, height)
            except Exception as e:
                print(f"Error loading '{img_path}': {e}", file=sys.stderr)
                sys.exit(1)

        # Auto-detect resolution from input if user didn't explicitly set it
        if args.resolution == "1K" and max_input_dim > 0:
            if max_input_dim >= 3000:
                output_resolution = "4K"
            elif max_input_dim >= 1500:
                output_resolution = "2K"
            elif max_input_dim < 600:
                output_resolution = "512"
            else:
                output_resolution = "1K"
            print(f"Auto-detected resolution: {output_resolution} (max input dim: {max_input_dim})")

    # Build contents
    if input_images:
        contents = [*input_images, args.prompt]
        print(f"Processing {len(input_images)} image(s) @ {output_resolution}...")
    else:
        contents = args.prompt
        print(f"Generating @ {output_resolution}...")

    # Build response modalities
    if args.text_only:
        response_modalities = ["TEXT"]
    else:
        response_modalities = ["TEXT", "IMAGE"]

    # Build image config
    image_config_kwargs = {"image_size": output_resolution}
    if args.aspect_ratio:
        image_config_kwargs["aspect_ratio"] = args.aspect_ratio
        print(f"Aspect ratio: {args.aspect_ratio}")

    # Build tools
    tools = []
    if args.search_grounding:
        tools.append(types.Tool(google_search=types.GoogleSearch()))
        print("Search grounding: enabled")

    config_kwargs = {
        "response_modalities": response_modalities,
        "image_config": types.ImageConfig(**image_config_kwargs),
    }
    if tools:
        config_kwargs["tools"] = tools

    # Add thinking config if not minimal
    if args.thinking != "minimal":
        thinking_mode_map = {
            "high": "HIGH",
            "dynamic": "DYNAMIC",
        }
        thinking_mode_str = thinking_mode_map.get(args.thinking, args.thinking.upper())
        # Try SDK types first, fall back to raw dict
        try:
            thinking_mode_val = getattr(types.ThinkingMode, thinking_mode_str, None)
            if thinking_mode_val is not None:
                config_kwargs["thinking_config"] = types.ThinkingConfig(thinking_mode=thinking_mode_val)
            else:
                config_kwargs["thinking_config"] = {"thinking_mode": args.thinking}
        except AttributeError:
            config_kwargs["thinking_config"] = {"thinking_mode": args.thinking}

    try:
        response = client.models.generate_content(
            model=model_id,
            contents=contents,
            config=types.GenerateContentConfig(**config_kwargs),
        )

        image_saved = False
        for part in response.parts:
            if part.text is not None:
                print(f"Model: {part.text}")
            elif part.inline_data is not None:
                from io import BytesIO

                image_data = part.inline_data.data
                if isinstance(image_data, str):
                    import base64
                    image_data = base64.b64decode(image_data)

                image = PILImage.open(BytesIO(image_data))

                if image.mode == 'RGBA':
                    rgb_image = PILImage.new('RGB', image.size, (255, 255, 255))
                    rgb_image.paste(image, mask=image.split()[3])
                    rgb_image.save(str(output_path), 'PNG')
                elif image.mode == 'RGB':
                    image.save(str(output_path), 'PNG')
                else:
                    image.convert('RGB').save(str(output_path), 'PNG')
                image_saved = True

        if args.text_only:
            print("\nText-only mode: no image output expected.")
        elif image_saved:
            full_path = output_path.resolve()
            print(f"\nImage saved: {full_path}")
            print(f"MEDIA: {full_path}")
        else:
            print("Error: No image in response.", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
