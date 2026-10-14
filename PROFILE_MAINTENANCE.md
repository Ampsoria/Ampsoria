# Profile artwork

The README uses local, self-contained SVG artwork. Original profile information,
all four projects, the original stack entries, and the original destination links are
preserved. The original portrait and banner files are retained.

## Rebuild

Python 3.9+ and its standard library are sufficient. From the repository root:

```sh
python3 scripts/build_profile.py          # Rebuild using the checked-in snapshot
python3 scripts/build_profile.py --refresh # Fetch public GitHub data, then rebuild
python3 -m unittest discover -s scripts -p 'test_*.py' -v
```

Edit `scripts/build_profile.py` for artwork, colors, labels, or layouts. Generated
SVGs live in `assets/generated/`. Their `<title>` and `<desc>` elements supply
accessible descriptions. README images also provide alt text. Animation uses SVG
CSS; `prefers-reduced-motion` disables it without hiding any information. The sakura hero embeds the original mascot PNG as a data URI. There are no
scripts, external fonts, or externally loaded images inside the SVGs.

The header uses `<picture>` for light/dark variants. Tech cards wrap individually
on narrow screens. Navigation, contact links, and the expandable activity panel
use native GitHub README markup. All README buttons and artwork are now local assets, including the former
Shields.io buttons. The README does not hotlink any external images. The header uses a local decorative welcome badge. The external Komarev
visitor counter was removed after repeated loading failures; the replacement
does not display or claim a visitor count.

## Automatic refresh

After these files are pushed to `main`, `.github/workflows/profile.yml` refreshes
public data daily at approximately **09:23 Asia/Bangkok (02:23 UTC)**. It also runs
when its source files change and supports **Actions → Refresh profile artwork →
Run workflow**. It uses the repository's built-in `GITHUB_TOKEN`; no personal
access token or extra secret is required. An optional local `GH_TOKEN` can avoid
the anonymous GitHub API rate limit. Never store tokens in this repository.

GitHub Actions must be enabled. Repository rules must permit the workflow's bot
to push the generated files to `main`; otherwise its final push will fail visibly
and the checked-in artwork remains available. GitHub may delay scheduled runs or
disable schedules on inactive public repositories. Trigger a manual run to check
the workflow after publication. The remote workflow cannot run before publication.

Statistics use the public GitHub REST API:

- Public repository and follower totals come from the user endpoint.
- Non-fork repositories and their stars are counted across all repository pages.
- Language bars count primary languages of public non-fork repositories with a
  detected language. They do not measure proficiency, commits, or lines of code.
- Recent projects are sorted by `pushed_at`, excluding forks and this profile.
- The card shows the snapshot time in UTC. Failed requests preserve the previous
  snapshot instead of overwriting it with empty or invented statistics.

## Icon attribution

Brand icons come from [Devicon](https://github.com/devicons/devicon) (MIT) and
[Simple Icons](https://github.com/simple-icons/simple-icons) (CC0). Pinned upstream
commits and individual source URLs are recorded in `assets/icons/sources.json`.
License texts are included alongside those sources. Brand marks remain the
property of their owners. TCP/IP and Nmap use custom network/radar illustrations;
they are not presented as official logos. MVC uses a custom three-component
Model–View–Controller diagram. The ASP.NET card uses the .NET ecosystem logo.


## Sakura theme and typography

The theme uses blush pink, rose, and plum, with drifting sakura petals, blossom
separators, an animated mascot, and pale pink tech cards. Light/dark hero variants
and mobile statistics layouts are preserved. Original brand logos retain their
source colors. All motion respects `prefers-reduced-motion`.

[Nunito](https://github.com/google/fonts/tree/main/ofl/nunito) is licensed under
SIL OFL 1.1; the original font, license, source commit, and prepared glyph outlines
live in `assets/fonts/`. SVG lettering is rendered as paths with accessible labels,
so it looks consistent without downloading fonts. GitHub controls the font of
normal README body text. The daily build still uses only Python's standard library.
To prepare glyphs again after intentionally updating the font, install `fonttools`
in a separate environment and run `python scripts/prepare_font.py` once. Commit the
resulting `assets/fonts/glyphs.json` alongside the font source.

The original anime mascot is `assets/illustrations/sakura-coder.png`, generated
with the built-in image generation tool. Its exact prompt is recorded in
`assets/illustrations/README.md`. The transparent original is embedded directly in
the hero SVGs; no image-generation service is called by scheduled builds.

## Section companions

The README now identifies Amp as a **4th-year** Computer Science student, including
its introduction and both hero variants. `character_ribbons()` builds the study
and maker ribbons from `sakura-study.png` and `sakura-maker.png`. The study ribbon
introduces the Tech Stack; the maker ribbon introduces Projects. A small waving
mascot also decorates the contact section. All original PNGs and exact generation
prompts are in `assets/illustrations/`. Ribbons have rounded Nunito lettering,
falling petals and gentle floating motion, with reduced-motion support.


## Cozy extras

`scripts/profile_extras.py` builds all new extras through the existing SVG/font
renderer. It adds no network requests, dependencies, tracking, or user scripts.

- **Character card:** an expandable game-inspired presentation of existing facts;
  no invented skill scores, credentials, or employment status.
- **Adventure menu:** native GitHub `<details>` links to code, the Shanghai guide,
  and the cozy corner. It works without JavaScript.
- **Project garden:** one gently swaying flower per public non-fork repository,
  using `original_repos` from `github-data.json`. Display caps at 49 flowers and
  explicitly labels the cap when necessary. This is not a contribution calendar.
  Light/dark versions show the same count and snapshot time.
- **Mochi:** a small original SVG cat animation, with breathing, a moving tail and
  tea steam. It is decorative, not an interactive pet application.
- **Daily note:** one of seven short messages selected deterministically from the
  snapshot's UTC calendar date, and refreshed by the existing daily workflow.
  No claim of real-time updates or personal predictions.
- **Secret corner:** a paw-print trail and a nested click-to-reveal souvenir stamp.
  The playful achievement is not a professional certificate.
- **Local buttons:** repository, demo, resume, gallery and contact links use local
  pink SVG buttons. Destination URLs and accessible labels remain unchanged.

All animation honors `prefers-reduced-motion`; all meaningful images have alt text.
The supplementary panels are collapsible to keep the main profile readable.


## Portrait frame

`portrait_frame()` embeds the unchanged `ampreadme.png` inside a rounded pink
SVG frame with a dotted inner border and sakura corner flowers. The README's
About section uses `assets/generated/portrait-framed.svg`. Updating the original
photo triggers the artwork workflow; the original file is never overwritten.
