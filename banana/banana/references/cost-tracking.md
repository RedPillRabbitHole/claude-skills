# Cost Tracking Reference

> Load this on-demand when the user asks about costs or before batch operations.

## Pricing Table

| Model | Resolution | Cost/Image | Notes |
|-------|-----------|-----------|-------|
| gemini-3.1-flash-image-preview | 512 | ~$0.020 | Quick drafts |
| gemini-3.1-flash-image-preview | 1K | ~$0.039 | Standard |
| gemini-3.1-flash-image-preview | 2K | ~$0.078 | Quality assets |
| gemini-3.1-flash-image-preview | 4K | ~$0.156 | Print/hero images |
| gemini-2.5-flash-image | 512 | ~$0.020 | Draft fallback |
| gemini-2.5-flash-image | 1K | ~$0.039 | Standard fallback |
| Batch API | Any | 50% of above | Asynchronous, higher latency |

Pricing is approximate, based on ~1,290 output tokens per image.
Research suggests actual costs may be ~$0.067/img at 1K. Verify at https://ai.google.dev/gemini-api/docs/pricing

## Free Tier Limits

- ~10 requests per minute (RPM)
- ~500 requests per day (RPD)
- Per Google Cloud project, resets midnight Pacific

## Cost Tracker Commands

```bash
# Log a generation
python3 ${CLAUDE_SKILL_DIR}/scripts/cost_tracker.py log \
  --model gemini-3.1-flash-image-preview \
  --resolution 1K \
  --prompt "coffee shop hero image"

# View summary (total + last 7 days)
python3 ${CLAUDE_SKILL_DIR}/scripts/cost_tracker.py summary

# Today's usage only
python3 ${CLAUDE_SKILL_DIR}/scripts/cost_tracker.py today

# Estimate before batch operation
python3 ${CLAUDE_SKILL_DIR}/scripts/cost_tracker.py estimate \
  --model gemini-3.1-flash-image-preview \
  --resolution 1K \
  --count 10

# Reset ledger (requires --confirm flag)
python3 ${CLAUDE_SKILL_DIR}/scripts/cost_tracker.py reset --confirm
```

## Storage

Ledger stored at `~/.banana/costs.json`. Created automatically on first use.

## When to Log

Log after every successful generation:
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/cost_tracker.py log \
  --model MODEL_ID \
  --resolution RES \
  --prompt "brief description of what was generated"
```

## When to Show Estimates

Always show cost estimate before batch operations (`/banana batch`):
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/cost_tracker.py estimate \
  --model gemini-3.1-flash-image-preview \
  --resolution 2K \
  --count N
```
