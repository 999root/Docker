docker-compose up -d --build --scale app=3

# Wait for the containers to be up
Write-Host "`nWaiting for containers to build"
Start-Sleep -Seconds 10
Write-Host "`n"

docker container rename captcha-nginx-1 nginx
docker container rename captcha-app-1 webproxy-one
docker container rename captcha-app-2 webproxy-two
docker container rename captcha-app-3 webproxy-three

Write-Host "`n"
docker ps
Write-Host "`n"