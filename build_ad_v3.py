#!/usr/bin/env python3
"""Via Laser — Square 1080x1080 Acne Laser Ad, fixed pricing"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = "/root/lead-form-lp-vialaser/video_ads"
IMG = "/root/lead-form-lp-vialaser/images"
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1080  # Square

FONT_B  = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

TEAL       = "#0d5252"
TEAL_DARK  = "#0a4242"
GOLD       = "#d4a254"
GOLD_DARK  = "#a87a30"
CREAM      = "#fdfcf8"
WHITE      = "#ffffff"
INK        = "#0a1f1f"
INK_SOFT   = "#4a5656"

def load_bg(path):
    img = Image.open(path).convert("RGB")
    return img.resize((W, H), Image.LANCZOS)

def darken(img, alpha=0.35):
    o = Image.new("RGBA", (W, H), (0, 0, 0, int(255 * alpha)))
    c = img.convert("RGBA")
    return Image.alpha_composite(c, o).convert("RGB")

def center(draw, text, y, font, color=WHITE, mw=W-120):
    lines = []
    for w in text.split():
        if not lines:
            lines.append(w)
        else:
            t = lines[-1] + " " + w
            b = draw.textbbox((0, 0), t, font=font)
            if b[2] - b[0] <= mw:
                lines[-1] = t
            else:
                lines.append(w)
    lh = draw.textbbox((0, 0), "A", font=font)[3] - draw.textbbox((0, 0), "A", font=font)[1]
    sp = max(6, int(lh * 0.3))
    th = lh * len(lines) + sp * (len(lines) - 1)
    cy = y - th // 2
    for ln in lines:
        tw = draw.textbbox((0, 0), ln, font=font)[2]
        draw.text(((W - tw) // 2, cy), ln, fill=color, font=font)
        cy += lh + sp

def build():
    bg = load_bg(os.path.join(IMG, "benefits-treatment.jpg"))
    bg = darken(bg, 0.40)
    draw = ImageDraw.Draw(bg)

    # === TOP: HEADLINE ===
    f_head = ImageFont.truetype(FONT_SB, 64)
    f_sub  = ImageFont.truetype(FONT_B, 34)
    f_tag  = ImageFont.truetype(FONT_R, 22)

    center(draw, "✦ VIA LASER LAS VEGAS ✦", 60, f_tag, GOLD, 800)
    center(draw, "Bye Bye Acne", 170, f_head, WHITE, 900)
    center(draw, "Laser Treatment", 250, f_sub, GOLD, 900)

    # Gold divider
    draw.line([(W//2 - 80, 290), (W//2 + 80, 290)], fill=GOLD, width=2)

    # === MIDDLE: BENEFITS ===
    f_ben = ImageFont.truetype(FONT_B, 24)
    benefits = [
        "ACNE CLEARING LASER",
        "REDUCES ACNE SCARS",
        "MINIMIZES PORES",
        "CALMS INFLAMMATION",
        "COLLAGEN-BOOSTING",
        "ZERO DOWNTIME",
    ]
    bx, by = 80, 330
    bw, bh = 600, 290
    draw.rounded_rectangle([bx, by, bx+bw, by+bh], radius=14, fill=(13, 82, 82, 200))

    by2 = by + 16
    for b in benefits[:5]:
        draw.ellipse([bx+22, by2+5, bx+32, by2+15], fill=GOLD)
        draw.text((bx+48, by2), b, fill=WHITE, font=f_ben)
        by2 += 52

    # Before/After inset
    bax, bay = bx+bw+20, by+8
    bs = 220
    try:
        ba = Image.open(os.path.join(IMG, "before-after-1.jpg")).convert("RGB")
        ba = ba.resize((bs, bs), Image.LANCZOS)
        bg.paste(ba, (bax, bay))
        draw.rounded_rectangle([bax, bay+bs-36, bax+bs, bay+bs], radius=6, fill=(0,0,0,180))
        f_bal = ImageFont.truetype(FONT_B, 18)
        draw.text((bax+16, bay+bs-28), "REAL RESULTS ✨", fill=GOLD, font=f_bal)
        draw.text((bax+16, bay+bs+8), "BEFORE → AFTER", fill=GOLD, font=f_bal)
    except:
        pass

    # === BOOK NOW ===
    f_book = ImageFont.truetype(FONT_B, 30)
    f_loc  = ImageFont.truetype(FONT_R, 20)
    f_ph   = ImageFont.truetype(FONT_B, 24)
    by3 = by + bh + 22
    center(draw, "BOOK NOW!", by3, f_book, WHITE, 400)
    center(draw, "9345 S Cimarron Rd, Las Vegas, NV 89178", by3+38, f_loc, CREAM, 950)
    center(draw, "(725) 772-0948", by3+64, f_ph, GOLD, 400)

    # === PRICING — FIXED LAYOUT (NO OVERLAP) ===
    pr_y = by3 + 110

    # --- $129 (left side) ---
    pw, ph = 300, 120
    px = W//2 - pw - 40   # left side
    py = pr_y
    draw.rounded_rectangle([px, py, px+pw, py+ph], radius=60, fill=TEAL)

    f_lbl = ImageFont.truetype(FONT_R, 20)
    draw.text((px+50, py+10), "FOR ONLY", fill=CREAM, font=f_lbl)
    center(draw, "$129", py+ph//2+10, ImageFont.truetype(FONT_B, 90), WHITE, pw-20)

    # --- $299 (right side) ---
    rw, rh = 260, 100
    rx = W//2 + 20   # right side
    ry = py + 10     # aligned middle
    f_rlbl = ImageFont.truetype(FONT_R, 18)
    f_rp   = ImageFont.truetype(FONT_B, 42)
    draw.text((rx+20, ry+6), "REGULAR PRICE", fill=CREAM, font=f_rlbl)
    draw.text((rx+40, ry+38), "$299", fill=CREAM, font=f_rp)
    # Strike through
    tw = draw.textbbox((0, 0), "$299", font=f_rp)[2]
    draw.line([(rx+40, ry+85), (rx+40+tw, ry+85)], fill=GOLD, width=4)

    # --- SAVE $170 (centered below both) ---
    svy = py + ph + 20
    draw.rounded_rectangle([W//2-130, svy, W//2+130, svy+52], radius=26, fill=GOLD)
    center(draw, "SAVE $170 ✨", svy+28, ImageFont.truetype(FONT_B, 26), TEAL_DARK, 240)

    # === BOTTOM TAG ===
    f_bot = ImageFont.truetype(FONT_B, 22)
    center(draw, "✦ LAS VEGAS LADIES, THIS IS YOUR GLOW-UP SIGN ✨", H-40, f_bot, GOLD, 950)

    return bg

print("🖌 Building 1080x1080 ad (fixed pricing)...")
img = build()
jpg = os.path.join(OUT, "acne_laser_ad_v3.jpg")
img.save(jpg, "JPEG", quality=95)
print(f"✅ Saved: {jpg} ({os.path.getsize(jpg)/1024:.0f} KB)")
