

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import urlparse


try:
    import qrcode
except ImportError as exc:
    raise SystemExit(
        "Missing dependency: qrcode. Install with: pip install qrcode[pil]"
    ) from exc


def _slugify(value: str, max_len: int = 60) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", value).strip("_")
    if not cleaned:
        return "qr_code"
    return cleaned[:max_len]


def _default_name_from_data(data: str) -> str:
    parsed = urlparse(data)
    if parsed.scheme and parsed.netloc:
        host = parsed.netloc.replace("www.", "")
        path = parsed.path.strip("/")
        base = f"{host}_{path}" if path else host
        return _slugify(base)
    return _slugify(data)


def generate_qr(data: str, output_path: Path, size: int = 10, border: int = 4) -> Path:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    image = qr.make_image(fill_color="black", back_color="white")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, format="PNG")
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate QR code image from text or URL")
    parser.add_argument("text", nargs="?", help="Text or URL to encode")
    parser.add_argument("--data", help="Text or URL to encode (same as positional)")
    parser.add_argument("--name", help="Output file name without extension")
    parser.add_argument(
        "--out-dir",
        default="qr_output",
        help="Folder where PNG image is saved (default: qr_output)",
    )
    parser.add_argument(
        "--size",
        type=int,
        default=10,
        help="QR pixel size per box (default: 10)",
    )
    parser.add_argument(
        "--border",
        type=int,
        default=4,
        help="QR border size (default: 4)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data = args.data or args.text

    if not data:
        raise SystemExit(
            "Please provide text or URL. Example: python qr_generator.py \"https://example.com\""
        )

    if args.size < 1 or args.border < 0:
        raise SystemExit("Invalid size/border. Use size >= 1 and border >= 0.")

    base_name = _slugify(args.name) if args.name else _default_name_from_data(data)
    output_path = Path(args.out_dir) / f"{base_name}.png"

    saved = generate_qr(data=data, output_path=output_path, size=args.size, border=args.border)
    print(f"QR code saved: {saved.resolve()}")


if __name__ == "__main__":
    main()
