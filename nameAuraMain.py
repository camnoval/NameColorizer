import streamlit as st
import colorsys
import random

# --- Helper functions ---

def name_to_colors(name):
    """Convert name string to a list of colors using hash and character codes."""
    name = name.strip().lower()
    colors = []
    seen = set()
    for char in name:
        if char.isalpha() and char not in seen:
            seen.add(char)
            # Use hash of character to generate a stable HSL color
            h = (ord(char) * 13) % 360
            s = 0.65
            l = 0.55
            r, g, b = colorsys.hls_to_rgb(h/360, l, s)
            hex_color = '#%02x%02x%02x' % (int(r*255), int(g*255), int(b*255))
            colors.append((char.upper(), hex_color))
    return colors

def get_color_traits(hue):
    if hue < 0.05 or hue > 0.95:
        return random.choice(["passionate", "fiery", "bold", "adventurous"])
    elif hue < 0.15:
        return random.choice(["energetic", "cheerful", "optimistic", "radiant"])
    elif hue < 0.25:
        return random.choice(["joyful", "bright", "lively", "uplifting"])
    elif hue < 0.4:
        return random.choice(["balanced", "nurturing", "grounded", "fresh"])
    elif hue < 0.55:
        return random.choice(["peaceful", "calm", "thoughtful", "wise"])
    elif hue < 0.7:
        return random.choice(["creative", "imaginative", "intuitive", "dreamy"])
    elif hue < 0.85:
        return random.choice(["calm", "serene", "gentle", "relaxed"])
    else:
        return random.choice(["mysterious", "enigmatic", "magical", "deep"])

# --- Streamlit UI ---

st.set_page_config(page_title="Name Colorizer", page_icon="🎨")

st.title("🎨 Name Colorizer")
st.subheader("Discover the colors hidden in your name")

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
                f"<code>{hex_color}</code></div>", 
                unsafe_allow_html=True
            )

    st.markdown("---")
    st.markdown("### Your Name Aura:")
    aura_traits = []
    for _, color in colors:
        r = int(color[1:3], 16)/255.0
        g = int(color[3:5], 16)/255.0
        b = int(color[5:7], 16)/255.0
        hue = colorsys.rgb_to_hls(r, g, b)[0]
        trait = get_color_traits(hue)
        aura_traits.append(trait)

    aura_traits = list(dict.fromkeys(aura_traits))  # Remove duplicates
    st.success(f"Your name radiates {', '.join(aura_traits)} energy.")
