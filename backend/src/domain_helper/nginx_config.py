from src.schemas import Domain, HostType

def get_nginx_domain_config(domain: Domain) -> str:
    server_config = f"""# {domain.domain} configuration
    server {{
        listen 80;
        listen [::]:80;
        server_name {domain.domain} www.{domain.domain};
        return 301 https://{domain.domain}$request_uri;
    }}

    server {{
        listen 443 ssl http2;
        listen [::]:443 ssl http2;

        server_name {domain.domain} www.{domain.domain};
        
        # Redirect www to non-www
        if ($host = www.{domain.domain}) {{
            return 301 https://{domain.domain}$request_uri;
        }}

        client_max_body_size 512M;

        ssl_certificate /etc/letsencrypt/live/{domain.domain}/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/{domain.domain}/privkey.pem;
        
        include /etc/letsencrypt/options-ssl-nginx.conf;
        ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
"""

    for host in domain.hosts:
        if host.type == HostType.WebSocket:
            server_config += f"""
        location {host.path} {{
            proxy_pass {host.host};
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "Upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }}
"""
        else:
            server_config += f"""
        location {host.path} {{
            proxy_pass {host.host};
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }}
    }}

    """
    
    return server_config