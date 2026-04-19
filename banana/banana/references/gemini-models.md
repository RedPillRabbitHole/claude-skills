# Gemini Image Generation Models Reference

> Load this on-demand before every generation to select the correct model and parameters.
> Last updated: March 2026

## Active Models

### Nano Banana 2 — `gemini-3.1-flash-image-preview` (DEFAULT)
- **Status:** Preview
- **Max resolution:** 4096×4096 (4K)
- **Aspect ratios:** All 14 ratios including extreme formats (1:4, 4:1, 1:8, 8:1, 21:9)
- **Features:** Google Search grounding, thinking levels, image-only output mode
- **Free tier:** ~5-15 RPM, significantly reduced quotas (post December 2025 cuts)
- **Use for:** Default — most production use cases

### Nano Banana Original — `gemini-2.5-flash-image` (BUDGET FALLBACK)
- **Status:** General availability
- **Max resolution:** 1024×1024 (1K)
- **Aspect ratios:** 10 standard ratios (excludes extreme: 1:4, 4:1, 1:8, 8:1)
- **Cost:** ~$0.039/image at 1K resolution
- **Use for:** Budget-conscious, free-tier users, quick drafts

### Nano Banana Pro — `gemini-3-pro-image-preview` (DEPRECATED)
- **Status:** SHUT DOWN March 9, 2026
- **Action:** Migrate all usage to `gemini-3.1-flash-image-preview`

## Aspect Ratio Support

| Ratio | Nano Banana 2 | Nano Banana Original | Use Case |
|-------|:---:|:---:|---------|
| `1:1` | ✓ | ✓ | Social posts, avatars |
| `16:9` | ✓ | ✓ | YouTube, blog headers |
| `9:16` | ✓ | ✓ | Stories, Reels, mobile |
| `4:3` | ✓ | ✓ | Classic display, product |
| `3:4` | ✓ | ✓ | Portrait, book covers |
| `2:3` | ✓ | ✓ | Pinterest, posters |
| `3:2` | ✓ | ✓ | DSLR print standard |
| `4:5` | ✓ | ✓ | Instagram portrait |
| `5:4` | ✓ | ✓ | Large format fine art |
| `21:9` | ✓ | ✗ | Cinematic ultrawide |
| `1:4` | ✓ | ✗ | Tall strip banner |
| `4:1` | ✓ | ✗ | Wide strip banner |
| `1:8` | ✓ | ✗ | Extreme tall |
| `8:1` | ✓ | ✗ | Extreme wide banner |

## Resolution Tiers (`imageSize` parameter — MUST BE UPPERCASE)

| `imageSize` | Pixels | Cost (3.1 Flash) | When to use |
|-------------|--------|-----------------|-------------|
| `512` | 512×512 | ~$0.020 | Quick drafts, rapid iteration |
| `1K` | 1024×1024 | ~$0.039 | Web thumbnails, social media |
| `2K` | 2048×2048 | ~$0.078 | **Default** — quality assets |
| `4K` | 4096×4096 | ~$0.156 | Print production, hero images |

> **CRITICAL:** `imageSize` values are case-sensitive. Lowercase values fail silently. Always use uppercase: `512`, `1K`, `2K`, `4K`.

## API Parameters

| Parameter | Values | Notes |
|-----------|--------|-------|
| `aspectRatio` | See table above | Set via `set_aspect_ratio` MCP tool |
| `imageSize` | `512`, `1K`, `2K`, `4K` | UPPERCASE required |
| `responseModalities` | `["TEXT", "IMAGE"]` or `["IMAGE"]` | Use IMAGE-only to suppress text |
| `thinkingConfig.thinkingLevel` | `minimal`, `low`, `medium`, `high` | Increases quality and latency |
| `googleSearch` | tool object | Enables Search grounding |

## Rate Limits

| Tier | RPM | RPD | Notes |
|------|-----|-----|-------|
| Free | ~5-15 | ~20-500 | Resets midnight Pacific |
| Tier 1 (billing enabled) | 150-300 | 1,500-10,000 | Standard paid |
| Tier 2+ | 1,000+ | Unlimited | Enterprise |

## Pricing Table

| Model | Resolution | Cost/Image |
|-------|-----------|-----------|
| gemini-3.1-flash-image-preview | 512 | ~$0.020 |
| gemini-3.1-flash-image-preview | 1K | ~$0.039 |
| gemini-3.1-flash-image-preview | 2K | ~$0.078 |
| gemini-3.1-flash-image-preview | 4K | ~$0.156 |
| gemini-2.5-flash-image | 512 | ~$0.020 |
| gemini-2.5-flash-image | 1K | ~$0.039 |
| Batch API | Any | 50% discount |

> Pricing approximate (~1,290 output tokens/image). Verify at https://ai.google.dev/gemini-api/docs/pricing

## Domain Routing Table

| Scenario | Model | Resolution | Thinking | Brief Level |
|----------|-------|-----------|----------|-------------|
| Quick draft | `gemini-2.5-flash-image` | 512 or 1K | minimal | 3-component |
| Standard | `gemini-3.1-flash-image-preview` | 2K | low | Full 5-component |
| Quality/hero | `gemini-3.1-flash-image-preview` | 2K or 4K | medium | 5-component + anchors |
| Text-heavy | `gemini-3.1-flash-image-preview` | 2K | high | 5-component |
| Cinema/landscape | `gemini-3.1-flash-image-preview` | 2K or 4K | high | 5-component |
| Batch/bulk | Either via Batch API | 1K | minimal | 5-component |

## Advanced Features

### Google Search Grounding
Integrates real-time web and image search into generation. Use for:
- Current events visualization
- Factual diagrams and infographics
- Product photography with real brand references
- Up to 14 reference images (10 object refs + 4 character refs)

### Thinking Levels
Controls computational depth before generation:
- `minimal` — Fastest, lowest quality for complex scenes
- `low` — Good for standard photorealistic prompts
- `medium` — Recommended for portraits, products, editorial
- `high` — Required for text rendering, logos, complex infographics

### Image-Only Output Mode
Suppress text response with `responseModalities: ["IMAGE"]`.
Use when you only need the image file path, not explanatory text.

## Output Specifications

- **Format:** PNG
- **Color space:** sRGB
- **Watermark:** Invisible SynthID watermark on all outputs
- **Metadata:** C2PA provenance metadata on paid tier
- **Text rendering:** Keep text under 25 characters for best results
- **Transparent backgrounds:** NOT supported natively — use green screen pipeline
- **Per-call limit:** One image per API call
- **No batch parameter:** Must loop for multiple images
- **Session context:** Resets between Claude Code conversations

## Safety Architecture

Two-layer filtering (input + output). `finishReason` codes:

| Code | Meaning | Action |
|------|---------|--------|
| `IMAGE_SAFETY` | Output blocked post-generation | Rephrase, retry (max 3, with user approval) |
| `PROHIBITED_CONTENT` | Topic blocked, non-retryable | Explain, suggest alternative concept |
| `SAFETY` | General safety block | Analyze prompt for triggers, rephrase |
| `RECITATION` | Copyright concern | Rephrase to avoid specific references |

> Filters are known to be overly cautious — benign prompts may be blocked. See `references/prompt-engineering.md` Safety Rephrase Strategies.
