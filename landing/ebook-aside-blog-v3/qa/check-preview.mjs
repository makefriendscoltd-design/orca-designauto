import { chromium } from '/Users/apple/orca/projects/1000project/videos/personal-branding-final-01/node_modules/playwright/index.mjs';
import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';
const dir = path.resolve(process.argv[2]);
const browser = await chromium.launch({channel:'chrome',headless:true});
const results = [];
try {
  for (const width of [390,740]) {
    const page = await browser.newPage({viewport:{width,height:844}});
    await page.goto(pathToFileURL(path.join(dir,'preview.html')).href);
    await page.evaluate(()=>Promise.all([...document.images].map(i=>i.decode())));
    const layout = await page.evaluate(()=>({viewport:innerWidth,width:document.documentElement.scrollWidth,
      images:[...document.images].map(i=>({src:i.getAttribute('src'),loaded:i.complete&&i.naturalWidth>0})),
      gaps:[...document.querySelector('main').children].slice(1).map((e,i)=>e.getBoundingClientRect().top-document.querySelector('main').children[i].getBoundingClientRect().bottom),
      gif:document.querySelector('[data-live-demo]').getAttribute('src')}));
    if(layout.width!==width||!layout.images.every(i=>i.loaded)||layout.gaps.some(g=>Math.abs(g)>.1)||!layout.gif.endsWith('.gif')) throw Error('Preview layout failed');
    await page.screenshot({path:path.join(dir,`qa/preview-${width}.png`)});
    const gif = page.locator('[data-live-demo]');
    await gif.scrollIntoViewIfNeeded();
    const first = await gif.screenshot({path:path.join(dir,`qa/gif-${width}-early.png`)});
    await page.waitForTimeout(12000);
    const later = await gif.screenshot({path:path.join(dir,`qa/gif-${width}-later.png`)});
    const hash = b=>createHash('sha256').update(b).digest('hex');
    if(hash(first)===hash(later)) throw Error('GIF did not change in browser');
    results.push({...layout,motion_changed:true,early_hash:hash(first),later_hash:hash(later)});
    await page.close();
  }
  await fs.writeFile(path.join(dir,'qa/preview-verification.json'),JSON.stringify(results,null,2));
  console.log('PASS: 390/740px, 12 PNGs + actual GIF, all loaded, no gaps/overflow, GIF visibly changes');
} finally { await browser.close(); }
