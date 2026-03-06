"""
Run this script first to test if image generation works on your system:
    python test_image.py
"""
import requests
import urllib.parse
import time
import io
import os

PROMPT = "breathtaking sunset over a calm river, orange pink purple sky, gentle ripples, distant trees, birds flying, serene peaceful mood, photorealistic"

print("=" * 60)
print("SANJU Image Generation Test")
print("=" * 60)

# ── Test 1: pollinations SDK ──
print("\n[Test 1] Trying pollinations SDK...")
try:
    import pollinations as pol
    img_model = pol.Image(model="flux", width=768, height=768, nologo=True, enhance=True)
    pil_img = img_model(PROMPT)
    buf = io.BytesIO()
    pil_img.save(buf, format="JPEG", quality=90)
    img_bytes = buf.getvalue()
    with open("test_output.jpg", "wb") as f:
        f.write(img_bytes)
    print(f"  ✅ SDK worked! Image saved as test_output.jpg ({len(img_bytes)//1024}KB)")
except ImportError:
    print("  ❌ pollinations not installed. Run: pip install pollinations")
except Exception as e:
    print(f"  ❌ SDK failed: {e}")

# ── Test 2: Direct HTTP ──
print("\n[Test 2] Trying direct HTTP (image.pollinations.ai)...")
try:
    encoded = urllib.parse.quote(PROMPT)
    seed = int(time.time())
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=768&height=768&nologo=true&model=flux&seed={seed}"
    print(f"  URL: {url[:80]}...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0"}
    print("  Waiting for response (may take 30-60s)...")
    resp = requests.get(url, timeout=120, headers=headers)
    print(f"  Status: {resp.status_code}, Size: {len(resp.content)} bytes")
    if resp.status_code == 200 and len(resp.content) > 5000:
        with open("test_http_output.jpg", "wb") as f:
            f.write(resp.content)
        print(f"  ✅ HTTP worked! Saved as test_http_output.jpg")
    else:
        print(f"  ❌ Bad response. Content: {resp.content[:200]}")
except Exception as e:
    print(f"  ❌ HTTP failed: {e}")

# ── Test 3: Together AI (free alternative) ──
print("\n[Test 3] Network check (google.com)...")
try:
    r = requests.get("https://www.google.com", timeout=5)
    print(f"  ✅ Internet working (status {r.status_code})")
except Exception as e:
    print(f"  ❌ No internet: {e}")

print("\n" + "=" * 60)
print("Done! Share the output above so we can debug.")
print("=" * 60)