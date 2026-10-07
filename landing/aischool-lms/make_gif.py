"""운영 실적 카운트업 GIF — 740×560. 카페24가 애니 WebP 로 변환해 상세에서 돈다."""
from PIL import Image, ImageDraw, ImageFont
import pathlib
R = pathlib.Path(__file__).resolve().parent
F = R / "assets/pretendard"
big  = ImageFont.truetype(str(F / "Pretendard-ExtraBold.woff2"), 128) if False else None
def font(sz, w="ExtraBold"):
    # woff2 는 PIL 이 못 읽는다 → 시스템 한글 폰트로 대체
    for p in ("/System/Library/Fonts/AppleSDGothicNeo.ttc",
              "/System/Library/Fonts/Supplemental/AppleGothic.ttf"):
        if pathlib.Path(p).exists():
            return ImageFont.truetype(p, sz, index=9 if p.endswith("ttc") else 0)
    return ImageFont.load_default()

W, H = 740, 560
ITEMS = [("쇼핑몰 CS 담당자", 3694, "건", "주문 안내 메일·문자 발송"),
         ("운영 매니저·비서", 441, "건", "업무 카드 배정"),
         ("스레드 운영", 1681, "건", "유입에서 발생한 결제")]
FR, HOLD = 26, 14
frames = []
f_lb, f_num, f_u, f_sub = font(30), font(132), font(52), font(27)

def draw(idx, t):
    im = Image.new("RGB", (W, H), "#000")
    d = ImageDraw.Draw(im)
    for r in range(260):                      # 상단 블루 글로우
        a = int(42 * (1 - r / 260))
        d.line([(0, r), (W, r)], fill=(a // 4, a // 2, a))
    who, target, unit, sub = ITEMS[idx]
    val = int(target * (t ** 0.5)) if t < 1 else target
    d.text((W // 2, 118), who, font=f_lb, fill="#60a5fa", anchor="mm")
    s = f"{val:,}"
    bb = d.textbbox((0, 0), s, font=f_num); nw = bb[2] - bb[0]
    uw = d.textbbox((0, 0), unit, font=f_u)[2]
    x = (W - nw - uw - 10) // 2
    d.text((x, 250), s, font=f_num, fill="#fff", anchor="lm")
    d.text((x + nw + 10, 285), unit, font=f_u, fill="#fff", anchor="lm")
    d.text((W // 2, 396), sub, font=f_sub, fill="#cfd9e8", anchor="mm")
    for i in range(len(ITEMS)):               # 하단 인디케이터
        cx = W // 2 + (i - 1) * 26
        c = "#60a5fa" if i == idx else "#2b3444"
        d.ellipse([cx - 5, 470, cx + 5, 480], fill=c)
    d.text((W // 2, 524), "학교 운영사 내부 기록 · 수강생 결과를 보장하지 않습니다",
           font=font(19), fill="#6f8099", anchor="mm")
    return im

for i in range(len(ITEMS)):
    for k in range(FR):
        frames.append(draw(i, (k + 1) / FR))
    frames += [draw(i, 1.0)] * HOLD

out = R / "ops_countup.gif"
frames[0].save(out, save_all=True, append_images=frames[1:], duration=55, loop=0, optimize=True)
print(f"{out.name} {len(frames)}프레임 {out.stat().st_size//1024}KB")
