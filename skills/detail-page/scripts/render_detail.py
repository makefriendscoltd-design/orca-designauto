"""
상세페이지/썸네일 HTML -> 전체 높이 PNG 렌더.

사용:
  python render_detail.py <input.html> <output.png> [--width 1080] [--maxh 40000] [--jpg]

동작:
  1) 격리 프로필로 Chromium 계열 headless 실행 (유저 브라우저 절대 안 건드림)
     윈도우=Edge/Chrome, 맥=Chrome/Edge/Chromium/Brave 를 자동 탐색한다
  2) --window-size=W,MAXH 로 한 장 캡처
  3) 아래쪽 '캔버스 배경색만 있는' 빈 줄을 잘라내 실제 문서 높이로 트림

주의:
  * taskkill /IM msedge.exe (맥: pkill Chrome) 는 절대 쓰지 말 것.
    유저가 열어둔 브라우저까지 죽는다. 이 스크립트는 자기가 띄운 PID만 종료한다.
  * 폰트는 CDN <link> 로 하면 headless에서 안 붙는다. 반드시 로컬 @font-face.
    HTML 옆에 assets/pretendard/*.woff2 가 있어야 한다.
  * 맥은 폰트 로딩 실패 시 Apple SD Gothic Neo 로 떨어져 '그럴싸하게' 보인다.
    윈도우의 맑은고딕처럼 티가 안 나니 렌더 후 반드시 자소 모양을 확인할 것.
  * --force-device-scale-factor=1 은 Retina 에서 2배로 찍히는 걸 막는다. 빼지 말 것.
"""
import glob
import os
import subprocess
import sys
import tempfile
import time
import pathlib


def _ensure_deps():
    """스킬 전용 venv 가 아니면 그쪽으로 재실행한다.

    'PIL 이 import 되나'로 판정하면 안 된다 — 맥 시스템 python3 에도 PIL 이 깔려 있어서
    통과해버리고, 정작 numpy/fitz/pptx 가 없어 한참 뒤에 터진다. 인터프리터를 못 박는다.
    """
    vdir = os.path.join(os.path.expanduser("~"), ".claude", "skills", ".venv")
    vpy = os.path.join(vdir, "Scripts" if os.name == "nt" else "bin",
                       "python.exe" if os.name == "nt" else "python")
    if os.path.exists(vpy) and os.path.realpath(sys.prefix) != os.path.realpath(vdir):
        os.execv(vpy, [vpy, os.path.abspath(__file__)] + sys.argv[1:])
    try:
        import PIL  # noqa: F401
    except ImportError:
        raise SystemExit(
            "Pillow 가 없음. 스킬 전용 venv 를 만들 것: "
            "python3 -m venv ~/.claude/skills/.venv && "
            "~/.claude/skills/.venv/bin/python -m pip install "
            "Pillow python-pptx PyMuPDF numpy requests"
        )


BROWSER_CANDIDATES = {
    "win32": [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ],
    "darwin": [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        os.path.expanduser("~/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
    ],
    "linux": [
        "/usr/bin/google-chrome", "/usr/bin/chromium",
        "/usr/bin/chromium-browser", "/usr/bin/microsoft-edge",
    ],
}

PLAYWRIGHT_GLOBS = [
    "~/Library/Caches/ms-playwright/chromium-*/chrome-mac/Chromium.app/Contents/MacOS/Chromium",
    "~/.cache/ms-playwright/chromium-*/chrome-linux/chrome",
    "~/AppData/Local/ms-playwright/chromium-*/chrome-win/chrome.exe",
]


def find_browser():
    key = "win32" if os.name == "nt" else ("darwin" if sys.platform == "darwin" else "linux")
    for p in BROWSER_CANDIDATES[key]:
        if os.path.exists(p):
            return p
    for pat in PLAYWRIGHT_GLOBS:          # playwright 번들 크로미움 폴백
        hit = sorted(glob.glob(os.path.expanduser(pat)))
        if hit:
            return hit[-1]
    raise SystemExit(
        "Chromium 계열 브라우저를 못 찾음.\n"
        "  맥:     brew install --cask google-chrome\n"
        "  윈도우: Edge 또는 Chrome 설치"
    )


def shoot(html, out_png, width, maxh):
    url = pathlib.Path(os.path.abspath(html)).as_uri()
    prof = tempfile.mkdtemp(prefix="edgeshot_")
    if os.path.exists(out_png):
        os.remove(out_png)
    cmd = [
        find_browser(), "--headless=new", "--disable-gpu", "--hide-scrollbars",
        "--force-device-scale-factor=1", "--virtual-time-budget=8000",
        f"--user-data-dir={prof}", f"--window-size={width},{maxh}",
        f"--screenshot={os.path.abspath(out_png)}", url,
    ]
    p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    deadline, last = time.time() + 90, -1
    while time.time() < deadline:
        time.sleep(1.0)
        if os.path.exists(out_png):
            sz = os.path.getsize(out_png)
            if sz > 0 and sz == last:
                break
            last = sz
        if p.poll() is not None and os.path.exists(out_png):
            break
    try:
        p.kill()          # 우리가 띄운 PID만
    except Exception:
        pass
    if not os.path.exists(out_png):
        raise SystemExit("렌더 실패: 스크린샷 파일이 안 생김")


def trim(out_png, maxh, to_jpg=False):
    from PIL import Image
    im = Image.open(out_png).convert("RGB")
    W, H = im.size
    px = im.load()
    bg = px[W - 2, H - 2]          # 캔버스 배경색 (보통 흰색)

    def blank(y):
        for x in range(0, W, 5):
            if px[x, y] != bg:
                return False
        return True

    bottom = H
    while bottom > 1 and blank(bottom - 1):
        bottom -= 1
    if bottom >= H - 2:
        print(f"[warn] 하단 여백이 없음 -> 콘텐츠가 {maxh}px 를 넘었을 수 있음. --maxh 를 키워서 다시 렌더할 것.")
    im = im.crop((0, 0, W, bottom))
    im.save(out_png)
    if to_jpg:
        jpg = os.path.splitext(out_png)[0] + ".jpg"
        im.save(jpg, quality=92, subsampling=0)
        print("jpg:", jpg)
    print(f"OK {out_png} {im.width}x{im.height} ({os.path.getsize(out_png)//1024}KB)")


def main():
    _ensure_deps()
    a = sys.argv[1:]
    if len(a) < 2:
        raise SystemExit(__doc__)
    html, out = a[0], a[1]
    width = int(a[a.index("--width") + 1]) if "--width" in a else 1080
    maxh = int(a[a.index("--maxh") + 1]) if "--maxh" in a else 40000
    shoot(html, out, width, maxh)
    trim(out, maxh, to_jpg="--jpg" in a)


if __name__ == "__main__":
    main()
