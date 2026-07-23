import sys
import os
import json
from datetime import datetime

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def render_heatmap_svg(json_path="data/contributions.json", output_svg="contrib-heatmap.svg"):
    if not os.path.exists(json_path):
        print(f"File {json_path} not found. Generating default structure...")
        data = {
            "username": "GFCOR",
            "total_contributions": 520,
            "days": []
        }
    else:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

    username = data.get("username", "GFCOR")
    total = data.get("total_contributions", 0)
    days = data.get("days", [])
    
    width = 860
    height = 175
    
    box_size = 11
    box_gap = 3
    step = box_size + box_gap
    
    margin_left = 40
    margin_top = 45
    
    num_days = len(days)
    weeks = num_days // 7 if num_days > 0 else 53
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('  <style>')
    svg.append('    .header-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 13px; font-weight: 600; fill: #c9d1d9; }')
    svg.append('    .sub-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 12px; fill: #8b949e; }')
    svg.append('    .day-label { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 9px; fill: #7d8590; }')
    svg.append('    .legend-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 10px; fill: #7d8590; }')
    svg.append('    .day-box { transform-origin: center; animation: revealBox 0.3s ease-out forwards; opacity: 0; }')
    svg.append('    @keyframes revealBox { 0% { opacity: 0; transform: scale(0.3); } 100% { opacity: 1; transform: scale(1); } }')
    svg.append('  </style>')
    
    # Outer frame
    svg.append(f'  <rect width="{width}" height="{height}" fill="#0d1117" stroke="#30363d" stroke-width="1" rx="8" />')
    
    # Header
    svg.append(f'  <text x="18" y="24" class="header-text">{total:,} contributions in the last year</text>')
    svg.append(f'  <text x="{width - 18}" y="24" class="sub-text" text-anchor="end">@{username}</text>')
    svg.append(f'  <line x1="0" y1="36" x2="{width}" y2="36" stroke="#21262d" stroke-width="1" />')
    
    # Day of week labels (Mon, Wed, Fri)
    day_labels = [("", 0), ("Mon", 1), ("", 2), ("Wed", 3), ("", 4), ("Fri", 5), ("", 6)]
    for label, d_idx in day_labels:
        if label:
            y_pos = margin_top + d_idx * step + 9
            svg.append(f'    <text x="16" y="{y_pos}" class="day-label">{label}</text>')

    # Grid of days
    for idx, day_info in enumerate(days):
        col = idx // 7
        row = idx % 7
        
        x = margin_left + col * step
        y = margin_top + row * step
        
        level = day_info.get("level", 0)
        level = max(0, min(len(PALETTE) - 1, level))
        fill_color = PALETTE[level]
        
        delay = round((col + row) * 0.012, 3)
        date_str = day_info.get("date", "")
        count = day_info.get("count", 0)
        
        svg.append(
            f'  <rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" rx="2" ry="2" '
            f'fill="{fill_color}" class="day-box" style="animation-delay: {delay}s;">'
            f'<title>{count} contributions on {date_str}</title></rect>'
        )

    # Legend at bottom right
    leg_x = width - 150
    leg_y = height - 16
    svg.append(f'  <text x="{leg_x - 30}" y="{leg_y + 9}" class="legend-text">Less</text>')
    for i, color in enumerate(PALETTE):
        cx = leg_x + i * (box_size + 3)
        svg.append(f'  <rect x="{cx}" y="{leg_y}" width="{box_size}" height="{box_size}" rx="2" ry="2" fill="{color}" />')
    svg.append(f'  <text x="{leg_x + len(PALETTE) * (box_size + 3) + 6}" y="{leg_y + 9}" class="legend-text">More</text>')

    svg.append('</svg>')
    
    with open(output_svg, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Contribution Heatmap SVG generated: {output_svg}")

if __name__ == "__main__":
    json_f = sys.argv[1] if len(sys.argv) > 1 else "data/contributions.json"
    render_heatmap_svg(json_f, "contrib-heatmap.svg")
