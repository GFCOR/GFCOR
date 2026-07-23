import sys
import os
from PIL import Image

RAMP = " .`:-=+*cs#%@"  # Bright (sparse/space) -> Dark (dense)

def image_to_ascii(img_path, width=90, aspect_ratio=0.55):
    img = Image.open(img_path).convert("L")
    w, h = img.size
    new_h = int((h / w) * width * aspect_ratio)
    img_resized = img.resize((width, new_h), Image.Resampling.LANCZOS)
    
    pixels = img_resized.getdata()
    num_chars = len(RAMP)
    
    lines = []
    for y in range(new_h):
        line_chars = []
        for x in range(width):
            val = pixels[y * width + x]
            # Map 255 (white) to 0 (space) and 0 (black) to RAMP end
            idx = int((255 - val) / 255.0 * (num_chars - 1))
            idx = max(0, min(num_chars - 1, idx))
            # Escape HTML special chars
            c = RAMP[idx]
            if c == "&": c = "&amp;"
            elif c == "<": c = "&lt;"
            elif c == ">": c = "&gt;"
            elif c == " ": c = "&#160;"
            line_chars.append(c)
        lines.append("".join(line_chars))
    return lines

def generate_ascii_svg(ascii_lines, output_svg="gfcor-ascii.svg"):
    font_size = 7
    line_height = 9.5
    char_width = 4.2
    
    num_lines = len(ascii_lines)
    max_len = max(len(l) for l in ascii_lines) if ascii_lines else 0
    
    svg_width = int(max_len * char_width + 20)
    svg_height = int(num_lines * line_height + 25)
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">')
    svg.append('  <style>')
    svg.append('    .ascii-text { font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; font-size: 7px; fill: #8b949e; white-space: pre; }')
    svg.append('    .row { opacity: 0; animation: fadeIn 0.05s forwards; }')
    svg.append('    @keyframes fadeIn { to { opacity: 1; } }')
    svg.append('  </style>')
    svg.append('  <rect width="100%" height="100%" fill="#0d1117" rx="6" />')
    
    for idx, line in enumerate(ascii_lines):
        y_pos = 18 + idx * line_height
        delay = round(idx * 0.035, 3)
        svg.append(f'  <text x="12" y="{y_pos:.1f}" class="ascii-text row" style="animation-delay: {delay}s;">{line}</text>')
        
    svg.append('</svg>')
    
    with open(output_svg, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"ASCII SVG generated: {output_svg} ({svg_width}x{svg_height})")

if __name__ == "__main__":
    img_file = "source-prepped.png" if os.path.exists("source-prepped.png") else "source-photo.jpg"
    if not os.path.exists(img_file):
        print(f"Error: {img_file} not found.")
        sys.exit(1)
        
    lines = image_to_ascii(img_file, width=88)
    generate_ascii_svg(lines, "gfcor-ascii.svg")
