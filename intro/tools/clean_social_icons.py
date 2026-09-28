"""The YouTube and Instagram icons were supplied as RGB images with a checkerboard baked in where the transparency should be.
Restore the transparency: flood-fill the light neutral background from the edges (the icons' own whites are enclosed by
colour, so they are never reached; any checkerboard showing through those whites is set back to white), feather the edge by one pixel, and give edge pixels the colour of the nearest inside
pixel so no grey fringe shows on the cream card. The icons' pixels are otherwise untouched."""
import numpy as np
from PIL import Image, ImageFilter
IMG = '/tmp/claude-0/-home-user-Rossen/3fdd0da9-e341-56c5-b3c5-1d0ea82e103b/images/'
def clean(src, dst):
    A = np.array(Image.open(src).convert('RGB')).astype(int); H, W, _ = A.shape
    mx, mn = A.max(2), A.min(2); bgish = (mx - mn < 24) & (mn > 200)          # light, unsaturated: the checkerboard
    out = np.zeros((H, W), bool); out[0, :] = out[-1, :] = out[:, 0] = out[:, -1] = True; out &= bgish
    while True:
        n = out.copy(); n[1:] |= out[:-1]; n[:-1] |= out[1:]; n[:, 1:] |= out[:, :-1]; n[:, :-1] |= out[:, 1:]; n &= bgish
        if (n == out).all(): break
        out = n
    body = ~out
    body = np.array(Image.fromarray((body * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3))) > 0   # drop the 1 px blended fringe
    alpha = np.array(Image.fromarray((body * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.8)))
    inner = np.array(Image.fromarray((body * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(5))) > 0
    rgb = A.copy().astype(np.uint8); src_img = Image.fromarray(np.where(inner[..., None], rgb, 0).astype(np.uint8))
    # spread inside colours outward a few pixels for the feathered edge
    acc = np.where(inner[..., None], rgb, 0).astype(float); wsum = inner.astype(float)
    for r in (3, 5, 9):
        k = Image.fromarray(np.uint8(inner * 255)).filter(ImageFilter.BoxBlur(r)); wk = np.array(k).astype(float) / 255
        ck = np.stack([np.array(Image.fromarray(np.uint8(acc[..., i])).filter(ImageFilter.BoxBlur(r))).astype(float) for i in range(3)], 2)
        fill = (wsum == 0) & (wk > 0); acc[fill] = ck[fill] / wk[fill][:, None]; wsum = np.where(fill, 1, wsum)
    glyph = bgish & body   # light neutral pixels INSIDE the icon: the white glyph, where the checkerboard also showed through
    A = A.copy(); A[glyph] = 255
    rgb = np.where(inner[..., None], A, acc).clip(0, 255).astype(np.uint8)
    ys, xs = np.nonzero(alpha > 0); x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    Image.fromarray(np.dstack([rgb, alpha])[y0:y1, x0:x1]).save(dst)
    print(dst, (x1 - x0, y1 - y0), 'background px removed', int(out.sum()))
clean(IMG + '18.png', 'assets/social/instagram_icon.png')
clean(IMG + '19.png', 'assets/social/youtube_icon.png')
