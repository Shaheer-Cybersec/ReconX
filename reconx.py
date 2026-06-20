#!/usr/bin/env python3
"""
ReconX - Automated Web Application Reconnaissance & Vulnerability Discovery Framework
Author: Shaheer Hussain
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

__version__ = "0.1.0"
__author__ = "Shaheer Hussain"

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    banner = f"""
{Colors.OKCYAN}
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║╚██╗██╔╝
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ╚███╔╝ 
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██╔██╗ 
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██╔╝ ██╗
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝
{Colors.ENDC}
{Colors.BOLD}Web Application Reconnaissance Framework{Colors.ENDC}
{Colors.OKGREEN}Version: {__version__} | Author: {__author__}{Colors.ENDC}
"""
    print(banner)

def parse_arguments():
    parser = argparse.ArgumentParser(description='ReconX - Web Application Security Scanner')
    parser.add_argument('-d', '--domain', required=True, help='Target domain')
    parser.add_argument('--recon', action='store_true', help='Run reconnaissance')
    parser.add_argument('--vuln', action='store_true', help='Run vulnerability scan')
    parser.add_argument('--sqli', action='store_true', help='SQL injection test')
    parser.add_argument('--xss', action='store_true', help='XSS test')
    parser.add_argument('--ports', action='store_true', help='Port scan')
    parser.add_argument('--url', help='Target URL for vulnerability testing')
    parser.add_argument('--scan', action='store_true', help='Full scan')
    parser.add_argument('--tech', action='store_true', help='Technology detection')
    parser.add_argument('--output', help='Path for HTML report output (default: reports/reconx_<domain>_<timestamp>.html)')
    parser.add_argument('--no-report', action='store_true', help='Skip HTML report generation')
    return parser.parse_args()

def main():
    print_banner()
    args = parse_arguments()

    print(f"\n{Colors.OKBLUE}[+] Target: {args.domain}{Colors.ENDC}")

    # Unified results container — this is what gets handed to the HTML report.
    # Every module below writes into this instead of being discarded after printing.
    scan_data = {
        'target': args.domain,
        'subdomains': [],
        'ports': [],
        'tech_stack': {},
        'sqli_vulns': [],
        'xss_vulns': [],
    }
    ran_any_module = False

    if args.recon or args.scan:
        print(f"{Colors.OKGREEN}[+] Starting reconnaissance...{Colors.ENDC}")
        from modules.recon.subdomain_enum import SubdomainEnumerator
        enum = SubdomainEnumerator(args.domain)
        results = enum.run()
        print(f"{Colors.OKGREEN}[✓] Found {results['total_subdomains']} subdomains{Colors.ENDC}")
        scan_data['subdomains'] = list(set(results['passive_results'] + results['bruteforce_results']))
        ran_any_module = True

    if args.ports or args.scan:
        print(f"{Colors.OKGREEN}[+] Starting port scan...{Colors.ENDC}")
        from modules.recon.port_scanner import PortScanner
        scanner = PortScanner()
        open_ports = scanner.scan_host(args.domain)
        print(f"{Colors.OKGREEN}[✓] Port scan complete{Colors.ENDC}")
        scan_data['ports'] = open_ports
        ran_any_module = True

    if args.tech or args.scan:
        print(f"{Colors.OKGREEN}[+] Starting technology detection...{Colors.ENDC}")
        from modules.recon.tech_detect import TechnologyDetector
        detector = TechnologyDetector()
        tech_stack = detector.detect(args.domain)
        scan_data['tech_stack'] = tech_stack
        ran_any_module = True

    # --scan now runs vuln tests too, as long as --url is supplied — same precondition
    # the standalone --sqli/--xss flags already required, just no longer skipped by --scan.
    if (args.sqli or args.scan) and args.url:
        print(f"{Colors.OKGREEN}[+] Starting SQL injection test...{Colors.ENDC}")
        from modules.vuln.sqli_detector import SQLiDetector
        scanner = SQLiDetector()
        vulns = scanner.test_url(args.url)
        if vulns:
            print(f"{Colors.FAIL}[!] Found {len(vulns)} SQL injection vulnerabilities{Colors.ENDC}")
        else:
            print(f"{Colors.OKGREEN}[✓] No SQL injection vulnerabilities found{Colors.ENDC}")
        scan_data['sqli_vulns'] = vulns
        ran_any_module = True

    if (args.xss or args.scan) and args.url:
        print(f"{Colors.OKGREEN}[+] Starting XSS test...{Colors.ENDC}")
        from modules.vuln.xss_scanner import XSSScanner
        scanner = XSSScanner()
        vulns = scanner.test_url(args.url)
        if vulns:
            print(f"{Colors.FAIL}[!] Found {len(vulns)} XSS vulnerabilities{Colors.ENDC}")
        else:
            print(f"{Colors.OKGREEN}[✓] No XSS vulnerabilities found{Colors.ENDC}")
        scan_data['xss_vulns'] = vulns
        ran_any_module = True

    if not ran_any_module:
        print(f"{Colors.WARNING}[!] No scan mode selected. Use --recon, --ports, --tech, --sqli/--xss (with --url), or --scan.{Colors.ENDC}")
        return

    if args.no_report:
        return

    # Build severity counts and hand everything to the report generator.
    high = len(scan_data['sqli_vulns']) + len(scan_data['xss_vulns'])
    scan_data['high'] = high
    scan_data['medium'] = 0
    scan_data['low'] = 0
    scan_data['total_findings'] = high

    from modules.report.html_report import HTMLReportGenerator
    reports_dir = Path('reports')
    reports_dir.mkdir(exist_ok=True)
    if args.output:
        output_path = args.output
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_domain = args.domain.replace('://', '_').replace('/', '_')
        output_path = str(reports_dir / f"reconx_{safe_domain}_{timestamp}.html")

    generator = HTMLReportGenerator(scan_data)
    final_path = generator.generate(output_path)
    print(f"\n{Colors.OKCYAN}[✓] Report generated: {final_path}{Colors.ENDC}")

if __name__ == "__main__":
    main()