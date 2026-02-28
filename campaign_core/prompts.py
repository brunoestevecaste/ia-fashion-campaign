def build_model_reference_prompt(model_desc):
    return f"""
Create a photorealistic CLOSE-UP model reference image for identity consistency.

Model description:
{model_desc}

Requirements:
- Tight close-up portrait, front-facing.
- Neutral expression, even studio lighting, clean plain background.
- No dramatic pose, no accessories covering face, no text or watermark.
- Fashion casting style, realistic skin texture.
- Composition (1:1).
"""


def build_shoot_prompts_request(style, location):
    return f"""
You are a world-class high-fashion creative director and Vogue-level editorial photographer.

CAMPAIGN INPUT:
- Style: {style}
- Location: {location}

TASK:
Generate exactly 4 highly detailed image prompts in ENGLISH for a high-fashion photorealistic campaign.
The final generation system will receive:
1) A garment reference photo.
2) A single model reference photo.

CONSISTENCY PRIORITY (CRITICAL):
- Treat model identity consistency as the highest priority across all 4 prompts.
- Treat garment consistency as the highest priority across all 4 prompts.
- Do NOT suggest changing garment design, color, fit, layers, or key materials.
- Do NOT suggest changing face identity, hairstyle, hair color, body type, or age.
- Any creative variation must come from camera, pose, framing, mood, and environment only.

So your prompts must focus on scene direction only:
- composition
- camera language
- pose
- mood
- lighting
- editorial storytelling
- background atmosphere

Creative constraints:
- Respect and amplify the user inputs for style and location.
- Keep all 4 prompts visually coherent as one campaign narrative.
- Every prompt must target SQUARE framing (1:1) and print-ready 4K detail.
- The look must be strictly photorealistic (no illustration, no CGI, no surreal distortion).
- Include premium fashion-photography language: lens choice, camera height/angle, body language,
  fabric behavior, skin and hair micro-texture, and nuanced lighting behavior.

Visual direction must be consistent across all prompts:
- high-fashion streetwear attitude
- cinematic editorial lighting with sculpted highlights and dimensional shadows
- controlled contrast, realistic atmospheric depth, and refined color grading
- high micro-detail in skin, fabrics, hair, and architectural textures
- strictly hyperrealistic fashion photography (no stylized or illustrative look)
- premium high-fashion editorial quality suitable for print magazine

Use these mandatory variations:
1) full body + walking pose
2) medium shot + seated pose
3) low-angle shot + static pose
4) detail shot + in-motion pose

For each prompt, explicitly include:
- framing and shot scale
- focal length (in mm)
- camera perspective
- lighting direction and quality
- emotional tone
- environment cues derived from the location input
- a brief consistency reminder to preserve the same model identity and same garment from references

Return ONLY valid JSON using this exact format:
{{
  "prompts": ["prompt 1", "prompt 2", "prompt 3", "prompt 4"]
}}
"""


def build_final_image_instruction(prompt_text):
    return f"""
You will receive reference images:
1) GARMENT_REFERENCE: preserve garment identity exactly (shape, details, colors, materials).
2) MODEL_REFERENCE: preserve facial identity, hairstyle, and overall model look.

Generate ONE photorealistic high-fashion campaign image using this direction:
{prompt_text}

Hard constraints:
- CONSISTENCY LOCK (HIGHEST PRIORITY):
  - The model must remain the exact same person as MODEL_REFERENCE in all facial and physical identity traits.
  - The garment must remain exactly the same item as GARMENT_REFERENCE with no redesign or substitution.
  - No wardrobe swap, no accessory that hides garment structure, and no identity drift.
- Keep the same garment and same model identity from references.
- Output must be square (1:1), native 4K (4096x4096).
- No text, logo, watermark, or frame.
- Strictly hyperrealistic quality, suitable for a top-tier fashion magazine.
- Preserve physically plausible anatomy, realistic skin detail, and true-to-life fabric rendering.
- Maintain a premium high-fashion editorial atmosphere aligned with the prompt direction.
"""
