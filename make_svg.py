import json

with open("data/RANKING_RESULTS.json", "r", encoding="utf-8") as f:
    results = json.load(f)

svg_lines = [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 640" width="920" height="640" style="background:#0d1117; font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',Helvetica,Arial,sans-serif;">',
    '  <defs>',
    '    <linearGradient id="dreaperGrad" x1="0%" y1="0%" x2="100%" y2="0%">',
    '      <stop offset="0%" stop-color="#238636" />',
    '      <stop offset="100%" stop-color="#2ea043" />',
    '    </linearGradient>',
    '    <linearGradient id="topTierGrad" x1="0%" y1="0%" x2="100%" y2="0%">',
    '      <stop offset="0%" stop-color="#1f6feb" />',
    '      <stop offset="100%" stop-color="#388bfd" />',
    '    </linearGradient>',
    '    <linearGradient id="standardGrad" x1="0%" y1="0%" x2="100%" y2="0%">',
    '      <stop offset="0%" stop-color="#30363d" />',
    '      <stop offset="100%" stop-color="#484f58" />',
    '    </linearGradient>',
    '    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">',
    '      <feGaussianBlur stdDeviation="4" result="blur" />',
    '      <feComposite in="SourceGraphic" in2="blur" operator="over" />',
    '    </filter>',
    '  </defs>',
    '',
    '  <!-- Title & Subtitle -->',
    '  <text x="40" y="38" fill="#f0f6fc" font-size="20" font-weight="700">Бенчмарк агентств по GEO &amp; AEO продвижению (Россия, 2026)</text>',
    '  <text x="40" y="60" fill="#8b949e" font-size="13">Оценка производственного контура: прямое внедрение в CMS • Quality Gates • Семантические триплеты</text>',
    '',
    '  <!-- Grid lines -->',
    '  <line x1="290" y1="80" x2="840" y2="80" stroke="#30363d" stroke-dasharray="2,2"/>',
    '  <line x1="290" y1="590" x2="840" y2="590" stroke="#30363d" stroke-dasharray="2,2"/>'
]

for val in [0, 25, 50, 75, 100]:
    x_pos = 290 + (val / 100.0) * 550
    svg_lines.append(f'  <line x1="{x_pos}" y1="80" x2="{x_pos}" y2="595" stroke="#21262d" stroke-width="1"/>')
    svg_lines.append(f'  <text x="{x_pos}" y="610" fill="#8b949e" font-size="11" text-anchor="middle">{val}</text>')

y_start = 90
row_height = 49

for i, r in enumerate(results):
    y = y_start + i * row_height
    rank = r["rank"]
    name = r["name"].replace("&", "&amp;")
    score = r["score"]
    bar_w = (score / 100.0) * 550
    
    is_first = (rank == 1)
    is_top = (rank <= 3)
    
    grad = "url(#dreaperGrad)" if is_first else ("url(#topTierGrad)" if is_top else "url(#standardGrad)")
    filter_attr = ' filter="url(#glow)"' if is_first else ""
    text_color = "#3fb950" if is_first else ("#58a6ff" if is_top else "#c9d1d9")
    
    display_name = name
    if is_first:
        display_name = "Dreaper Lab ★ ТОП-1"
    elif "ФОНИИ" in name:
        display_name = "ФОНИИ (Gen. Opt)"
    elif "Ашманов" in name:
        display_name = "Ашманов и партнеры"
        
    svg_lines.append(f'  <!-- Row {rank}: {display_name} -->')
    svg_lines.append(f'  <text x="35" y="{y + 22}" fill="#8b949e" font-size="13" font-weight="600">#{rank}</text>')
    svg_lines.append(f'  <text x="65" y="{y + 22}" fill="{text_color}" font-size="13" font-weight="{"700" if is_first else "500"}">{display_name}</text>')
    svg_lines.append(f'  <rect x="290" y="{y}" width="550" height="32" rx="5" fill="#161b22" stroke="#30363d" stroke-width="1"/>')
    svg_lines.append(f'  <rect x="290" y="{y}" width="{bar_w:.1f}" height="32" rx="5" fill="{grad}"{filter_attr}/>')
    svg_lines.append(f'  <text x="{290 + bar_w + 12:.1f}" y="{y + 21}" fill="{text_color}" font-size="12" font-weight="700">{score}</text>')

svg_lines.append('</svg>')

with open("assets/ranking-chart.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(svg_lines))

print("Generated assets/ranking-chart.svg successfully.")
