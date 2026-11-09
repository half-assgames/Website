"""Makes the website's images and fonts from the game's store art.

Run it again whenever the store screenshots or key art change:

    uv run --no-project --with pillow --with fonttools --with brotli python tools/build-assets.py

It reads the studio logo from Documents\Half-Ass Games\Brand, and the store art and UI
fonts from the Unity project, and writes small, web-sized copies into docs. It never
changes the originals.
"""

from pathlib import Path
import shutil

from PIL import Image, ImageChops, ImageDraw, ImageFilter
from fontTools import subset

UNITY = Path(r"C:\UnityProjects\Submarine_Game")
GRAPHICS = UNITY / "Store" / "Graphics"
FONTS = UNITY / "Assets" / "_DeepSeaPanic" / "UI" / "Fonts"
REPO = Path(__file__).resolve().parent.parent
STUDIO_LOGO = REPO.parent / "Brand" / "Half-Ass-Games-logo.png"   # the studio folder's Brand

SITE = REPO / "docs"
IMG = SITE / "img" / "deep-sea-panic"
FONT_OUT = SITE / "fonts"

NAVY = (14, 34, 54)         # #0E2236, the site's panel colour
NAVY_DEEP = (7, 18, 31)     # #07121F, the site's background

# The five screenshots used on itch.io, in the same order.
SCREENSHOTS = [
    "01-chain-reaction",
    "02-bubble-burst",
    "03-treasure-and-crates",
    "05-five-subs-shop",
    "06-run-summary",
]
TRAILER_POSTER = "08-main-menu"


def resized(src: Path, width: int) -> Image.Image:
    im = Image.open(src).convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    return im


def save_webp(im: Image.Image, dest: Path, quality: int = 80) -> None:
    im.save(dest, "WEBP", quality=quality, method=6)
    print(f"  {dest.relative_to(SITE)}  {dest.stat().st_size // 1024} KB")


def save_jpg(im: Image.Image, dest: Path, quality: int = 84) -> None:
    im.save(dest, "JPEG", quality=quality, optimize=True, progressive=True)
    print(f"  {dest.relative_to(SITE)}  {dest.stat().st_size // 1024} KB")


def images() -> None:
    IMG.mkdir(parents=True, exist_ok=True)
    key_art = GRAPHICS / "Feature options" / "feature-A-key-art.png"
    for w in (640, 1024):
        save_webp(resized(key_art, w), IMG / f"key-art-{w}.webp", 82)
    # Link previews (Discord, Facebook, iMessage...) want a JPEG.
    save_jpg(resized(key_art, 1024), IMG / "key-art-share.jpg")

    icon = GRAPHICS / "app-icon-512.png"
    save_webp(resized(icon, 256), IMG / "icon-256.webp", 85)

    for name in SCREENSHOTS:
        src = GRAPHICS / "Screenshots" / f"{name}.png"
        for w in (800, 1600):
            save_webp(resized(src, w), IMG / f"{name}-{w}.webp", 78)

    # The picture on the trailer's play button.
    poster = GRAPHICS / "Screenshots" / f"{TRAILER_POSTER}.png"
    for w in (800, 1600):
        save_webp(resized(poster, w), IMG / f"trailer-poster-{w}.webp", 78)


def sticker(src: Path, border: int = 9):
    """Cuts the logo off its flat cream background, keeping a thin cream edge like a sticker.
    Returns the cut-out and the (left, top) of where it sat in the original."""
    im = Image.open(src).convert("RGB")
    w, h = im.size
    bg = im.getpixel((0, 0))
    work = im.copy()
    mark = (1, 254, 3)  # a colour the logo never uses
    edge = [(x, 0) for x in range(0, w, 12)] + [(x, h - 1) for x in range(0, w, 12)]
    edge += [(0, y) for y in range(0, h, 12)] + [(w - 1, y) for y in range(0, h, 12)]
    for xy in edge:
        p = work.getpixel(xy)
        if p != mark and sum(abs(a - b) for a, b in zip(p, bg)) < 60:
            ImageDraw.floodfill(work, xy, mark, thresh=40)
    not_bg = ImageChops.difference(work, Image.new("RGB", (w, h), mark)).convert("L").point(lambda v: 255 if v else 0)
    alpha = not_bg.filter(ImageFilter.MaxFilter(2 * border + 1)).filter(ImageFilter.GaussianBlur(1.2))
    out = im.convert("RGBA")
    out.putalpha(alpha)
    box = alpha.getbbox()
    return out.crop(box), box[:2]


def fit(im: Image.Image, size: int, pad: int = 0, bg=None) -> Image.Image:
    """Scales an RGBA image into a size x size square, centred."""
    box = size - 2 * pad
    scale = min(box / im.width, box / im.height)
    small = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    sq = Image.new("RGBA", (size, size), bg + (255,) if bg else (0, 0, 0, 0))
    sq.alpha_composite(small, ((size - small.width) // 2, (size - small.height) // 2))
    return sq


def logo() -> None:
    out = SITE / "img"
    full, (left, top) = sticker(STUDIO_LOGO)
    small = full.resize((560, round(full.height * 560 / full.width)), Image.LANCZOS)
    small.save(out / "half-ass-games-logo.webp", "WEBP", quality=88, method=6)
    print(f"  img/half-ass-games-logo.webp  {(out / 'half-ass-games-logo.webp').stat().st_size // 1024} KB")

    # The donkey peeking over its sign, for the header and browser tabs.
    # The box is in the original logo's pixels: ear tips down to the top of the sign.
    head = full.crop((385 - left, 15 - top, 1010 - left, 520 - top))
    side = max(head.size)
    peek = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    peek.alpha_composite(head, ((side - head.width) // 2, side - head.height))

    fit(peek, 128).save(out / "donkey-128.webp", "WEBP", quality=90, method=6)
    fit(peek, 48).save(SITE / "favicon-48.png", optimize=True)
    fit(peek, 192).save(SITE / "icon-192.png", optimize=True)
    # iPhones fill see-through corners with black, so this one gets the navy behind it.
    fit(peek, 180, pad=14, bg=NAVY).convert("RGB").save(SITE / "apple-touch-icon.png", optimize=True)
    print("  img/donkey-128.webp, favicon-48.png, icon-192.png, apple-touch-icon.png")

    # Link preview for the home page (1200 x 630 is what Facebook, Discord and others expect).
    card = Image.new("RGB", (1200, 630), NAVY_DEEP)
    glow = Image.new("L", (1200, 630), 0)
    ImageDraw.Draw(glow).ellipse((250, -260, 950, 560), fill=110)
    card.paste(Image.new("RGB", (1200, 630), (34, 92, 128)), (0, 0), glow.filter(ImageFilter.GaussianBlur(120)))
    art = full.resize((round(full.width * 560 / full.height), 560), Image.LANCZOS)
    card.paste(art, ((1200 - art.width) // 2, 35), art)
    card.save(SITE / "img" / "half-ass-games-share.jpg", "JPEG", quality=86, optimize=True, progressive=True)
    print("  img/half-ass-games-share.jpg")


# Basic Latin, Latin-1 (accents, ©, ×) and the punctuation the copy uses.
UNICODES = "U+0020-007E,U+00A0-00FF,U+2013-2014,U+2018-201A,U+201C-201E,U+2022,U+2026,U+2190-2193,U+2122"


def fonts() -> None:
    FONT_OUT.mkdir(parents=True, exist_ok=True)
    for ttf, out in (("Bungee-Regular.ttf", "bungee.woff2"), ("Nunito-SemiBold.ttf", "nunito-semibold.woff2")):
        dest = FONT_OUT / out
        subset.main([
            str(FONTS / ttf),
            f"--unicodes={UNICODES}",
            "--flavor=woff2",
            "--layout-features=*",
            f"--output-file={dest}",
        ])
        print(f"  {dest.relative_to(SITE)}  {dest.stat().st_size // 1024} KB")
    # The fonts are free under the SIL Open Font License, which travels with them.
    for lic, out in (("Bungee-OFL.txt", "Bungee-OFL.txt"), ("Nunito-OFL.txt", "Nunito-OFL.txt")):
        shutil.copyfile(FONTS / lic, FONT_OUT / out)


if __name__ == "__main__":
    print("Studio logo:")
    logo()
    print("Game images:")
    images()
    print("Fonts:")
    fonts()
    print("Done.")
