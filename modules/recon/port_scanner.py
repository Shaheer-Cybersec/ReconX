#!/usr/bin/env python3
"""
ReconX - Port Scanner Module
"""

import socket
from typing import List, Dict
import concurrent.futures

class PortScanner:
    
    # Common web service ports
    COMMON_PORTS = [80, 443, 8080, 8443, 8000, 8888, 3000, 5000]
    
    # Extended port list
    EXTENDED_PORTS = [
        21, 22, 23, 25, 53, 80, 110, 143, 443, 
        445, 3306, 3389, 5432, 5900, 8080, 8443
    ]
    
    def __init__(self, timeout: int = 2):
        self.timeout = timeout
        self.open_ports = []
    
    def scan_port(self, host: str, port: int) -> Dict:
        """Scan single port on host"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                service = self.get_service_name(port)
                return {
                    'port': port,
                    'state': 'open',
                    'service': service
                }
        except:
            pass
        return None
    
    def get_service_name(self, port: int) -> str:
        """Get common service name for port"""
        services = {
            21: 'FTP',
            22: 'SSH',
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            143: 'IMAP',
            443: 'HTTPS',
            445: 'SMB',
            3306: 'MySQL',
            3389: 'RDP',
            5432: 'PostgreSQL',
            5900: 'VNC',
            8000: 'HTTP-Alt',
            8080: 'HTTP-Proxy',
            8443: 'HTTPS-Alt',
            8888: 'HTTP-Alt'
        }
        return services.get(port, 'Unknown')
    
    def scan_host(self, host: str, ports: List[int] = None, threads: int = 10) -> List[Dict]:
        """Scan multiple ports on host"""
        if ports is None:
            ports = self.COMMON_PORTS
        
        print(f"\n[*] Scanning {len(ports)} ports on {host}...")
        
        open_ports = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {executor.submit(self.scan_port, host, port): port for port in ports}
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    open_ports.append(result)
                    print(f"[+] Port {result['port']} ({result['service']}) - OPEN")
        
        print(f"[✓] Found {len(open_ports)} open ports")
        return open_ports
