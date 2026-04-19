# ReconX

**Automated Web Application Reconnaissance & Vulnerability Discovery Framework**

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-v0.2-brightgreen)]()

> Modular Python framework for OWASP Top 10 vulnerability detection and web application reconnaissance

## Features

### Reconnaissance

- ✅ Subdomain enumeration (Certificate Transparency + DNS brute-force)
- ✅ Port scanning & service detection
- ✅ Technology fingerprinting (web server, CMS, frameworks, JS libraries)
- ✅ Security header analysis

### Vulnerability Detection

- ✅ SQL Injection detector (error-based, 15 payloads)
- ✅ XSS scanner (reflected, 10 payloads)
- 🚧 Open Redirect detection (planned)
- 🚧 Security misconfiguration checks (planned)

### Reporting

- ✅ HTML report generation
- 🚧 Markdown output (planned)
- 🚧 JSON export (planned)

## Installation

```bash
git clone https://github.com/Shaheer-Cybersec/ReconX.git
cd ReconX
python3 -m venv venv
source venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

## Usage

```bash
# Subdomain enumeration
python reconx.py -d example.com --recon

# Port scanning
python reconx.py -d example.com --ports

# Technology detection
python reconx.py -d example.com --tech

# SQL injection testing
python reconx.py -d example.com --sqli --url "http://example.com/page.php?id=1"

# XSS testing
python reconx.py -d example.com --xss --url "http://example.com/search.php?q=test"

# Full reconnaissance scan
python reconx.py -d example.com --scan
```

## Example Output

[*] Starting subdomain enumeration for example.com
[+] Found 25 subdomains from crt.sh
[+] Found: www.example.com
[+] Found: mail.example.com
[*] Scanning 8 ports on example.com
[+] Port 80 (HTTP) - OPEN
[+] Port 443 (HTTPS) - OPEN
[*] Detecting technologies for example.com
[+] Web Server: nginx
[+] CMS: WordPress
[+] Language: PHP
[+] JavaScript Libraries: jQuery, Bootstrap

## ⚠️ Legal Disclaimer

**AUTHORIZED TESTING ONLY**

Only use on systems you own or have written permission to test.

Unauthorized access is illegal under CFAA (USA), Computer Misuse Act (UK), and similar laws worldwide.

## Development Progress

**v0.2 (Current - April 2025)**

- [x] Core framework structure
- [x] Subdomain enumeration module
- [x] Port scanner
- [x] Technology detection
- [x] SQL injection detector
- [x] XSS scanner
- [x] Basic HTML report generator

**v0.3 (Planned - May 2025)**

- [ ] Complete report system with all findings
- [ ] Open redirect detector
- [ ] Security misconfiguration checks
- [ ] JSON export
- [ ] Test against DVWA/bWAPP

## Tested Against

- ✅ Google.com (subdomain enumeration)
- ✅ Tesla.com (subdomain enumeration)
- ✅ WordPress.com (technology detection)
- ✅ Public vulnerable sites (SQLi, XSS)

## Author

**Shaheer Hussain**  
Cybersecurity Analyst | Penetration Testing Enthusiast

- 🎯 TryHackMe: [Top 6%](https://tryhackme.com/p/Cicada664)
- 💼 LinkedIn: [shaheer-hussain-ch](https://www.linkedin.com/in/shaheer-hussain-ch-2906601a0/)
- 📧 shaheerch6@gmail.com

**Certifications:**

- API Penetration Testing (APIsec University)
- ISC2 Certified in Cybersecurity

## License

MIT License - see [LICENSE](LICENSE)

---

⭐ **Star this repo if you find it useful!**
