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
        return self.reload_nginx()

    def remove_domain(self, domain: Domain):
        """Remove existing domain config"""
        config_block = get_nginx_domain_config(domain)
        self.config = self.config.replace(config_block, "")
        self.save_config()
        return self.reload_nginx()
    
    def save_config(self):
        """Save configuration to file using elevated privileges"""
        try:
            temp_file_path = "/tmp/nginx_temp_config"
            # Write the config to a temporary file
            with open(temp_file_path, 'w') as temp_file:
                temp_file.write(self.config)
            
            # Use sudo to move the temporary file to the actual Nginx config path
            subprocess.run(
                ["sudo", "mv", temp_file_path, NGINX_CONFIG_PATH],
                check=True
            )
        except Exception as e:
            print(f"Error saving Nginx config: {e}")
    
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
            return True
        except subprocess.CalledProcessError as e:
            print(e)
            return False

    def get_current_domains(self) -> List[Domain]:
        """Get current domain settings from Nginx configuration"""
        return self.parse_existing_config()

    def get_hosting_summary(self) -> dict:
        """Get a summary of current hosting settings"""
        domains = self.get_current_domains()
        summary = {
            'total_domains': len(domains),
            'domains': []
        }
        
        for domain in domains:
            domain_info = {
                'domain': domain.domain,
                'hosts': []
            }
            
            for host in domain.hosts:
                host_info = {
                    'path': host.path,
                    'proxy_host': host.host,
                    'type': 'WebSocket' if host.type == HostType.WebSocket else 'Default'
                }
                domain_info['hosts'].append(host_info)
            
            summary['domains'].append(domain_info)
        
        return summary

    def parse_existing_config(self) -> List[Domain]:
        """Parse the existing Nginx configuration and extract domain settings"""
        ssl_server_pattern = r'server\s*\{[^}]*listen\s+443\s+ssl[^}]*(?!default_server)[^}]*\}'
        server_blocks = re.findall(ssl_server_pattern, self.config, re.DOTALL)
        
        domains = []
        for server_block in server_blocks:
            try:
                domain = self.extract_domain_from_config(server_block)
                if domain and not self.is_default_server_block(server_block):
                    domains.append(domain)
            except Exception as e:
                print(f"Error parsing config block: {e}")
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