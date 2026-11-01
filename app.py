# URLPulse - Bulk URL Health Checker
# Signature: Mourad.Soltani

"""
Minimal Bulk URL Health Checker micro-SaaS tool.
Check multiple URLs for status codes, response times, and health.
"""

from flask import Flask, request, jsonify, render_template
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

app = Flask(__name__)

# Signature: Mourad.Soltani

def check_url(url: str, timeout: int = 10) -> dict:
    """Check a single URL health."""
    start = time.time()
    try:
        # Add scheme if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        response = requests.get(url, timeout=timeout, allow_redirects=True)
        elapsed = round((time.time() - start) * 1000, 2)  # ms
        return {
            'url': url,
            'status_code': response.status_code,
            'healthy': 200 <= response.status_code < 400,
            'response_time_ms': elapsed,
            'error': None
        }
    except requests.RequestException as e:
        elapsed = round((time.time() - start) * 1000, 2)
        return {
            'url': url,
            'status_code': None,
            'healthy': False,
            'response_time_ms': elapsed,
            'error': str(e)
        }

def check_urls(urls: list, max_workers: int = 10) -> list:
    """Check multiple URLs concurrently."""
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(check_url, url.strip()): url for url in urls if url.strip()}
        for future in as_completed(future_to_url):
            results.append(future.result())
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/check', methods=['POST'])
def api_check():
    data = request.get_json() or {}
    urls = data.get('urls', [])
    if isinstance(urls, str):
        urls = [u.strip() for u in urls.split('\n') if u.strip()]
    if not urls:
        return jsonify({'error': 'No URLs provided'}), 400
    if len(urls) > 50:
        return jsonify({'error': 'Maximum 50 URLs per request'}), 400
    results = check_urls(urls)
    healthy_count = sum(1 for r in results if r['healthy'])
    return jsonify({
        'results': results,
        'summary': {
            'total': len(results),
            'healthy': healthy_count,
            'unhealthy': len(results) - healthy_count
        }
    })

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'service': 'URLPulse', 'signature': 'Mourad.Soltani'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
