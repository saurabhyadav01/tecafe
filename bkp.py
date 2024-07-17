[Unit]
Description=Gunicorn instance to serve myapp
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/var/www/faceapp
ExecStart=/usr/local/bin/gunicorn -w 4 -b 0.0.0.0:5001 --certfile=/etc/letsencrypt/live/157.173.218.32/fullchain.pem --keyfile=/etc/letsencrypt/live/157.173.218.32/privkey.pem app:app
Restart=always

[Install]
WantedBy=multi-user.target





# [Unit]
# Description=Gunicorn instance to serve myapp
# After=network.target

# [Service]
# User=root
# Group=root
# WorkingDirectory=/var/www/faceapp
# ExecStart=/usr/local/bin/gunicorn -w 4 -b 0.0.0.0:5001 --certfile=/etc/ssl/certs/selfsigned.crt --keyfile=/etc/ssl/private/selfsigned.key app:app

# Restart=always

# [Install]
# WantedBy=multi-user.target




[Unit]
Description=Gunicorn instance to serve myapp over HTTPS
After=network.target

[Service]
User=user
Group=group
WorkingDirectory=/var/www/faceapp
ExecStart=/usr/local/bin/gunicorn -w 4 -b 0.0.0.0:443 --certfile=/etc/ssl/certs/selfsigned.crt --keyfile=/etc/ssl/private/selfsigned.key app:app

[Install]
WantedBy=multi-user.target












server {
    listen 443 ssl;
    server_name 157.173.218.32;  # Replace with your actual server IP or domain name

    ssl_certificate /etc/ssl/certs/selfsigned.crt;
    ssl_certificate_key /etc/ssl/private/selfsigned.key;

    # Other SSL/TLS settings as needed
    ssl_protocols TLSv1.2 TLSv1.3;  # Adjust as per your security requirements
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;

    location / {
        proxy_pass http://127.0.0.1:5001;  # Assuming Gunicorn is running on localhost
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}
