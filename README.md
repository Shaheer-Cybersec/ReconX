# ReconX

**Automated Web Application Reconnaissance & Vulnerability Discovery Framework**

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-v0.1--dev-orange)]()

> Modular Python framework for OWASP Top 10 vulnerability detection and web application reconnaissance

## Features

### Reconnaissance

- ✅ Subdomain enumeration (Certificate Transparency + DNS brute-force)
- 🚧 Port scanning & service detection (planned)
- 🚧 Technology fingerprinting (planned)
- 🚧 HTTP security header analysis (planned)

### Vulnerability Detection

- ✅ SQL Injection detector (error-based)
- ✅ XSS scanner (reflected)
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

# SQL injection testing
python reconx.py -d example.com --sqli --url "http://example.com/page.php?id=1"

# XSS testing
python reconx.py -d example.com --xss --url "http://example.com/search.php?q=test"
```

## ⚠️ Legal Disclaimer

**AUTHORIZED TESTING ONLY**

Only use on systems you own or have written permission to test.

Unauthorized access is illegal under CFAA (USA), Computer Misuse Act (UK), and similar laws worldwide.

## Development Progress

**v0.1 (Current)**

- [x] Core framework structure
- [x] Subdomain enumeration module
- [x] SQL injection detector
- [x] XSS scanner
- [x] Basic HTML report generator

**v0.2 (Next)**

- [ ] Port scanner
- [ ] Technology detection
- [ ] Complete report system
- [ ] Test against DVWA

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
