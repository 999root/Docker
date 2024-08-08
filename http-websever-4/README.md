# Auto Renewal
```
crontab -e
```

Select NANO editor

```
/usr/bin/docker compose -f /root/https-webserver/docker-compose.yml up certbot
```

# Run CMD
```
docker compose up -d
```

# NGINX.CONF
Modify the HTTPS Server section to include the domains 
