"""Local sakura decorations and snapshot-driven extras; standard library only."""

from datetime import date
import json
import textwrap


STYLES = '''<style>
.sway{animation:sway 5s ease-in-out infinite;transform-box:fill-box;transform-origin:bottom center}
.breathe{animation:breathe 4s ease-in-out infinite;transform-box:fill-box;transform-origin:bottom center}
.tail{animation:tail 6s ease-in-out infinite;transform-box:fill-box;transform-origin:left bottom}
.steam{animation:steam 4s ease-in-out infinite}
.sparkle{animation:twinkle 5s ease-in-out infinite}
@keyframes sway{0%,100%{transform:rotate(-4deg)}50%{transform:rotate(4deg)}}
@keyframes breathe{0%,100%{transform:scaleY(1)}50%{transform:scaleY(1.025)}}
@keyframes tail{0%,100%{transform:rotate(0)}50%{transform:rotate(-10deg)}}
@keyframes steam{0%,100%{transform:translateY(0);opacity:.3}50%{transform:translateY(-9px);opacity:.7}}
@keyframes twinkle{0%,100%{opacity:.35}50%{opacity:1}}
@media(prefers-reduced-motion:reduce){.sway,.breathe,.tail,.steam,.sparkle{animation:none!important}}
</style>'''


NOTES = [
    "Small steps still count.",
    "Make something small. Make it yours.",
    "It's okay to pause and come back.",
    "Curiosity is a lovely place to start.",
    "A little progress, a little blossom.",
    "One idea can become something useful.",
    "Try, learn, and let the idea grow.",
]


def heart(x, y, scale=1, color="#d874a1"):
    return f'<path transform="translate({x} {y}) scale({scale})" d="M0 7C-26-10-15-29 0-17C15-29 26-10 0 7Z" fill="{color}"/>'


def panel(width, height, dark=False):
    bg, border = ("#281728", "#70415f") if dark else ("#fff2f7", "#edb8cf")
    return f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="26" fill="{bg}" stroke="{border}"/>'


def garden(svg, text, flower, data):
    count = max(0, int(data["original_repos"]))
    shown = min(count, 49)
    rows = max(1, (shown + 6) // 7)
    height = max(338, 172 + rows * 62)
    for dark in (False, True):
        foreground, muted = ("#ffe7f2", "#dfadc8") if dark else ("#843859", "#9c5274")
        b = STYLES + panel(640, height, dark)
        b += text(28, 43, "My little project garden", 29, foreground, 800)
        b += text(28, 76, f"{count} public non-fork repositories", 19, muted)
        b += '<path d="M25 94H615" stroke="#cd87ab" opacity=".35"/>'
        for index in range(shown):
            x, y = 60 + (index % 7) * 86, 121 + (index // 7) * 62
            color = ["#f7a8c9", "#e8b6ef", "#ffcad9"][index % 3]
            b += f'<g data-repo-flower="true" transform="translate({x} {y})"><g class="sway" style="animation-delay:-{index%7}s">'
            b += '<path d="M0 4v30M0 22q-13 2-15-8Q-3 11 0 22M0 27q12 1 14-8Q2 17 0 27" fill="#abd0b3" stroke="#83aa92" stroke-width="2"/>'
            b += flower(0, 0, .65, color) + '</g></g>'
        if shown == 0:
            b += text(320, 181, "A little garden, ready to grow.", 23, foreground, 800, extra='text-anchor="middle"')
        # Decorative soil is separate from the exact repository flower count.
        b += f'<path d="M26 {height-78}Q150 {height-90}320 {height-78}T614 {height-78}" fill="none" stroke="#adc6a7" stroke-width="3"/>'
        legend = "One flower = one repository" if count <= 49 else f"Showing 49 of {count} repositories"
        b += text(28, height-47, legend, 18, muted)
        b += text(28, height-20, "Snapshot: " + data["updated_at"], 15, muted)
        svg(f'project-garden-{"dark" if dark else "light"}.svg', 640, height, b,
            "Amp's repository garden", f"{count} public non-fork repositories; {shown} flowers shown. {legend}. Snapshot {data['updated_at']}. This is a repository count, not a contribution calendar.")


def build(svg, text, flower, out):
    data = json.loads((out / "github-data.json").read_text())
    garden(svg, text, flower, data)

    # A game-inspired card with factual profile details, not invented skill scores.
    b = panel(640, 402)
    b += '<rect x="16" y="16" width="608" height="370" rx="20" fill="none" stroke="#edb8cf" stroke-dasharray="3 7"/>'
    b += text(32, 53, "Amp's character card", 30, "#843859", 800)
    b += '<g class="pulse">' + heart(579, 52, .65) + '</g>'
    b += text(32, 91, "A curious developer, one chapter at a time.", 19, "#9c5274")
    rows = [(137, "Chapter", "4th-year Computer Science"),
            (185, "Campus", "Huachiew Chalermprakiet"),
            (252, "Interests", "Coding / systems / security"),
            (300, "Off-screen", "Calisthenics / games")]
    for y, label, value in rows:
        b += text(32, y, label, 18, "#a15379", 800)
        b += text(170, y, value, 21, "#843859", 800)
    b += text(170, 213, "University", 21, "#843859", 800)
    b += '<rect x="31" y="331" width="578" height="41" rx="20" fill="#f9dce9"/>'
    b += text(320, 359, "Friendly  ·  cooperative  ·  always learning", 18, "#843859", 800, extra='text-anchor="middle"')
    svg("character-card.svg", 640, 402, b, "Amp's developer character card", "4th-year Computer Science student at Huachiew Chalermprakiet University. Interests: coding, systems, security. Hobbies: calisthenics and games.")

    # A code-native mochi cat scene: gentle breathing, tail movement and tea steam.
    b = STYLES + panel(560, 320)
    b += text(280, 42, "Mochi's tiny break corner", 25, "#843859", 800, extra='text-anchor="middle"')
    b += '<ellipse cx="280" cy="236" rx="210" ry="19" fill="#f3d5e3"/>'
    b += '<rect x="113" y="212" width="278" height="26" rx="10" fill="#cf8aac" stroke="#aa6489" stroke-width="2"/>'
    b += '<path d="M221 216h57" stroke="#fce9f1" stroke-width="3" stroke-linecap="round"/>'
    b += '<g class="breathe"><path class="tail" d="M341 185Q393 210 399 174Q401 154 384 156" fill="none" stroke="#b67c91" stroke-width="24" stroke-linecap="round"/>'
    b += '<ellipse cx="269" cy="169" rx="102" ry="50" fill="#fff6eb" stroke="#b67c91" stroke-width="3"/>'
    b += '<path d="M147 156L139 99Q158 95 177 125L221 123Q238 96 251 104L247 163" fill="#fff6eb" stroke="#b67c91" stroke-width="3" stroke-linejoin="round"/>'
    b += '<path d="M150 116l6 23 13-8M230 131l12-15-2 25" fill="#f2b1c8"/>'
    b += '<ellipse cx="195" cy="164" rx="62" ry="45" fill="#fff6eb"/>'
    b += '<path d="M161 160q10-10 20 0M208 160q10-10 20 0M188 176q7 9 14 0" fill="none" stroke="#795565" stroke-width="3" stroke-linecap="round"/>'
    b += '<path d="M190 166h10l-5 6Z" fill="#d989a6"/><ellipse cx="157" cy="175" rx="10" ry="5" fill="#f8bed0"/><ellipse cx="232" cy="175" rx="10" ry="5" fill="#f8bed0"/>'
    b += '<ellipse cx="176" cy="209" rx="24" ry="10" fill="#fff6eb" stroke="#b67c91" stroke-width="2"/><ellipse cx="270" cy="211" rx="23" ry="9" fill="#fff6eb" stroke="#b67c91" stroke-width="2"/>'
    b += flower(237, 127, .37) + '</g>'
    b += '<path d="M433 170h38v47q-19 15-38 0Z" fill="#ead5f6" stroke="#b381a9" stroke-width="2"/><path d="M471 177q30 0 18 22q-7 7-18 4" fill="none" stroke="#b381a9" stroke-width="4"/>'
    b += '<g class="steam" stroke="#d096b4" stroke-width="3" fill="none" stroke-linecap="round"><path d="M441 153q-9-9 0-18t0-18M457 152q-9-9 0-18"/></g>'
    b += text(350, 107, "z z z", 19, "#a15379", 800)
    b += text(280, 287, "A little pause is part of the process.", 20, "#843859", 800, extra='text-anchor="middle"')
    svg("mochi-break.svg", 560, 320, b, "Mochi the sleeping cat", "An animated cream-colored cat naps on a pink laptop beside a warm cup. A little pause is part of the process.")

    # Date is the stored data snapshot's UTC date, so rebuilds are deterministic.
    snapshot_day = date.fromisoformat(data["updated_at"][:10])
    note = NOTES[snapshot_day.toordinal() % len(NOTES)]
    b = panel(640, 260)
    b += text(30, 45, "A little note for today", 27, "#843859", 800)
    b += '<g class="float"><rect x="35" y="99" width="128" height="91" rx="13" fill="#f4bfd5" stroke="#c67c9f" stroke-width="2"/><path d="M36 103l63 51 63-51M36 188l47-46M162 188l-47-46" fill="none" stroke="#c67c9f" stroke-width="2"/>'
    b += heart(99, 147, .65, "#bb658f") + '</g>'
    for index, line in enumerate(textwrap.wrap(note, 29)):
        b += text(195, 123 + index * 37, line, 24, "#843859", 800)
    b += text(30, 230, "Garden note · " + snapshot_day.isoformat(), 16, "#9c5274")
    b += flower(599, 216, .6)
    svg("daily-note.svg", 640, 260, b, "Daily sakura note", f"{snapshot_day.isoformat()}: {note} Changes with the daily data refresh; not a live clock.")

    b = ''
    for index in range(7):
        x, y = 30 + index * 80, 30 if index % 2 else 47
        b += f'<g transform="translate({x} {y}) rotate({-12 if index%2 else 12})"><g class="pulse" style="animation-delay:-{index*.5}s" fill="#d38cae"><ellipse cy="6" rx="10" ry="8"/><ellipse cx="-12" cy="-6" rx="4" ry="6"/><ellipse cx="-4" cy="-12" rx="4" ry="6"/><ellipse cx="5" cy="-12" rx="4" ry="6"/><ellipse cx="13" cy="-5" rx="4" ry="6"/></g></g>'
    svg("paw-trail.svg", 560, 80, b, "Follow the tiny paw prints", "A decorative trail of seven softly pulsing pink paw prints.")

    b = panel(560, 215)
    b += '<circle cx="86" cy="104" r="49" fill="#f7d5e4" stroke="#d590b1" stroke-width="2" stroke-dasharray="4 5"/>'
    b += '<g class="pulse">' + heart(86, 113, 1.2) + '</g>'
    b += text(161, 78, "Tiny secret found!", 28, "#843859", 800)
    b += text(161, 117, "Achievement: curiosity", 20, "#9c5274", 800)
    b += text(161, 151, "Thanks for wandering by.", 18, "#9c5274")
    b += flower(520, 177, .65)
    svg("secret-stamp.svg", 560, 215, b, "Tiny secret found — achievement: curiosity", "A playful decorative Easter egg, not a professional certificate.")

    buttons = [
        ("source", "Source code", 165), ("demo", "Watch demo", 172),
        ("live", "Explore live demo", 214), ("resume", "View my resume", 208),
        ("gallery", "Explore the gallery", 229), ("email", "Email", 108),
        ("github", "GitHub", 120), ("line", "LINE", 105),
        ("phone", "+66 65-498-6129", 214),
    ]
    for name, label, width in buttons:
        b = panel(width, 44)
        b += flower(23, 22, .3)
        b += text((width+30)/2, 28, label, 16, "#843859", 800, extra='text-anchor="middle"')
        svg(f"button-{name}.svg", width, 44, b, label)
