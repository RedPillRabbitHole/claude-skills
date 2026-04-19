# MCP Tools Reference — @ycse/nanobanana-mcp

> Load this on-demand when calling MCP tools or troubleshooting MCP issues.

## Package Info
- **Package:** `@ycse/nanobanana-mcp`
- **Command:** `npx @ycse/nanobanana-mcp`
- **Output directory:** `~/Documents/nanobanana_generated/`
- **Required env:** `GOOGLE_AI_API_KEY`
- **Optional env:** `NANOBANANA_MODEL` (overrides default model)

## Core Tools

### `gemini_generate_image`
Creates a new image from a text prompt.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | Yes | The image generation prompt |

**Returns:** Image saved to `~/Documents/nanobanana_generated/`, file path in response.

**Notes:**
- Always call `set_aspect_ratio` first if ratio differs from 1:1
- Uses currently configured model and aspect ratio
- One image per call

---

### `gemini_edit_image`
Modifies an existing image using text instructions.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `image` | string | Yes | Absolute path to the source image file |
| `prompt` | string | Yes | Editing instructions |

**Returns:** Edited image saved to output directory with timestamped filename.

**Supported input formats:** `.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`

---

### `gemini_chat`
Multi-turn visual conversation that maintains session context.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | Yes | Message or image refinement instruction |

**Notes:**
- Maintains character consistency, style, and context across turns
- Use for: character design sheets, sequential storytelling, iterative refinement
- Context resets between Claude Code sessions

---

### `set_aspect_ratio`
Configures output dimensions for subsequent generations.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `ratio` | string | Yes | Aspect ratio (e.g., `"16:9"`, `"1:1"`, `"9:16"`) |

**Supported ratios:** `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `2:3`, `3:2`, `4:5`, `5:4`, `21:9`, `1:4`, `4:1`, `1:8`, `8:1`

**Note:** `21:9`, `1:4`, `4:1`, `1:8`, `8:1` require Nano Banana 2 model.

---

### `set_model`
Switches between available Gemini models.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | Yes | Model ID to use |

**Valid values:**
- `gemini-3.1-flash-image-preview` (default, Nano Banana 2)
- `gemini-2.5-flash-image` (Nano Banana Original, budget)

---

### `get_image_history`
Retrieves generated images from the current session.

**Parameters:** None

**Returns:** List of images with file paths and associated prompts from current session.

---

### `clear_conversation`
Resets session context and conversation history.

**Parameters:** None

**Use when:** Starting a new creative direction, clearing character consistency constraints, or troubleshooting context drift.

## ImageConfig Parameters

Parameters that work with the MCP:

| Parameter | Type | Notes |
|-----------|------|-------|
| `aspect_ratio` | string | Set via `set_aspect_ratio` tool |
| `image_size` | string | UPPERCASE: `512`, `1K`, `2K`, `4K` |
| `person_generation` | string | Safety level for people |

**Parameters that do NOT work (from other systems):**
- `seed` — Not supported
- `negativePrompt` — Not supported
- `numberOfImages` — Not supported (one image per call)
- `cfg_scale` — Not supported
- `steps` — Not supported

## Workflow Sequence

```
1. set_aspect_ratio (if not 1:1)
2. set_model (if not using default)
3. gemini_generate_image OR gemini_edit_image OR gemini_chat
4. Check response for errors
5. Save path, log cost
```

## Error Taxonomy

| Error | HTTP Code | Cause | Solution |
|-------|-----------|-------|---------|
| Rate limited | 429 | Too many requests | Wait 60s, retry with exponential backoff |
| Billing error | 400 FAILED_PRECONDITION | Billing not configured | Enable billing at console.cloud.google.com |
| Invalid API key | 401 | Wrong or expired key | Get new key at aistudio.google.com/apikey |
| IMAGE_SAFETY | 200 (blocked finish) | Content policy | Rephrase prompt, retry with user approval |
| PROHIBITED_CONTENT | 200 (blocked finish) | Non-retryable block | Explain to user, suggest alternatives |
| Empty response | 200 (no image parts) | responseModalities issue | Verify IMAGE is in responseModalities, retry once |
| MCP not found | — | Package not installed | Run `/banana setup` |

## Feature Availability by Package Version

Some newer Gemini features may not be available in all MCP package versions:

| Feature | Availability |
|---------|-------------|
| Basic generate/edit | All versions |
| Aspect ratio control | All versions |
| Model switching | All versions |
| `imageSize` (resolution) | Newer versions |
| Thinking levels | Newer versions |
| Search grounding | Newer versions |

If a feature is unavailable via MCP, fall back to direct API scripts:
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/generate.py --prompt "..." --aspect-ratio "16:9" --resolution "2K"
python3 ${CLAUDE_SKILL_DIR}/scripts/edit.py --image /path/to/image.png --prompt "..."
```
