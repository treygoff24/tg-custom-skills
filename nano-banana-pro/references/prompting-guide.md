# Nano Banana 2 — Prompting Reference

Read this when crafting complex prompts, using reference images, or rendering text.

## Prompt Anatomy (10-field schema)

Build prompts by filling these fields in order. Skip fields that don't apply.

1. **Task & deliverable** — Generate vs edit; what "done" looks like (hero image, icon set, product shot, poster).
2. **Subject** — Focal subject with identity/brand constraints and required attributes.
3. **Scene context** — Environment, time of day, era, narrative context.
4. **Composition** — Shot type, camera position, framing, negative space, foreground/background layering.
5. **Camera & optics** (photorealistic only) — Lens, focal length, DOF, motion blur, film stock. E.g. "shot on 35mm film, f/1.4 shallow depth of field, slight motion blur."
6. **Lighting & mood** — Softbox, golden hour, dramatic rim light, neon glow, etc.
7. **Style & rendering** — Photorealistic, vector, 3D tactile icon, oil painting, storyboard sketch, watercolor, etc.
8. **Typography** (if any) — Exact text in quotes, language, font style described, placement, contrast, "no other text."
9. **Constraints** — Semantic negatives, "preserve everything else," "no watermark other than SynthID," "no extra logos."
10. **Output spec** — Aspect ratio + resolution set via CLI flags; optionally restate in prompt for emphasis.

## Templates

### Photorealistic scene

> A photorealistic [shot type] of [subject], [action or expression], set in [environment]. The scene is illuminated by [lighting description], creating a [mood] atmosphere. Captured with a [camera/lens details], emphasizing [key textures and details]. The image should be in a [aspect ratio] format.

### Typography / text-heavy asset

> A [style] [asset type] featuring the text "[EXACT TEXT]" in [font style description]. The text is [placement: centered/top/bottom] against a [background description]. [Additional design elements]. The overall feel is [mood/brand tone].

Use the two-stage text workflow (see below) for multi-line or spelling-critical text.

### Product / marketing shot

> A [style] product photograph of [product description] on [surface/background]. [Lighting setup]. The composition emphasizes [key feature]. Shot from [angle] with [lens details]. [Brand elements if any].

### Illustration / stylized

> A [art style] illustration of [subject] in [scene]. [Color palette description]. [Composition details]. The style evokes [reference artist/movement/era].

### Multi-image composition

> Using the provided reference images: [image 1] as [role], [image 2] as [role], [image 3] as [role]. Create a [deliverable] that [instruction]. Maintain [consistency requirements].

## Reference Image Protocol

NB2 supports up to 14 reference images (5 high-fidelity, 9 lower-fidelity guidance).

### Labeling roles in the prompt

Always state each image's role explicitly:

- **Subject identity**: "Use image 1 as the character reference — maintain face, hair, and build exactly."
- **Product/object**: "Image 2 is the product; preserve its shape, color, and branding."
- **Style/mood**: "Match the color palette and lighting style of image 3."
- **Layout/composition**: "Use image 4's framing and negative space arrangement."
- **Brand assets**: "Image 5 contains the logo; place it in the upper-left corner."

### Ordering

Put the most important references first (images 1–5 get high-fidelity treatment).

## Two-Stage Text Rendering Workflow

For posters, menus, diagrams, ads, or any multi-line typography:

**Stage 1 — Draft & verify text (use `--text-only`):**
> "I need a restaurant menu with these items: [list]. Format the text with headers for each section, prices right-aligned. Check spelling and layout."

**Stage 2 — Render with verified text:**
> "Create a [style] restaurant menu image using exactly this text: [paste verified text from stage 1]. Use [font style], [color scheme], [layout]. No additional text or modifications to the provided copy."

## Text Translation Workflow

Use NB2 to localize in-image text to another language while preserving all visual elements.

**Basic translation (supply source image with `-i`):**
> "Translate all text in this image from English to Spanish. Preserve the layout, font styles, colors, background, and all non-text visual elements exactly. Replace only the text with its natural Spanish equivalent — do not alter the design."

**Verify-then-render approach (recommended for multi-line assets):**

Stage 1 (`--text-only`): "Here is an image of a menu. Extract all the text and translate it into French, preserving the section structure and formatting. Return the translated text only."

Stage 2: "Re-render this image replacing all text with exactly the following French translation: [paste from stage 1]. Keep all visual design elements unchanged."

**Producing multi-language variants:**
> "Generate three versions of this poster image: one with the text in English (as-is), one in German, one in Japanese. Each version must be visually identical except for the text."

## Semantic Negatives

Instead of "no X" lists, describe the desired world:

| ❌ Brittle | ✅ Semantic |
|---|---|
| "no people" | "an empty, deserted scene with no signs of human presence" |
| "no text, no watermark" | "a clean image with only the visual subject, free of overlaid text or marks" |
| "no blur" | "tack-sharp focus throughout the entire frame" |
| "don't make it dark" | "bright, evenly lit with high-key lighting" |

## Iteration Patterns

### Small targeted edits (preferred)

> "Keep everything the same, but [specific change]."

Examples:
- "Keep everything the same, but warm the lighting and reduce background clutter."
- "Preserve the character from the references; only change the outfit to navy."
- "Same composition, but shift to a 16:9 crop with more negative space on the right."

### When to re-anchor (drift after many edits)

If features drift after 3+ iterative edits:
1. Start a fresh generation (don't continue the conversation).
2. Re-supply reference images.
3. Restate the full canonical description.

## Thinking-Aware Prompting

When using `--thinking high`, the model reasons before rendering. This unlocks more complex, layered prompts that would produce inconsistent results otherwise.

**With minimal thinking:** Keep prompts tight and concrete. One or two focal instructions. Complex multi-constraint prompts may get partially ignored.

**With high thinking:** You can write numbered constraint lists and the model will reason through them systematically before generating:

> "Generate a product advertisement with the following requirements:
> 1. The product (image 1) must appear in the center-right third, fully visible, no cropping.
> 2. The background should feel warm and domestic — soft-focus kitchen, afternoon light.
> 3. The headline 'Start fresh.' appears top-left in a clean sans-serif, white, 48pt weight.
> 4. A small legal disclaimer line appears bottom-center at 50% opacity.
> 5. No other text. No shadows on the product. The product casts no reflection."

At `--thinking high`, the model works through each constraint before composing the scene, producing significantly better instruction adherence.

**With dynamic thinking:** Good when you're unsure how complex a prompt is. The model allocates reasoning budget as needed — you get near-minimal speed for simple prompts and near-high quality for complex ones.

## Resolution & Aspect Ratio Heuristics

| Use case | Resolution | Aspect ratio |
|---|---|---|
| Rapid concept draft | 512 | any |
| Quick draft / iteration | 1K | any |
| Social media post | 2K | 1:1 or 4:3 |
| Story / reel / portrait | 2K | 9:16 |
| Banner / hero image | 2K | 16:9 |
| Print / tight typography | 4K | match print spec |
| Widescreen cinematic | 4K | 16:9 |
| Ultrawide banner / filmstrip | 2K–4K | 4:1 or 8:1 |
| Tall scrolling / billboard | 2K–4K | 1:4 or 1:8 |

### Extreme aspect ratios

| Ratio | Pixel shape | Best for |
|---|---|---|
| `4:1` | Very wide | Website hero banners, email headers, panoramic landscapes |
| `1:4` | Very tall | Mobile splash screens, vertical scroll ads, tall infographics |
| `8:1` | Ultra-wide strip | Filmstrip contact sheets, timeline visualizations, cinematic letterbox |
| `1:8` | Ultra-tall column | Vertical billboards, scrolling phone wallpapers, sequential story panels |

Note: Extreme ratios work best at 2K or 4K resolution so the narrow dimension still has enough pixels to look sharp.

## Search Grounding

Enable `--search-grounding` when the image requires:
- Real-world accuracy (maps, landmarks, current events)
- Specific product appearances
- Real-time data visualization
- Factual claims embedded in the image

When grounding is on, instruct the model to validate facts before rendering.
