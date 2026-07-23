import sys
import os
import xml.sax.saxutils as xml_utils

def generate_info_card(output_svg="info-card.svg"):
    width = 490
    height = 360
    
    rows = [
        ("OS", "GitHub Linux x86_64", "#58a6ff"),
        ("Host", "Profile README v2.0", "#8b949e"),
        ("Role", "Computer Science Student & AI Developer", "#7ee787"),
        ("University", "UTEC (Universidad de Ingeniería y Tecnología)", "#ffa657"),
        ("Languages", "Python, C++, Autodesk, SQL, Bash", "#d2a8ff"),
        ("Frameworks", "React, Next.js, Node.js, PyTorch", "#79c0ff"),
        ("Focus", "AI Agents,Prompt Engineering, Software Engineering & Systems", "#ff7b72"),
        ("Location", "Peru / Remote", "#a5d6ff"),
    ]
    
    palette_colors = [
        "#484f58", "#ff7b72", "#7ee787", "#ffa657",
        "#79c0ff", "#d2a8ff", "#a5d6ff", "#f0f6fc"
    ]
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('  <style>')
    svg.append('    .term-header { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 13px; font-weight: 600; fill: #8b949e; }')
    svg.append('    .key { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 12.5px; font-weight: bold; }')
    svg.append('    .val { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 12.5px; fill: #c9d1d9; }')
    svg.append('    .sep { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 12.5px; fill: #484f58; }')
    svg.append('    .title-user { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 14px; font-weight: bold; fill: #7ee787; }')
    svg.append('    .row-item { opacity: 0; animation: fadeInRow 0.4s forwards; }')
    svg.append('    @keyframes fadeInRow { to { opacity: 1; transform: translateY(0); } }')
    svg.append('  </style>')
    
    # Background card
    svg.append(f'  <rect width="{width}" height="{height}" fill="#0d1117" stroke="#30363d" stroke-width="1" rx="8" />')
    
    # Header bar
    svg.append('  <circle cx="20" cy="20" r="6" fill="#ff5f56" />')
    svg.append('  <circle cx="40" cy="20" r="6" fill="#ffbd2e" />')
    svg.append('  <circle cx="60" cy="20" r="6" fill="#27c93f" />')
    svg.append('  <text x="80" y="24" class="term-header">GFCOR@github: ~ (neofetch)</text>')
    svg.append('  <line x1="0" y1="38" x2="490" y2="38" stroke="#21262d" stroke-width="1" />')
    
    # Content Title
    svg.append('  <g class="row-item" style="animation-delay: 0.1s;">')
    svg.append('    <text x="24" y="66" class="title-user">GFCOR@github</text>')
    svg.append('    <text x="24" y="78" class="val">----------------------------------------</text>')
    svg.append('  </g>')
    
    # Rows
    y_start = 104
    y_step = 26
    for idx, (k, v, color) in enumerate(rows):
        y_pos = y_start + idx * y_step
        delay = round(0.15 + idx * 0.07, 2)
        v_escaped = xml_utils.escape(v)
        svg.append(f'  <g class="row-item" style="animation-delay: {delay}s;">')
        svg.append(f'    <text x="24" y="{y_pos}" class="key" fill="{color}">{k:<11}</text>')
        svg.append(f'    <text x="125" y="{y_pos}" class="sep">~&gt;</text>')
        svg.append(f'    <text x="150" y="{y_pos}" class="val">{v_escaped}</text>')
        svg.append('  </g>')
        
    # Color palette circles at bottom
    y_palette = y_start + len(rows) * y_step + 18
    delay = round(0.15 + len(rows) * 0.07, 2)
    svg.append(f'  <g class="row-item" style="animation-delay: {delay}s;">')
    for i, c in enumerate(palette_colors):
        cx = 24 + i * 22
        svg.append(f'    <circle cx="{cx}" cy="{y_palette}" r="7" fill="{c}" />')
    svg.append('  </g>')
    
    svg.append('</svg>')
    
    with open(output_svg, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Info card SVG generated: {output_svg}")

if __name__ == "__main__":
    generate_info_card("info-card.svg")
