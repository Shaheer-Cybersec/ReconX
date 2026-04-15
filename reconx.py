#!/usr/bin/env python3
"""
ReconX - Automated Web Application Reconnaissance & Vulnerability Discovery Framework
Author: Shaheer Hussain
"""

import argparse
import sys
from pathlib import Path

__version__ = "1.0.0-dev"
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
    parser.add_argument('--url', help='Target URL for vulnerability testing')
    parser.add_argument('--scan', action='store_true', help='Full scan')
    return parser.parse_args()

def main():
    print_banner()
    args = parse_arguments()
    
    print(f"\n{Colors.OKBLUE}[+] Target: {args.domain}{Colors.ENDC}")
    
    if args.recon or args.scan:
        print(f"{Colors.OKGREEN}[+] Starting reconnaissance...{Colors.ENDC}")
        from modules.recon.subdomain_enum import SubdomainEnumerator
        enum = SubdomainEnumerator(args.domain)
        results = enum.run()
        print(f"{Colors.OKGREEN}[✓] Found {results['total_subdomains']} subdomains{Colors.ENDC}")
    
    if args.sqli and args.url:
        print(f"{Colors.OKGREEN}[+] Starting SQL injection test...{Colors.ENDC}")
        from modules.vuln.sqli_detector import SQLiDetector
        scanner = SQLiDetector()
        vulns = scanner.test_url(args.url)
        if vulns:
            print(f"{Colors.FAIL}[!] Found {len(vulns)} SQL injection vulnerabilities{Colors.ENDC}")
        else:
            print(f"{Colors.OKGREEN}[✓] No SQL injection vulnerabilities found{Colors.ENDC}")

if __name__ == "__main__":
    main()