#!/usr/bin/env python3
"""
ReconX - Subdomain Enumeration Module
"""

import requests
import dns.resolver
import logging
from typing import Set, Dict
import time

class SubdomainEnumerator:
    def __init__(self, domain: str, timeout: int = 10):
        self.domain = domain
        self.timeout = timeout
        self.subdomains: Set[str] = set()
        self.logger = logging.getLogger('ReconX.SubdomainEnum')
    
    def passive_enum_crtsh(self) -> Set[str]:
        """Query Certificate Transparency logs"""
        print(f"[*] Querying crt.sh for {self.domain}...")
        
        try:
            url = f"https://crt.sh/?q=%.{self.domain}&output=json"
            response = requests.get(url, timeout=self.timeout)
            data = response.json()
            
            for entry in data:
                name_value = entry.get('name_value', '')
                for subdomain in name_value.split('\n'):
                    subdomain = subdomain.strip().lower()
                    if '*' not in subdomain and subdomain.endswith(self.domain):
                        self.subdomains.add(subdomain)
            
            print(f"[+] Found {len(self.subdomains)} subdomains from crt.sh")
            return self.subdomains
        except Exception as e:
            print(f"[!] Error querying crt.sh: {str(e)}")
            return set()
    
    def dns_bruteforce(self, wordlist_path: str = None) -> Set[str]:
        """Brute-force subdomains using DNS"""
        print(f"[*] Starting DNS brute-force for {self.domain}...")
        
        default_subdomains = ['www', 'mail', 'ftp', 'admin', 'api', 'dev', 'test']
        
        if wordlist_path:
            try:
                with open(wordlist_path, 'r') as f:
                    subdomains_to_test = [line.strip() for line in f if line.strip()]
            except:
                subdomains_to_test = default_subdomains
        else:
            subdomains_to_test = default_subdomains
        
        resolver = dns.resolver.Resolver()
        resolver.timeout = 2
        resolver.lifetime = 2
        
        discovered = set()
        
        for subdomain in subdomains_to_test:
            test_domain = f"{subdomain}.{self.domain}"
            try:
                answers = resolver.resolve(test_domain, 'A')
                if answers:
                    discovered.add(test_domain)
                    print(f"[+] Found: {test_domain}")
                time.sleep(0.1)
            except:
                pass
        
        self.subdomains.update(discovered)
        return discovered
    
    def run(self) -> Dict:
        """Execute full subdomain enumeration"""
        print(f"\n[*] Starting subdomain enumeration for {self.domain}\n")
        
        results = {
            'domain': self.domain,
            'passive_results': [],
            'bruteforce_results': [],
            'total_subdomains': 0
        }
        
        passive_subs = self.passive_enum_crtsh()
        results['passive_results'] = list(passive_subs)
        
        bruteforce_subs = self.dns_bruteforce('wordlists/subdomains.txt')
        results['bruteforce_results'] = list(bruteforce_subs)
        
        results['total_subdomains'] = len(self.subdomains)
        
        return results
