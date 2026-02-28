DEFAULT_STYLE = (
    "Photorealistic high-fashion campaign with luxury editorial direction, "
    "print-magazine quality art direction, refined cinematic color grading, and elegant visual storytelling. "
    "Mood: confident, modern, and sophisticated."
)

DEFAULT_LOCATION = (
    "A high rooftop at sunset above a dense city skyline, with concrete surfaces, parapets, railings, "
    "architectural service structures, warm low-angle sunlight, and atmospheric haze that enhances depth "
    "for hyperrealistic high-fashion editorial photography."
)

STYLE_PROMPT_PRESETS = {
    "Luxury Editorial Minimalism": (
        "Luxury high-fashion editorial styling with clean visual hierarchy, understated sophistication, "
        "precise tailoring emphasis, restrained neutral palette, controlled body language, polished wardrobe "
        "coordination, and magazine-grade refinement focused on elegance and exclusivity."
    ),
    "Avant-Garde Couture Drama": (
        "Avant-garde couture styling with bold sculptural silhouettes, dramatic proportion play, visual tension "
        "between structure and movement, experimental layering, assertive pose language, and runway-level "
        "editorial intensity with rich textile detail."
    ),
    "90s Supermodel Power": (
        "Iconic 90s supermodel styling with commanding pose language, strong attitude, glossy magazine polish, "
        "high-contrast wardrobe direction, timeless silhouette choices, and bold confidence-driven editorial impact."
    ),
    "Contemporary Quiet Luxury": (
        "Contemporary quiet-luxury styling with minimalist wardrobe storytelling, tactile premium fabrics, "
        "muted tonal harmony, subtle sensuality, clean line work, and an elegant premium mood with refined restraint."
    ),
    "Cinematic Urban Glamour": (
        "Cinematic urban glamour styling with dynamic editorial rhythm, modern aspirational attitude, "
        "premium street-luxury wardrobe combinations, bolder contrasts, expressive movement cues, and impactful "
        "magazine-ready visual energy."
    ),
    "Neo-Noir Night Editorial": (
        "Neo-noir editorial styling with deep black tonal control, sleek monochrome accents, sharp silhouette definition, "
        "dramatic tension, minimal yet precise accessories, and dark cinematic fashion attitude."
    ),
    "Sport-Luxe Precision": (
        "Sport-luxe styling that balances athletic energy with couture refinement, dynamic body language, "
        "technical textile focus, functional layering, clean modern lines, and high-performance luxury attitude."
    ),
    "Romantic Haute Boheme": (
        "Romantic haute-boheme styling with graceful movement, soft yet intentional layering, flowing silhouettes, "
        "organic texture depth, poetic mood, and delicate luxury detailing with elevated editorial softness."
    ),
    "Monochrome Studio Authority": (
        "Monochrome styling direction with assertive silhouette emphasis, disciplined tonal palette, minimal distractions, "
        "sharp tailoring, strong authority-driven pose language, and polished high-fashion editorial clarity."
    ),
    "Futurist Metallic Couture": (
        "Futurist couture styling with metallic accents, clean geometric layering, directional fashion poses, "
        "forward-looking luxury attitude, technical-glam finish, and bold next-generation editorial expression."
    ),
}

LOCATION_PROMPT_PRESETS = {
    "Sunset Rooftop Skyline": (
        "High rooftop at sunset above a dense metropolitan skyline, with concrete textures, railings, service "
        "structures, warm low-angle sun, long shadows, and layered atmospheric urban depth."
    ),
    "Brutalist Museum Forecourt": (
        "Open-air brutalist museum forecourt with monumental concrete geometry, strong linear perspective, "
        "clean negative space, hard edges, and directional daylight with sculpted shadows."
    ),
    "Historic European Avenue": (
        "Historic European avenue with classic facades, stone pavement, wrought-iron details, subtle street reflections, "
        "deep perspective lines, and soft natural light across architectural surfaces."
    ),
    "Industrial Loft Daylight": (
        "Large industrial loft with tall steel-frame windows, textured walls, polished concrete flooring, "
        "soft directional daylight, and natural interior depth with gentle light falloff."
    ),
    "Coastal Cliff Golden Hour": (
        "Coastal cliff landscape at golden hour with textured rock formations, clean horizon separation, "
        "salt-air haze, warm highlights, and expansive natural depth."
    ),
    "Art Deco Hotel Lobby": (
        "Grand art deco hotel lobby with geometric symmetry, polished stone floors, brass accents, patterned walls, "
        "warm ambient interior light, and layered architectural depth."
    ),
    "Desert Modernist Villa": (
        "Desert modernist villa with travertine and concrete planes, open volumes, dry atmosphere, "
        "sun-sculpted shadows, and clean architectural transitions."
    ),
    "Tokyo Neon Backstreet": (
        "Narrow Tokyo backstreet at blue hour with neon signage glow, wet asphalt reflections, dense vertical details, "
        "tight urban perspective, and layered city ambience."
    ),
    "Marble Gallery Hall": (
        "Large marble gallery hall with monumental columns, pristine stone surfaces, soft directional top light, "
        "subtle reflections, and calm museum-scale symmetry."
    ),
    "Rainy Financial District Night": (
        "Modern financial district at night after rain, reflective pavement, glass-and-steel facades, light bloom, "
        "misty air, and deep metropolitan perspective."
    ),
    "Botanical Glasshouse": (
        "Historic botanical glasshouse with iron framework, diffused daylight through glass panels, layered greenery, "
        "subtle humidity haze, and rich organic depth."
    ),
}

DEFAULT_MODEL_DESC = (
    "Young woman with radiant, natural beauty. She has a symmetrical oval face with smooth white skin "
    "covered in delicate freckles across her nose and cheeks. Her eyes are almond-shaped, light hazel-green "
    "with a soft, captivating gaze, framed by defined eyebrows that are full and natural. Her nose is small "
    "and proportionate, with subtle definition. She has full, well-shaped lips with a soft natural pink tone. "
    "Her hair is curly, voluminous, and black with platinum blond undertones, styled half-up and half-down, "
    "with loose curls framing her forehead and temples. The curls are defined and bouncy, adding texture around her head."
)

MODEL_DESC_PRESETS = {
    "Freckled Natural Muse": DEFAULT_MODEL_DESC,
    "Androgynous Runway Edge": (
        "Young androgynous model with a sharp jawline and high cheekbones, neutral warm-beige skin tone, deep-set "
        "dark brown eyes, naturally full brows, straight nose bridge, and medium lips with subtle definition. Hair is "
        "short, dark, and slightly wet-textured, brushed back from the forehead. Overall look is modern, bold, and "
        "editorial with clean facial structure and minimal styling."
    ),
    "Afro-Textured Editorial Icon": (
        "Young woman with deep brown skin and luminous undertones, oval face, expressive almond-shaped eyes, softly "
        "arched brows, balanced nose profile, and full naturally defined lips. Hair is a voluminous, well-defined afro "
        "with rich texture and shape. The look feels powerful, elegant, and unmistakably high-fashion with realistic "
        "skin detail and strong editorial presence."
    ),
    "Mediterranean Classic Beauty": (
        "Young woman with olive skin, symmetrical face, hazel eyes, thick dark eyebrows, softly contoured straight nose, "
        "and full lips with a natural rose tone. Hair is long, dark chestnut, and glossy with soft waves parted at the center. "
        "Overall appearance is timeless, sophisticated, and suitable for premium fashion editorials."
    ),
    "East Asian Minimal Elegance": (
        "Young woman with porcelain-neutral skin tone, refined oval face, dark almond-shaped eyes, straight brows, "
        "small balanced nose, and softly sculpted lips. Hair is straight, jet black, and shoulder-length with a precise "
        "center part. The look is understated, modern, and highly editorial with clean, elegant facial harmony."
    ),
    "Mature Silver-Hair Authority": (
        "Mature woman with radiant fair skin showing natural texture, striking high cheekbones, grey-green eyes, "
        "defined eyebrows, elegant nose line, and balanced lips with subtle neutral tone. Hair is silver, shoulder-length, "
        "and styled in soft polished waves. Overall look conveys confidence, luxury, and iconic fashion authority."
    ),
    "Latin Curly Glamour": (
        "Young Latina model with warm golden-olive skin, bright brown eyes, softly arched eyebrows, refined nose bridge, "
        "and naturally full lips. Hair is long, dark brown, and densely curly with controlled volume and healthy shine. "
        "The face is expressive and magnetic, with a glamorous yet realistic high-fashion editorial presence."
    ),
    "Classic Tailored Male Lead": (
        "Young man with defined jawline, balanced oval face, medium-light warm skin tone, deep brown eyes, "
        "thick natural eyebrows, straight nose bridge, and medium full lips. Hair is short, dark brown, neatly "
        "textured with subtle volume on top. Overall look is elegant, confident, and ideal for premium editorial menswear."
    ),
    "Athletic Modern Male": (
        "Young man with athletic build, medium tan skin, sharp cheekbone structure, dark hazel eyes, straight brows, "
        "proportionate nose, and natural lip definition. Hair is short black with clean sides and slightly tousled top. "
        "The appearance feels modern, energetic, and polished for contemporary high-fashion campaigns."
    ),
    "Mature Silver-Hair Gentleman": (
        "Mature man with refined facial structure, fair-to-neutral skin tone with realistic texture, light grey eyes, "
        "well-groomed brows, straight nose line, and subtle beard shadow. Hair is silver, medium-short, combed back "
        "with natural volume. The look conveys authority, sophistication, and timeless luxury."
    ),
    "Afro-Textured Male Icon": (
        "Young Black man with deep brown skin, strong jawline, expressive dark eyes, natural thick brows, and full lips. "
        "Hair is a defined short afro with dense texture and clean shape. Overall presence is bold, elegant, and strongly "
        "editorial with high realism."
    ),
    "East Asian Sharp Menswear": (
        "Young East Asian man with clear neutral skin tone, structured face, almond-shaped dark eyes, straight brows, "
        "balanced nose, and clean lip line. Hair is straight jet black, short on the sides with controlled top volume. "
        "The look is precise, contemporary, and ideal for minimalist luxury menswear editorials."
    ),
}

