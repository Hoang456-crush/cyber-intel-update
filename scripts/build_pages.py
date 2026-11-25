#!/usr/bin/env python3
"""
scripts/build_pages.py
Static Site Builder for GitHub Pages deployment.
- Scans reports/ and generates reports/index.json
- Copies web/index.html, cache/latest_intel.json, and reports/ into dist/
- Creates .nojekyll for GitHub Pages
"""

import os
import sys
import json
import shutil
import datetime
from pathlib import Path

def main():
    base_dir = Path(__file__).resolve().parent.parent
    reports_dir = base_dir / "reports"
    cache_dir = base_dir / ".agents" / "skills" / "daily-security-digest" / "cache"
    web_dir = base_dir / "web"
    dist_dir = base_dir / "dist"

    print("==================================================")
    print("🚀 BUILDING STATIC SITE FOR GITHUB PAGES")
    print(f"📁 Base Dir: {base_dir}")
    print("==================================================")

    # 1. Generate reports/index.json
    reports = []
    if reports_dir.exists():
        for f in sorted(reports_dir.glob("*.md"), reverse=True):
            mtime = datetime.datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            # Extract first title line if possible
            title = f.name
            try:
                with open(f, "r", encoding="utf-8") as rf:
                    first_line = rf.readline().strip()
                    if first_line.startswith("#"):
                        title = first_line.lstrip("# ").strip()
            except Exception:
                pass
            reports.append({
                "filename": f.name,
                "size": f.stat().st_size,
                "modified": mtime,
                "title": title
            })
    
    reports_index_file = reports_dir / "index.json"
    with open(reports_index_file, "w", encoding="utf-8") as f:
        json.dump({"reports": reports}, f, ensure_ascii=False, indent=2)
    print(f"[✓] Generated reports index: {reports_index_file} ({len(reports)} reports)")

    # 2. Clean and create dist directory
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir(parents=True, exist_ok=True)

    # 3. Copy web/index.html to dist/index.html
    html_src = web_dir / "index.html"
    if html_src.exists():
        shutil.copy2(html_src, dist_dir / "index.html")
        print(f"[✓] Copied index.html -> {dist_dir / 'index.html'}")
    else:
        print(f"[!] Warning: {html_src} not found!", file=sys.stderr)

    # 4. Copy cache files to dist/cache/
    dist_cache = dist_dir / "cache"
    dist_cache.mkdir(parents=True, exist_ok=True)
    intel_src = cache_dir / "latest_intel.json"
    if intel_src.exists():
        shutil.copy2(intel_src, dist_cache / "latest_intel.json")
        print(f"[✓] Copied latest_intel.json -> {dist_cache / 'latest_intel.json'}")
    else:
        # Create empty fallback intel file
        with open(dist_cache / "latest_intel.json", "w", encoding="utf-8") as f:
            json.dump({"collected_at": datetime.datetime.now().isoformat(), "top_actionable_cves": []}, f)
        print(f"[!] Warning: {intel_src} not found, created placeholder.", file=sys.stderr)

    cve_guides_src = cache_dir / "cve_guides.json"
    if cve_guides_src.exists():
        shutil.copy2(cve_guides_src, dist_cache / "cve_guides.json")
        print(f"[✓] Copied cve_guides.json -> {dist_cache / 'cve_guides.json'}")

    # 5. Copy reports/ to dist/reports/
    dist_reports = dist_dir / "reports"
    dist_reports.mkdir(parents=True, exist_ok=True)
    if reports_dir.exists():
        for item in reports_dir.iterdir():
            if item.is_file() and (item.suffix in [".md", ".json"]):
                shutil.copy2(item, dist_reports / item.name)
        print(f"[✓] Copied reports directory -> {dist_reports}")

    # 6. Add .nojekyll to prevent Jekyll processing on GitHub Pages
    nojekyll_file = dist_dir / ".nojekyll"
    nojekyll_file.touch()
    print(f"[✓] Created {nojekyll_file}")

    print("==================================================")
    print("🎉 BUILD SUCCESSFUL! Files ready in dist/")
    print("==================================================")

if __name__ == "__main__":
    main()
