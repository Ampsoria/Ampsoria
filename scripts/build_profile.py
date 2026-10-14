#!/usr/bin/env python3
"""Build self-contained README SVGs; optionally refresh public GitHub data.

Standard library only. Run from any directory. No remote image dependencies.
"""

import argparse
import base64
import re
from collections import Counter
from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
import urllib.request
import xml.etree.ElementTree as ET
from profile_extras import build as build_extras

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/generated"
ACCOUNT = "Ampsoria"
PINK = "#ffacd0"
LILAC = "#dbb4ff"
FONT = "'Arial Rounded MT Bold', 'Trebuchet MS', sans-serif"
MONO = FONT
GLYPHS = json.loads((ROOT / "assets/fonts/glyphs.json").read_text())
USED_GLYPHS = {}
STACK = [
    ("java", "Java", "#f89820"), ("python", "Python", "#ffd343"),
    ("c", "C", "#77a9ff"), ("csharp", "C#", "#a179dc"), ("php", "PHP", "#aaa5ff"),
    ("javascript", "JavaScript", "#f7df1e"),
    ("html5", "HTML5", "#ff7954"), ("css3", "CSS3", "#65baff"),
    ("react", "React", "#61dafb"), ("nodejs", "Node.js", "#8cce7a"),
    ("aspnet", "ASP.NET", "#8a65d2"), ("blazor", "Blazor", "#9d78dd"),
    ("sqlserver", "SQL Server", "#cd657b"), ("mvc", "MVC", "#bc70a0"),
    ("mysql", "MySQL", "#77c7ed"), ("firebase", "Firebase", "#ffcb4c"),
    ("git", "Git", "#ff806a"), ("docker", "Docker", "#59baff"),
    ("n8n", "n8n", "#ff8097"), ("linux", "Linux", "#ffde69"),
    ("windows", "Windows", "#64baff"),
    ("raspberrypi", "Raspberry Pi", "#f76c9e"), ("esp32", "ESP32", "#ff7676"),
    ("yolo", "YOLO", "#72f5eb"), ("roboflow", "Roboflow", "#bc95ff"),
    ("tcpip", "TCP / IP", "#ffacd0"), ("nmap", "Nmap", "#dbb4ff"),
]


def text(x, y, value, size=16, color="#fff0f6", weight=400, family=FONT, extra=""):
    """Use local rounded font outlines, retaining labels for accessibility."""
    value = str(value)
    font_weight = "800" if weight >= 650 else "600"
    font = GLYPHS[font_weight]
    if any(char not in font["glyphs"] for char in value):
        return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-family="{family}" {extra}>{escape(value)}</text>'
    scale = size / font["units"]
    match = re.search(r'letter-spacing="([^"]+)"', extra)
    spacing = float(match.group(1)) if match else 0
    width = sum(font["glyphs"][char]["advance"] * scale for char in value) + max(0, len(value)-1) * spacing
    if 'text-anchor="middle"' in extra:
        x -= width / 2
    elif 'text-anchor="end"' in extra:
        x -= width
    parts = [f'<g fill="{color}" role="img" aria-label="{escape(value, quote=True)}"><title>{escape(value)}</title>']
    for char in value:
        glyph = font["glyphs"][char]
        if glyph["path"]:
            key = f'font-{font_weight}-{ord(char)}'
            USED_GLYPHS[key] = glyph["path"]
            parts.append(f'<use href="#{key}" transform="translate({x:.2f} {y}) scale({scale:.5f} {-scale:.5f})"/>')
        x += glyph["advance"] * scale + spacing
    return "".join(parts) + '</g>'


def flower(x, y, size=1, color="#ffc2d9"):
    petals = ''.join(f'<ellipse cx="0" cy="-11" rx="7" ry="11" transform="rotate({angle})"/>' for angle in range(0, 360, 72))
    return f'<g transform="translate({x} {y}) scale({size})" fill="{color}">{petals}<circle r="4" fill="#ffdc9f"/><circle r="2" fill="#c87996"/></g>'


def petals(width, height, count=18):
    result = []
    for i in range(count):
        x, y = 24 + (i * 137) % (width-48), (i * 79) % height
        color = ["#ff9fc9", "#ffd1e3", "#eeb4e5"][i % 3]
        result.append(f'<g transform="translate({x} {y})"><g class="petal" style="animation-delay:-{i * 1.73:.2f}s;animation-duration:{13+i%5}s"><path d="M0 0C-15-13-5-28 5-20C19-17 13-4 0 0Z" fill="{color}" opacity=".55"/></g></g>')
    return ''.join(result)


def svg(name, width, height, body, title, description=""):
    document = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description or title)}</desc>
<defs>
{"".join(f'<path id="{key}" d="{path}"/>' for key, path in USED_GLYPHS.items())}
  <clipPath id="frame"><rect width="{width}" height="{height}" rx="24"/></clipPath>
  <linearGradient id="accent"><stop stop-color="{PINK}"/><stop offset=".55" stop-color="{LILAC}"/><stop offset="1" stop-color="#b8a2ff"/></linearGradient>
  <radialGradient id="aura"><stop stop-color="#d56caa" stop-opacity=".5"/><stop offset="1" stop-color="#251524" stop-opacity="0"/></radialGradient>
  <pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" fill="none" stroke="#ffb2d5" stroke-opacity=".055"/></pattern>
</defs>
<style>
  .petal {{animation:petal-fall 15s linear infinite}}
  @keyframes petal-fall {{0% {{transform:translate(-30px,-500px) rotate(0deg);opacity:0}} 12%,85% {{opacity:1}} 100% {{transform:translate(80px,500px) rotate(230deg);opacity:0}}}}
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
  @media (prefers-reduced-motion:reduce) {{.orbit,.pulse,.float,.scan,.blink,.trace,.petal {{animation:none!important}}}}
</style>
{body}
</svg>'''
    ET.fromstring(document)
    (OUT / name).write_text(document + "\n")
    USED_GLYPHS.clear()


def hero(light=False):
    bg, fg, muted, edge = ("#fff2f7", "#843859", "#9c5274", "#edb8cf") if light else ("#281728", "#ffe7f2", "#dfadc8", "#70415f")
    b = f'<rect x="1" y="1" width="1198" height="498" rx="24" fill="{bg}" stroke="{edge}"/>'
    b += '<g clip-path="url(#frame)">'
    b += '<ellipse cx="981" cy="270" rx="300" ry="270" fill="#e79abf" opacity=".10"/>'
    b += '<ellipse cx="938" cy="290" rx="196" ry="185" fill="#f2abc9" opacity=".12"/>'
    b += f'<path d="M1208 28C1090 21 1070 82 1001 96M1125 43l-45-30M1101 58l16 49M1040 89l-31-27" fill="none" stroke="{muted}" stroke-width="5" stroke-linecap="round" opacity=".45"/>'
    for x,y,z in [(1152,35,1.3),(1084,15,.9),(1108,98,1.1),(1008,61,1),(1048,86,.7),(1192,78,1)]:
        b += flower(x,y,z)
    b += text(52, 49, "AMPSORIA  /  SAKURA EDITION", 15, muted, 800, extra='letter-spacing="2"')
    b += text(52, 121, "A little curiosity. A lot of heart.", 22, muted, 600)
    b += text(48, 205, "Hello, I'm Amp!", 78, fg, 800, extra='letter-spacing="-2"')
    b += text(52, 258, "Code. Connect. Keep blooming.", 32, muted, 800)
    b += text(52, 299, "Aspiring Software Developer & Cybersecurity Enthusiast", 18, muted)
    b += '<rect x="52" y="338" width="615" height="91" rx="24" fill="#743954" opacity=".12"/>'
    b += text(76, 367, "a tiny developer diary", 14, muted, 800, extra='letter-spacing="1"')
    b += text(76, 403, "> building skills, one project at a time", 21, fg, 600)
    b += f'<rect x="452" y="384" width="9" height="22" rx="3" fill="{muted}" class="blink"/>'
    portrait = base64.b64encode((ROOT / 'assets/illustrations/sakura-coder.png').read_bytes()).decode('ascii')
    b += f'<g class="float"><image x="748" y="86" width="412" height="380" href="data:image/png;base64,{portrait}"/></g>'
    b += petals(1200, 500)
    b += text(52, 468, "4th-year B.Sc. Computer Science  /  Learning one day at a time", 15, muted)
    b += '</g>'
    svg(f'hero-{"light" if light else "dark"}.svg', 1200, 500, b, "Hi, I'm Amp — aspiring software developer and cybersecurity enthusiast", "Pink sakura garden with falling petals, a floating original anime programmer mascot and rounded Nunito lettering. 4th-year B.Sc. Computer Science student.")


def icon_markup(slug, color):
    if slug == "mvc":
        # A custom three-component diagram, not a product or vendor logo.
        return ('<g fill="none" stroke="#bc70a0" stroke-width="5" stroke-linejoin="round">'
                '<path d="M51 38L30 78M77 38l21 40M42 96h44"/>'
                '<rect x="43" y="6" width="42" height="36" rx="10" fill="#f9d9e8"/>'
                '<rect x="3" y="79" width="42" height="36" rx="10" fill="#ead5f6"/>'
                '<rect x="83" y="79" width="42" height="36" rx="10" fill="#f9d9e8"/>'
                '</g>' + text(64, 32, "M", 22, "#843859", 800, extra='text-anchor="middle"')
                + text(24, 104, "V", 22, "#843859", 800, extra='text-anchor="middle"')
                + text(104, 104, "C", 22, "#843859", 800, extra='text-anchor="middle"'))
    if slug == "tcpip":
        return '<g fill="none" stroke="#ffacd0" stroke-width="6"><path d="M64 35v28M25 85V63h78v22"/><rect x="43" y="6" width="42" height="29" rx="6"/><rect x="5" y="85" width="40" height="29" rx="6"/><rect x="83" y="85" width="40" height="29" rx="6"/></g>'
    if slug == "nmap":
        return '<g fill="none" stroke="#dbb4ff" stroke-width="5"><circle cx="64" cy="64" r="51"/><circle cx="64" cy="64" r="30" opacity=".5"/><path d="M64 13v51l35-35M13 64h102M64 64v51" opacity=".6"/><circle cx="81" cy="45" r="7" fill="#ffacd0" stroke="none"/></g>'
    source = ET.parse(ROOT / "assets/icons" / f"{slug}.svg").getroot()
    for node in source.iter():
        node.tag = node.tag.split("}")[-1]
    viewbox = source.attrib.get("viewBox", "0 0 128 128")
    content = "".join(ET.tostring(child, encoding="unicode") for child in source if child.tag != "title")
    # Simple Icons paths are monochrome, while Devicon keeps its original colors.
    return f'<svg width="128" height="128" viewBox="{viewbox}" fill="{color}">{content}</svg>'


def stack_tiles():
    for index, (slug, label, color) in enumerate(STACK):
        b = f'<rect x="1" y="1" width="126" height="146" rx="18" fill="#fff2f7" stroke="#f0bbd2"/>'
        b += f'<rect x="17" y="17" width="94" height="83" rx="15" fill="{color}" opacity=".055"/>'
        b += f'<g transform="translate(37 32) scale(.421875)">{icon_markup(slug, color)}</g>'
        b += flower(110, 18, .28)
        b += text(64, 121, label, 13, "#763754", 800, extra='text-anchor="middle"')
        b += f'<path d="M45 136h38" stroke="{color}" stroke-width="2" stroke-linecap="round" class="pulse" style="animation-delay:-{index%4}s"/>'
        svg(f"tech-{slug}.svg", 128, 148, b, label, f"{label} — Amp's languages and tools")


def accents():
    badge = '<rect x="1" y="1" width="338" height="42" rx="21" fill="#fff2f7" stroke="#edb8cf"/>'
    badge += flower(25, 22, .32)
    badge += text(183, 28, "Learning · building · growing", 16, "#843859", 800, extra='text-anchor="middle"')
    svg("welcome-badge.svg", 340, 44, badge, "Learning · building · growing", "Decorative welcome badge; not a visitor counter.")
    b = '<path d="M0 24H545M655 24H1200" stroke="url(#accent)" stroke-opacity=".65" stroke-width="2" class="trace"/>'
    b += flower(600, 24, .8) + flower(560, 24, .35) + flower(640, 24, .35)
    svg("divider.svg", 1200, 48, b, "Sakura blossom divider")
    b = '<rect x="1" y="1" width="1198" height="178" rx="28" fill="#fff2f7" stroke="#edb8cf"/>'
    b += text(44, 53, "Let's connect and share ideas.", 24, "#a15379", 800)
    b += text(44, 113, "Growing through code & curiosity.", 40, "#843859", 800)
    b += text(44, 151, "Software  +  security  +  a little curiosity", 18, "#a15379")
    b += '<g clip-path="url(#frame)">' + petals(1200, 180, 12)
    for x,y,size in [(1030,72,1.8),(1110,114,1),(1139,46,.7)]:
        b += flower(x,y,size)
    b += '</g>'
    svg("footer.svg", 1200, 180, b, "Growing through code & curiosity — connect with Amp")


def portrait_frame():
    """Frame the unchanged original photograph with a local sakura SVG."""
    photograph = base64.b64encode((ROOT / "ampreadme.png").read_bytes()).decode("ascii")
    b = '<defs><clipPath id="portrait-window"><rect x="32" y="34" width="360" height="369" rx="22"/></clipPath></defs>'
    b += '<rect x="5" y="5" width="414" height="430" rx="34" fill="#fff2f7" stroke="#dfa2bf" stroke-width="3"/>'
    b += '<rect x="15" y="15" width="394" height="410" rx="27" fill="none" stroke="#edb8cf" stroke-width="2" stroke-dasharray="3 7"/>'
    b += '<rect x="27" y="29" width="370" height="379" rx="27" fill="#ffffff" stroke="#efc7d9" stroke-width="2"/>'
    b += f'<image x="32" y="34" width="360" height="369" preserveAspectRatio="xMidYMid meet" clip-path="url(#portrait-window)" href="data:image/png;base64,{photograph}"/>'
    b += flower(395, 29, 1.0) + flower(30, 401, .95)
    b += flower(369, 17, .4) + flower(51, 422, .38)
    b += '<path d="M188 421h48" stroke="#d38cae" stroke-width="3" stroke-linecap="round"/>'
    svg("portrait-framed.svg", 424, 440, b, "Amp — Gorrawit Puttabarramee", "Original profile photograph with rounded corners and a pink sakura frame.")


def character_ribbons():
    """Compact matching section decorations with self-contained mascot images."""
    layouts = [
        ("study", "A little toolkit.", "A lot of curiosity.", "Learn / experiment / grow", False),
        ("maker", "Small ideas.", "Real-world projects.", "Explore / build / improve", True),
    ]
    for character, line1, line2, caption, right in layouts:
        image_x, text_x = (490, 36) if right else (24, 254)
        art = base64.b64encode((ROOT / f'assets/illustrations/sakura-{character}.png').read_bytes()).decode('ascii')
        b = '<rect x="1" y="1" width="718" height="218" rx="30" fill="#fff2f7" stroke="#edb8cf"/>'
        b += '<rect x="9" y="9" width="702" height="202" rx="24" fill="none" stroke="#f0c2d8" stroke-dasharray="3 7"/>'
        b += f'<ellipse cx="{image_x+100}" cy="112" rx="103" ry="96" fill="#fbe0ec"/>'
        b += f'<g class="float"><image x="{image_x}" y="12" width="200" height="196" href="data:image/png;base64,{art}"/></g>'
        b += text(text_x, 83, line1, 31, "#843859", 800)
        b += text(text_x, 126, line2, 31, "#843859", 800)
        b += text(text_x, 165, caption, 17, "#a15379", 600)
        b += '<g clip-path="url(#frame)">' + petals(720, 220, 7) + '</g>'
        b += flower(684 if not right else 452, 38, .55)
        svg(f"{character}-ribbon.svg", 720, 220, b, line1 + " " + line2,
            "Original male anime sakura mascot, softly floating with falling petals. " + caption + ".")


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
    b = '<rect x="1" y="1" width="1198" height="229" rx="20" fill="#251524" stroke="#70405f"/>'
    b += text(34, 40, "GITHUB / AT A GLANCE", 13, PINK, 600, MONO, 'letter-spacing="2"')
    b += text(1166, 40, data["updated_at"], 12, "#dcb5c9", family=MONO, extra='text-anchor="end"')
    for index, (value, label) in enumerate([(data["public_repos"], "PUBLIC REPOSITORIES"), (data["original_repos"], "NON-FORK REPOSITORIES"), (data["stars"], "STARS · NON-FORK REPOS"), (data["followers"], "FOLLOWERS")]):
        x = 34 + index * 299
        b += text(x, 127, value, 62, "#fff0f6", 700, MONO)
        b += text(x, 164, label, 11, "#e2b9cd", family=MONO, extra='letter-spacing="1"')
        if index < 3:
            b += f'<path d="M{x+264} 77v97" stroke="#70405f"/>'
    b += text(34, 207, "PUBLIC GITHUB DATA  /  REFRESHED DAILY VIA GITHUB ACTIONS", 10, "#dcb5c9", family=MONO, extra='letter-spacing="1"')
    svg("github-stats.svg", 1200, 230, b, f"GitHub statistics for {ACCOUNT}", f"Snapshot {data['updated_at']}: {data['public_repos']} public repositories, {data['original_repos']} non-fork repositories, {data['stars']} stars on non-fork repositories, {data['followers']} followers.")
    b = '<rect x="1" y="1" width="1198" height="311" rx="20" fill="#251524" stroke="#70405f"/>'
    b += text(34, 39, "LANGUAGE LANDSCAPE", 13, PINK, 600, MONO, 'letter-spacing="2"')
    b += text(34, 66, "Primary language · public non-fork repositories", 13, "#dcb5c9")
    languages = sorted(data["languages"].items(), key=lambda item: (-item[1], item[0]))
    top = languages[:5]
    if len(languages) > 5:
        top.append(("Other", sum(count for _, count in languages[5:])))
    maximum = max((count for _, count in top), default=1)
    colors = [PINK, LILAC, "#e9b8ff", "#ffcfdb", "#ff95c4", "#c3a2ca"]
    for index, (language, count) in enumerate(top):
        y = 104 + index * 32
        b += text(34, y, language, 13, "#f8dce9")
        b += f'<rect x="162" y="{y-11}" width="278" height="10" rx="5" fill="#553149"/><rect x="162" y="{y-11}" width="{278*count/maximum:.1f}" height="10" rx="5" fill="{colors[index]}"/>'
        b += text(473, y, count, 13, colors[index], family=MONO, extra='text-anchor="end"')
    b += '<path d="M531 32v248" stroke="#70405f"/>'
    b += text(565, 39, "RECENTLY PUSHED", 13, LILAC, 600, MONO, 'letter-spacing="2"')
    b += text(565, 66, "Public non-fork projects · profile repository excluded", 13, "#dcb5c9")
    for index, repo in enumerate(data["recent"]):
        y = 111 + index * 49
        name = repo["name"] if len(repo["name"]) <= 44 else repo["name"][:41] + "…"
        b += f'<circle cx="570" cy="{y-5}" r="3" fill="{colors[index]}"/>'
        b += text(586, y, name, 14, "#ffeaf4", 600)
        b += text(586, y+19, repo["language"] + "  /  " + repo["pushed_at"], 11, "#dcb5c9", family=MONO)
    svg("github-activity.svg", 1200, 312, b, "Language landscape and recently pushed repositories", "Counts of primary repository languages, not skill levels or lines of code. Data timestamp is on the statistics card above.")
    # Separate narrow layouts keep text readable when GitHub scales images down.
    b = '<rect x="1" y="1" width="598" height="387" rx="20" fill="#251524" stroke="#70405f"/>'
    b += text(28, 38, "GITHUB / AT A GLANCE", 17, PINK, 600, MONO)
    for index, (value, label) in enumerate([(data["public_repos"], "Public repositories"), (data["original_repos"], "Non-fork repositories"), (data["stars"], "Stars · non-fork repos"), (data["followers"], "Followers")]):
        x, y = 28 + index % 2 * 298, 130 + index // 2 * 133
        b += text(x, y, value, 60, "#fff0f6", 700, MONO)
        b += text(x, y+32, label, 18, "#e2b9cd")
    b += text(28, 356, "Snapshot: " + data["updated_at"], 17, "#dcb5c9", family=MONO)
    svg("github-stats-mobile.svg", 600, 389, b, "Public GitHub statistics", f"Snapshot: {data['updated_at']}")
    b = '<rect x="1" y="1" width="598" height="697" rx="20" fill="#251524" stroke="#70405f"/>'
    b += text(28, 42, "LANGUAGE LANDSCAPE", 19, PINK, 600, MONO)
    b += text(28, 74, "Primary language · public non-fork repositories", 18, "#dcb5c9")
    for index, (language, count) in enumerate(top):
        y = 118 + index * 36
        b += text(28, y, language, 19, "#f8dce9")
        b += f'<rect x="178" y="{y-13}" width="326" height="13" rx="6" fill="#553149"/><rect x="178" y="{y-13}" width="{326*count/maximum:.1f}" height="13" rx="6" fill="{colors[index]}"/>'
        b += text(558, y, count, 20, colors[index], family=MONO, extra='text-anchor="end"')
    b += '<path d="M28 332h544" stroke="#70405f"/>'
    b += text(28, 376, "RECENTLY PUSHED", 19, LILAC, 600, MONO)
    b += text(28, 405, "Public non-fork projects · profile excluded", 18, "#dcb5c9")
    for index, repo in enumerate(data["recent"]):
        y = 451 + index * 61
        name = repo["name"] if len(repo["name"]) <= 38 else repo["name"][:35] + "…"
        b += text(28, y, name, 20, "#ffeaf4", 600)
        b += text(28, y+26, repo["language"] + "  /  " + repo["pushed_at"], 17, "#dcb5c9", family=MONO)
    svg("github-activity-mobile.svg", 600, 699, b, "Language landscape and recently pushed projects", "Primary language counts across public non-fork repositories, not proficiency.")


def gallery_banner():
    """A clickable gallery cover; all navigation stays in README markup."""
    b = '<rect x="1" y="1" width="718" height="298" rx="24" fill="#251524" stroke="#e796bd" stroke-width="2"/>'
    b += '<rect width="720" height="300" rx="24" fill="url(#grid)"/>'
    b += '<ellipse cx="635" cy="80" rx="170" ry="150" fill="url(#aura)"/>'
    b += text(32, 37, "THE PORTFOLIO EDIT", 14, PINK, 800, extra='letter-spacing="2"')
    b += text(32, 88, "My work. My journey.", 40, "#fff0f6", 800)
    b += text(32, 119, "A gallery of experiences, milestones & moments.", 19, "#e2b9cd")
    for x, label, subtitle in [(32, "Competitions", "Ideas put to the test"),
                               (255, "Certificates", "Learning in action"),
                               (478, "Activities", "Beyond the classroom")]:
        b += f'<rect x="{x}" y="145" width="210" height="70" rx="14" fill="#3b2336" stroke="#80506a"/>'
        b += text(x+15, 174, label, 20, "#ffcee3", 800)
        b += text(x+15, 198, subtitle, 14, "#e2b9cd")
    b += '<rect x="32" y="235" width="258" height="44" rx="22" fill="url(#accent)"/>'
    b += text(161, 264, "Explore my gallery  >", 19, "#44213a", 800, extra='text-anchor="middle"')
    b += text(320, 263, "Photos / stories / achievements", 16, "#e2b9cd")
    b += '<g class="pulse">' + flower(666, 51, .9) + flower(690, 114, .45) + '</g>'
    svg("gallery-showcase.svg", 720, 300, b, "Explore Amp's portfolio gallery",
        "Competitions, certificates and activities. Open the gallery for photos and stories.")


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
    gallery_banner()
    portrait_frame()
    character_ribbons()
    dashboard()
    build_extras(svg=svg, text=text, flower=flower, out=OUT)
    print(f"Built {len(list(OUT.glob('*.svg')))} SVG assets")


if __name__ == "__main__":
    main()
