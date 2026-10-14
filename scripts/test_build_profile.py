"""Check aggregation and failure safety without network access."""

import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET
from unittest.mock import patch

import build_profile as profile
import profile_extras


def repo(name, *, fork=False, language="Python", stars=1, pushed="2026-01-01T00:00:00Z"):
    return {"name": name, "fork": fork, "language": language, "stargazers_count": stars, "pushed_at": pushed}


class RefreshTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.out = Path(self.temp.name)
        self.patch_out = patch.object(profile, "OUT", self.out)
        self.patch_out.start()
        self.addCleanup(self.patch_out.stop)

    def test_forks_empty_languages_and_profile_activity(self):
        repos = [repo("real-project", stars=7), repo("forked", fork=True, stars=100), repo("notes", language=None), repo("Ampsoria", language=None)]
        with patch.object(profile, "api", side_effect=[{"public_repos": 4, "followers": 2}, repos]):
            profile.refresh()
        data = json.loads((self.out / "github-data.json").read_text())
        self.assertEqual(data["stars"], 9)
        self.assertEqual(data["original_repos"], 3)
        self.assertEqual(data["languages"], {"Python": 1})
        self.assertEqual([r["name"] for r in data["recent"]], ["real-project", "notes"])

    def test_all_repository_pages_are_counted(self):
        pages = [[repo(f"project-{n}") for n in range(100)], [repo("last-page", language="Java")]]
        with patch.object(profile, "api", side_effect=[{"public_repos": 101, "followers": 0}, *pages]) as api:
            profile.refresh()
        data = json.loads((self.out / "github-data.json").read_text())
        self.assertEqual(data["original_repos"], 101)
        self.assertEqual(data["languages"], {"Python": 100, "Java": 1})
        self.assertIn("page=2", api.call_args.args[0])

    def test_failed_request_keeps_last_good_snapshot(self):
        snapshot = self.out / "github-data.json"
        snapshot.write_text('{"last_good": true}\n')
        with patch.object(profile, "api", side_effect=[{"public_repos": 1, "followers": 0}, OSError("GitHub unavailable")]):
            with self.assertRaises(OSError):
                profile.refresh()
        self.assertEqual(snapshot.read_text(), '{"last_good": true}\n')

    def test_empty_account_renders_without_division_by_zero(self):
        with patch.object(profile, "api", side_effect=[{"public_repos": 0, "followers": 0}, []]):
            profile.refresh()
        profile.dashboard()
        self.assertTrue((self.out / "github-stats.svg").is_file())
        self.assertTrue((self.out / "github-activity.svg").is_file())

    def test_garden_count_and_visible_cap_are_honest(self):
        for count, expected in [(0, 0), (25, 25), (100, 49)]:
            with self.subTest(repositories=count):
                profile_extras.garden(profile.svg, profile.text, profile.flower,
                                      {"original_repos": count, "updated_at": "2026-10-14 07:00 UTC"})
                for theme in ("dark", "light"):
                    root = ET.parse(self.out / f"project-garden-{theme}.svg").getroot()
                    blooms = [el for el in root.iter() if el.get("data-repo-flower") == "true"]
                    self.assertEqual(len(blooms), expected)
                    description = root.find("{http://www.w3.org/2000/svg}desc").text
                    self.assertIn(f"{count} public non-fork repositories", description)
                    if count > 49:
                        self.assertIn(f"Showing 49 of {count}", description)


if __name__ == "__main__":
    unittest.main()
