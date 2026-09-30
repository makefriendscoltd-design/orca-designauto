"""Check restored evidence references against the editable page, before rendering/upload."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            self.images.append(dict(attrs).get("src", ""))

    def handle_data(self, data):
        self.text.append(data)


def referenced_assets(node):
    result = []
    if isinstance(node, dict):
        for key, value in node.items():
            if key in ("asset", "used_assets"):
                candidates = value if isinstance(value, list) else [value]
                result.extend(v for v in candidates if isinstance(v, str) and v.startswith("assets/"))
            else:
                result.extend(referenced_assets(value))
    elif isinstance(node, list):
        for value in node:
            result.extend(referenced_assets(value))
    return result


results = []
folders = sorted(p.parent for p in ROOT.glob("*/detail.html"))
folders.append(ROOT.parent / "ebook-concept-ecommerce-v10")
for folder in folders:
    manifest = folder / "qa/evidence-restored.json"
    assert manifest.exists(), f"Missing evidence disposition: {folder.name}"
    source = (folder / "detail.html").read_text()
    page = Page()
    page.feed(source)
    text = re.sub(r"\s+", "", "".join(page.text))
    assert "114.9" not in text, f"Superseded cumulative revenue: {folder.name}"
    declared_assets = referenced_assets(json.loads(manifest.read_text()))
    for asset in declared_assets:
        assert (folder / asset).is_file(), f"Missing asset: {folder.name}/{asset}"
        assert asset in source, f"Evidence removed from page: {folder.name}/{asset}"
    proof = sorted(set(p for p in page.images if p in declared_assets or any(x in p for x in ("/evidence/", "/proof/", "/reviews/", "/kakao/", "/hl/"))))
    assert proof, f"No source evidence image on page: {folder.name}"
    assert all((folder / p).is_file() for p in page.images if not p.startswith("http"))
    if any(marker in source for marker in ("company-annual-revenue", "company-results", "annual-stats")):
        assert all(value in text for value in ("40.5", "41.3", "27.6")), folder.name
    results.append({"book": folder.name, "evidence_images": len(proof), "manifest_present": True, "all_referenced_assets_in_page": True})

out = {"pages": len(results), "pass": True, "results": results}
(ROOT / "qa-evidence-coverage.json").write_text(json.dumps(out, ensure_ascii=False, indent=2))
print(json.dumps({"pages": len(results), "evidence_images": sum(x["evidence_images"] for x in results), "pass": True}))
