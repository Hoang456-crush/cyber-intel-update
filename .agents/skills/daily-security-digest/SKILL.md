---
name: daily-security-digest
description: >-
  Thu thập, phân tích và lập báo cáo tình báo an toàn thông tin hàng ngày bao gồm tin tức Hacking,
  AI Security, report disclosure mới từ HackerOne, Bugcrowd, YesWeHack, và phân tích sâu các CVE
  có thể tiếp cận được kèm Bảng Hướng Dẫn Sử Dụng (PoC, lab setup, trinh sát, khai thác).
  Sử dụng khi người dùng yêu cầu cập nhật tin tức bảo mật hôm nay, tạo báo cáo CVE mới, hoặc khi
  automation chạy định kỳ mỗi ngày.
---

# Daily Security & Bug Bounty Intelligence Skill

Skill này cung cấp quy trình tự động hóa toàn diện 5 bước để thu thập, phân tích và xuất bản báo cáo an toàn thông tin hàng ngày, đặc biệt chú trọng vào các kỹ thuật thực chiến và khả năng tiếp cận mục tiêu trong Bug Bounty.

## Cấu Trúc Thư Mục Skill
```text
.agents/skills/daily-security-digest/
├── SKILL.md                          # Hướng dẫn chính của skill
├── scripts/
│   └── fetch_intel.py                # Python script tự động thu thập từ CISA, Nuclei, H1, BC, YWH, Feeds
├── references/
│   ├── cve_evaluation_criteria.md    # Tiêu chí sàng lọc CVE có thể tiếp cận được
│   └── report_template.md            # Mẫu chuẩn báo cáo và Bảng hướng dẫn sử dụng CVE
└── cache/                            # Thư mục chứa dữ liệu JSON tạm thời (tự sinh)
```

---

## Quy Trình 5 Bước Thực Hiện

### Bước 1: Thu Thập Dữ Liệu Tự Động (Data Collection)
Chạy script `fetch_intel.py` để quét và tổng hợp dữ liệu từ các nguồn:
```powershell
python .agents/skills/daily-security-digest/scripts/fetch_intel.py --days 2 --output .agents/skills/daily-security-digest/cache/latest_intel.json
```
Script sẽ lấy:
1. **CISA KEV Catalog**: Lỗ hổng đang bị khai thác thực tế (Known Exploited Vulnerabilities).
2. **ProjectDiscovery Nuclei-Templates**: Release notes và các CVE mới được bổ sung template (đây là nguồn chuẩn nhất cho các CVE có PoC thực chiến).
3. **HackerOne Disclosed Reports**: Các báo cáo công khai mới nhất từ cộng đồng HackerOne.
4. **Bugcrowd Blog & Disclosures**: Nghiên cứu kỹ thuật và báo cáo mới từ Bugcrowd.
5. **YesWeHack Disclosures**: Writeup và phân tích lỗ hổng từ YesWeHack.
6. **Hacking & Offensive News**: The Hacker News, BleepingComputer, PortSwigger Research.
7. **AI Security News**: Simon Willison AI Security, các sự cố Prompt Injection và LLM Vulnerabilities.

*Ghi chú*: Nếu cần kiểm tra thêm tin tức nóng tức thời, Agent có thể bổ sung bằng công cụ `search_web` cho các từ khóa chuyên sâu.

### Bước 2: Sàng Lọc & Phân Loại Thông Tin (Filtering & Triage)
1. Đọc dữ liệu từ file cache vừa xuất ra.
2. Lọc các báo cáo Bug Bounty:
   - Gom nhóm theo nền tảng: HackerOne, Bugcrowd, YesWeHack.
   - Trích xuất: Tên mục tiêu, Loại lỗ hổng (XSS, SSRF, IDOR, RCE, Auth Bypass), Kỹ thuật bypass, Mức tiền thưởng (bounty).
3. Lọc tin tức Hacking & AI: Chọn 3-5 tin có tầm ảnh hưởng lớn nhất.

### Bước 3: Đánh Giá & Chọn Lọc 2-3 Actionable CVEs (CVE Tiếp Cận Được)
Đọc hướng dẫn đánh giá tại:
[cve_evaluation_criteria.md](./references/cve_evaluation_criteria.md)

Áp dụng bộ lọc thực chiến:
- **CVSS >= 7.0 (High/Critical)**.
- **Unauthenticated / Low Privileges**.
- **Web / API / Phổ biến trên Internet**: Ví dụ các Web Frameworks (Laravel, Spring Boot, Next.js), CMS (WordPress, Craft CMS), Môi trường DevOps/AI (MLflow, GitLab, Jenkins), Gateway/VPN.
- **Đã có PoC công khai hoặc Nuclei Template chạy được ngay**.

Chọn ra **2 đến 3 CVE xuất sắc nhất** để đưa vào mục phân tích sâu.

### Bước 4: Soạn Thảo Bảng Hướng Dẫn Sử Dụng CVE (CVE Usage Guide)
Tuân thủ cấu trúc chi tiết 6 phần quy định tại:
[report_template.md](./references/report_template.md)

Với mỗi CVE chọn lọc, viết chi tiết:
1. **Thông tin định danh**: CVE-ID, Tên lỗi, CVSS Score, CWE, Phiên bản ảnh hưởng.
2. **Cơ chế & Nguyên nhân gốc rễ (Root Cause)**: Bản chất lỗi ở đâu, tại sao xảy ra.
3. **Môi trường Lab an toàn**: Lệnh Docker run hoặc docker-compose để dựng lab local chỉ trong 1 lệnh.
4. **Nhận diện & Trinh sát**: Dork Shodan, FOFA, Google, câu lệnh kiểm tra version / Nuclei template.
5. **Khai thác từng bước (Step-by-Step PoC)**: HTTP Request mẫu, lệnh cURL/Python, phân tích payload và dấu hiệu nhận biết thành công (Oracle).
6. **Biện pháp phòng vệ**: Cách vá và cách phòng thủ tạm thời.

### Bước 5: Xuất Báo Cáo & Trình Bày
1. Ghi file báo cáo hoàn chỉnh vào:
   `d:\Bug Bounty\News\reports\YYYY-MM-DD-daily-security-report.md` (với YYYY-MM-DD là ngày thực tế).
2. Trả lời người dùng trong đoạn chat với bản tóm tắt hấp dẫn:
   - Điểm tin nổi bật (Executive Summary).
   - Tóm tắt các report Bug Bounty mới.
   - Bảng so sánh nhanh các CVE tiếp cận được.
   - Link trực tiếp tới file báo cáo đầy đủ trong thư mục `reports/`.
   - Action Checklist cho Bug Hunter.
