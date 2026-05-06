#!/usr/bin/env python3
"""Via Laser — Square 1080x1080 Acne Laser Ad v4 — fixed pricing"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = "/root/lead-form-lp-vialaser/video_ads"
IMG = "/root/lead-form-lp-vialaser/images"
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1080

FONT_B  = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

TEAL = "#0d5252"
GOLD = "#d4a254"
CREAM = "#fdfcf8"
WHITE = "#ffffff"

def load_bg(path):
    return Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS)

def dt(img, a=0.35):
    o = Image.new("RGBA", (W, H), (0, 0, 0, int(255*a)))
    return Image.alpha_composite(img.convert("RGBA"), o).convert("RGB")

def center(draw, text, y, font, color=WHITE, mw=W-120):
    lines = []
    for w in text.split():
        if not lines: lines.append(w)
        else:
            t = lines[-1] + " " + w
            b = draw.textbbox((0,0), t, font=font)
            if b[2]-b[0] <= mw: lines[-1] = t
            else: lines.append(w)
    lh = draw.textbbox((0,0),"A",font=font)[3]-draw.textbbox((0,0),"A",font=font)[1]
    sp = max(6,int(lh*0.3))
    th = lh*len(lines)+sp*(len(lines)-1)
    cy = y - th//2
    for ln in lines:
        tw = draw.textbbox((0,0),ln,font=font)[2]
        draw.text(((W-tw)//2,cy),ln,fill=color,font=font)
        cy += lh + sp

def build():
    bg = load_bg(os.path.join(IMG,"benefits-treatment.jpg"))
    bg = dt(bg, 0.38)
    draw = ImageDraw.Draw(bg)

    # === HEADER ===
    f_tag = ImageFont.truetype(FONT_R, 20)
    center(draw, "✦ VIA LASER LAS VEGAS ✦", 55, f_tag, GOLD, 800)

    f_h = ImageFont.truetype(FONT_SB, 60)
    f_s = ImageFont.truetype(FONT_B, 32)
    center(draw, "Bye Bye Acne", 160, f_h, WHITE, 900)
    center(draw, "Laser Treatment", 235, f_s, GOLD, 900)
    draw.line([(W//2-80,270),(W//2+80,270)], fill=GOLD, width=2)

    # === BENEFITS BOX ===
    bx, by, bw, bh = 70, 310, 580, 260
    draw.rounded_rectangle([bx,by,bx+bw,by+bh], radius=14, fill=(13,82,82,210))

    f_b = ImageFont.truetype(FONT_B, 24)
    bullets = ["ACNE CLEARING LASER","REDUCES ACNE SCARS","MINIMIZES PORES",
               "CALMS INFLAMMATION","COLLAGEN-BOOSTING"]
    by2 = by + 16
    for b in bullets:
        draw.ellipse([bx+22,by2+5,bx+32,by2+15], fill=GOLD)
        draw.text((bx+48,by2),b,fill=WHITE,font=f_b)
        by2 += 48

    # === BEFORE/AFTER INSET ===
    bax, bay = bx+bw+22, by+8
    bs = 200
    try:
        ba = Image.open(os.path.join(IMG,"before-after-1.jpg")).convert("RGB").resize((bs,bs), Image.LANCZOS)
        bg.paste(ba, (bax,bay))
        draw.rounded_rectangle([bax,bay+bs-34,bax+bs,bay+bs], radius=6, fill=(0,0,0,180))
        fl = ImageFont.truetype(FONT_B,17)
        draw.text((bax+14,bay+bs-26),"REAL RESULTS ✨",fill=GOLD,font=fl)
        draw.text((bax+14,bay+bs+8),"BEFORE → AFTER",fill=GOLD,font=fl)
    except: pass

    # === BOOK NOW ===
    bk_y = by + bh + 18
    center(draw, "BOOK NOW!", bk_y, ImageFont.truetype(FONT_B,28), WHITE, 400)
    center(draw, "9345 S Cimarron Rd, Las Vegas, NV 89178", bk_y+34,
           ImageFont.truetype(FONT_R,18), CREAM, 950)
    center(draw, "(725) 772-0948", bk_y+58,
           ImageFont.truetype(FONT_B,22), GOLD, 400)

    # === PRICING — SIDE BY SIDE, NO OVERLAP ===
    pr_top = bk_y + 105

    # --- LEFT: $129 pill ---
    pw, ph = 280, 110
    px = 140  # left side pill
    py = pr_top
    draw.rounded_rectangle([px,py,px+pw,py+ph], radius=55, fill=TEAL)

    f_l = ImageFont.truetype(FONT_R, 18)
    draw.text((px+55, py+8), "FOR ONLY", fill=CREAM, font=f_l)

    # Center $129 within the pill manually
    f_129 = ImageFont.truetype(FONT_B, 85)
    tw129 = draw.textbbox((0,0), "$129", font=f_129)[2]
    draw.text((px+(pw-tw129)//2, py+42), "$129", fill=WHITE, font=f_129)

    # --- RIGHT: Regular price ---
    rx = 590  # right side position
    f_rl = ImageFont.truetype(FONT_R, 17)
    f_rp = ImageFont.truetype(FONT_B, 38)
    draw.text((rx+20, pr_top+8), "REGULAR PRICE", fill=CREAM, font=f_rl)
    draw.text((rx+50, pr_top+38), "$299", fill=CREAM, font=f_rp)
    tw299 = draw.textbbox((0,0), "$299", font=f_rp)[2]
    draw.line([(rx+50, pr_top+80), (rx+50+tw299, pr_top+80)], fill=GOLD, width=4)

    # --- CENTER: SAVE $170 below both ---
    svy = py + ph + 18
    draw.rounded_rectangle([W//2-130, svy, W//2+130, svy+50], radius=25, fill=GOLD)
    center(draw, "SAVE $170 ✨", svy+27, ImageFont.truetype(FONT_B, 25), "#0a4242", 240)

    # === BOTTOM TAG ===
    center(draw, "✦ LAS VEGAS LADIES, THIS IS YOUR GLOW-UP SIGN ✨",
           H-35, ImageFont.truetype(FONT_B, 21), GOLD, 950)

    return bg

print("🖌 Building 1080x1080 ad v4 (fixed pricing layout)...")
img = build()
jpg = os.path.join(OUT,"acne_laser_ad_v4.jpg")
img.save(jpg, "JPEG", quality=95)
print(f"✅ Saved: {jpg} ({os.path.getsize(jpg)/1024:.0f} KB)")
