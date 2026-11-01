# URLPulse - Bulk URL Health Checker

**Signature: Mourad.Soltani**

A minimal, shippable micro-SaaS tool for checking the health of multiple URLs at once.

## Features

- Bulk check up to 50 URLs concurrently
- Reports HTTP status code, response time (ms), and health status (2xx/3xx)
- Simple web UI
- JSON API endpoint
- Health check endpoint

## Quick Start

```bash
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000

## API

POST /api/check

```json
{
  "urls": ["https://example.com", "https://github.com"]
}
```

Or pass a newline-separated string.

GET /health → `{"status": "ok", ...}`

## Tests

```bash
pytest
```

## License

MIT - see LICENSE

Built by Mourad.Soltani
