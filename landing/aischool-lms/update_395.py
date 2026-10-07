"""상품 395 ([AIxSCHOOL] AI 학교 입학 신청하기) 상세설명 교체.

  python update_395.py --dry-run
  python update_395.py

이미 있는 상품을 고치는 용도다(신규 등록은 register_* 계열).
카페24는 같은 파일도 올릴 때마다 새 경로를 만들기 때문에 `_uploaded.json` 에 캐시한다.
shop 1·4 양쪽에 description 을 넣는다 — 한쪽만 넣으면 다른 도메인에서 빈 상세가 뜬다.
"""
import argparse
import base64
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / "orca/projects/cafe24"))
_HERE = Path(__file__).resolve().parent
os.chdir(Path.home() / "orca/projects/cafe24")

from dotenv import load_dotenv                       # noqa: E402
from cafe24_client import Cafe24Client, Cafe24Error  # noqa: E402

load_dotenv()

PRODUCT_NO = 395
SLICES = _HERE / "out" / "slices"
CACHE = _HERE / "_uploaded.json"


def b64(p):
    return base64.b64encode(p.read_bytes()).decode()


def rel(u):
    """절대 URL -> 상대경로. 멀티도메인 양쪽에서 떠야 한다."""
    return re.sub(r"^https?://[^/]+", "", u)


def upload(c, paths):
    out = []
    for i in range(0, len(paths), 10):
        chunk = paths[i:i + 10]
        res = c.post("/api/v2/admin/products/images",
                     {"requests": [{"image": b64(p)} for p in chunk]})
        imgs = res.get("images") or res.get("image") or []
        if len(imgs) != len(chunk):
            raise SystemExit(f"업로드 수 불일치 {len(chunk)}/{len(imgs)}")
        out += [im.get("path") or im.get("image_path") for im in imgs]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    slices = sorted(SLICES.glob("*.jpg"),
                    key=lambda p: int(re.search(r"(\d+)$", p.stem).group(1)))
    if not slices:
        sys.exit(f"슬라이스 없음: {SLICES}")
    print(f"상품 {PRODUCT_NO} · 상세 {len(slices)}조각 ({slices[0].name}~{slices[-1].name})")

    c = Cafe24Client()
    cur = c.get(f"/api/v2/admin/products/{PRODUCT_NO}").get("product", {})
    print(f"현재: {cur.get('product_name')} / desc {len(cur.get('description') or '')}자")
    if args.dry_run:
        print("--dry-run 이라 여기서 멈춥니다.")
        return

    if CACHE.exists() and json.loads(CACHE.read_text()).get("count") == len(slices):
        urls = json.loads(CACHE.read_text())["detail"]
        print(f"  캐시 재사용 ({len(urls)}장)")
    else:
        urls = upload(c, slices)
        CACHE.write_text(json.dumps({"count": len(slices), "detail": urls},
                                    ensure_ascii=False, indent=1))
        print(f"  업로드 {len(urls)}장")

    imgs = "\n".join(
        f'<img src="{rel(u)}" style="display:block;max-width:100%;" alt="">' for u in urls)
    desc = (f'<div style="max-width:740px;margin:0 auto;font-size:0;line-height:0;">\n'
            f'{imgs}\n</div>')

    for shop in (1, 4):
        try:
            c.put(f"/api/v2/admin/products/{PRODUCT_NO}",
                  {"shop_no": shop, "request": {"description": desc}})
            print(f"  shop{shop} 주입 OK")
        except Cafe24Error as e:
            print(f"  shop{shop} 실패 {e.status}: {str(e.body)[:200]}")

    print(f"\n상품페이지: https://makefamily.kr/product/detail.html?product_no={PRODUCT_NO}")


if __name__ == "__main__":
    main()
