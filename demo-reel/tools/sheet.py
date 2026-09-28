"""Contact sheet of vertical frames: python3 tools/sheet.py <frames dir> <out.jpg> [cols] [tile width]"""
import sys, os, glob
from PIL import Image, ImageDraw
d, out = sys.argv[1], sys.argv[2]; cols = int(sys.argv[3]) if len(sys.argv) > 3 else 8; tw = int(sys.argv[4]) if len(sys.argv) > 4 else 240
fs = sorted(glob.glob(os.path.join(d, '*.png'))); th = tw * 16 // 9; rows = (len(fs) + cols - 1) // cols
S = Image.new('RGB', (cols * tw, rows * th), (30, 30, 30)); D = ImageDraw.Draw(S)
for k, f in enumerate(fs):
    im = Image.open(f).convert('RGB').resize((tw, th), Image.LANCZOS); x, y = k % cols * tw, k // cols * th; S.paste(im, (x, y))
    D.text((x + 4, y + 4), f'{int(os.path.basename(f)[:4]) / 24:.2f}s', fill=(255, 0, 0))
S.save(out, quality=88); print(out, S.size)
