from pathlib import Path
import subprocess,concurrent.futures,json
R=Path(__file__).resolve().parents[1]
def run(p):
 with (p/'qa/render.log').open('w') as out:
  for args in [['node',str(p/'qa/render.mjs'),str(p)],['python3',str(p/'qa/package.py')],['node',str(p/'qa/check-preview.mjs'),str(p)]]:
   r=subprocess.run(args,stdout=out,stderr=subprocess.STDOUT)
   if r.returncode:return p.name,'FAIL'
 return p.name,json.loads((p/'qa/validation.json').read_text())
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 for name,r in pool.map(run,sorted(p for p in R.iterdir() if (p/'detail.html').exists())):print(name,json.dumps(r),flush=True)
