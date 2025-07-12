NGINX_DEFAUT_CONFIG = """user www-data;
worker_processes auto;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    server_names_hash_bucket_size 1024;
    
    include /etc/nginx/conf.d/*.conf;

    # roman-terpeliuk.portfolio-app.online configuration
    server {
        listen 80;
        listen [::]:80;
        server_name roman-terpeliuk.portfolio-app.online www.roman-terpeliuk.portfolio-app.online;
        return 301 https://roman-terpeliuk.portfolio-app.online$request_uri;
    }

    server {
        listen 443 ssl http2;
        listen [::]:443 ssl http2;

        server_name roman-terpeliuk.portfolio-app.online www.roman-terpeliuk.portfolio-app.online;
        
        # Redirect www to non-www
        if ($host = www.roman-terpeliuk.portfolio-app.online) {
            return 301 https://roman-terpeliuk.portfolio-app.online$request_uri;
        }

        client_max_body_size 512M;

        ssl_certificate /etc/letsencrypt/live/roman-terpeliuk.portfolio-app.online/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/roman-terpeliuk.portfolio-app.online/privkey.pem;
        
        include /etc/letsencrypt/options-ssl-nginx.conf;
        ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

        location / {
            proxy_pass http://localhost:8081;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "Upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /api {
            proxy_pass http://localhost:5001;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "Upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }

    # Add Servers Here

    # Default server block for unmatched requests
    server {
        listen 80 default_server;
        listen [::]:80 default_server;
        server_name _;
        return 444;
    }

    server {
        listen 443 ssl default_server;
        listen [::]:443 ssl default_server;
        server_name _;
        ssl_certificate /etc/letsencrypt/live/monate.site/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/monate.site/privkey.pem;
        return 444;
    }
}"""

NGINX_CONFIG_PATH = "/etc/nginx/nginx.conf"