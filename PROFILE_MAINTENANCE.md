# Profile artwork

The README uses local, self-contained SVG artwork. Original profile information,
all four projects, all 22 stack entries, and the original destination links are
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
CSS; `prefers-reduced-motion` disables it without hiding any information. There
are no scripts, external fonts, or externally loaded images inside the SVGs.

The header uses `<picture>` for light/dark variants. Tech cards wrap individually
on narrow screens. Navigation, contact links, and the expandable activity panel
use native GitHub README markup. Shields.io buttons and the existing Komarev view
counter remain external services; local artwork does not depend on them.

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
they are not presented as official logos.
