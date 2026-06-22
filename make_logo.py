from PIL import Image, ImageDraw, ImageFilter

# Render at 2× then downsample for smooth edges
DRAW = 1024
OUT  = 512

def lerp(a, b, t): return int(a + (b - a) * t)

def make_logo():
    S = DRAW
    f = S / 512  # scale factor

    # ── Diagonal gradient (top-left blue → bottom-right purple) ──
    # Premium palette: rich electric blue → deep violet
    c1 = (29, 78, 216)    # #1D4ED8
    c2 = (109, 40, 217)   # #6D28D9
    grad = Image.new('RGB', (S, S))
    gd = ImageDraw.Draw(grad)
    for i in range(S * 2):           # diagonal bands
        t  = i / (S * 2 - 1)
        r  = lerp(c1[0], c2[0], t)
        g  = lerp(c1[1], c2[1], t)
        b  = lerp(c1[2], c2[2], t)
        x1 = max(0, i - S)
        y1 = min(i, S - 1)
        x2 = min(i, S - 1)
        y2 = max(0, i - S)
        gd.line([(x1, y1), (x2, y2)], fill=(r, g, b))

    # ── Silhouette mask ──
    mask = Image.new('L', (S, S), 0)
    md   = ImageDraw.Draw(mask)

    # ── Telescoping handle ──
    # Two thin vertical bars + top crossbar
    bar_w    = int(15 * f)
    bar_r    = int(8  * f)
    bar_top  = int(62 * f)
    bar_bot  = int(155* f)
    lx       = int(192* f)   # left bar x-start
    rx       = int(315* f)   # right bar x-start
    cross_h  = int(14 * f)

    md.rounded_rectangle([lx, bar_top, lx+bar_w, bar_bot], radius=bar_r, fill=255)
    md.rounded_rectangle([rx, bar_top, rx+bar_w, bar_bot], radius=bar_r, fill=255)
    md.rounded_rectangle([lx, bar_top, rx+bar_w, bar_top+cross_h], radius=bar_r, fill=255)

    # ── Main body ──
    bx1, by1 = int(118*f), int(148*f)
    bx2, by2 = int(394*f), int(424*f)
    br       = int(36 * f)
    md.rounded_rectangle([bx1, by1, bx2, by2], radius=br, fill=255)

    # ── Wheels ──
    wr  = int(20 * f)
    wy  = int(437* f)
    md.ellipse([int(155*f)-wr, wy-wr, int(155*f)+wr, wy+wr], fill=255)
    md.ellipse([int(357*f)-wr, wy-wr, int(357*f)+wr, wy+wr], fill=255)

    # Axle nubs
    nr = int(8 * f)
    md.ellipse([int(155*f)-nr, wy-nr, int(155*f)+nr, wy+nr], fill=255)
    md.ellipse([int(357*f)-nr, wy-nr, int(357*f)+nr, wy+nr], fill=255)

    # ── Paste gradient through mask ──
    result = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    result.paste(grad, mask=mask)

    # ── White detail layer ──
    detail = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    dd     = ImageDraw.Draw(detail)

    # Horizontal shell grooves (2 lines — clean, not cluttered)
    groove_alpha = 55
    groove_h     = int(4 * f)
    groove_r     = int(2 * f)
    margin       = int(26 * f)
    for gy in [int(228*f), int(298*f)]:
        dd.rounded_rectangle(
            [bx1+margin, gy, bx2-margin, gy+groove_h],
            radius=groove_r,
            fill=(255, 255, 255, groove_alpha)
        )

    # Centre zipper seam (slightly brighter)
    zp_y = int(263*f)
    zp_h = int(4 * f)
    dd.rounded_rectangle(
        [bx1+int(8*f), zp_y, bx2-int(8*f), zp_y+zp_h],
        radius=int(2*f),
        fill=(255, 255, 255, 85)
    )

    # Lock clasp
    lk_w, lk_h = int(34*f), int(22*f)
    lk_cx = S // 2
    lk_cy = zp_y + zp_h // 2
    lk_r  = int(6 * f)
    # Clasp body
    dd.rounded_rectangle(
        [lk_cx - lk_w//2, lk_cy - lk_h//2,
         lk_cx + lk_w//2, lk_cy + lk_h//2],
        radius=lk_r,
        fill=(255, 255, 255, 200)
    )
    # Clasp keyhole dot
    kh_r = int(4 * f)
    dd.ellipse(
        [lk_cx - kh_r, lk_cy - kh_r, lk_cx + kh_r, lk_cy + kh_r],
        fill=(130, 100, 220, 200)
    )

    # Subtle top-left shine (gives depth)
    shine = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    sd    = ImageDraw.Draw(shine)
    sd.ellipse([bx1-int(30*f), by1-int(30*f),
                bx1+int(160*f), by1+int(160*f)],
               fill=(255, 255, 255, 28))
    shine = shine.filter(ImageFilter.GaussianBlur(radius=int(40*f)))

    result = Image.alpha_composite(result, shine)
    result = Image.alpha_composite(result, detail)

    # ── Downsample to output size ──
    result = result.resize((OUT, OUT), Image.LANCZOS)
    return result

logo = make_logo()
logo.save('/Users/choi/pack-all/packo-logo.png', 'PNG')
print(f'Saved packo-logo.png ({OUT}×{OUT})')
