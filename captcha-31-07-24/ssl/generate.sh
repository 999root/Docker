openssl genpkey -algorithm RSA -out server.key -nodes
cmd
openssl req -new -key server.key -out server.csr -subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=example.com"