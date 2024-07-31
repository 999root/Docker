echo ""
echo "Updating Linux"
echo ""
sudo apt update -y && sudo apt upgrade -y

echo ""
echo "-- LINE -----------------------------------------------------------------------------------------------------------"

echo ""
echo "Installing Docker and Docker Compose"
echo ""
sudo apt install docker.io docker-compose