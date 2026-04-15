#!/usr/bin/env python3
"""
ReconX - Subdomain Enumeration Module
Implements passive and active subdomain discovery techniques
"""

import requests
import dns.resolver
import logging
from typing import Set, List, Dict
from urllib.parse import urlparse
import time

class SubdomainEnumerator:
    """
    Subdomain enumeration using multiple techniques:
    - Certificate Transparency logs (crt.sh)
    - DNS brute-forcing
    - Live host validation
    """
    
    def __init__(self, domain: str, timeout: int = 10):
        """
        Initialize subdomain enumerator
        
        Args:
            domain: Target domain (e.g., 'example.com')
            timeout: HTTP request timeout in seconds
        """
        self.domain = domain
        self.timeout = timeout
        self.subdomains: Set[str] = set()
        self.logger = logging.getLogger('ReconX.SubdomainEnum')
        
        # Validate domain
        if not self._validate_domain():
            raise ValueError(f"Invalid domain: {domain}")
    
    def _validate_domain(self) -> bool:
        """
        Validate domain format
        
        Returns:
            True if domain is valid, False otherwise
        """
        # Basic validation: contains dot, no spaces, no protocol
        if '.' not in self.domain:
            return False
        if ' ' in self.domain:
            return False
        if self.domain.startswith('http'):
            # Extract domain from URL
            parsed = urlparse(self.domain)
            self.domain = parsed.netloc or parsed.path
        return True
    
    def passive_enum_crtsh(self) -> Set[str]:
        """
        Query Certificate Transparency logs via crt.sh API
        
        Returns:
            Set of discovered subdomains
        """
        self.logger.info(f"Querying Certificate Transparency logs for {self.domain}")
        
        try:
            # crt.sh API endpoint
            url = f"https://crt.sh/?q=%.{self.domain}&output=json"
            
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract subdomains from results
            for entry in data:
                name_value = entry.get('name_value', '')
                
                # Handle multiple subdomains in one entry (separated by newlines)
                for subdomain in name_value.split('\n'):
                    subdomain = subdomain.strip().lower()
                    
                    # Filter wildcards and invalid entries
                    if '*' not in subdomain and subdomain.endswith(self.domain):
                        self.subdomains.add(subdomain)
            
            self.logger.info(f"Found {len(self.subdomains)} subdomains from crt.sh")
            return self.subdomains
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error querying crt.sh: {str(e)}")
            return set()
        except Exception as e:
            self.logger.error(f"Unexpected error in passive enumeration: {str(e)}")
            return set()
    
    def dns_bruteforce(self, wordlist_path: str = None) -> Set[str]:
        """
        Brute-force subdomains using DNS resolution
        
        Args:
            wordlist_path: Path to wordlist file (default: use built-in list)
        
        Returns:
            Set of discovered subdomains
        """
        self.logger.info(f"Starting DNS brute-force for {self.domain}")
        
        # Default common subdomain list
        default_subdomains = [
            'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 
            'ns2', 'admin', 'server', 'api', 'dev', 'staging', 'test', 'portal',
            'blog', 'shop', 'store', 'mobile', 'vpn', 'secure', 'support',
            'cdn', 'static', 'media', 'images', 'img', 'download', 'files'
        ]
        
        # Load wordlist if provided
        if wordlist_path:
            try:
                with open(wordlist_path, 'r') as f:
                    subdomains_to_test = [line.strip() for line in f if line.strip()]
                self.logger.info(f"Loaded {len(subdomains_to_test)} entries from wordlist")
            except FileNotFoundError:
                self.logger.warning(f"Wordlist not found: {wordlist_path}, using default list")
                subdomains_to_test = default_subdomains
        else:
            subdomains_to_test = default_subdomains
        
        # Configure DNS resolver
        resolver = dns.resolver.Resolver()
        resolver.timeout = 2
        resolver.lifetime = 2
        
        discovered = set()
        
        for subdomain in subdomains_to_test:
            test_domain = f"{subdomain}.{self.domain}"
            
            try:
                # Try to resolve A record
                answers = resolver.resolve(test_domain, 'A')
                
                if answers:
                    discovered.add(test_domain)
                    self.logger.debug(f"Found: {test_domain}")
                    
                    # Optional: rate limiting to avoid overwhelming DNS servers
                    time.sleep(0.1)
                    
            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
                # Domain doesn't exist or no A record
                pass
            except dns.exception.Timeout:
                self.logger.warning(f"DNS timeout for {test_domain}")
            except Exception as e:
                self.logger.debug(f"Error resolving {test_domain}: {str(e)}")
        
        self.subdomains.update(discovered)
        self.logger.info(f"DNS brute-force found {len(discovered)} subdomains")
        
        return discovered
    
    def validate_live_hosts(self) -> List[Dict]:
        """
        Check HTTP/HTTPS availability for discovered subdomains
        
        Returns:
            List of dictionaries with subdomain and status information
        """
        self.logger.info(f"Validating {len(self.subdomains)} subdomains")
        
        live_hosts = []
        
        for subdomain in self.subdomains:
            result = {
                'subdomain': subdomain,
                'http': False,
                'https': False,
                'status_code': None,
                'title': None
            }
            
            # Try HTTPS first (more common now)
            for protocol in ['https', 'http']:
                url = f"{protocol}://{subdomain}"
                
                try:
                    response = requests.get(
                        url,
                        timeout=self.timeout,
                        allow_redirects=True,
                        verify=False  # Ignore SSL verification for testing
                    )
                    
                    result[protocol] = True
                    result['status_code'] = response.status_code
                    
                    # Extract page title if available
                    if 'text/html' in response.headers.get('content-type', ''):
                        from bs4 import BeautifulSoup
                        soup = BeautifulSoup(response.text, 'html.parser')
                        title_tag = soup.find('title')
                        if title_tag:
                            result['title'] = title_tag.get_text().strip()
                    
                    self.logger.debug(f"Live: {url} ({response.status_code})")
                    break  # If HTTPS works, no need to try HTTP
                    
                except requests.exceptions.SSLError:
                    self.logger.debug(f"SSL error for {url}, trying HTTP")
                    continue
                except requests.exceptions.RequestException as e:
                    self.logger.debug(f"Failed to connect to {url}: {str(e)}")
                    continue
            
            # Only add if at least one protocol responded
            if result['http'] or result['https']:
                live_hosts.append(result)
        
        self.logger.info(f"Found {len(live_hosts)} live hosts")
        return live_hosts
    
    def run(self, wordlist_path: str = None, validate_hosts: bool = True) -> Dict:
        """
        Execute full subdomain enumeration workflow
        
        Args:
            wordlist_path: Optional path to custom wordlist
            validate_hosts: Whether to check HTTP/HTTPS availability
        
        Returns:
            Dictionary containing all enumeration results
        """
        self.logger.info(f"Starting subdomain enumeration for {self.domain}")
        
        results = {
            'domain': self.domain,
            'passive_results': [],
            'bruteforce_results': [],
            'live_hosts': [],
            'total_subdomains': 0
        }
        
        # Passive enumeration
        passive_subs = self.passive_enum_crtsh()
        results['passive_results'] = list(passive_subs)
        
        # Active brute-forcing
        bruteforce_subs = self.dns_bruteforce(wordlist_path)
        results['bruteforce_results'] = list(bruteforce_subs)
        
        # Validate live hosts
        if validate_hosts:
            results['live_hosts'] = self.validate_live_hosts()
        
        results['total_subdomains'] = len(self.subdomains)
        
        self.logger.info(f"Enumeration complete. Total subdomains: {len(self.subdomains)}")
        
        return results
    
    def get_subdomains(self) -> Set[str]:
        """
        Get all discovered subdomains
        
        Returns:
            Set of subdomain strings
        """
        return self.subdomains

# Example usage and testing
if __name__ == "__main__":
    # Configure logging for standalone testing
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s - %(message)s'
    )
    
    # Suppress SSL warnings for testing
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # Test domain
    test_domain = "example.com"
    
    print(f"\n[*] Testing SubdomainEnumerator with {test_domain}\n")
    
    try:
        # Initialize enumerator
        enum = SubdomainEnumerator(test_domain)
        
        # Run full enumeration
        results = enum.run(validate_hosts=True)
        
        # Display results
        print("\n" + "="*60)
        print(f"Subdomain Enumeration Results for {test_domain}")
        print("="*60)
        
        print(f"\nPassive Enumeration (crt.sh): {len(results['passive_results'])} subdomains")
        for sub in sorted(results['passive_results'][:10]):  # Show first 10
            print(f"  - {sub}")
        if len(results['passive_results']) > 10:
            print(f"  ... and {len(results['passive_results']) - 10} more")
        
        print(f"\nDNS Brute-force: {len(results['bruteforce_results'])} subdomains")
        for sub in sorted(results['bruteforce_results']):
            print(f"  - {sub}")
        
        print(f"\nLive Hosts: {len(results['live_hosts'])}")
        for host in results['live_hosts']:
            protocol = 'https' if host['https'] else 'http'
            title = f" - {host['title']}" if host['title'] else ""
            print(f"  - {protocol}://{host['subdomain']} [{host['status_code']}]{title}")
        
        print(f"\nTotal Unique Subdomains: {results['total_subdomains']}")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"[!] Error: {str(e)}")
        import traceback
        traceback.print_exc()
