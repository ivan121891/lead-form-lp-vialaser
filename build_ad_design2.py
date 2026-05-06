#!/usr/bin/env python3
"""Via Laser — Acne Laser Ad Design #2 (totally different style)"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = "/root/lead-form-lp-vialaser/video_ads"
IMG = "/root/lead-form-lp-vialaser/images"
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1080

FONT_B  = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

TEAL       = "#0d5252"
TEAL_DARK  = "#0a4242"
GOLD       = "#d4a254"
CREAM      = "#fdfcf8"
WHITE      = "#ffffff"
INK        = "#0a1f1f"

def load_bg(path):
    return Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS)

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
    """
    DESIGN 2: Bold full-bleed treatment image.
    Split layout — image on top 65%, solid teal panel on bottom 35%.
    No darken overlay. Text sits on the solid bottom panel instead.
    """
    # === TOP: Full-bleed image ===
    split_y = int(H * 0.65)
    
    img = load_bg(os.path.join(IMG, "transformation-2.jpg"))
    draw = ImageDraw.Draw(img)
    
    # Blur the image slightly for a softer look
    blur_img = img.filter(ImageFilter.GaussianBlur(radius=2))
    img.paste(blur_img)
    draw = ImageDraw.Draw(img)
    
    # === BOTTOM: Solid teal panel with soft top edge ===
    panel_top = split_y - 30
    draw.rectangle([0, panel_top, W, H], fill=TEAL_DARK)
    
    # Gold accent line at panel top
    draw.line([(80, panel_top + 5), (W - 80, panel_top + 5)], fill=GOLD, width=2)
    
    # === ON IMAGE SECTION (top) ===
    # Big bold headline on the image area
    f1 = ImageFont.truetype(FONT_SB, 72)
    
    # "Bye Bye Acne" with a subtle text shadow
    draw.text((W//2 - 250, 100), "Bye Bye", fill=WHITE, font=f1)
    draw.text((W//2 - 250, 185), "Acne", fill=GOLD, font=f1)
    
    # Tagline
    f2 = ImageFont.truetype(FONT_R, 24)
    center(draw, "Advanced Laser Technology · Zero Downtime", 320, f2, CREAM, 900)
    
    # === ON TEAL PANEL (bottom) ===
    py = panel_top + 40
    
    # "Only" label
    center(draw, "✦ LIMITED TIME OFFER ✦", py, 
           ImageFont.truetype(FONT_R, 20), GOLD, 600)
    
    # Large $129
    f_big = ImageFont.truetype(FONT_B, 96)
    center(draw, "$129", py + 55, f_big, WHITE, 500)
    
    # "per session" next to it smaller
    f_s = ImageFont.truetype(FONT_R, 22)
    center(draw, "per session — regular $299", py + 120, f_s, CREAM, 500)
    
    # Strike $299
    tw = draw.textbbox((0,0), "$299", font=f_s)[2]
    cx = (W - tw) // 2
    draw.line([(cx, py + 140), (cx + tw, py + 140)], fill=GOLD, width=3)
    
    # Save badge
    svy = py + 145
    draw.rounded_rectangle([W//2-140, svy, W//2+140, svy+52], radius=26, fill=GOLD)
    center(draw, "SAVE $170 ✨", svy+28, ImageFont.truetype(FONT_B, 24), TEAL_DARK, 260)
    
    # === BOTTOM INFO ===
    info_y = svy + 70
    f_b = ImageFont.truetype(FONT_B, 26)
    f_sm = ImageFont.truetype(FONT_R, 20)
    center(draw, "BOOK NOW — (725) 772-0948", info_y, f_b, GOLD, 800)
    center(draw, "9345 S Cimarron Rd, Las Vegas, NV 89178", info_y + 35, f_sm, CREAM, 900)
    
    return img

print("🖌 Building Design #2 — full-bleed + teal panel...")
img = build()
jpg = os.path.join(OUT, "acne_laser_ad_design2.jpg")
img.save(jpg, "JPEG", quality=95)
print(f"✅ Saved: {jpg} ({os.path.getsize(jpg)/1024:.0f} KB)")
