#!/usr/bin/env python3
"""
ReconX - Technology Detection Module
"""

import requests
import re
from typing import Dict, List

class TechnologyDetector:
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.technologies = []
    
    def detect(self, url: str) -> Dict:
        """Detect technologies used by target"""
        print(f"\n[*] Detecting technologies for {url}...")
        
        tech_stack = {
            'web_server': None,
            'frameworks': [],
            'cms': None,
            'programming_language': None,
            'javascript_libraries': [],
            'security_headers': {}
        }
        
        try:
            # Add protocol if missing
            if not url.startswith('http'):
                url = f"http://{url}"
            
            response = requests.get(url, timeout=self.timeout, verify=False, allow_redirects=True)
            headers = response.headers
            content = response.text
            
            # Detect web server
            tech_stack['web_server'] = self._detect_web_server(headers)
            
            # Detect frameworks
            tech_stack['frameworks'] = self._detect_frameworks(headers, content)
            
            # Detect CMS
            tech_stack['cms'] = self._detect_cms(content)
            
            # Detect programming language
            tech_stack['programming_language'] = self._detect_language(headers, content)
            
            # Detect JavaScript libraries
            tech_stack['javascript_libraries'] = self._detect_js_libraries(content)
            
            # Check security headers
            tech_stack['security_headers'] = self._check_security_headers(headers)
            
            self._print_results(tech_stack)
            
            return tech_stack
            
        except Exception as e:
            print(f"[!] Error detecting technologies: {str(e)}")
            return tech_stack
    
    def _detect_web_server(self, headers: Dict) -> str:
        """Detect web server from headers"""
        server = headers.get('Server', 'Unknown')
        if server != 'Unknown':
            print(f"[+] Web Server: {server}")
        return server
    
    def _detect_frameworks(self, headers: Dict, content: str) -> List[str]:
        """Detect web frameworks"""
        frameworks = []
        
        # Check headers
        if 'X-Powered-By' in headers:
            frameworks.append(headers['X-Powered-By'])
        
        # Check content patterns
        patterns = {
            'Django': r'csrfmiddlewaretoken',
            'Laravel': r'laravel',
            'Ruby on Rails': r'rails',
            'Express': r'express',
            'Flask': r'Flask',
            'Spring': r'spring',
        }
        
        for framework, pattern in patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                frameworks.append(framework)
        
        if frameworks:
            print(f"[+] Frameworks: {', '.join(frameworks)}")
        
        return list(set(frameworks))
    
    def _detect_cms(self, content: str) -> str:
        """Detect Content Management System"""
        cms_patterns = {
            'WordPress': r'wp-content|wp-includes',
            'Joomla': r'joomla',
            'Drupal': r'drupal',
            'Magento': r'magento',
            'Shopify': r'shopify',
            'Wix': r'wix\.com',
        }
        
        for cms, pattern in cms_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                print(f"[+] CMS: {cms}")
                return cms
        
        return None
    
    def _detect_language(self, headers: Dict, content: str) -> str:
        """Detect programming language"""
        
        # Check headers first
        powered_by = headers.get('X-Powered-By', '')
        
        if 'PHP' in powered_by:
            print(f"[+] Language: PHP")
            return 'PHP'
        elif 'ASP.NET' in powered_by:
            print(f"[+] Language: ASP.NET")
            return 'ASP.NET'
        
        # Check file extensions in content
        if re.search(r'\.php', content):
            print(f"[+] Language: PHP")
            return 'PHP'
        elif re.search(r'\.aspx', content):
            print(f"[+] Language: ASP.NET")
            return 'ASP.NET'
        elif re.search(r'\.jsp', content):
            print(f"[+] Language: Java")
            return 'Java'
        
        return None
    
    def _detect_js_libraries(self, content: str) -> List[str]:
        """Detect JavaScript libraries"""
        libraries = []
        
        js_patterns = {
            'jQuery': r'jquery',
            'React': r'react',
            'Vue': r'vue\.js',
            'Angular': r'angular',
            'Bootstrap': r'bootstrap',
        }
        
        for lib, pattern in js_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                libraries.append(lib)
        
        if libraries:
            print(f"[+] JavaScript Libraries: {', '.join(libraries)}")
        
        return libraries
    
    def _check_security_headers(self, headers: Dict) -> Dict:
        """Check for security headers"""
        security_headers = {
            'Strict-Transport-Security': headers.get('Strict-Transport-Security'),
            'X-Frame-Options': headers.get('X-Frame-Options'),
            'X-Content-Type-Options': headers.get('X-Content-Type-Options'),
            'Content-Security-Policy': headers.get('Content-Security-Policy'),
            'X-XSS-Protection': headers.get('X-XSS-Protection'),
        }
        
        missing = [k for k, v in security_headers.items() if v is None]
        
        if missing:
            print(f"[!] Missing Security Headers: {', '.join(missing)}")
        else:
            print(f"[+] All security headers present")
        
        return security_headers
    
    def _print_results(self, tech_stack: Dict):
        """Print detection results summary"""
        print(f"\n[✓] Technology detection complete")