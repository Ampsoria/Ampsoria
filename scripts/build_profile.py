#!/usr/bin/env python3
"""Build self-contained README SVGs; optionally refresh public GitHub data.

Standard library only. Run from any directory. No remote image dependencies.
"""

import argparse
from collections import Counter
from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/generated"
ACCOUNT = "Ampsoria"
MINT = "#8fffd2"
CYAN = "#74dcff"
FONT = "'Segoe UI', Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, monospace"
STACK = [
    ("java", "Java", "#f89820"), ("python", "Python", "#ffd343"),
    ("c", "C", "#77a9ff"), ("php", "PHP", "#aaa5ff"),
    ("javascript", "JavaScript", "#f7df1e"),
    ("html5", "HTML5", "#ff7954"), ("css3", "CSS3", "#65baff"),
    ("react", "React", "#61dafb"), ("nodejs", "Node.js", "#8cce7a"),
    ("mysql", "MySQL", "#77c7ed"), ("firebase", "Firebase", "#ffcb4c"),
    ("git", "Git", "#ff806a"), ("docker", "Docker", "#59baff"),
    ("n8n", "n8n", "#ff8097"), ("linux", "Linux", "#ffde69"),
    ("windows", "Windows", "#64baff"),
    ("raspberrypi", "Raspberry Pi", "#f76c9e"), ("esp32", "ESP32", "#ff7676"),
    ("yolo", "YOLO", "#72f5eb"), ("roboflow", "Roboflow", "#bc95ff"),
    ("tcpip", "TCP / IP", "#8fffd2"), ("nmap", "Nmap", "#74dcff"),
]


def text(x, y, value, size=16, color="#e9f1f7", weight=400, family=FONT, extra=""):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" font-family="{family}" {extra}>{escape(str(value))}</text>'


def svg(name, width, height, body, title, description=""):
    document = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description or title)}</desc>
<defs>
  <linearGradient id="accent"><stop stop-color="{MINT}"/><stop offset=".55" stop-color="{CYAN}"/><stop offset="1" stop-color="#b8a2ff"/></linearGradient>
  <radialGradient id="aura"><stop stop-color="#145665" stop-opacity=".5"/><stop offset="1" stop-color="#0b111b" stop-opacity="0"/></radialGradient>
  <pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" fill="none" stroke="#91cce2" stroke-opacity=".055"/></pattern>
</defs>
<style>
  .orbit {{transform-box:fill-box;transform-origin:center;animation:rotate 38s linear infinite}}
  .reverse {{animation-direction:reverse;animation-duration:52s}}
  .pulse {{animation:pulse 4s ease-in-out infinite}}
  .float {{animation:float 7s ease-in-out infinite}}
  .scan {{animation:scan 9s ease-in-out infinite}}
  .blink {{animation:pulse 2s ease-in-out infinite}}
  .trace {{stroke-dasharray:14 14;animation:trace 18s linear infinite}}
  @keyframes rotate {{to {{transform:rotate(360deg)}}}}
  @keyframes pulse {{0%,100% {{opacity:.45}} 50% {{opacity:1}}}}
  @keyframes float {{0%,100% {{transform:translateY(0)}} 50% {{transform:translateY(-8px)}}}}
  @keyframes scan {{0%,100% {{transform:translateX(0);opacity:.15}} 50% {{transform:translateX(70px);opacity:.65}}}}
  @keyframes trace {{to {{stroke-dashoffset:-280}}}}
  @media (prefers-reduced-motion:reduce) {{.orbit,.pulse,.float,.scan,.blink,.trace {{animation:none!important}}}}
</style>
{body}
</svg>'''
    ET.fromstring(document)
    (OUT / name).write_text(document + "\n")


def hero(light=False):
    bg, fg, muted, edge = ("#f4f9fc", "#172d43", "#456078", "#d4e2ed") if light else ("#0b111b", "#edf7ff", "#92a8bb", "#223343")
    accent = "#157763" if light else MINT
    b = f'<rect x="1" y="1" width="1198" height="458" rx="24" fill="{bg}" stroke="{edge}"/><rect x="1" y="1" width="1198" height="458" rx="24" fill="url(#grid)"/>'
    b += '<ellipse cx="935" cy="215" rx="290" ry="260" fill="url(#aura)"/>'
    b += text(48, 49, "AMPSORIA", 15, fg, 700, MONO, 'letter-spacing="4"')
    b += text(1150, 49, "SOFTWARE / SYSTEMS / SECURITY", 12, muted, 400, MONO, 'text-anchor="end" letter-spacing="1.5"')
    b += f'<path d="M48 73H1152" stroke="{edge}"/>'
    b += f'<circle cx="55" cy="111" r="4" fill="{accent}" class="pulse"/>'
    b += text(69, 115, "CURIOUS MIND. HANDS-ON BUILDER.", 12, accent, 600, MONO, 'letter-spacing="1.8"')
    b += text(44, 193, "Hello, I'm Amp.", 68, fg, 750, extra='letter-spacing="-3"')
    b += text(47, 248, "Code. Connect. Keep learning.", 31, muted, 500, extra='letter-spacing="-1"')
    b += text(49, 285, "Aspiring Software Developer & Cybersecurity Enthusiast", 17, muted)
    b += '<rect x="48" y="319" width="586" height="86" rx="12" fill="#0a1420" stroke="#284051"/>'
    b += '<circle cx="65" cy="337" r="3" fill="#ff827d"/><circle cx="77" cy="337" r="3" fill="#ffd879"/><circle cx="89" cy="337" r="3" fill="#8fffd2"/>'
    b += text(108, 341, "amp@dev: ~", 11, "#91aabd", family=MONO)
    b += text(65, 380, "> building skills, one project at a time", 17, MINT, family=MONO)
    b += '<rect x="483" y="366" width="9" height="17" fill="#8fffd2" class="blink"/>'
    # Orbiting nodes, network paths, a floating central monogram and scan line.
    b += '<g fill="none" stroke="#547185" stroke-opacity=".36"><circle cx="936" cy="250" r="148"/><circle cx="936" cy="250" r="113"/><path d="M759 250h354M936 89v322" stroke-dasharray="3 8"/></g>'
    b += '<g class="orbit"><circle cx="936" cy="250" r="148" fill="none" stroke="url(#accent)" stroke-dasharray="76 390" stroke-width="2"/><circle cx="1084" cy="250" r="6" fill="#8fffd2"/><circle cx="788" cy="250" r="4" fill="#b8a2ff"/></g>'
    b += '<g class="orbit reverse"><circle cx="936" cy="250" r="113" fill="none" stroke="#74dcff" stroke-opacity=".65" stroke-dasharray="3 16"/><circle cx="936" cy="137" r="5" fill="#74dcff"/><circle cx="936" cy="363" r="5" fill="#74dcff"/></g>'
    b += '<g class="float"><rect x="871" y="185" width="130" height="130" rx="32" fill="#101e2b" stroke="#406379"/>'
    b += text(936, 269, "A_", 57, MINT, 700, MONO, 'text-anchor="middle"') + '</g>'
    b += '<path class="scan" d="M853 225v49" stroke="#8fffd2" stroke-width="2"/>'
    for x, y, label in [(787, 131, "</> SOFTWARE"), (1008, 343, "{ } SYSTEMS"), (771, 388, "[*] SECURITY")]:
        b += f'<rect x="{x-10}" y="{y-19}" width="138" height="30" rx="8" fill="#111f2b" stroke="#355064"/>'
        b += text(x, y, label, 11, "#c7e5ee", family=MONO)
    b += text(49, 436, "B.Sc. COMPUTER SCIENCE", 10, muted, family=MONO, extra='letter-spacing="2"')
    b += text(1150, 436, "ALWAYS A WORK IN PROGRESS  /  ALWAYS MOVING FORWARD", 10, muted, family=MONO, extra='text-anchor="end" letter-spacing="1"')
    svg(f'hero-{"light" if light else "dark"}.svg', 1200, 460, b, "Hi, I'm Amp — aspiring software developer and cybersecurity enthusiast", "Animated orbital illustration and coding terminal. B.Sc. Computer Science student. Code. Connect. Keep learning.")


def icon_markup(slug, color):
    if slug == "tcpip":
        return '<g fill="none" stroke="#8fffd2" stroke-width="6"><path d="M64 35v28M25 85V63h78v22"/><rect x="43" y="6" width="42" height="29" rx="6"/><rect x="5" y="85" width="40" height="29" rx="6"/><rect x="83" y="85" width="40" height="29" rx="6"/></g>'
    if slug == "nmap":
        return '<g fill="none" stroke="#74dcff" stroke-width="5"><circle cx="64" cy="64" r="51"/><circle cx="64" cy="64" r="30" opacity=".5"/><path d="M64 13v51l35-35M13 64h102M64 64v51" opacity=".6"/><circle cx="81" cy="45" r="7" fill="#8fffd2" stroke="none"/></g>'
    source = ET.parse(ROOT / "assets/icons" / f"{slug}.svg").getroot()
    for node in source.iter():
        node.tag = node.tag.split("}")[-1]
    viewbox = source.attrib.get("viewBox", "0 0 128 128")
    content = "".join(ET.tostring(child, encoding="unicode") for child in source if child.tag != "title")
    # Simple Icons paths are monochrome, while Devicon keeps its original colors.
    return f'<svg width="128" height="128" viewBox="{viewbox}" fill="{color}">{content}</svg>'


def stack_tiles():
    for index, (slug, label, color) in enumerate(STACK):
        b = f'<rect x="1" y="1" width="126" height="146" rx="18" fill="#101a27" stroke="#2b3b4e"/>'
        b += f'<rect x="17" y="17" width="94" height="83" rx="15" fill="{color}" opacity=".055"/>'
        b += f'<g transform="translate(37 32) scale(.421875)">{icon_markup(slug, color)}</g>'
        b += text(64, 121, label, 12, "#e6f0fa", 600, extra='text-anchor="middle"')
        b += f'<path d="M45 136h38" stroke="{color}" stroke-width="2" stroke-linecap="round" class="pulse" style="animation-delay:-{index%4}s"/>'
        svg(f"tech-{slug}.svg", 128, 148, b, label, f"{label} — Amp's languages and tools")


def accents():
    svg("divider.svg", 1200, 28, '<path d="M0 14H1200" stroke="#41536a" stroke-opacity=".35"/><path d="M0 14H1200" stroke="url(#accent)" stroke-opacity=".7" class="trace"/>', "Animated section divider")
    b = '<rect x="1" y="1" width="1198" height="148" rx="20" fill="#0b111b" stroke="#25374a"/><rect x="1" y="1" width="1198" height="148" rx="20" fill="url(#grid)"/>'
    b += '<circle cx="55" cy="46" r="5" fill="#8fffd2" class="pulse"/>'
    b += text(73, 50, "LET'S BUILD SOMETHING MEANINGFUL.", 12, MINT, 500, MONO, 'letter-spacing="2"')
    b += text(48, 104, "Open to a 4-month internship.", 34, "#e9f1f7", 650)
    b += text(1149, 100, "SOFTWARE  +  SECURITY  +  CURIOSITY", 12, "#92a8bb", family=MONO, extra='text-anchor="end"')
    svg("footer.svg", 1200, 150, b, "Open to a 4-month internship — let's build something meaningful")


def api(path):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "Ampsoria-profile", "X-GitHub-Api-Version": "2022-11-28"}
    if os.environ.get("GH_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GH_TOKEN"]
    request = urllib.request.Request("https://api.github.com" + path, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def refresh():
    user = api(f"/users/{ACCOUNT}")
    repos = []
    page = 1
    while True:
        batch = api(f"/users/{ACCOUNT}/repos?per_page=100&type=owner&page={page}")
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    original = [r for r in repos if not r["fork"]]
    snapshot = {
        "account": ACCOUNT,
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "public_repos": user["public_repos"], "followers": user["followers"],
        "stars": sum(r["stargazers_count"] for r in original),
        "original_repos": len(original),
        "languages": dict(Counter(r["language"] for r in original if r["language"])),
        "recent": [{"name": r["name"], "language": r["language"] or "—", "pushed_at": r["pushed_at"][:10]} for r in sorted((r for r in original if r["pushed_at"] and r["name"] != ACCOUNT), key=lambda r: r["pushed_at"], reverse=True)[:4]],
    }
    # Write only after all requests succeed, retaining the previous snapshot on failure.
    destination = OUT / "github-data.json"
    temporary = destination.with_suffix(".tmp")
    temporary.write_text(json.dumps(snapshot, indent=2) + "\n")
    temporary.replace(destination)


def dashboard():
    data = json.loads((OUT / "github-data.json").read_text())
    b = '<rect x="1" y="1" width="1198" height="229" rx="20" fill="#0b111b" stroke="#25374a"/>'
    b += text(34, 40, "GITHUB / AT A GLANCE", 13, MINT, 600, MONO, 'letter-spacing="2"')
    b += text(1166, 40, data["updated_at"], 12, "#91a7bb", family=MONO, extra='text-anchor="end"')
    for index, (value, label) in enumerate([(data["public_repos"], "PUBLIC REPOSITORIES"), (data["original_repos"], "NON-FORK REPOSITORIES"), (data["stars"], "STARS · NON-FORK REPOS"), (data["followers"], "FOLLOWERS")]):
        x = 34 + index * 299
        b += text(x, 127, value, 62, "#edf7ff", 700, MONO)
        b += text(x, 164, label, 11, "#9cb3c5", family=MONO, extra='letter-spacing="1"')
        if index < 3:
            b += f'<path d="M{x+264} 77v97" stroke="#25374a"/>'
    b += text(34, 207, "PUBLIC GITHUB DATA  /  REFRESHED DAILY VIA GITHUB ACTIONS", 10, "#91a7bb", family=MONO, extra='letter-spacing="1"')
    svg("github-stats.svg", 1200, 230, b, f"GitHub statistics for {ACCOUNT}", f"Snapshot {data['updated_at']}: {data['public_repos']} public repositories, {data['original_repos']} non-fork repositories, {data['stars']} stars on non-fork repositories, {data['followers']} followers.")
    b = '<rect x="1" y="1" width="1198" height="311" rx="20" fill="#0b111b" stroke="#25374a"/>'
    b += text(34, 39, "LANGUAGE LANDSCAPE", 13, MINT, 600, MONO, 'letter-spacing="2"')
    b += text(34, 66, "Primary language · public non-fork repositories", 13, "#91a7bb")
    languages = sorted(data["languages"].items(), key=lambda item: (-item[1], item[0]))
    top = languages[:5]
    if len(languages) > 5:
        top.append(("Other", sum(count for _, count in languages[5:])))
    maximum = max((count for _, count in top), default=1)
    colors = [MINT, CYAN, "#c1a4ff", "#ffcf7a", "#ff99b7", "#9caec2"]
    for index, (language, count) in enumerate(top):
        y = 104 + index * 32
        b += text(34, y, language, 13, "#cfdeeb")
        b += f'<rect x="162" y="{y-11}" width="278" height="10" rx="5" fill="#213042"/><rect x="162" y="{y-11}" width="{278*count/maximum:.1f}" height="10" rx="5" fill="{colors[index]}"/>'
        b += text(473, y, count, 13, colors[index], family=MONO, extra='text-anchor="end"')
    b += '<path d="M531 32v248" stroke="#25374a"/>'
    b += text(565, 39, "RECENTLY PUSHED", 13, CYAN, 600, MONO, 'letter-spacing="2"')
    b += text(565, 66, "Public non-fork projects · profile repository excluded", 13, "#91a7bb")
    for index, repo in enumerate(data["recent"]):
        y = 111 + index * 49
        name = repo["name"] if len(repo["name"]) <= 44 else repo["name"][:41] + "…"
        b += f'<circle cx="570" cy="{y-5}" r="3" fill="{colors[index]}"/>'
        b += text(586, y, name, 14, "#e7eff6", 600)
        b += text(586, y+19, repo["language"] + "  /  " + repo["pushed_at"], 11, "#91a7bb", family=MONO)
    svg("github-activity.svg", 1200, 312, b, "Language landscape and recently pushed repositories", "Counts of primary repository languages, not skill levels or lines of code. Data timestamp is on the statistics card above.")
    # Separate narrow layouts keep text readable when GitHub scales images down.
    b = '<rect x="1" y="1" width="598" height="387" rx="20" fill="#0b111b" stroke="#25374a"/>'
    b += text(28, 38, "GITHUB / AT A GLANCE", 17, MINT, 600, MONO)
    for index, (value, label) in enumerate([(data["public_repos"], "Public repositories"), (data["original_repos"], "Non-fork repositories"), (data["stars"], "Stars · non-fork repos"), (data["followers"], "Followers")]):
        x, y = 28 + index % 2 * 298, 130 + index // 2 * 133
        b += text(x, y, value, 60, "#edf7ff", 700, MONO)
        b += text(x, y+32, label, 18, "#9cb3c5")
    b += text(28, 356, "Snapshot: " + data["updated_at"], 17, "#91a7bb", family=MONO)
    svg("github-stats-mobile.svg", 600, 389, b, "Public GitHub statistics", f"Snapshot: {data['updated_at']}")
    b = '<rect x="1" y="1" width="598" height="697" rx="20" fill="#0b111b" stroke="#25374a"/>'
    b += text(28, 42, "LANGUAGE LANDSCAPE", 19, MINT, 600, MONO)
    b += text(28, 74, "Primary language · public non-fork repositories", 18, "#91a7bb")
    for index, (language, count) in enumerate(top):
        y = 118 + index * 36
        b += text(28, y, language, 19, "#cfdeeb")
        b += f'<rect x="178" y="{y-13}" width="326" height="13" rx="6" fill="#213042"/><rect x="178" y="{y-13}" width="{326*count/maximum:.1f}" height="13" rx="6" fill="{colors[index]}"/>'
        b += text(558, y, count, 20, colors[index], family=MONO, extra='text-anchor="end"')
    b += '<path d="M28 332h544" stroke="#25374a"/>'
    b += text(28, 376, "RECENTLY PUSHED", 19, CYAN, 600, MONO)
    b += text(28, 405, "Public non-fork projects · profile excluded", 18, "#91a7bb")
    for index, repo in enumerate(data["recent"]):
        y = 451 + index * 61
        name = repo["name"] if len(repo["name"]) <= 38 else repo["name"][:35] + "…"
        b += text(28, y, name, 20, "#e7eff6", 600)
        b += text(28, y+26, repo["language"] + "  /  " + repo["pushed_at"], 17, "#91a7bb", family=MONO)
    svg("github-activity-mobile.svg", 600, 699, b, "Language landscape and recently pushed projects", "Primary language counts across public non-fork repositories, not proficiency.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true", help="Fetch current public GitHub statistics")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if args.refresh:
        refresh()
    hero()
    hero(light=True)
    stack_tiles()
    accents()
    dashboard()
    print(f"Built {len(list(OUT.glob('*.svg')))} SVG assets")


if __name__ == "__main__":
    main()
