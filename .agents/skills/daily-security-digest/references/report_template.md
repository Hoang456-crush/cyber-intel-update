# Mẫu Báo Cáo Chuẩn (Daily Security Report Template)

Mọi báo cáo an toàn thông tin hàng ngày do Agent xuất ra phải tuân thủ cấu trúc Markdown chuẩn mực dưới đây:

---

```markdown
# 🛡️ BÁO CÁO TÌNH BÁO BẢO MẬT & BUG BOUNTY HÀNG NGÀY
**Ngày xuất bản**: YYYY-MM-DD | **Người thực hiện**: Antigravity Security Agent
**Trọng tâm**: Hacking News, AI Security, HackerOne/Bugcrowd/YesWeHack Disclosures, Actionable CVEs & Usage Guides

---

## ⚡ 1. TỔNG QUAN NHANH TRONG NGÀY (EXECUTIVE SUMMARY)
- [3-4 gạch đầu dòng tóm tắt các sự kiện nổi bật nhất trong 24h qua]
- Điểm tin nóng nhất về chiến dịch tấn công hoặc lỗ hổng 0-day/1-day.
- Cảnh báo mới về các mô hình AI hoặc công nghệ phổ biến.
- Thống kê ngắn về số lượng report công khai và CVE nguy hiểm mới.

---

## 🌐 2. TIN TỨC HACKING & OFFENSIVE SECURITY MỚI NHẤT
### 🔹 [Tiêu đề tin tức 1]
- **Nguồn**: [Tên báo/Blog] - [Link nếu có]
- **Tóm tắt sự kiện**: Mô tả vụ việc, tác nhân tấn công, mục tiêu bị ảnh hưởng.
- **Kỹ thuật tấn công (TTPs)**: Phân tích kỹ thuật (Initial Access, Privilege Escalation, Lateral Movement, Exfiltration).
- **Bài học rút ra**: Cách áp dụng vào tư duy kiểm thử thâm nhập hoặc phòng ngự.

### 🔹 [Tiêu đề tin tức 2]
...

---

## 🤖 3. AI SECURITY & LLM VULNERABILITIES
*(Chuyên mục theo dõi an ninh trí tuệ nhân tạo, tấn công mô hình ngôn ngữ lớn, prompt injection, framework AI)*

### 🔹 [Tiêu đề nghiên cứu/sự cố AI 1]
- **Chủ đề**: Prompt Injection / Jailbreak / LLM Agent Hijacking / RAG Poisoning / Lỗ hổng trong Framework (LangChain, MLflow, Ollama, vLLM, v.v.).
- **Bản chất kỹ thuật**: Kẻ tấn công đã lừa mô hình hoặc khai thác điểm yếu như thế nào.
- **Payload / Kịch bản minh họa**: Ví dụ câu lệnh hoặc định dạng tấn công.
- **Khuyến nghị an toàn**: Cách lập hàng rào bảo vệ (Guardrails, Sandboxing, Sanitization).

---

## 🎯 4. BUG BOUNTY DISCLOSURES MỚI (HACKERONE, BUGCROWD, YESWEHACK)

### 📊 Bảng Tổng Hợp Báo Cáo Công Khai
| Nền Tảng | Chương Trình (Target) | Lỗ Hổng / Tiêu Đề | Mức Độ | Tiền Thưởng | Kỹ Thuật Chính |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **HackerOne** | [Program] | [Title] | Critical | $X,XXX | [Bypass WAF, SSRF, IDOR] |
| **Bugcrowd** | [Program] | [Title] | P1/High | - | [Account Takeover, Logic Flaw] |
| **YesWeHack**| [Program] | [Title] | High | €X,XXX | [OAuth Misconfig, CORS] |

### 🔍 Phân Tích Kỹ Thuật Chi Tiết 1-2 Report Tiêu Biểu
#### [Tên Report - Nền Tảng - Bounty]
- **Vấn đề cốt lõi**: Lỗi logic phát sinh từ đâu?
- **Vector tấn công**: Hacker đã tìm ra điểm yếu và xâu chuỗi (chaining) các bước như thế nào?
- **Kỹ thuật bypass đáng chú ý**: (Ví dụ: cách lách qua regex kiểm tra domain, cách bypass bộ lọc JSON, v.v.).
- **Góc nhìn Bug Hunter**: Làm thế nào để áp dụng kỹ thuật này vào các chương trình săn lỗi khác?

---

## 🛠️ 5. TOP ACTIONABLE CVES & BẢNG HƯỚNG DẪN SỬ DỤNG (CVE USAGE GUIDES)
*(Chỉ chọn lọc 2-3 CVE có tính tiếp cận và khả thi cao nhất đối với Bug Hunter)*

---

### 🔴 CVE-XXXX-YYYYY: [Tên Lỗ Hổng / Phần Mềm Bị Ảnh Hưởng]

#### 📌 1. Thông Tin Chung
| Chỉ Số | Giá Trị Chi Tiết |
| :--- | :--- |
| **CVE ID** | `CVE-XXXX-YYYYY` |
| **Điểm CVSS** | `X.X` (Severity: Critical / High) - `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/...` |
| **CWE** | `CWE-XX` (Tên phân loại lỗi) |
| **Phiên Bản Ảnh Hưởng** | `< X.Y.Z` hoặc `A.B.C - D.E.F` |
| **Phiên Bản Đã Vá** | `>= X.Y.Z` |
| **Tình Trạng PoC** | Đã có Public PoC / Có trong Nuclei Templates / CISA KEV |

#### 🎯 2. Cơ Chế & Nguyên Nhân Gốc Rễ (Root Cause)
- [Giải thích kỹ thuật: Lỗi nằm ở file nào, hàm nào, đoạn mã xử lý dữ liệu đầu vào bị thiếu sót gì].
- [Mô hình hóa luồng dữ liệu lỗi nếu cần].

#### 🧪 3. Môi Trường Thử Nghiệm An Toàn (Lab Setup)
Chạy lệnh Docker sau trên máy để dựng môi trường thử nghiệm an toàn:
```bash
docker run -d --name lab-cve-test -p 8080:8080 <vulnerable-image>:<tag>
```

#### 🔍 4. Nhận Diện & Trinh Sát (Discovery & Fingerprinting)
- **Shodan Dork**: `title:"Vulnerable App" http.component:"Framework"`
- **FOFA Dork**: `app="Vulnerable-App" && country="VN"`
- **Google Dork**: `inurl:/vulnerable/path`
- **Nuclei Command**:
  ```bash
  nuclei -t http/cves/YYYY/CVE-XXXX-YYYYY.yaml -l targets.txt
  ```

#### ⚡ 5. Hướng Dẫn Khai Thác Từng Bước (Step-by-Step PoC Execution)
**Bước 1**: Gửi HTTP Request mẫu:
```http
POST /vulnerable/endpoint HTTP/1.1
Host: 127.0.0.1:8080
Content-Type: application/x-www-form-urlencoded

payload_param=exploit_code_here
```

Hoặc sử dụng lệnh cURL một dòng:
```bash
curl -X POST -d "payload_param=test" "http://127.0.0.1:8080/vulnerable/endpoint"
```

**Bước 2: Phân tích Payload**:
- Giải thích chi tiết các thành phần trong payload.

**Bước 3: Dấu hiệu nhận biết thành công (Success Oracle)**:
- HTTP Response code: `200 OK`
- Chuỗi phản hồi xuất hiện: `root:x:0:0:root:/root:/bin/bash`
- Hoặc độ trễ thời gian (Time delay): Response mất > 5 giây.

#### 🛡️ 6. Biện Pháp Khắc Phục (Remediation)
- Nâng cấp gói phần mềm lên phiên bản `>= X.Y.Z`.
- Workaround khẩn cấp: Thêm quy tắc WAF hoặc chặn truy cập endpoint `/vulnerable/endpoint`.

---

*(Lặp lại mục trên cho CVE thứ 2 và thứ 3)*

---

## 📋 6. BUG HUNTER ACTION CHECKLIST HÔM NAY
- [ ] **Target Recon**: Tìm các subdomain sử dụng phần mềm [A] qua Dork Shodan.
- [ ] **Nuclei Scan**: Cập nhật template mới nhất và chạy kiểm tra nhanh trên các chương trình có phạm vi Wildcard (*.target.com).
- [ ] **Thử Nghiệm Kỹ Thuật Bypass**: Kiểm tra kỹ thuật bypass từ Report HackerOne [B] trên các tính năng upload file / reset mật khẩu.
- [ ] **Hardening / Phòng Ngự**: Kiểm tra và vá ngay nếu hệ thống nội bộ đang chạy phiên bản dính CVE [C].

---
*Báo cáo được tổng hợp tự động bởi Antigravity Daily Security Digest Skill.*
```
