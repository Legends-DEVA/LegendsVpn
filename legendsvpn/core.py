import os
import random
import requests
import time
from bs4 import BeautifulSoup
import socket
import urllib3
from typing import List, Tuple, Optional
import logging

class ProxyManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.proxy_file = os.path.join(self.data_dir, "proxies.txt")
        self.sources = [
            "https://www.proxy-list.download/api/v1/get?type=http",
            "https://spys.me/proxy.txt",
            "https://free-proxy-list.net/"
        ]
        self.ensure_data_directory()
        # Disable SSL warnings
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("LegendsVPN")

    def ensure_data_directory(self) -> None:
        """Create data directory if it doesn't exist."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def fetch_proxies(self) -> List[str]:
        """Fetch proxies from multiple sources and return list of proxies."""
        all_proxies = set()
        
        for source in self.sources:
            try:
                self.logger.info(f"Fetching proxies from {source}")
                
                if "free-proxy-list.net" in source:
                    response = requests.get(source, timeout=10)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    proxy_table = soup.find('textarea')
                    if proxy_table:
                        proxies = proxy_table.text.strip().split('\n')
                        all_proxies.update(proxy.strip() for proxy in proxies if proxy.strip())
                
                elif "spys.me" in source:
                    response = requests.get(source, timeout=10)
                    lines = response.text.split('\n')
                    for line in lines:
                        if line.strip() and line[0].isdigit():
                            proxy = line.split()[0]
                            all_proxies.add(proxy)
                
                else:
                    response = requests.get(source, timeout=10)
                    proxies = response.text.strip().split('\n')
                    all_proxies.update(proxy.strip() for proxy in proxies if proxy.strip())
            
            except Exception as e:
                self.logger.error(f"Error fetching from {source}: {str(e)}")
                continue

        # Save proxies to file
        if all_proxies:
            with open(self.proxy_file, 'w') as f:
                f.write('\n'.join(sorted(all_proxies)))
            self.logger.info(f"Saved {len(all_proxies)} proxies to {self.proxy_file}")
        
        return list(all_proxies)

    def test_proxy(self, proxy: str, timeout: int = 5) -> Tuple[bool, float]:
        """Test proxy and return (is_working, latency)."""
        try:
            proxies = {
                'http': f'http://{proxy}',
                'https': f'http://{proxy}'
            }
            
            start_time = time.time()
            response = requests.get('http://ip-api.com/json', 
                                proxies=proxies, 
                                timeout=timeout,
                                verify=False)
            latency = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            if response.status_code == 200:
                return True, latency
        except:
            pass
        return False, float('inf')

    def find_working_proxies(self, min_working: int = 3, max_tests: Optional[int] = None) -> List[Tuple[float, str]]:
        """Find working proxies and return them sorted by speed.
        
        Args:
            min_working: Minimum number of working proxies to find before stopping
            max_tests: Maximum number of proxies to test (None for all)
        
        Returns:
            List of tuples (latency, proxy) sorted by latency
        """
        if not os.path.exists(self.proxy_file):
            self.logger.error("No proxy file found")
            return []

        with open(self.proxy_file, 'r') as f:
            proxies = f.read().strip().split('\n')

        if not proxies:
            self.logger.error("No proxies found in file")
            return []

        # Shuffle proxies for random testing
        random.shuffle(proxies)
        working_proxies = []
        tested = 0
        max_tests = max_tests or len(proxies)

        while tested < max_tests and (len(working_proxies) < min_working or tested < len(proxies)):
            proxy = proxies[tested]
            self.logger.info(f"Testing proxy {tested + 1}/{len(proxies)}: {proxy}")
            
            is_working, latency = self.test_proxy(proxy)
            tested += 1
            
            if is_working:
                working_proxies.append((latency, proxy))
                self.logger.info(f"Found working proxy: {proxy} (latency: {latency:.0f}ms)")
            else:
                self.logger.debug(f"Proxy failed: {proxy}")

        # Sort by latency
        working_proxies.sort()
        return working_proxies

    def get_proxy_location(self, proxy: str) -> dict:
        """Get location information for a proxy."""
        try:
            proxies = {
                'http': f'http://{proxy}',
                'https': f'http://{proxy}'
            }
            response = requests.get('http://ip-api.com/json', 
                                proxies=proxies, 
                                timeout=5,
                                verify=False)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            self.logger.error(f"Error getting proxy location: {str(e)}")
        return {}

    def get_current_ip_info(self) -> dict:
        """Get current IP information."""
        try:
            response = requests.get('http://ip-api.com/json', timeout=5)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            self.logger.error(f"Error getting current IP info: {str(e)}")
        return {}
