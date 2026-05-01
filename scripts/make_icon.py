"""
Generate assets/AppIcon.icns from a simple programmatic design.
Requires: pip install Pillow
"""

import os
import struct
import subprocess
import sys
import tempfile
import zlib

try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False


SIZES = [16, 32, 64, 128, 256, 512, 1024]

# Icon: dark rounded square with "C" glyph in Anthropic orange
BG_COLOR = (30, 30, 30, 255)
FG_COLOR = (209, 97, 24, 255)   # Anthropic orange-ish


def make_png_pillow(size: int) -> bytes:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    radius = size // 5
    draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=BG_COLOR)

    font_size = int(size * 0.62)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except Exception:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), "C", font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - tw) // 2 - bbox[0]
    y = (size - th) // 2 - bbox[1]
    draw.text((x, y), "C", fill=FG_COLOR, font=font)

    import io
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def make_png_fallback(size: int) -> bytes:
    """Minimal valid PNG: solid dark square, no Pillow needed."""
    def chunk(name: bytes, data: bytes) -> bytes:
        c = name + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

    raw_rows = []
    for y in range(size):
        row = b"\x00"  # filter byte
        for x in range(size):
            row += bytes(BG_COLOR)
        raw_rows.append(row)

    compressed = zlib.compress(b"".join(raw_rows))
    ihdr_data = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr_data)
    png += chunk(b"IDAT", compressed)
    png += chunk(b"IEND", b"")
    return png


def build_icns(out_path: str) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        iconset = os.path.join(tmp, "AppIcon.iconset")
        os.makedirs(iconset)

        renderer = make_png_pillow if HAS_PILLOW else make_png_fallback
        if not HAS_PILLOW:
            print("Pillow not found — using plain dark square icon. Run: pip install Pillow")

        pairs = [
            (16,  "icon_16x16.png"),
            (32,  "icon_16x16@2x.png"),
            (32,  "icon_32x32.png"),
            (64,  "icon_32x32@2x.png"),
            (128, "icon_128x128.png"),
            (256, "icon_128x128@2x.png"),
            (256, "icon_256x256.png"),
            (512, "icon_256x256@2x.png"),
            (512, "icon_512x512.png"),
            (1024,"icon_512x512@2x.png"),
        ]

        rendered: dict[int, bytes] = {}
        for size, name in pairs:
            if size not in rendered:
                rendered[size] = renderer(size)
            with open(os.path.join(iconset, name), "wb") as f:
                f.write(rendered[size])

        subprocess.run(
            ["iconutil", "-c", "icns", iconset, "-o", out_path],
            check=True,
        )
        print(f"Icon written to {out_path}")


if __name__ == "__main__":
    dest = os.path.join(os.path.dirname(__file__), "..", "assets", "AppIcon.icns")
    dest = os.path.normpath(dest)
    build_icns(dest)
