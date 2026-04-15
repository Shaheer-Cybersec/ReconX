#!/usr/bin/env python3
"""
ReconX - HTML Report Generator
"""

from datetime import datetime
from typing import Dict, List

class HTMLReportGenerator:
    
    def __init__(self, scan_data: Dict):
        self.data = scan_data
    
    def generate(self, output_path: str) -> str:
        """Generate HTML report"""
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>ReconX Security Report - {self.data.get('target', 'Unknown')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
        .section {{ background: white; margin: 20px 0; padding: 20px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .high {{ color: #e74c3c; font-weight: bold; }}
        .medium {{ color: #f39c12; font-weight: bold; }}
        .low {{ color: #3498db; font-weight: bold; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #34495e; color: white; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>ReconX Security Assessment Report</h1>
        <p>Target: {self.data.get('target', 'Unknown')}</p>
        <p>Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="section">
        <h2>Executive Summary</h2>
        <p>Total Findings: {self.data.get('total_findings', 0)}</p>
        <p class="high">High Severity: {self.data.get('high', 0)}</p>
        <p class="medium">Medium Severity: {self.data.get('medium', 0)}</p>
        <p class="low">Low Severity: {self.data.get('low', 0)}</p>
    </div>
    
    <div class="section">
        <h2>Reconnaissance Results</h2>
        <p>Subdomains Found: {len(self.data.get('subdomains', []))}</p>
    </div>
    
    <div class="section">
        <h2>Vulnerability Findings</h2>
        <table>
            <tr>
                <th>Type</th>
                <th>Severity</th>
                <th>Count</th>
            </tr>
            <tr>
                <td>SQL Injection</td>
                <td class="high">HIGH</td>
                <td>{len(self.data.get('sqli_vulns', []))}</td>
            </tr>
            <tr>
                <td>Cross-Site Scripting</td>
                <td class="high">HIGH</td>
                <td>{len(self.data.get('xss_vulns', []))}</td>
            </tr>
        </table>
    </div>
</body>
</html>
"""
        
        with open(output_path, 'w') as f:
            f.write(html)
        
        return output_path
