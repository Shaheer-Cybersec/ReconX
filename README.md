# ReconX

**Automated Web Application Reconnaissance & Vulnerability Discovery Framework**

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> Modular Python framework for OWASP Top 10 vulnerability detection and web application reconnaissance

## Features

### Reconnaissance
- 🔍 Subdomain enumeration (Certificate Transparency + DNS brute-force)
- 🌐 Port scanning & service detection
- 🛠️ Technology fingerprinting
- 🔒 HTTP security header analysis

### Vulnerability Detection
- 💉 SQL Injection testing
- 🚨 Cross-Site Scripting (XSS)
- 🔓 Open Redirect detection
- ⚙️ Security misconfiguration checks

### Reporting
- 📄 HTML reports with CVSS scoring
- 📝 Markdown output
- 🔗 JSON export for CI/CD

## Installation

```bash
git clone https://github.com/Shaheer-Cybersec/ReconX.git
cd ReconX
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
# Subdomain enumeration
python reconx.py -d example.com --recon

# Full vulnerability scan
python reconx.py -d example.com --vuln

# Generate report
python reconx.py -d example.com --scan --report
```

## ⚠️ Legal Disclaimer

**AUTHORIZED TESTING ONLY**

Only use on systems you own or have written permission to test.

Unauthorized access is illegal under CFAA (USA), Computer Misuse Act (UK), and similar laws worldwide.

## Development Status

🚧 **Active Development** - v0.1

- [x] Core framework
- [x] Subdomain enumeration
- [ ] SQL injection detector
- [ ] XSS scanner
- [ ] Report generation

## Author

**Shaheer Hussain**

- 🎯 TryHackMe: [Top 6%](https://tryhackme.com/p/Cicada664)
- 💼 LinkedIn: [shaheer-hussain-ch](https://www.linkedin.com/in/shaheer-hussain-ch-2906601a0/)
- 📧 shaheerch6@gmail.com

**Certifications:**
- CEH v12 (In Progress)
- API Penetration Testing (APIsec University)
- ISC2 Certified in Cybersecurity

## License

MIT License - see [LICENSE](LICENSE)
