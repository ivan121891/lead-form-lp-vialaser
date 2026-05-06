#!/usr/bin/env python3
"""Via Laser — Alternative Acne Laser Ad (different design)"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = "/root/lead-form-lp-vialaser/video_ads"
IMG = "/root/lead-form-lp-vialaser/images"
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1920
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_S = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

TEAL = "#0d5252"
GOLD = "#d4a254"
CREAM = "#fdfcf8"
WHITE = "#ffffff"
INK = "#0a1f1f"

def load_bg(path):
    img = Image.open(path).convert("RGB")
    iw, ih = img.size
    tr = H / W
    ir = ih / iw
    if ir > tr:
        nh = int(iw * tr)
        o = (ih - nh) // 2
        img = img.crop((0, o, iw, o + nh))
    else:
        nw = int(ih / tr)
        o = (iw - nw) // 2
        img = img.crop((o, 0, o + nw, ih))
    return img.resize((W, H), Image.LANCZOS)

def center(draw, text, y, font, color=WHITE, mw=W-160):
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

# ================================================================
# DESIGN 2 — Clean, modern card-style, split layout
# Top half: image | Bottom half: clean info card on teal
# ================================================================

def build():
    bg = load_bg(os.path.join(IMG, "benefits-treatment.jpg"))
    
    # Split: top 55% is image, bottom 45% is solid teal card
    split_y = int(H * 0.48)
    
    # Darken the image portion slightly
    overlay = Image.new("RGBA", (W, split_y), (0, 0, 0, int(255 * 0.35)))
    img_part = bg.crop((0, 0, W, split_y)).convert("RGBA")
    img_part = Image.alpha_composite(img_part, overlay)
    bg.paste(img_part, (0, 0))
    
    draw = ImageDraw.Draw(bg)
    
    # Teal card on bottom
    card_y = split_y - 40
    draw.rounded_rectangle([0, card_y, W, H], radius=30, fill=TEAL)
    
    # === TOP HALF — Overlaid text on image ===
    f1 = ImageFont.truetype(FONT_S, 72)
    f2 = ImageFont.truetype(FONT_B, 36)
    f3 = ImageFont.truetype(FONT_R, 20)
    
    center(draw, "Bye Bye Acne", 200, f1, WHITE, 900)
    center(draw, "Laser Treatment", 290, f2, GOLD, 900)
    center(draw, "Clear Skin · Zero Downtime · Safe for All Skin Types", 360, f3, CREAM, 900)
    
    # Gold divider
    draw.line([(W//2 - 80, 400), (W//2 + 80, 400)], fill=GOLD, width=2)
    
    # === BOTTOM CARD — Clean info grid ===
    
    # Benefits — 2 columns, 3 rows
    f_ben = ImageFont.truetype(FONT_B, 26)
    f_ben_s = ImageFont.truetype(FONT_R, 20)
    
    benefits = [
        ("✓ Acne Clearing", "Targets breakouts at the source"),
        ("✓ Scar Reduction", "Fades post-acne marks"),
        ("✓ Pore Minimizing", "Refines skin texture"),
        ("✓ Calms Inflammation", "Reduces redness & swelling"),
        ("✓ Collagen Boost", "Stimulates natural repair"),
        ("✓ Zero Downtime", "Return to your day immediately"),
    ]
    
    col_w = 460
    start_x = 60
    start_y = card_y + 60
    row_h = 70
    
    for i, (title, desc) in enumerate(benefits):
        col = i % 2
        row = i // 2
        x = start_x + col * col_w
        y = start_y + row * row_h
        
        draw.text((x, y), title, fill=GOLD, font=f_ben)
        draw.text((x, y + 30), desc, fill=CREAM, font=f_ben_s)
    
    # === PRICING ===
    pr_y = start_y + 3 * row_h + 30
    
    # "for only" label
    f_lbl = ImageFont.truetype(FONT_R, 22)
    center(draw, "FOR ONLY", pr_y, f_lbl, CREAM, 400)
    
    # $129 big
    f_big = ImageFont.truetype(FONT_B, 100)
    center(draw, "$129", pr_y + 50, f_big, WHITE, 300)
    
    # Regular price
    f_r = ImageFont.truetype(FONT_R, 20)
    f_rp = ImageFont.truetype(FONT_B, 36)
    center(draw, "REGULAR PRICE", pr_y + 130, f_r, CREAM, 500)
    center(draw, "$299", pr_y + 165, f_rp, CREAM, 200)
    tw = draw.textbbox((0, 0), "$299", font=f_rp)[2]
    draw.line([(W//2 - tw//2, pr_y + 200), (W//2 + tw//2, pr_y + 200)], fill=GOLD, width=4)
    
    # Save badge
    svy = pr_y + 215
    draw.rounded_rectangle([W//2 - 140, svy, W//2 + 140, svy + 58], radius=29, fill=GOLD)
    center(draw, "SAVE $170", svy + 32, ImageFont.truetype(FONT_B, 28), TEAL, 250)
    
    # === BOTTOM INFO ===
    info_y = svy + 85
    f_info = ImageFont.truetype(FONT_B, 30)
    f_addr = ImageFont.truetype(FONT_R, 22)
    
    center(draw, "Book Now — (725) 772-0948", info_y, f_info, GOLD, 800)
    center(draw, "9345 S Cimarron Rd, Las Vegas, NV 89178", info_y + 50, f_addr, CREAM, 900)
    
    # Bottom tag
    center(draw, "✦ LAS VEGAS LADIES, YOUR GLOW-UP AWAITS ✨", 
           H - 50, ImageFont.truetype(FONT_B, 22), GOLD, 950)
    
    return bg

# Run
print("🖌 Building alternate design...")
img = build()
jpg = os.path.join(OUT, "acne_laser_ad_v2.jpg")
img.save(jpg, "JPEG", quality=95)
print(f"✅ Saved: {jpg} ({os.path.getsize(jpg)/1024:.0f} KB)")
