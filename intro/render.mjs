// Render rossen-live-intro.html to PNG frames + mp4 (video only). Serves the folder over http so canvas stays untainted.
// usage: node render.mjs [--html film.html] [--only 0,72,180] [--grid 24] [--all] [--query safe=1]
import puppeteer from 'puppeteer-core';
import http from 'node:http';
import {readFileSync, existsSync, mkdirSync, writeFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import path from 'node:path';
const root = path.dirname(new URL(import.meta.url).pathname);
const argv = process.argv.slice(2), flag = n => { const k = argv.indexOf(n); return k >= 0 ? argv[k + 1] : undefined; };
const types = {'.html': 'text/html', '.js': 'text/javascript', '.png': 'image/png', '.ttf': 'font/ttf'};
const srv = http.createServer((q, s) => { const p = path.join(root, decodeURIComponent(q.url.split('?')[0])); if (!existsSync(p)) { s.writeHead(404); return s.end(); } s.writeHead(200, {'content-type': types[path.extname(p)] || 'application/octet-stream'}); s.end(readFileSync(p)); }).listen(0);
const port = srv.address().port;
const html = flag('--html') || 'rossen-live-intro.html', query = flag('--query'), sub = (html === 'rossen-live-intro.html' ? '' : path.basename(html, '.html')) + (query ? '_check' : '');   // --query renders to a separate folder
const out = path.join(root, 'out', sub), frames = path.join(out, 'frames'); mkdirSync(frames, {recursive: true});
const browser = await puppeteer.launch({executablePath: process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', headless: true, args: ['--no-sandbox']});
const errors = [];
try {
  const page = await browser.newPage();
  page.on('pageerror', e => errors.push(String(e))); page.on('console', m => { if (m.type() === 'error' && !/404/.test(m.text())) errors.push(m.text()); });
  await page.goto(`http://127.0.0.1:${port}/${html}?bare=1${query ? '&' + query : ''}`);
  await page.waitForFunction('window.__ready === true || window.__error', {timeout: 60000}).catch(()=>{}); const perr = await page.evaluate(() => window.__error); if (perr || errors.length) { console.error('load error', perr, errors); process.exit(1); }
  const N = await page.evaluate(() => window.__NFR);
  const save = (f, d) => writeFileSync(f, Buffer.from(d.split(',')[1], 'base64'));
  let list;
  if (flag('--only')) list = flag('--only').split(',').map(Number);
  else if (flag('--grid')) { const n = +flag('--grid'); list = [...Array(n).keys()].map(k => Math.round(k * (N - 1) / (n - 1))); }
  else list = [...Array(N).keys()];
  const t0 = Date.now();
  for (const i of list) { save(path.join(frames, `${String(i).padStart(4, '0')}.png`), await page.evaluate(i => window.__frame(i), i)); process.stdout.write(`\r${i}`); }
  console.log(`\n${list.length} frames in ${((Date.now() - t0) / 1000).toFixed(1)}s`);
  if (flag('--grid')) {
    const n = list.length, inputs = list.flatMap(i => ['-i', path.join(frames, `${String(i).padStart(4, '0')}.png`)]);
    execFileSync('ffmpeg', ['-v', 'error', '-y', ...inputs, '-filter_complex', list.map((_, k) => `[${k}:v]scale=480:-1,drawtext=text='${(list[k] / 24).toFixed(2)}s':fontcolor=red:fontsize=22:x=6:y=6[v${k}]`).join(';') + ';' + list.map((_, k) => `[v${k}]`).join('') + `xstack=inputs=${n}:layout=${list.map((_, k) => `${(k % 4) * 480}_${Math.floor(k / 4) * 270}`).join('|')}`, path.join(out, 'grid.jpg')]);
    console.log('grid:', path.join(out, 'grid.jpg'));
  }
} finally { await browser.close(); srv.close(); }
if (errors.length) { console.error('page errors:\n ' + [...new Set(errors)].join('\n ')); process.exit(1); }
if (argv.includes('--all')) {
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-framerate', '24', '-i', path.join(frames, '%04d.png'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '16', '-preset', 'slow', '-r', '24', path.join(out, 'video.mp4')], {stdio: 'inherit'});
  console.log('video:', path.join(out, 'video.mp4'));
}
