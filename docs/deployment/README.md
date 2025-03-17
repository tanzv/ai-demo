# Deployment Guide

## Prerequisites

- Docker and Docker Compose
- Domain name (for production)
- SSL certificate (for production)
- Server with minimum requirements:
  - 2 CPU cores
  - 4GB RAM
  - 20GB SSD
  - Ubuntu 20.04 LTS or later

## Development Deployment

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-demo.git
cd ai-demo
```

2. Copy environment file:
```bash
cp .env.example .env
```

3. Start services:
```bash
make start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Production Deployment

### Server Setup

1. Update system:
```bash
sudo apt update && sudo apt upgrade -y
```

2. Install Docker and Docker Compose:
```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

3. Install Nginx:
```bash
sudo apt install nginx -y
```

### SSL Certificate

1. Install Certbot:
```bash
sudo apt install certbot python3-certbot-nginx -y
```

2. Obtain SSL certificate:
```bash
sudo certbot --nginx -d yourdomain.com
```

### Application Deployment

1. Clone repository:
```bash
git clone https://github.com/yourusername/ai-demo.git
cd ai-demo
```

2. Create production environment file:
```bash
cp .env.example .env.prod
```

3. Update production environment variables:
```bash
nano .env.prod
```

4. Build and start services:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Nginx Configuration

Create Nginx configuration:

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### Monitoring Setup

1. Install Prometheus and Grafana:
```bash
docker-compose -f docker-compose.monitoring.yml up -d
```

2. Configure alerts in Grafana:
- System metrics
- Application metrics
- Error rates
- Response times

### Backup Strategy

1. Database backups:
```bash
# Daily backups
0 0 * * * docker exec postgres pg_dump -U postgres ai_demo > /backups/ai_demo_$(date +\%Y\%m\%d).sql
```

2. Application data backups:
```bash
# Weekly backups
0 0 * * 0 tar -czf /backups/app_data_$(date +\%Y\%m\%d).tar.gz /app/data
```

### Maintenance

1. Update application:
```bash
git pull
docker-compose -f docker-compose.prod.yml up -d --build
```

2. View logs:
```bash
docker-compose -f docker-compose.prod.yml logs -f
```

3. Monitor resources:
```bash
docker stats
```

### Troubleshooting

1. Check service status:
```bash
docker-compose -f docker-compose.prod.yml ps
```

2. View service logs:
```bash
docker-compose -f docker-compose.prod.yml logs -f service_name
```

3. Restart services:
```bash
docker-compose -f docker-compose.prod.yml restart service_name
``` 