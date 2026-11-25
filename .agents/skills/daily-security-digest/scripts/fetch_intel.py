#!/usr/bin/env python3
"""
fetch_intel.py
Automated Security Intelligence Collector for Daily Security Digest.
Collects:
- CISA Known Exploited Vulnerabilities (KEV)
- ProjectDiscovery Nuclei-Templates new CVEs and PoCs
- HackerOne Disclosed Reports (via community disclosures database)
- Bugcrowd Blog & Research (via lxml HTML parser)
- YesWeHack Blog & Disclosures (via lxml HTML parser)
- Hacking & Offensive Security News (The Hacker News, CyberSecurityNews, DarkReading, PortSwigger)
- AI Security & LLM Vulnerability News (Simon Willison, AI Security feeds)
"""

import os
import sys
import io
import csv
import json
import argparse
import datetime
import re
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional

try:
    from lxml import html
    HAS_LXML = True
except ImportError:
    HAS_LXML = False

DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,application/json,*/*;q=0.8'
}

def fetch_url(url: str, timeout: int = 12) -> Optional[bytes]:
    try:
        req = urllib.request.Request(url, headers=DEFAULT_HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read()
    except Exception as e:
        print(f"[!] Warning: Failed to fetch {url}: {e}", file=sys.stderr)
        return None

def clean_html(raw_html: str) -> str:
    clean = re.sub(r'<[^>]+>', ' ', raw_html or '')
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean[:400]

def parse_rss_items(xml_bytes: bytes, max_items: int = 10) -> List[Dict[str, str]]:
    items = []
    if not xml_bytes:
        return items
    try:
        root = ET.fromstring(xml_bytes)
        channel_items = root.findall('.//item')
        if channel_items:
            for item in channel_items[:max_items]:
                title = item.findtext('title') or ''
                link = item.findtext('link') or ''
                pub_date = item.findtext('pubDate') or ''
                description = item.findtext('description') or ''
                items.append({
                    'title': clean_html(title),
                    'link': link.strip(),
                    'pub_date': pub_date.strip(),
                    'summary': clean_html(description)
                })
        else:
            namespaces = {'atom': 'http://www.w3.org/2005/Atom'}
            atom_entries = root.findall('.//atom:entry', namespaces) or root.findall('.//{http://www.w3.org/2005/Atom}entry')
            for entry in atom_entries[:max_items]:
                title = entry.findtext('{http://www.w3.org/2005/Atom}title') or ''
                link_el = entry.find('{http://www.w3.org/2005/Atom}link')
                link = link_el.attrib.get('href', '') if link_el is not None else ''
                updated = entry.findtext('{http://www.w3.org/2005/Atom}updated') or ''
                summary = entry.findtext('{http://www.w3.org/2005/Atom}summary') or entry.findtext('{http://www.w3.org/2005/Atom}content') or ''
                items.append({
                    'title': clean_html(title),
                    'link': link.strip(),
                    'pub_date': updated.strip(),
                    'summary': clean_html(summary)
                })
    except Exception as e:
        # Fallback to regex if XML parse has formatting glitches
        item_matches = re.findall(r'<item>(.*?)</item>', xml_bytes.decode('utf-8', 'ignore'), re.DOTALL)
        for im in item_matches[:max_items]:
            t_match = re.search(r'<title>(.*?)</title>', im, re.DOTALL)
            l_match = re.search(r'<link>(.*?)</link>', im, re.DOTALL)
            d_match = re.search(r'<description>(.*?)</description>', im, re.DOTALL)
            if t_match and l_match:
                items.append({
                    'title': clean_html(t_match.group(1)),
                    'link': l_match.group(1).strip(),
                    'pub_date': '',
                    'summary': clean_html(d_match.group(1) if d_match else '')
                })
    return items

def fetch_cisa_kev(max_entries: int = 8) -> List[Dict[str, Any]]:
    print("[*] Fetching CISA Known Exploited Vulnerabilities (KEV)...")
    url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
    raw = fetch_url(url, timeout=15)
    if not raw:
        return []
    try:
        data = json.loads(raw.decode('utf-8'))
        vulns = data.get('vulnerabilities', [])
        recent = vulns[-max_entries:]
        recent.reverse()
        results = []
        for v in recent:
            results.append({
                'cve_id': v.get('cveID'),
                'vendor_project': v.get('vendorProject'),
                'product': v.get('product'),
                'vulnerability_name': v.get('vulnerabilityName'),
                'date_added': v.get('dateAdded'),
                'short_description': v.get('shortDescription'),
                'required_action': v.get('requiredAction'),
                'known_ransomware_use': v.get('knownRansomwareCampaignUse')
            })
        return results
    except Exception as e:
        print(f"[!] Error processing CISA KEV: {e}", file=sys.stderr)
        return []

def fetch_nuclei_templates_releases() -> Dict[str, Any]:
    print("[*] Fetching ProjectDiscovery Nuclei-Templates latest release & actionable CVEs...")
    url = "https://api.github.com/repos/projectdiscovery/nuclei-templates/releases/latest"
    raw = fetch_url(url, timeout=10)
    if not raw:
        return {'tag': '', 'cves': []}
    try:
        data = json.loads(raw.decode('utf-8'))
        tag = data.get('tag_name', '')
        name = data.get('name', '')
        body = data.get('body', '')
        
        cve_lines = []
        for line in body.split('\n'):
            line_str = line.strip()
            if 'CVE-' in line_str:
                cve_match = re.search(r'\[(CVE-\d{4}-\d+)\]\s*(.+?)(?:\s*\[(critical|high|medium|low|info)\]|$)', line_str, re.IGNORECASE)
                if cve_match:
                    cve_id = cve_match.group(1)
                    desc = cve_match.group(2).strip(' -')
                    sev = (cve_match.group(3) or 'high').lower()
                    cve_lines.append({
                        'cve_id': cve_id,
                        'description': desc,
                        'severity': sev,
                        'raw_line': line_str
                    })
        return {
            'tag': tag,
            'name': name,
            'body_summary': body[:600],
            'cves': cve_lines[:20]
        }
    except Exception as e:
        print(f"[!] Error parsing Nuclei release: {e}", file=sys.stderr)
        return {'tag': '', 'cves': []}

def fetch_hackerone_disclosures() -> Dict[str, Any]:
    print("[*] Fetching HackerOne disclosures (10 Newest from Late 2026 + 50 Top Popular)...")
    url = "https://raw.githubusercontent.com/reddelexc/hackerone-reports/master/data.csv"
    raw = fetch_url(url, timeout=15)
    if not raw:
        return {'all': [], 'newest': [], 'popular': []}
    try:
        import csv
        reader = csv.reader(io.StringIO(raw.decode('utf-8', errors='ignore')))
        header = next(reader, None)

        all_parsed = []
        for r in reader:
            if len(r) >= 5:
                link = r[2].strip()
                if not link.startswith('http'):
                    link = f"https://{link}" if link.startswith('hackerone.com') else f"https://hackerone.com/reports/{link}"
                m = re.search(r'reports/(\d+)', link)
                rep_id = int(m.group(1)) if m else 0
                upvotes = int(r[3].strip()) if r[3].strip().isdigit() else 0
                bounty = r[4].strip()
                bounty_str = f"${bounty}" if bounty and bounty != '0.0' else 'Publicly Disclosed'
                vuln_type = r[5].strip() if len(r) > 5 and r[5].strip() else 'Web Security Flaw'
                all_parsed.append({
                    'rep_id': rep_id,
                    'platform': 'HackerOne',
                    'program': r[0].strip(),
                    'title': r[1].strip(),
                    'link': link,
                    'upvotes': upvotes,
                    'bounty': bounty_str,
                    'vuln_type': vuln_type
                })

        # 1. 10 Newest Reports: Sort by HackerOne report ID descending (IDs > 4,100,000 from late 2026 / Nov 2026)
        all_parsed.sort(key=lambda x: x['rep_id'], reverse=True)
        newest = []
        seen_links = set()

        for p in all_parsed[:10]:
            seen_links.add(p['link'])
            newest.append({
                **p,
                'is_new': True,
                'is_popular': False,
                'badge': '🔥 MỚI NHẤT (T11/2026)'
            })

        # 2. 50 Top Popular Reports: Sort by Upvotes descending (excluding those in newest)
        by_upvotes = sorted(all_parsed, key=lambda x: x['upvotes'], reverse=True)
        popular = []
        rank = 1
        for p in by_upvotes:
            if p['link'] not in seen_links:
                seen_links.add(p['link'])
                popular.append({
                    **p,
                    'is_new': False,
                    'is_popular': True,
                    'rank': rank,
                    'badge': f"⭐ TOP #{rank} PHỔ BIẾN"
                })
                rank += 1
                if len(popular) >= 50:
                    break

        all_reports = newest + popular
        return {
            'all': all_reports,
            'newest': newest,
            'popular': popular
        }
    except Exception as e:
        print(f"[!] Error parsing HackerOne CSV: {e}", file=sys.stderr)
        return {'all': [], 'newest': [], 'popular': []}

def fetch_bugcrowd_intel(max_items: int = 6) -> List[Dict[str, Any]]:
    print("[*] Fetching Bugcrowd Blog & Research...")
    url = "https://www.bugcrowd.com/blog/"
    raw = fetch_url(url, timeout=12)
    results = []
    if not raw or not HAS_LXML:
        return results
    try:
        content = raw.decode("utf-8", "ignore")
        tree = html.fromstring(content)
        seen = set()
        for a in tree.xpath(".//a[contains(@href, '/blog/')]"):
            href = a.get("href", "")
            if not href or href == "https://www.bugcrowd.com/blog/" or href == "/blog/":
                continue
            if href in seen or '/category/' in href or '/author/' in href:
                continue
            seen.add(href)
            
            # Find parent card title
            parent = a
            title = ""
            for _ in range(4):
                parent = parent.getparent()
                if parent is None:
                    break
                headings = parent.xpath(".//h2 | .//h3 | .//h4")
                if headings:
                    title = headings[0].text_content().strip()
                    if title and len(title) > 10:
                        break
            if not title or len(title) < 10:
                slug = href.strip("/").split("/")[-1].replace("-", " ").title()
                title = slug
                
            if not href.startswith("http"):
                href = f"https://www.bugcrowd.com{href}"
                
            results.append({
                'platform': 'Bugcrowd',
                'title': title,
                'link': href,
                'summary': f"Bugcrowd technical article & intelligence: {title}",
                'is_new': True,
                'is_popular': False,
                'badge': '🔥 MỚI NHẤT (T11/2026)'
            })
            if len(results) >= max_items:
                break
    except Exception as e:
        print(f"[!] Error parsing Bugcrowd HTML: {e}", file=sys.stderr)
    return results

def fetch_yeswehack_intel(max_items: int = 6) -> List[Dict[str, Any]]:
    print("[*] Fetching YesWeHack Disclosures & Writeups...")
    urls = [
        "https://blog.yeswehack.com/yeswehack-disclosures/",
        "https://blog.yeswehack.com/news/",
        "https://blog.yeswehack.com/"
    ]
    results = []
    seen = set()
    if not HAS_LXML:
        return results
    for u in urls:
        raw = fetch_url(u, timeout=10)
        if not raw:
            continue
        try:
            content = raw.decode("utf-8", "ignore")
            tree = html.fromstring(content)
            for a in tree.xpath(".//a"):
                href = a.get("href", "")
                text = (a.text_content() or "").strip()
                if not href or href in seen or len(text) < 15:
                    continue
                if any(k in href for k in ['/yeswehack-disclosures/', '/news/', '/web-security/', '/talent/']):
                    seen.add(href)
                    if not href.startswith("http"):
                        href = f"https://blog.yeswehack.com{href}"
                    results.append({
                        'platform': 'YesWeHack',
                        'title': text,
                        'link': href,
                        'summary': f"YesWeHack security disclosure & writeup: {text}",
                        'is_new': True,
                        'is_popular': False,
                        'badge': '🔥 MỚI NHẤT (T11/2026)'
                    })
                    if len(results) >= max_items:
                        break
        except Exception as e:
            print(f"[!] Error parsing YesWeHack HTML: {e}", file=sys.stderr)
        if len(results) >= max_items:
            break
    return results

def fetch_hacking_news(max_items: int = 8) -> List[Dict[str, Any]]:
    print("[*] Fetching Hacking & Offensive Security News...")
    sources = [
        ('The Hacker News', 'https://feeds.feedburner.com/TheHackersNews', 4),
        ('CyberSecurityNews', 'https://cybersecuritynews.com/feed/', 4),
        ('PortSwigger Daily Swig', 'https://portswigger.net/daily-swig/rss', 3),
        ('DarkReading', 'https://www.darkreading.com/rss.xml', 3)
    ]
    all_news = []
    for name, feed_url, limit in sources:
        raw = fetch_url(feed_url, timeout=8)
        if raw:
            items = parse_rss_items(raw, max_items=limit)
            for it in items:
                it['source'] = name
                all_news.append(it)
    return all_news[:max_items]

def fetch_ai_security_news(max_items: int = 6) -> List[Dict[str, Any]]:
    print("[*] Fetching AI Security & LLM Vulnerabilities Intel...")
    url = "https://simonwillison.net/atom/everything/"
    raw = fetch_url(url, timeout=10)
    ai_items = []
    if raw:
        items = parse_rss_items(raw, max_items=20)
        keywords = ['ai', 'llm', 'prompt injection', 'jailbreak', 'agent', 'model', 'chatgpt', 'claude', 'gemini', 'deepseek', 'security', 'vulnerability']
        for it in items:
            text = f"{it['title']} {it['summary']}".lower()
            if any(kw in text for kw in keywords):
                it['source'] = 'Simon Willison AI Research'
                ai_items.append(it)
                if len(ai_items) >= max_items:
                    break
    return ai_items

def synthesize_actionable_cves(nuclei_info: Dict[str, Any], kev_vulns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    actionable = []
    seen = set()

    # Priority 1: Nuclei release CVEs
    for cve in nuclei_info.get('cves', []):
        cid = cve['cve_id']
        if cid in seen:
            continue
        seen.add(cid)
        actionable.append({
            'cve_id': cid,
            'title': cve['description'],
            'severity': cve['severity'].upper(),
            'has_nuclei_template': True,
            'is_in_kev': any(k['cve_id'] == cid for k in kev_vulns),
            'source': 'Nuclei-Templates Release',
            'actionability_score': 9 if cve['severity'].lower() == 'critical' else 8
        })

    # Priority 2: CISA KEV entries
    for kv in kev_vulns:
        cid = kv['cve_id']
        if cid in seen:
            for a in actionable:
                if a['cve_id'] == cid:
                    a['is_in_kev'] = True
            continue
        seen.add(cid)
        actionable.append({
            'cve_id': cid,
            'title': f"{kv['vendor_project']} {kv['product']} - {kv['vulnerability_name']}",
            'severity': 'HIGH/CRITICAL',
            'has_nuclei_template': False,
            'is_in_kev': True,
            'source': 'CISA KEV Catalog',
            'actionability_score': 8
        })

    actionable.sort(key=lambda x: x.get('actionability_score', 0), reverse=True)
    return actionable

def main():
    parser = argparse.ArgumentParser(description="Collect daily security intelligence data.")
    parser.add_argument('--days', type=int, default=2, help="Days lookback (default: 2)")
    parser.add_argument('--output', type=str, default="", help="Output JSON path")
    args = parser.parse_args()

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    print(f"=== Running Security Intelligence Collector [{now}] ===")

    kev_vulns = fetch_cisa_kev(max_entries=8)
    nuclei_info = fetch_nuclei_templates_releases()
    h1_data = fetch_hackerone_disclosures()
    h1_reports = h1_data.get('all', [])
    h1_newest = h1_data.get('newest', [])
    h1_popular = h1_data.get('popular', [])
    bc_reports = fetch_bugcrowd_intel(max_items=6)
    ywh_reports = fetch_yeswehack_intel(max_items=6)
    hacking_news = fetch_hacking_news(max_items=8)
    ai_news = fetch_ai_security_news(max_items=6)
    actionable_cves = synthesize_actionable_cves(nuclei_info, kev_vulns)

    payload = {
        'collected_at': now,
        'summary_counts': {
            'cisa_kev_count': len(kev_vulns),
            'nuclei_cves_count': len(nuclei_info.get('cves', [])),
            'hackerone_disclosures_count': len(h1_reports),
            'hackerone_newest_count': len(h1_newest),
            'hackerone_popular_count': len(h1_popular),
            'bugcrowd_articles_count': len(bc_reports),
            'yeswehack_articles_count': len(ywh_reports),
            'hacking_news_count': len(hacking_news),
            'ai_security_news_count': len(ai_news),
            'total_actionable_cves': len(actionable_cves)
        },
        'top_actionable_cves': actionable_cves[:12],
        'nuclei_release': {
            'tag': nuclei_info.get('tag'),
            'name': nuclei_info.get('name')
        },
        'cisa_kev_recent': kev_vulns,
        'bug_bounty_disclosures': {
            'all': h1_newest + bc_reports + ywh_reports + h1_popular,
            'newest_10': h1_newest,
            'popular_50': h1_popular,
            'hackerone': h1_reports,
            'hackerone_newest': h1_newest,
            'hackerone_popular': h1_popular,
            'bugcrowd': bc_reports,
            'yeswehack': ywh_reports
        },
        'hacking_news': hacking_news,
        'ai_security_news': ai_news
    }

    output_path = args.output
    if not output_path:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        cache_dir = os.path.join(os.path.dirname(base_dir), 'cache')
        os.makedirs(cache_dir, exist_ok=True)
        output_path = os.path.join(cache_dir, 'latest_intel.json')
    else:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"\n[✓] SUCCESS: Data saved to: {output_path}")
    print(f"    - Actionable CVEs: {len(actionable_cves)}")
    print(f"    - HackerOne Reports: {len(h1_reports)}")
    print(f"    - Bugcrowd Articles: {len(bc_reports)}")
    print(f"    - YesWeHack Articles: {len(ywh_reports)}")
    print(f"    - Hacking News: {len(hacking_news)}")
    print(f"    - AI Security Items: {len(ai_news)}")

if __name__ == '__main__':
    main()
