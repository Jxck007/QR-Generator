# Quick Free QR Generator

Small Python CLI tool to generate QR code images from links or plain text.

## Web App

A premium, production-ready QR Code Generator web app is available as `index.html`. Open it in any modern web browser for a full-featured QR generation experience with customization options, patterns, logos, and export capabilities.

## Requirements

- Python 3.9+
- Dependencies in `requirements.txt`

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Usage

Generate from URL:

```powershell
python qr_generator.py "https://example.com"
```

Generate from text with custom file name:

```powershell
python qr_generator.py "hello world" --name my_qr
```

Save to a custom output folder:

```powershell
python qr_generator.py --data "https://example.com/page" --out-dir output
```

Adjust QR size/border:

```powershell
python qr_generator.py "https://example.com" --size 12 --border 4
```

## Notes

- Images are saved as PNG.
- Default output folder is `qr_output`.
- If `--name` is not provided, the tool auto-generates a safe filename.
