#!/usr/bin/env python3
"""
ReconX - Automated Web Application Reconnaissance & Vulnerability Discovery Framework
Author: Shaheer Hussain
GitHub: https://github.com/Shaheer-Cybersec/ReconX
"""

import argparse
import sys
import logging
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

# Version information
__version__ = "1.0.0-dev"
__author__ = "Shaheer Hussain"

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def setup_logging(verbose: bool = False) -> logging.Logger:
    """
    Configure logging for the application
    
    Args:
        verbose: Enable verbose logging if True
    
    Returns:
        Configured logger instance
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    
    # Create logs directory if it doesn't exist
    log_dir = Path("output/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # File handler
    log_file = log_dir / f"reconx_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter(log_format))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    
    # Root logger
    logger = logging.getLogger('ReconX')
    logger.setLevel(log_level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def print_banner():
    """Display ReconX banner"""
    banner = f"""
{Colors.OKCYAN}
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║╚██╗██╔╝
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ╚███╔╝ 
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██╔██╗ 
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██╔╝ ██╗
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝
{Colors.ENDC}
{Colors.BOLD}Web Application Reconnaissance & Vulnerability Discovery Framework{Colors.ENDC}
{Colors.OKGREEN}Version: {__version__} | Author: {__author__}{Colors.ENDC}
{Colors.WARNING}[!] Only test systems you own or have written permission to test{Colors.ENDC}
"""
    print(banner)

class ReconX:
    """Main ReconX scanner class"""
    
    def __init__(self, target: str, config: Dict = None):
        """
        Initialize ReconX scanner
        
        Args:
            target: Target domain or URL
            config: Configuration dictionary
        """
        self.target = target
        self.config = config or {}
        self.logger = logging.getLogger('ReconX.Scanner')
        
        # Results storage
        self.results = {
            'target': target,
            'scan_start': datetime.now().isoformat(),
            'scan_end': None,
            'recon': {},
            'vulnerabilities': {},
            'summary': {}
        }
        
        self.logger.info(f"Initialized ReconX scanner for target: {target}")
    
    def run_reconnaissance(self) -> Dict:
        """
        Execute reconnaissance phase
        
        Returns:
            Dictionary containing reconnaissance results
        """
        print(f"\n{Colors.OKBLUE}[+] Starting Reconnaissance Phase{Colors.ENDC}")
        
        # TODO: Implement subdomain enumeration
        # from modules.recon.subdomain_enum import SubdomainEnumerator
        # enum = SubdomainEnumerator(self.target)
        # subdomains = enum.run()
        
        # TODO: Implement port scanning
        # from modules.recon.port_scanner import PortScanner
        # scanner = PortScanner(self.target)
        # ports = scanner.scan()
        
        # TODO: Implement technology detection
        # from modules.recon.tech_detect import TechnologyDetector
        # tech = TechnologyDetector(self.target)
        # technologies = tech.detect()
        
        # TODO: Implement header analysis
        # from modules.recon.header_check import HeaderAnalyzer
        # headers = HeaderAnalyzer(self.target)
        # header_results = headers.analyze()
        
        # Placeholder results
        self.results['recon'] = {
            'subdomains': [],
            'open_ports': [],
            'technologies': [],
            'security_headers': []
        }
        
        print(f"{Colors.OKGREEN}[✓] Reconnaissance phase completed{Colors.ENDC}")
        return self.results['recon']
    
    def run_vulnerability_scan(self) -> Dict:
        """
        Execute vulnerability detection phase
        
        Returns:
            Dictionary containing vulnerability findings
        """
        print(f"\n{Colors.OKBLUE}[+] Starting Vulnerability Detection Phase{Colors.ENDC}")
        
        # TODO: Implement SQL injection testing
        # from modules.vuln.sqli_detector import SQLiDetector
        # sqli = SQLiDetector(self.target)
        # sqli_results = sqli.scan()
        
        # TODO: Implement XSS testing
        # from modules.vuln.xss_scanner import XSSScanner
        # xss = XSSScanner(self.target)
        # xss_results = xss.scan()
        
        # TODO: Implement open redirect testing
        # from modules.vuln.open_redirect import OpenRedirectTester
        # redirect = OpenRedirectTester(self.target)
        # redirect_results = redirect.test()
        
        # TODO: Implement misconfiguration checks
        # from modules.vuln.misconfig_check import MisconfigChecker
        # misconfig = MisconfigChecker(self.target)
        # misconfig_results = misconfig.check()
        
        # Placeholder results
        self.results['vulnerabilities'] = {
            'sqli': [],
            'xss': [],
            'open_redirect': [],
            'misconfig': [],
            'data_leak': []
        }
        
        print(f"{Colors.OKGREEN}[✓] Vulnerability detection completed{Colors.ENDC}")
        return self.results['vulnerabilities']
    
    def generate_report(self, output_dir: str = "output/reports") -> Dict:
        """
        Generate scan reports in multiple formats
        
        Args:
            output_dir: Directory to save reports
        
        Returns:
            Dictionary with paths to generated reports
        """
        print(f"\n{Colors.OKBLUE}[+] Generating Reports{Colors.ENDC}")
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Update scan end time
        self.results['scan_end'] = datetime.now().isoformat()
        
        # TODO: Implement HTML report generation
        # from modules.report.html_report import HTMLReportGenerator
        # html_gen = HTMLReportGenerator(self.results)
        # html_path = html_gen.generate(output_path)
        
        # TODO: Implement Markdown report generation
        # from modules.report.md_report import MarkdownReportGenerator
        # md_gen = MarkdownReportGenerator(self.results)
        # md_path = md_gen.generate(output_path)
        
        # TODO: Implement JSON export
        # from modules.report.json_export import JSONExporter
        # json_exp = JSONExporter(self.results)
        # json_path = json_exp.export(output_path)
        
        report_paths = {
            'html': None,
            'markdown': None,
            'json': None
        }
        
        print(f"{Colors.OKGREEN}[✓] Reports generated{Colors.ENDC}")
        return report_paths
    
    def calculate_summary(self) -> Dict:
        """
        Calculate scan summary statistics
        
        Returns:
            Dictionary containing summary information
        """
        # Count vulnerabilities by severity
        high = 0
        medium = 0
        low = 0
        
        # TODO: Implement severity classification logic
        
        self.results['summary'] = {
            'total_findings': high + medium + low,
            'high_severity': high,
            'medium_severity': medium,
            'low_severity': low
        }
        
        return self.results['summary']

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments"""
    
    parser = argparse.ArgumentParser(
        description='ReconX - Web Application Security Scanner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full reconnaissance
  python reconx.py -d example.com --recon
  
  # Vulnerability scan
  python reconx.py -d example.com --vuln
  
  # Complete scan with reporting
  python reconx.py -d example.com --scan --report
  
  # Authenticated scan
  python reconx.py -d example.com --scan --auth-cookie "session=abc123"
        """
    )
    
    # Required arguments
    parser.add_argument(
        '-d', '--domain',
        required=True,
        help='Target domain or URL'
    )
    
    # Scan mode arguments
    scan_group = parser.add_argument_group('Scan Modes')
    scan_group.add_argument(
        '--recon',
        action='store_true',
        help='Run reconnaissance phase only'
    )
    scan_group.add_argument(
        '--vuln',
        action='store_true',
        help='Run vulnerability detection only'
    )
    scan_group.add_argument(
        '--scan',
        action='store_true',
        help='Run complete scan (recon + vuln)'
    )
    
    # Specific module arguments
    module_group = parser.add_argument_group('Specific Modules')
    module_group.add_argument(
        '--subdomains',
        action='store_true',
        help='Subdomain enumeration only'
    )
    module_group.add_argument(
        '--ports',
        action='store_true',
        help='Port scanning only'
    )
    module_group.add_argument(
        '--tech',
        action='store_true',
        help='Technology detection only'
    )
    module_group.add_argument(
        '--sqli',
        action='store_true',
        help='SQL injection testing only'
    )
    module_group.add_argument(
        '--xss',
        action='store_true',
        help='XSS testing only'
    )
    
    # Reporting arguments
    report_group = parser.add_argument_group('Reporting Options')
    report_group.add_argument(
        action='store_true',
        help='Generate all report formats'
    )
    report_group.add_argument(

        '--html-report',
        action='store_true',
        help='Generate HTML report only'
    )
    report_group.add_argument(
        '--md-report',

        action='store_true',
        help='Generate Markdown report only'
    )
    report_group.add_argument(
        '--json-export',
        metavar='PATH',

        help='Export results to JSON file'
    )
    report_group.add_argument(
        '--output',
        default='output/reports',
        help='Output directory for reports (default: output/reports)'
    )
    
    # Authentication arguments

    auth_group = parser.add_argument_group('Authentication')
    auth_group.add_argument(
        '--auth-cookie',
        metavar='COOKIE',
        help='Authentication cookie for authenticated scanning'
    )
    auth_group.add_argument(
        '--auth-header',
        metavar='HEADER',
        help='Authentication header (e.g., "Authorization: Bearer token")'
    )
    
    # Advanced options
    advanced_group = parser.add_argument_group('Advanced Options')
    advanced_group.add_argument(
        '--threads',
        type=int,
        default=5,
        help='Number of concurrent threads (default: 5)'
    )
    advanced_group.add_argument(

        '--timeout',
        type=int,
        default=10,
        help='Request timeout in seconds (default: 10)'
    )
    advanced_group.add_argument(
        '--delay',
        type=float,
        default=1.0,
        help='Delay between requests in seconds (default: 1.0)'
    )
    advanced_group.add_argument(
        '--user-agent',
        help='Custom User-Agent string'
    )
    advanced_group.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    return parser.parse_args()

def main():
    """Main execution function"""
    
    # Parse arguments
    args = parse_arguments()
    
    # Display banner
    print_banner()
    
    # Setup logging
    logger = setup_logging(args.verbose)
    
    try:
        # Initialize scanner
        scanner = ReconX(target=args.domain)
        
        # Determine scan mode
        if args.scan:
            # Full scan
            scanner.run_reconnaissance()
            scanner.run_vulnerability_scan()
        elif args.recon:
            # Reconnaissance only
            scanner.run_reconnaissance()
        elif args.vuln:
            # Vulnerability scan only
            scanner.run_vulnerability_scan()
        else:
            # Specific modules
            if args.subdomains or args.ports or args.tech:
                print(f"{Colors.WARNING}[!] Specific module scanning not yet implemented{Colors.ENDC}")
            elif args.sqli or args.xss:
                print(f"{Colors.WARNING}[!] Specific vulnerability testing not yet implemented{Colors.ENDC}")
            else:
                print(f"{Colors.FAIL}[!] No scan mode specified. Use --help for usage{Colors.ENDC}")
                return
        
        # Generate reports if requested
        if args.report or args.html_report or args.md_report or args.json_export:
            scanner.generate_report(output_dir=args.output)
        
        # Calculate and display summary
        summary = scanner.calculate_summary()
        
        print(f"\n{Colors.OKBLUE}{'='*60}{Colors.ENDC}")
        print(f"{Colors.BOLD}Scan Summary{Colors.ENDC}")
        print(f"{Colors.OKBLUE}{'='*60}{Colors.ENDC}")
        print(f"Target: {args.domain}")
        print(f"Total Findings: {summary['total_findings']}")
        print(f"  High Severity: {summary['high_severity']}")
        print(f"  Medium Severity: {summary['medium_severity']}")
        print(f"  Low Severity: {summary['low_severity']}")
        print(f"{Colors.OKBLUE}{'='*60}{Colors.ENDC}\n")
        
        logger.info("Scan completed successfully")
        
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}[!] Scan interrupted by user{Colors.ENDC}")
        logger.warning("Scan interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.FAIL}[!] Error: {str(e)}{Colors.ENDC}")
        logger.error(f"Scan failed: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()

