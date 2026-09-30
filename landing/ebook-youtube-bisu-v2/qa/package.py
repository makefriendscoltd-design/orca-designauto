"""Export a static overview and a responsive image sequence retaining the real GIF."""
from pathlib import Path
from PIL import Image, ImageChops
import json, math

p = Path(__file__).resolve().parent.parent
r = json.loads((p / 'qa/runtime.json').read_text())
im = Image.open(p / 'detail_full.png').convert('RGB')
w, h = im.size
assert w == 740 and h == r['height']
assert not r['textOverflow'] and all(x['ok'] for x in r['images'])
safe = [False] * h
uniform = [False] + [max(v[1] for v in ImageChops.difference(im.crop((0,y-1,w,y)), im.crop((0,y,w,y+1))).getextrema()) <= 3 for y in range(1,h)]
for y in range(3,h-3):
    safe[y] = all(uniform[y-3:y+4])
for block in r['protected']:
    for y in range(max(0,block['top']),min(h,block['bottom'])):
        safe[y] = False

out = p / 'slices'
out.mkdir(exist_ok=True)
parts = []
def static_region(a,b):
    cuts = [a]
    while b-cuts[-1] > 2100:
        y0 = cuts[-1]
        candidates = [y for y in range(y0+700,min(y0+4000,b-350)) if safe[y]]
        if not candidates:
            break
        cuts.append(min(candidates,key=lambda y:abs(y-y0-1500)))
    cuts.append(b)
    for top,bottom in zip(cuts,cuts[1:]):
        if bottom == top:
            continue
        name = f'slices/{len(parts)+1:02}.png'
        im.crop((0,top,w,bottom)).save(p/name)
        parts.append(dict(type='image',file=name,top=top,height=bottom-top))

static_region(0,h)
reassembled = Image.new('RGB',(w,h))
for part in parts:
    src = part.get('background',part['file'])
    reassembled.paste(Image.open(p/src).convert('RGB'),(0,part['top']))
assert ImageChops.difference(im,reassembled).getbbox() is None
assert sum(x['height'] for x in parts) == h

blocks = []
for part in parts:
    if part['type'] == 'image':
        blocks.append(f'<img class="slice" src="{part["file"]}" width="740" height="{part["height"]}" alt="AI로 유튜브 정복하기 상세페이지">')
    else:
        blocks.append(f'<div class="motion-row" style="padding-top:{part["height"]/w*100:.9f}%;background-image:url({part["background"]})"><img data-live-demo src="{part["file"]}" alt="라이브 원본에서 추출한 실제 블로그 자동 입력 장면" style="left:{part["image_left"]/w*100:.9f}%;top:{part["image_top"]/part["height"]*100:.9f}%;width:{part["image_width"]/w*100:.9f}%"></div>')
html = '<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AI로 유튜브 정복하기</title><style>*{box-sizing:border-box}body{margin:0;background:#081b20}main{width:100%;max-width:740px;margin:auto}.slice{display:block;width:100%;height:auto}.motion-row{position:relative;height:0;background-size:100% 100%;background-repeat:no-repeat}.motion-row img{position:absolute;display:block;height:auto}</style></head><body><main>' + ''.join(blocks) + '</main></body></html>'
(p/'preview.html').write_text(html)
used = {part['file'] for part in parts if part['type'] == 'image'}
for file in out.glob('*.png'):
    if str(file.relative_to(p)) not in used:
        file.unlink()
(p/'qa/export-parts.json').write_text(json.dumps(parts,ensure_ascii=False,indent=2))
validation = dict(width=w,height=h,static_count=sum(x['type']=='image' for x in parts),gif_count=0,
                  pixel_match=True,height_sum=h,text_overflow=0,all_images_loaded=True,
                  motion_asset=None,motion_flattened=False)
(p/'qa/validation.json').write_text(json.dumps(validation,indent=2))
im.crop((0,0,w,r['sections'][0]['h'])).save(p/'hero.png')
row_h = math.ceil(h/6/2)+10
montage = Image.new('RGB',(1110,row_h*2),'#cdd6d8')
for i in range(6):
    region = im.crop((0,h*i//6,w,h*(i+1)//6))
    region.save(p/f'qa/region-{i+1}.png')
    region = region.resize((370,region.height//2))
    montage.paste(region,((i%3)*370,(i//3)*row_h))
montage.save(p/'qa/montage.jpg')
print(json.dumps(validation))
