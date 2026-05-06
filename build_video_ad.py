#!/usr/bin/env python3
"""
Via Laser — Acne Laser Video Ads
Teal + Gold brand · $129 / $299
Reference layout: laser.via style ad
"""
import subprocess, os, shutil, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT  = "/root/lead-form-lp-vialaser/video_ads"
IMG  = "/root/lead-form-lp-vialaser/images"
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1920  # 9:16 vertical

# Colors
C = {
    'teal':       '#0d5252',
    'teal_dark':  '#0a4242',
    'teal_light': '#e2eded',
    'gold':       '#d4a254',
    'gold_dark':  '#a87a30',
    'cream':      '#fdfcf8',
    'ink':        '#0a1f1f',
    'ink_soft':   '#4a5656',
    'white':      '#ffffff',
    'black':      '#000000',
}

FONT_B  = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

def load_bg(path):
    """Load image, center-crop to 9:16, resize to 1080x1920"""
    img = Image.open(path).convert("RGB")
    iw, ih = img.size
    target_ratio = H / W  # 1.778
    img_ratio = ih / iw
    if img_ratio > target_ratio:
        # taller than needed — crop height
        new_ih = int(iw * target_ratio)
        offset = (ih - new_ih) // 2
        img = img.crop((0, offset, iw, offset + new_ih))
    else:
        # wider than needed — crop width
        new_iw = int(ih / target_ratio)
        offset = (iw - new_iw) // 2
        img = img.crop((offset, 0, offset + new_iw, ih))
    return img.resize((W, H), Image.LANCZOS)

def darken(img, alpha=0.45):
    """Dark overlay"""
    o = Image.new("RGBA", (W, H), (0, 0, 0, int(255 * alpha)))
    c = img.convert("RGBA")
    return Image.alpha_composite(c, o).convert("RGB")

def wrap_text(draw, text, font, max_w):
    """Word-wrap text, return list of lines"""
    lines = []
    for word in text.split():
        if not lines:
            lines.append(word)
        else:
            test = lines[-1] + " " + word
            b = draw.textbbox((0, 0), test, font=font)
            if b[2] - b[0] <= max_w:
                lines[-1] = test
            else:
                lines.append(word)
    return lines

def draw_centered(draw, text, y, font, color=C['white'], max_w=W-160):
    """Centered text with auto-wrap"""
    lines = wrap_text(draw, text, font, max_w)
    lh = draw.textbbox((0, 0), "A", font=font)[3] - draw.textbbox((0, 0), "A", font=font)[1]
    sp = max(6, int(lh * 0.3))
    total = lh * len(lines) + sp * (len(lines) - 1)
    cy = y - total // 2
    for line in lines:
        tw = draw.textbbox((0, 0), line, font=font)[2]
        draw.text(((W - tw) // 2, cy), line, fill=color, font=font)
        cy += lh + sp

def draw_left(draw, text, x, y, font, color=C['white'], max_w=500):
    """Left-aligned with wrap"""
    lines = wrap_text(draw, text, font, max_w)
    lh = draw.textbbox((0, 0), "A", font=font)[3] - draw.textbbox((0, 0), "A", font=font)[1]
    for line in lines:
        draw.text((x, y), line, fill=color, font=font)
        y += lh + 4
    return y

# ================================================================
# SCENE FRAMES (each returns a PIL Image)
# ================================================================

def scene_hero():
    """Headline: 'Bye Bye Acne' + 'Laser Treatment' over treatment bg"""
    img = load_bg(os.path.join(IMG, "benefits-treatment.jpg"))
    img = darken(img, 0.48)
    draw = ImageDraw.Draw(img)
    
    # Top badge
    f_tag = ImageFont.truetype(FONT_SB, 26)
    draw_centered(draw, "✦ VIA LASER LAS VEGAS ✦", 320, f_tag, C['gold'], 800)
    
    # Headline
    f1 = ImageFont.truetype(FONT_B, 96)
    draw_centered(draw, "Bye Bye Acne", 700, f1, C['white'], 920)
    
    # Sub
    f2 = ImageFont.truetype(FONT_B, 44)
    draw_centered(draw, "Laser Treatment", 820, f2, C['gold'], 900)
    
    # Gold line
    draw.line([(W//2 - 100, 880), (W//2 + 100, 880)], fill=C['gold'], width=3)
    
    # Bottom hint
    f3 = ImageFont.truetype(FONT_R, 24)
    draw_centered(draw, "Clear Skin · Zero Downtime · Las Vegas NV", 950, f3, C['cream'], 900)
    
    return img

def scene_benefits():
    """Benefits box + before/after"""
    img = load_bg(os.path.join(IMG, "acne-treatment-1.jpg"))
    img = darken(img, 0.50)
    draw = ImageDraw.Draw(img)
    
    # Title
    f1 = ImageFont.truetype(FONT_B, 48)
    draw_centered(draw, "Why Acne Laser?", 160, f1, C['white'], 900)
    draw.line([(W//2 - 50, 210), (W//2 + 50, 210)], fill=C['gold'], width=2)
    
    # Benefits box
    bx, by, bw, bh = 60, 280, 600, 380
    draw.rounded_rectangle([bx, by, bx+bw, by+bh], radius=18, fill=(13, 82, 82, 200))
    
    f_b = ImageFont.truetype(FONT_B, 30)
    bullets = [
        "ACNE CLEARING LASER",
        "REDUCES ACNE SCARS",
        "MINIMIZES PORES",
        "CALMS INFLAMMATION",
        "COLLAGEN-BOOSTING",
        "ZERO DOWNTIME",
    ]
    by2 = by + 20
    for b in bullets:
        draw.ellipse([bx + 22, by2 + 6, bx + 32, by2 + 16], fill=C['gold'])
        draw.text((bx + 48, by2), b, fill=C['white'], font=f_b)
        by2 += 58
    
    # Before/After inset
    bax, bay = bx + bw + 25, by + 15
    ba_size = 240
    try:
        ba = Image.open(os.path.join(IMG, "before-after-1.jpg")).convert("RGB")
        ba = ba.resize((ba_size, ba_size), Image.LANCZOS)
        img.paste(ba, (bax, bay))
        # Bottom label overlay
        draw.rounded_rectangle([bax, bay+ba_size-40, bax+ba_size, bay+ba_size], 
                               radius=6, fill=(0,0,0,180))
        f_bal = ImageFont.truetype(FONT_B, 20)
        draw.text((bax+30, bay+ba_size-32), "REAL RESULTS ✨", fill=C['gold'], font=f_bal)
        draw.text((bax+30, bay+ba_size+10), "BEFORE → AFTER", fill=C['gold'], font=f_bal)
    except:
        pass
    
    return img

def scene_pricing():
    """$129 / $299 focus"""
    img = load_bg(os.path.join(IMG, "transformation-1.jpg"))
    img = darken(img, 0.52)
    draw = ImageDraw.Draw(img)
    
    # Tag
    f_tag = ImageFont.truetype(FONT_R, 24)
    draw_centered(draw, "★ LIMITED TIME ★", 380, f_tag, C['gold'], 700)
    
    # Price pill
    f_price = ImageFont.truetype(FONT_B, 130)
    pw, ph = 380, 140
    px, py = (W-pw)//2, 480
    draw.rounded_rectangle([px, py, px+pw, py+ph], radius=70, fill=C['teal'])
    
    draw_centered(draw, "FOR ONLY", py-50, ImageFont.truetype(FONT_R, 24), C['cream'], 300)
    draw_centered(draw, "$129", py+ph//2+10, f_price, C['white'], 300)
    
    f_s = ImageFont.truetype(FONT_R, 22)
    draw_centered(draw, "per session", py+ph+20, f_s, C['cream'], 500)
    
    # Regular price
    fy = py + ph + 90
    f_r = ImageFont.truetype(FONT_R, 24)
    f_rp = ImageFont.truetype(FONT_B, 48)
    draw_centered(draw, "REGULAR PRICE", fy, f_r, C['cream'], 500)
    draw_centered(draw, "$299", fy+55, f_rp, C['cream'], 200)
    # Strike through
    cw = draw.textbbox((0, 0), "$299", font=f_rp)[2]
    draw.line([(W//2 - cw//2, fy+95), (W//2 + cw//2, fy+95)], fill=C['gold'], width=5)
    
    # Save badge
    svy = fy + 130
    draw.rounded_rectangle([W//2-170, svy, W//2+170, svy+65], radius=32, fill=C['gold'])
    draw_centered(draw, "SAVE $170 ✨", svy+35, ImageFont.truetype(FONT_B, 30), C['teal_dark'], 300)
    
    # Bottom
    draw_centered(draw, "Safe for All Skin Types · Zero Downtime · Las Vegas Studio", 
                  1420, f_s, C['cream'], 900)
    
    return img

def scene_cta():
    """Book Now CTA"""
    img = Image.new("RGB", (W, H), color=C['teal_dark'])
    draw = ImageDraw.Draw(img)
    
    # Gold accent
    draw.rectangle([0, 0, W, 8], fill=C['gold'])
    
    f1 = ImageFont.truetype(FONT_SB, 52)
    draw_centered(draw, "Your Clear Skin", 360, f1, C['white'], 900)
    draw_centered(draw, "Starts Here", 430, f1, C['white'], 900)
    
    draw.line([(W//2-50, 470), (W//2+50, 470)], fill=C['gold'], width=2)
    
    # Book button
    bw, bh = 380, 80
    bx, by = (W-bw)//2, 540
    draw.rounded_rectangle([bx, by, bx+bw, by+bh], radius=40, fill=C['gold'])
    draw_centered(draw, "BOOK NOW ➜", by+bh//2+2, 
                  ImageFont.truetype(FONT_B, 48), C['teal_dark'], 320)
    
    # Info
    f2 = ImageFont.truetype(FONT_R, 28)
    f3 = ImageFont.truetype(FONT_B, 34)
    
    draw_centered(draw, "Via Laser", 700, ImageFont.truetype(FONT_SB, 40), C['gold'], 800)
    draw_centered(draw, "9345 S Cimarron Rd · Las Vegas, NV 89178", 760, f2, C['cream'], 900)
    draw_centered(draw, "(725) 772-0948", 810, f3, C['white'], 500)
    
    # Bottom tag
    draw_centered(draw, "✦ LAS VEGAS LADIES, THIS IS YOUR GLOW-UP SIGN ✨", 
                  1560, ImageFont.truetype(FONT_B, 26), C['gold'], 950)
    
    # Fine print
    draw_centered(draw, "Pay upon arrival · Appointments filling quickly", 
                  1720, ImageFont.truetype(FONT_R, 20), C['cream'], 800)
    
    return img

# ================================================================
# STATIC AD (reference layout)
# ================================================================

def static_ad():
    """Full layout matching reference: hero img → headline → benefits+ba → book → pricing → tag"""
    bg = load_bg(os.path.join(IMG, "benefits-treatment.jpg"))
    bg = darken(bg, 0.45)
    draw = ImageDraw.Draw(bg)
    
    # === HEADLINE ===
    f_h = ImageFont.truetype(FONT_B, 72)
    f_s = ImageFont.truetype(FONT_B, 36)
    draw_centered(draw, "Bye Bye Acne", 200, f_h, C['white'], 920)
    draw_centered(draw, "Laser Treatment", 290, f_s, C['gold'], 900)
    
    # === BENEFITS + B/A ===
    bx, by, bw, bh = 70, 400, 560, 340
    draw.rounded_rectangle([bx, by, bx+bw, by+bh], radius=16, fill=(10, 31, 31, 200))
    
    f_b = ImageFont.truetype(FONT_B, 28)
    bullets = [
        "ACNE CLEARING LASER",
        "REDUCES ACNE SCARS",
        "MINIMIZES PORES",
        "CALMS INFLAMMATION",
        "COLLAGEN-BOOSTING",
    ]
    by2 = by + 20
    for b in bullets:
        draw.ellipse([bx+22, by2+5, bx+32, by2+15], fill=C['gold'])
        draw.text((bx+46, by2), b, fill=C['white'], font=f_b)
        by2 += 62
    
    # Before/After inset
    bax, bay = bx+bw+25, by+10
    bs = 220
    try:
        ba = Image.open(os.path.join(IMG, "before-after-1.jpg")).convert("RGB")
        ba = ba.resize((bs, bs), Image.LANCZOS)
        bg.paste(ba, (bax, bay))
        draw.rounded_rectangle([bax, bay+bs-38, bax+bs, bay+bs], radius=6, fill=(0,0,0,180))
        f_bal = ImageFont.truetype(FONT_B, 18)
        draw.text((bax+22, bay+bs-30), "REAL RESULTS ✨", fill=C['gold'], font=f_bal)
        draw.text((bax+22, bay+bs+8), "BEFORE → AFTER", fill=C['gold'], font=f_bal)
    except:
        pass
    
    # === BOOK INFO ===
    biy = by + bh + 35
    f_c = ImageFont.truetype(FONT_B, 32)
    f_a = ImageFont.truetype(FONT_R, 22)
    draw_centered(draw, "BOOK NOW!", biy, f_c, C['white'], 400)
    draw_centered(draw, "9345 S Cimarron Rd, Las Vegas, NV 89178", biy+48, f_a, C['cream'], 900)
    draw_centered(draw, "(725) 772-0948", biy+78, ImageFont.truetype(FONT_B, 26), C['gold'], 400)
    
    # === PRICING ===
    pry = biy + 140
    f_lbl = ImageFont.truetype(FONT_R, 22)
    
    # $129 pill
    pw, ph = 280, 85
    px, py = W//2 - 320, pry
    draw.rounded_rectangle([px, py, px+pw, py+ph], radius=42, fill=C['teal'])
    draw.text((px+30, py+8), "FOR ONLY", fill=C['cream'], font=f_lbl)
    draw_centered(draw, "$129", py+ph//2+8, 
                  ImageFont.truetype(FONT_B, 85), C['white'], pw-20)
    draw.text((px+210, py+50), "per session", fill=C['cream'], font=ImageFont.truetype(FONT_R, 18))
    
    # $299 regular
    rx = W//2 + 10
    draw.text((rx, pry+6), "REGULAR PRICE", fill=C['cream'], font=f_lbl)
    f_rp = ImageFont.truetype(FONT_B, 42)
    draw.text((rx+10, pry+34), "$299", fill=C['cream'], font=f_rp)
    draw.line([(rx+10, pry+80), (rx+130, pry+80)], fill=C['gold'], width=4)
    
    # Save badge
    svy = pry + 110
    draw.rounded_rectangle([W//2-130, svy, W//2+130, svy+55], radius=28, fill=C['gold'])
    draw_centered(draw, "SAVE $170 ✨", svy+30, ImageFont.truetype(FONT_B, 26), C['teal_dark'], 240)
    
    # === BOTTOM TAG ===
    draw_centered(draw, "✦ LAS VEGAS LADIES, THIS IS YOUR GLOW-UP SIGN ✨", 
                  1680, ImageFont.truetype(FONT_B, 24), C['gold'], 950)
    
    return bg

# ================================================================
# VIDEO BUILDER
# ================================================================

def build_video():
    """Build 9:16 video ~8s with Ken Burns zoom and crossfade transitions"""
    frames_dir = os.path.join(OUT, "_frames")
    os.makedirs(frames_dir, exist_ok=True)
    
    scenes = [
        ("hero", scene_hero),
        ("benefits", scene_benefits),
        ("pricing", scene_pricing),
        ("cta", scene_cta),
    ]
    
    FPS = 24
    SECONDS_PER_SCENE = 2.5
    FRAMES_PER_SCENE = int(FPS * SECONDS_PER_SCENE)
    ZOOM_MAX = 1.08  # 8% zoom over the scene duration
    
    idx = 0
    for name, fn in scenes:
        base = fn()
        iw, ih = base.size
        for i in range(FRAMES_PER_SCENE):
            t = i / max(FRAMES_PER_SCENE - 1, 1)
            zoom = 1 + (ZOOM_MAX - 1) * t
            nw, nh = int(iw * zoom), int(ih * zoom)
            zoomed = base.resize((nw, nh), Image.LANCZOS)
            left = (nw - iw) // 2
            top = (nh - ih) // 2
            frame = zoomed.crop((left, top, left + iw, top + ih))
            fp = os.path.join(frames_dir, f"f_{idx:04d}.png")
            frame.save(fp, "PNG")
            idx += 1
        print(f"  Scene '{name}': {FRAMES_PER_SCENE} frames")
    
    total_frames = idx
    total_sec = total_frames / FPS
    print(f"\n  Total: {total_frames} frames = {total_sec:.1f}s at {FPS}fps")
    
    # Render video — use concat with crossfade
    # We'll render each scene as a separate video, then crossfade with ffmpeg
    video_path = os.path.join(OUT, "acne_laser_reel.mp4")
    
    # Simple approach: render all frames as one video
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", f"{frames_dir}/f_%04d.png",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        "-crf", "20",
        "-r", str(FPS),
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=#0a1f1f",
        video_path
    ]
    
    subprocess.run(cmd, check=True, capture_output=True)
    
    # Clean up frames
    shutil.rmtree(frames_dir)
    
    # Verify
    dur = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", video_path
    ], capture_output=True, text=True)
    print(f"\n  ✅ Video: {video_path} ({dur.stdout.strip()}s)")
    
    return video_path

# ================================================================
# MAIN
# ================================================================

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════╗")
    print("║  Via Laser — Acne Laser Video Ads Builder   ║")
    print("║  Teal + Gold · $129 / $299                  ║")
    print("╚══════════════════════════════════════════════╝")
    
    # Static ad
    print("\n📸 Building static ad...")
    s_img = static_ad()
    s_png = os.path.join(OUT, "acne_laser_ad_static.png")
    s_jpg = os.path.join(OUT, "acne_laser_ad_static.jpg")
    s_img.save(s_png, "PNG")
    s_img.save(s_jpg, "JPEG", quality=92)
    print(f"  ✅ PNG: {s_png}")
    print(f"  ✅ JPG: {s_jpg}")
    
    # Video reel
    print("\n🎬 Building video reel...")
    v_path = build_video()
    
    # Summary
    print(f"\n{'='*50}")
    print(f"📁 All files in: {OUT}")
    for f in sorted(os.listdir(OUT)):
        if f.endswith(('.mp4', '.png', '.jpg')) and not f.startswith('_'):
            fp = os.path.join(OUT, f)
            sz = os.path.getsize(fp)
            print(f"  📄 {f:40s} {sz/1024:.0f} KB")
