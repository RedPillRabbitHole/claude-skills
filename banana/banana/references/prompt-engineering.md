# Prompt Engineering Reference

> Load this on-demand before constructing any image generation prompt.

## Core Framework: 5-Component Formula

Prompts must use natural narrative paragraphs — not comma-separated keyword lists.

**Components (in order):**
1. **Subject** — Detailed physical characteristics (age, materials, expressions) not generic descriptions
2. **Action** — Strong present-tense verbs describing what the subject does or its pose
3. **Location/Context** — Environmental details including time, atmosphere, and surroundings
4. **Composition** — Camera perspective, framing, and spatial relationships (e.g., "intimate close-up shot")
5. **Style** — Visual register, medium, and lighting combined, often referencing real cameras or photographers

**Component Weight Distribution:**
- Subject: 30%
- Style: 25%
- Context: 15%
- Composition: 10%
- Lighting: 10%
- Action: 10%

## Banned Keywords

Never use these Stable Diffusion-era terms — they degrade Gemini output quality:

- "4K", "8K", "ultra HD", "masterpiece", "highly detailed", "hyperrealistic"
- "trending on artstation", "best quality", "ultra-realistic", "high resolution"
- "award winning", "sharp focus", "intricate details", "stunning"

**Instead:** Use prestigious context anchors like "Pulitzer Prize-winning photograph" or "National Geographic cover story" to improve composition organically. Control resolution via `imageSize` parameter.

## Prompt Length Guidance

| Category | Length | Notes |
|----------|--------|-------|
| Quick concept | 20–60 words | Ideation |
| Standard production | 100–200 words | Default approach |
| Complex professional | 200–300 words | Full 5-component treatment |
| Maximum specification | Up to 2,600 tokens | Structured formats supported |

## Domain Mode Libraries

### Cinema Mode
- **Camera models:** RED Monstro, ARRI Alexa Mini LF, Sony Venice 2, Blackmagic URSA
- **Lenses:** Cooke S7/i, Zeiss Master Primes, Leica Summilux-C
- **Film stocks:** Kodak Vision3 500T, Fujifilm Eterna Cinema, Kodak 5219
- **Lighting:** practicals, motivated sources, negative fill, bounce cards
- **Keywords:** anamorphic bokeh, lens flares, film grain, aspect ratio

### Product Mode
- **Style references:** Apple product photography, Aesop, Glossier, Muji
- **Surface materials:** marble, brushed aluminum, matte acrylic, weathered oak
- **Lighting:** softbox arrays, beauty dishes, rim lights, table-top studio
- **Keywords:** "logo prominently displayed", "product hero shot", clean background

### Portrait Mode
- **Focal lengths:** 85mm, 135mm, 50mm f/1.2 for compression and bokeh
- **Cameras:** Canon EOS R5, Sony A7R IV, Hasselblad X2D
- **Lighting:** Rembrandt, butterfly, clamshell, window light
- **Micro-details:** skin texture, catchlights, hair wisps, fabric texture

### Editorial/Fashion Mode
- **Publication references:** Vogue, Harper's Bazaar, Vanity Fair, i-D, AnOther Magazine
- **Photographers:** Annie Leibovitz, Steven Meisel, Tim Walker, Nick Knight
- **Locations:** rooftops, industrial spaces, luxury interiors, open landscapes
- **Keywords:** editorial spread, fashion story, full-page bleed

### UI/Web Mode
- **Styles:** flat vector, isometric 3D, material design, glassmorphism, neomorphism
- **Specs:** hex colors, pixel-precise layouts, grid systems
- **Assets:** app icons, hero illustrations, empty states, onboarding graphics
- **Keywords:** clean white background, scalable, brand colors

### Logo Mode
- **Construction:** geometric grids, negative space, letterforms, monograms
- **Palette:** monochrome first, 2-3 colors maximum
- **Compatibility:** SVG-ready, works at favicon size
- **Keywords:** minimal, scalable, timeless, vector-style

### Landscape Mode
- **Depth layers:** foreground detail, midground subject, background atmosphere
- **Atmospheric:** golden hour, blue hour, magic hour, overcast diffused light
- **Time of day:** sunrise, midday harsh, dusk gradients, night with stars
- **Weather:** mist, fog, dramatic clouds, clear cerulean sky

### Abstract Mode
- **Color harmonies:** complementary, triadic, analogous, split-complementary
- **Forms:** Voronoi patterns, Perlin noise, reaction-diffusion, fractal geometry
- **Movement:** fluid dynamics, particle systems, wave interference
- **Textures:** micro-photography style, material closeups

### Infographic Mode
- **Layout structures:** grid, radial, timeline, flow diagram, comparison table
- **Text hierarchy:** headline, subhead, body, caption sizes
- **Data visualization:** bar charts, pie charts, scatter plots, network graphs
- **Keep text under 25 characters** per text element

## Proven Prompt Templates

### Instagram Ad / Social Media
```
[Subject: age + appearance + expression], wearing [outfit with brand/texture],
[action verb] in [specific location + time]. [Micro-detail about skin/hair/
sweat/texture]. Captured with [camera model], [focal length] lens at [f-stop],
[lighting description]. [Prestigious context: "Vanity Fair editorial" /
"Pulitzer Prize-winning cover photograph"].
```

### Product / Commercial Photography
```
[Product with brand name] with [dynamic element: condensation/splashes/glow],
[product detail: "logo prominently displayed"], [surface/setting description].
[Supporting visual elements: light rays, particles, reflections].
Commercial photography for an advertising campaign. [Publication reference:
"Bon Appetit feature spread" / "Wallpaper* design editorial"].
```

### Fashion / Editorial
```
[Subject description] wearing [designer/brand] [garment description],
photographed for [publication] [season] issue. [Location with atmosphere].
Shot on [camera] with [focal length], [lighting setup].
[Mood/color palette description].
```

### SaaS / Tech Marketing
```
A [art style] illustration for [product type] showing [core value prop
as visual metaphor]. [Color palette with hex codes if brand-specific].
Clean [design style] aesthetic. [Supporting elements]. White or [brand color]
background. [Usage context: "app store screenshot" / "landing page hero"].
```

### Logo / Brand Mark
```
A [geometric construction description] logo mark for [industry/company type].
[Symbol description with construction notes]. [Color: monochrome / 2-color palette].
Minimal and scalable. [Typography if applicable: font style, weight].
Works at small sizes. Vector illustration style on white background.
```

### Landscape / Environment
```
[Location description] during [time of day], [atmospheric conditions].
[Foreground element] leads the eye toward [midground subject].
[Background atmosphere]. [Lighting quality and direction].
Captured with [camera] and [lens], [technical settings].
[Mood or emotional tone].
```

## Advanced Techniques

### Character Consistency (Multi-turn)
For sequential generation, establish an exhaustive physical description initially:
- Exact hair color, length, style
- Distinctive clothing with brand/material details
- Unique physical identifiers (tattoos, accessories, features)

In subsequent turns: "the same character from the previous image" + 2-3 key identifiers.

### Style Transfer Without Reference Images
Describe the target aesthetic exhaustively:
- "1950s travel poster: flat color areas, bold geometric shapes, hand-lettered text, limited palette of 4 colors, slight texture overlay"
- Do not say "in the style of [artist]" — describe the visual characteristics instead

### Text Rendering Best Practices
- Enclose desired text in quotation marks within the prompt
- Limit to ~25 characters maximum
- Specify font characteristics: "bold geometric sans-serif", "thin elegant serif"
- Specify placement and contrast: "centered, white text on dark background"
- Use high contrast for readability

### Positive Framing (No Negative Prompts)
Gemini has no negative prompt parameter. Rephrase exclusions positively:
- "no blur" → "tack-sharp, crisp detail throughout"
- "no text" → "purely visual, no typography"
- "no people" → "empty scene, unpopulated environment"
- "not dark" → "bright, well-lit, cheerful atmosphere"

### Search-Grounded Generation
For data-driven or factual images, use three-part formula:
1. [Source/Search request] — what to look up
2. [Analytical task] — what to extract
3. [Visual translation] — how to render it

### Critical Details Placement
Put the most important constraints early in the prompt (first 50 words), not at the end. Gemini weights earlier tokens more heavily.

Use ALL CAPS for non-negotiable requirements: "MUST show exactly three people", "MUST include the company logo".

## Safety Rephrase Strategies

When `IMAGE_SAFETY` or `PROHIBITED_CONTENT` is returned:

| Trigger Category | Rephrase Strategy |
|-----------------|------------------|
| Violence/conflict | Reframe as historical, documentary, or abstract |
| Medical/clinical | Use artistic or scientific illustration framing |
| Real public figures | Use fictional character with similar description |
| Children's content | Age up characters slightly, use professional context |
| NSFW/suggestive | Shift to fashion editorial, swimwear catalog context |
| Weapons | Reframe as antique, prop, or museum artifact |

**General strategies:**
- **Abstraction** — Replace dangerous elements with abstract concepts
- **Artistic framing** — Position as editorial, documentary, or fine art
- **Metaphor** — Use symbolic language instead of literal descriptions
- **Positive emphasis** — Describe what's present, not what's absent
- **Context shift** — Reposition threatening scenarios as professional ones

## Common Mistakes

1. **Keyword stuffing** — Generic quality terms degrade output; use context anchors instead
2. **Tag lists** — Use prose paragraphs, not comma-separated tags
3. **Missing lighting** — Always specify lighting direction and quality
4. **No composition direction** — Always include camera perspective and framing
5. **Vague style references** — Name real cameras, brands, publications
6. **Ignoring aspect ratio** — Set `set_aspect_ratio` before generating
7. **Prompts too long** — Stay under 300 words for standard production
8. **Too much text** — Keep rendered text under 25 characters
9. **Critical details at end** — Put must-haves in the first 50 words
10. **No iteration** — Generate, evaluate, refine with follow-up prompts
