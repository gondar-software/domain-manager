import subprocess
import re
from typing import List

from .constants import NGINX_CONFIG_PATH, NGINX_DEFAUT_CONFIG
from .nginx_config import get_nginx_domain_config
from src.schemas import Domain, Host, HostType

class NginxManager:
    def __init__(self):
        self.load_existing_config()
    
    def load_existing_config(self):
        """Load existing configuration from Nginx"""
        try:
            with open(NGINX_CONFIG_PATH, 'r') as f:
                self.config = f.read()
        except FileNotFoundError:
            self.config = NGINX_DEFAUT_CONFIG
            self.save_config()
    
    def refresh_config(self):
        """Reload configuration from file"""
        self.load_existing_config()
    
    def add_domain(self, domain: Domain):
        """Add a new domain to the proxy"""
        new_config_block = get_nginx_domain_config(domain)
        self.config = self.config.replace("# Add Servers Here", f"{new_config_block}# Add Servers Here")
        self.save_config()

    def remove_domain(self, domain: Domain):
        """Remove existing domain config"""
        config_block = get_nginx_domain_config(domain)
        self.config = self.config.replace(config_block, "")
        self.save_config()
    
    def save_config(self):
        """Save configuration to file using elevated privileges"""
        temp_file_path = "/tmp/nginx_temp_config"
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(self.config)
        
        subprocess.run(
            ["sudo", "mv", "-f", temp_file_path, NGINX_CONFIG_PATH],
            check=True
        )
        if not self.reload_nginx():
            self.restart_nginx()
    
    def reload_nginx(self):
        """Reload Nginx configuration"""
        try:
            subprocess.run(["sudo", "nginx", "-s", "reload"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(e)
            return False

    def restart_nginx(self):
        """Restart Nginx service"""
        try:
            subprocess.run(["sudo", "systemctl", "restart", "nginx"])
        except subprocess.CalledProcessError as e:
            print(e)
            raise

    def get_current_domains(self) -> List[Domain]:
        """Get current domain settings from Nginx configuration"""
        return self.parse_existing_config()

    def get_hosting_summary(self) -> dict:
        """Get a summary of current hosting settings"""
        domains = self.get_current_domains()
        summary = {
            'total_domains': len(domains),
            'domains': {}
        }
        
        for domain in domains:
            summary['domains'][domain.domain] = domain
        
        return summary

    def parse_existing_config(self) -> List[Domain]:
        """Parse the existing Nginx configuration and extract domain settings"""
        def extract_server_blocks(config_text: str) -> list[str]:
            blocks = []
            inside_block = False
            brace_count = 0
            current_block = []

            lines = config_text.splitlines()
            for line in lines:
                stripped = line.strip()
                if stripped.startswith("server"):
                    if "{" in stripped:
                        inside_block = True
                        brace_count = stripped.count("{") - stripped.count("}")
                        current_block.append(line)
                        continue
                
                if inside_block:
                    current_block.append(line)
                    brace_count += line.count("{") - line.count("}")
                    if brace_count == 0:
                        block_text = "\n".join(current_block).strip()
                        if "location" in block_text and "443" in block_text:
                            blocks.append(block_text)
                        current_block = []
                        inside_block = False

            return blocks
        
        server_blocks = extract_server_blocks(self.config)
        
        domains = []
        for server_block in server_blocks:
            domain = self.extract_domain_from_config(server_block)
            if domain and not self.is_default_server_block(server_block):
                domains.append(domain)

        return domains

    def is_default_server_block(self, config: str) -> bool:
        """Check if this is a default server block that should be ignored"""
        return 'default_server' in config or 'server_name _;' in config

    def extract_domain_from_config(self, config: str) -> Domain:
        """Extract domain information from a config block"""
        try:
            server_name_match = re.search(r'server_name\s+(.*?);', config)
            if not server_name_match:
                return None
            
            server_names = server_name_match.group(1).strip().split()
            primary_domain = None
            for name in server_names:
                if not name.startswith('www.'):
                    primary_domain = name
                    break
            
            if not primary_domain:
                return None
            
            hosts = []
            location_pattern = r'location\s+(.*?)\s*\{(.*?)\}'
            location_matches = re.findall(location_pattern, config, re.DOTALL)
            
            for path, location_content in location_matches:
                path = path.strip()
                
                proxy_pass_match = re.search(r'proxy_pass\s+(.*?);', location_content)
                if proxy_pass_match:
                    proxy_host = proxy_pass_match.group(1).strip()
                    
                    is_websocket = 'proxy_set_header Upgrade $http_upgrade' in location_content
                    host_type = HostType.WebSocket if is_websocket else HostType.Default
                    
                    host = Host(type=host_type, path=path, host=proxy_host)
                    hosts.append(host)
            
            return Domain(domain=primary_domain, hosts=hosts)
            
        except Exception as e:
            print(f"Error extracting domain from config: {e}")
            return None