import sys
import os
from PIL import Image

RAMP = " .`:-=+*cs#%@"  # Bright (sparse/space) -> Dark (dense)

def image_to_ascii(img_path, width=72, aspect_ratio=0.55):
    img = Image.open(img_path).convert("L")
    w, h = img.size
    new_h = int((h / w) * width * aspect_ratio)
    img_resized = img.resize((width, new_h), Image.Resampling.LANCZOS)
    
    pixels = img_resized.getdata()
    num_chars = len(RAMP)
    
    raw_lines = []
    svg_lines = []
    for y in range(new_h):
        line_chars = []
        svg_chars = []
        for x in range(width):
            val = pixels[y * width + x]
            # Map 255 (white) to 0 (space) and 0 (black) to RAMP end
            idx = int((255 - val) / 255.0 * (num_chars - 1))
            idx = max(0, min(num_chars - 1, idx))
            
            c = RAMP[idx]
            line_chars.append(c)
            
            # HTML entity escaping for SVG
            if c == "&": c_svg = "&amp;"
            elif c == "<": c_svg = "&lt;"
            elif c == ">": c_svg = "&gt;"
            elif c == " ": c_svg = "&#160;"
            else: c_svg = c
            svg_chars.append(c_svg)
            
        raw_lines.append("".join(line_chars))
        svg_lines.append("".join(svg_chars))
        
    return raw_lines, svg_lines

def generate_ascii_svg(raw_lines, svg_lines, output_svg="gfcor-ascii.svg"):
    font_size = 9
    line_height = 11.5
    char_width = 5.4
    
    num_lines = len(raw_lines)
    num_cols = max(len(l) for l in raw_lines) if raw_lines else 72
    
    # Exact box bounds with padding
    pad_x = 16
    pad_y = 16
    svg_width = int(num_cols * char_width + pad_x * 2)
    svg_height = int(num_lines * line_height + pad_y * 2)
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">')
    svg.append('  <style>')
    svg.append(f'    .ascii-text {{ font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; font-size: {font_size}px; fill: #3fb950; white-space: pre; }}')
    svg.append('    .row { opacity: 0; animation: fadeIn 0.05s forwards; }')
    svg.append('    @keyframes fadeIn { to { opacity: 1; } }')
    svg.append('  </style>')
    svg.append(f'  <rect width="100%" height="100%" fill="#0d1117" stroke="#30363d" stroke-width="1" rx="8" />')
    
    for idx, line in enumerate(svg_lines):
        y_pos = pad_y + font_size + idx * line_height
        delay = round(idx * 0.035, 3)
        svg.append(f'  <text x="{pad_x}" y="{y_pos:.1f}" class="ascii-text row" style="animation-delay: {delay}s;">{line}</text>')
        
    svg.append('</svg>')
    
    with open(output_svg, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"ASCII SVG generated: {output_svg} (viewBox: {svg_width}x{svg_height})")

if __name__ == "__main__":
    img_file = "source-prepped.png" if os.path.exists("source-prepped.png") else "source-photo.jpg"
    if not os.path.exists(img_file):
        print(f"Error: {img_file} not found.")
        sys.exit(1)
        
    raw_lines, svg_lines = image_to_ascii(img_file, width=72)
    generate_ascii_svg(raw_lines, svg_lines, "gfcor-ascii.svg")
