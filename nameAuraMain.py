import streamlit as st
import colorsys

# --- Main: Deterministic, cohesive color mapping ---

def name_to_colors(name):
    """Generate a consistent-style color palette based on a name. Only one style is used per name."""
    name = name.strip().lower()
    colors = []
    seen = set()
    prev_seed = 0

    def style_from_seed(seed):
        styles = ["pastel", "neon", "metallic", "vivid"]
        return styles[seed % len(styles)]

    def stable_uniform(min_val, max_val, seed_val):
        return min_val + (seed_val % 1000) / 1000 * (max_val - min_val)

    if not name:
        return []

    # Set style ONCE based on first valid letter
    first_letter = next((char for char in name if char.isalpha()), None)
    if not first_letter:
        return []

    style_seed = ord(first_letter) * 37 % 10000
    style = style_from_seed(style_seed)

    for char in name:
        if char.isalpha() and char not in seen:
            seen.add(char)
            seed = (ord(char) * 37 + prev_seed * 11) % 10000
            prev_seed = seed

            # Apply the one fixed style to all characters
            if style == "pastel":
                s = stable_uniform(0.3, 0.5, seed)
                l = stable_uniform(0.75, 0.9, seed)
            elif style == "neon":
                s = stable_uniform(0.9, 1.0, seed)
                l = stable_uniform(0.5, 0.65, seed)
            elif style == "metallic":
                s = stable_uniform(0.6, 0.8, seed)
                l = stable_uniform(0.3, 0.5, seed)
            elif style == "vivid":
                s = stable_uniform(0.75, 0.85, seed)
                l = stable_uniform(0.55, 0.65, seed)

            h = (seed * 1.3) % 360
            r, g, b = colorsys.hls_to_rgb(h / 360, l, s)
            hex_color = '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))

            colors.append((char.upper(), hex_color))

    return colors

def get_color_traits(hue):
    """Assign descriptive traits based on hue group."""
    if hue < 0.05 or hue > 0.95:
        return "passionate"
    elif hue < 0.15:
        return "energetic"
    elif hue < 0.25:
        return "joyful"
    elif hue < 0.4:
        return "balanced"
    elif hue < 0.55:
        return "peaceful"
    elif hue < 0.7:
        return "creative"
    elif hue < 0.85:
        return "calm"
    else:
        return "mysterious"

# --- UI ---

st.set_page_config(page_title="Name Colorizer", page_icon="🎨")

st.title("🎨 Name Colorizer")
st.subheader("Turn your name into a unique color palette and personality")

name_input = st.text_input("Enter your first name:")

if name_input:
    st.markdown("### Your Name Palette:")
    colors = name_to_colors(name_input)
    
    cols = st.columns(len(colors))
    for i, (char, hex_color) in enumerate(colors):
        with cols[i]:
            st.markdown(
                f"<div style='text-align: center;'>"
                f"<b>{char}</b><br>"
                f"<div style='background-color:{hex_color}; width:60px; height:60px; border-radius:6px; margin:auto;'></div><br>"
                f"<code>{hex_color}</code>"
                f"</div>", 
                unsafe_allow_html=True
            )


    st.markdown("---")
    st.markdown("### Your Name Aura:")

    aura_traits = []
    for _, hex_color in colors:
        r = int(hex_color[1:3], 16)/255.0
        g = int(hex_color[3:5], 16)/255.0
        b = int(hex_color[5:7], 16)/255.0
        hue = colorsys.rgb_to_hls(r, g, b)[0]
        trait = get_color_traits(hue)
        aura_traits.append(trait)

    aura_traits = list(dict.fromkeys(aura_traits))  # Deduplicate
    if aura_traits:
        st.success(f"Your name radiates {', '.join(aura_traits)} energy.")
    else:
        st.warning("Couldn’t generate your aura. Try a different name.")
