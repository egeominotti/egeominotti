#!/usr/bin/env python3
"""Generate the profile README's SVG artwork, in a dark and a light variant.

Run `python3 assets/generate.py` from the repository root after changing a text
below. Every SVG is self-contained: system fonts, CSS animations that stop under
prefers-reduced-motion, and no scripts (GitHub serves them as images).
"""

from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

THEMES = {
    "dark": {
        "bg": "#0d1117", "panel": "#161b22", "pill": "#0b0f14", "line": "#30363d",
        "text": "#e6edf3", "muted": "#8b949e", "faint": "#21262d",
        "pink": "#f472b6", "violet": "#a08cff", "green": "#3fb950", "amber": "#d29922",
        "glow": 0.22,
    },
    "light": {
        "bg": "#ffffff", "panel": "#f6f8fa", "pill": "#ffffff", "line": "#d0d7de",
        "text": "#1f2328", "muted": "#59636e", "faint": "#eaeef2",
        "pink": "#bf3989", "violet": "#6e56cf", "green": "#1a7f37", "amber": "#9a6700",
        "glow": 0.12,
    },
}

LANG = {"TypeScript": "#3178c6", "Rust": "#dea584"}

REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def svg(width: int, height: int, title: str, body: str, style: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">\n'
        f"<title>{escape(title)}</title>\n<style>{style}</style>\n{body}\n</svg>\n"
    )


def text(x, y, s, size, fill, *, font=SANS, weight=400, anchor="start", length=None, extra=""):
    fit = f' textLength="{length:.1f}" lengthAdjust="spacingAndGlyphs"' if length else ""
    return (
        f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}"{fit}{extra}>{escape(s)}</text>'
    )


def logo(x: float, y: float, size: float, t: dict, pulse: bool = True) -> str:
    """agentvm's mark: corner brackets around a sealed block cursor (64-unit grid)."""
    k = size / 64
    cls = ' class="blk"' if pulse else ""
    return (
        f'<g transform="translate({x} {y}) scale({k})">'
        f'<g stroke="{t["text"]}" stroke-width="5" stroke-linecap="square" fill="none">'
        '<path d="M6 20V6h14"/><path d="M44 6h14v14"/><path d="M58 44v14H44"/><path d="M20 58H6V44"/></g>'
        f'<rect{cls} x="22" y="22" width="12" height="20" fill="{t["violet"]}"/>'
        f'<rect x="38" y="36" width="6" height="6" fill="{t["text"]}" opacity=".5"/></g>'
    )


def pill(x, y, label, fg, bg, stroke, cw=6.6):
    w = len(label) * cw
    return (
        f'<rect x="{x}" y="{y}" width="{w + 18:.1f}" height="22" rx="11" fill="{bg}" stroke="{stroke}"/>'
        + text(x + 9, y + 15, label, 11, fg, font=MONO, weight=700, length=w)
    ), w + 18


# Header: name, role, a prompt that types what is being built, and jobs flowing
# into agentvm's sealed machine.
PHRASES = [
    "building agentvm: sealed VMs for Claude Code",
    "shipping bunqueue: one queue, eight languages",
    "writing Rust that moves millions of jobs/sec",
    "turning ideas into products people use",
]
LOOP = 20.0  # seconds for the four phrases
SLOT = LOOP / len(PHRASES)
TYPE_S, SHOW_S = 1.8, 4.7
CW, FONT = 12.6, 21  # monospace cell and size; textLength pins every glyph to its cell


def pct(seconds: float) -> str:
    return f"{seconds / LOOP * 100:.2f}%"


def header(t: dict) -> str:
    w, h = 1200, 300
    px, py = 64, 204  # prompt pill
    tx = px + 46  # typed text start
    pill_w = 46 + max(map(len, PHRASES)) * CW + 34
    css = [
        ".blk{animation:pulse 2s ease-in-out infinite}",
        "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}",
        ".cur{animation:blink 1s step-end infinite}",
        "@keyframes blink{0%{fill-opacity:1}50%{fill-opacity:0}}",
        ".job{animation:flow 4s linear infinite}",
        "@keyframes flow{0%{transform:translateX(0);opacity:0}12%{opacity:1}78%{opacity:1}100%{transform:translateX(196px);opacity:0}}",
    ]
    phrases = []
    for i, phrase in enumerate(PHRASES):
        n, start = len(phrase), i * SLOT
        width = n * CW
        first = "1" if i == 0 else "0"
        vis = f"0%{{opacity:{first}}}" + ("" if i == 0 else f"{pct(start)}{{opacity:1}}") + f"{pct(start + SHOW_S)}{{opacity:0}}100%{{opacity:0}}"
        steps = f"animation-timing-function:steps({n},end)"
        move = (
            f"0%{{transform:translateX(0);{steps if i == 0 else ''}}}"
            + ("" if i == 0 else f"{pct(start)}{{transform:translateX(0);{steps}}}")
            + f"{pct(start + TYPE_S)}{{transform:translateX({width:.1f}px)}}100%{{transform:translateX({width:.1f}px)}}"
        )
        css.append(f".ph{i}{{animation:v{i} {LOOP}s step-end infinite}}@keyframes v{i}{{{vis}}}")
        css.append(f".mv{i}{{animation:m{i} {LOOP}s infinite}}@keyframes m{i}{{{move}}}")
        phrases.append(
            f'<g class="ph{i}" opacity="{first}">'
            + text(tx, py + 31, phrase, FONT, t["text"], font=MONO, length=width)
            + f'<g class="mv{i}"><rect x="{tx}" y="{py + 8}" width="{width + 14:.1f}" height="32" fill="{t["pill"]}"/>'
            + f'<rect class="cur" x="{tx}" y="{py + 12}" width="12" height="25" fill="{t["pink"]}"/></g></g>'
        )
    css.append(
        "@media (prefers-reduced-motion: reduce){*{animation:none!important}"
        ".mv0,.mv1,.mv2,.mv3{display:none}.ph1,.ph2,.ph3{opacity:0}.ph0{opacity:1}}"
    )

    jobs = "".join(
        f'<rect class="job" style="animation-delay:{-d}s" x="808" y="158" width="14" height="14" rx="3" fill="{t["pink"]}"/>'
        for i, d in enumerate((0, 1, 2, 3))
    )
    body = f"""
<defs>
  <radialGradient id="g1" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(120 0) scale(620 360)">
    <stop offset="0" stop-color="{t['pink']}" stop-opacity="{t['glow']}"/><stop offset="1" stop-color="{t['pink']}" stop-opacity="0"/></radialGradient>
  <radialGradient id="g2" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(1080 300) scale(560 320)">
    <stop offset="0" stop-color="{t['violet']}" stop-opacity="{t['glow']}"/><stop offset="1" stop-color="{t['violet']}" stop-opacity="0"/></radialGradient>
  <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="{t['line']}"/></pattern>
  <clipPath id="win"><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16"/></clipPath>
  <clipPath id="prompt"><rect x="{px}" y="{py}" width="{pill_w:.1f}" height="48" rx="12"/></clipPath>
</defs>
<g clip-path="url(#win)">
  <rect width="{w}" height="{h}" fill="{t['bg']}"/>
  <rect width="{w}" height="{h}" fill="url(#dots)" opacity=".55"/>
  <rect width="{w}" height="{h}" fill="url(#g1)"/><rect width="{w}" height="{h}" fill="url(#g2)"/>
  <rect y="0" width="{w}" height="40" fill="{t['panel']}" opacity=".9"/><rect y="40" width="{w}" height="1" fill="{t['line']}"/>
  <circle cx="26" cy="20" r="6" fill="#ff5f57"/><circle cx="46" cy="20" r="6" fill="#febc2e"/><circle cx="66" cy="20" r="6" fill="#28c840"/>
  {text(w / 2, 25, "egeominotti — zsh", 13, t["muted"], font=MONO, anchor="middle")}
</g>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16" fill="none" stroke="{t['line']}" stroke-width="2"/>
{text(px, 122, "Egeo Minotti", 58, t["text"], weight=800, extra=' letter-spacing="-1.5"')}
{text(px + 2, 162, "Software Engineer  ·  Blockchain Developer  ·  AI Agent Builder", 21, t["muted"], weight=500)}
<rect x="{px}" y="{py}" width="{pill_w:.1f}" height="48" rx="12" fill="{t['pill']}" stroke="{t['line']}"/>
{text(px + 18, py + 31, "❯", FONT, t["pink"], font=MONO, weight=700)}
<g clip-path="url(#prompt)">{''.join(phrases)}</g>
<path d="M800 165H990" stroke="{t['line']}" stroke-width="2" stroke-dasharray="4 8"/>
{jobs}
{logo(990, 90, 150, t)}
"""
    return svg(w, h, "Egeo Minotti: Software Engineer, Blockchain Developer, AI Agent Builder", body, "".join(css))


def agentvm_card(t: dict) -> str:
    w, h = 830, 200
    p1, w1 = pill(196, 26, "NEW", t["bg"], t["violet"], t["violet"])
    p2, _ = pill(196 + w1 + 8, 26, "APPLE SILICON ONLY", t["amber"], "none", t["amber"])
    facts = "~2 s to a ready VM  ·  root inside  ·  work back as a branch  ·  snapshots + S3"
    body = f"""
<defs><linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="{t['violet']}"/><stop offset="1" stop-color="{t['pink']}"/></linearGradient></defs>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="{t['panel']}" stroke="{t['line']}" stroke-width="2"/>
<rect x="1" y="1" width="{w - 2}" height="4" rx="2" fill="url(#edge)"/>
<rect x="28" y="36" width="136" height="136" rx="18" fill="{t['bg']}" stroke="{t['line']}"/>
{logo(44, 52, 104, t)}
{p1}{p2}
{text(196, 88, "agentvm", 34, t["text"], weight=800, extra=' letter-spacing="-1"')}
{text(w - 28, 44, "github.com/egeominotti/agentvm  ↗", 12, t["muted"], font=MONO, anchor="end")}
{text(196, 120, "Every terminal is a sealed machine.", 19, t["text"], weight=600)}
{text(196, 146, "Claude Code agents in parallel on your Mac, each in its own disposable Debian VM.", 14.5, t["muted"])}
{text(196, 178, facts, 12, t["muted"], font=MONO, length=len(facts) * 7.2)}
"""
    return svg(w, h, "agentvm: Claude Code agents in parallel, each in its own disposable Debian VM. Apple silicon only.", body, ".blk{animation:pulse 2s ease-in-out infinite}@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}" + REDUCED)


PROJECTS = {
    "bunqueue": {
        "wide": True, "accent": "pink", "lang": "TypeScript", "link": "bunqueue.dev  ↗",
        "lead": "Add a background job in one language. Process it in another.",
        "lines": ["Clients for Node.js, Deno, Python, PHP, Go, Rust, Elixir and Bun.",
                  "SQLite by default, PostgreSQL when you scale. DLQ, cron, S3 backups, native MCP. No Redis."],
        "tags": "Bun  ·  SQLite  ·  PostgreSQL  ·  MCP  ·  MIT",
    },
    "bunqueue-dashboard": {
        "name": "bunqueue dashboard", "accent": "pink", "lang": "TypeScript",
        "lines": ["Operate a bunqueue server from the browser:", "queues, jobs, DLQ, cron, workers, the process."],
        "tags": "React  ·  one bunx command",
    },
    "flashq": {
        "accent": "amber", "lang": "Rust",
        "lines": ["Blazingly fast job queue server in Rust.", "Millions of jobs/sec, sub-millisecond latency."],
        "tags": "job queue server",
    },
    "binja": {
        "accent": "violet", "lang": "TypeScript",
        "lines": ["Bun templates: Jinja2/DTL, Handlebars, Liquid.", "2-4x faster than Nunjucks, 160x with AOT."],
        "tags": "Bun  ·  84 filters",
    },
    "bunpilot": {
        "accent": "green", "lang": "TypeScript",
        "lines": ["PM2 for Bun: clustering, crash recovery,", "health checks and zero-downtime deploys."],
        "tags": "Bun  ·  process manager",
    },
}


def card(slug: str, p: dict, t: dict) -> str:
    wide = p.get("wide", False)
    w, h = (830, 186) if wide else (406, 150)
    accent = t[p["accent"]]
    name = p.get("name", slug)
    parts = [
        f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="{t["panel"]}" stroke="{t["line"]}" stroke-width="2"/>',
        f'<rect x="22" y="{24 if wide else 22}" width="4" height="{26 if wide else 22}" rx="2" fill="{accent}"/>',
        text(36, 46 if wide else 40, name, 26 if wide else 19, t["text"], weight=800 if wide else 700, extra=' letter-spacing="-.5"'),
        text(w - 22, 44 if wide else 39, p.get("link", "↗"), 12 if wide else 15, t["muted"], font=MONO if wide else SANS, anchor="end"),
    ]
    y = 80 if wide else 70
    if wide:
        parts.append(text(24, y, p["lead"], 18, t["text"], weight=600))
        y += 26
    for line in p["lines"]:
        parts.append(text(24, y, line, 14.5 if wide else 14, t["muted"]))
        y += 22 if wide else 21
    ty = h - 22
    parts.append(f'<circle cx="30" cy="{ty - 4}" r="6" fill="{LANG[p["lang"]]}"/>')
    tags = f'{p["lang"]}  ·  {p["tags"]}'
    parts.append(text(44, ty, tags, 12, t["muted"], font=MONO, length=len(tags) * 7.2))
    return svg(w, h, f"{name}: {' '.join(p['lines'])}", "\n".join(parts))


def main() -> None:
    for mode, t in THEMES.items():
        (OUT / f"header-{mode}.svg").write_text(header(t))
        (OUT / f"agentvm-{mode}.svg").write_text(agentvm_card(t))
        for slug, p in PROJECTS.items():
            (OUT / f"{slug}-{mode}.svg").write_text(card(slug, p, t))


if __name__ == "__main__":
    main()
