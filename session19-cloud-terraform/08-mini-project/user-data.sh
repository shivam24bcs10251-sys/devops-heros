#!/usr/bin/env bash
set -euo pipefail
dnf install -y nginx
cat > /usr/share/nginx/html/index.html <<'HTML'
<!doctype html>
<html><head><title>Session 19 Terraform cloud lab</title></head>
<body><h1>Shivam Jaiswal — Session 19</h1>
<p>Terraform provisioned this EC2 web server, VPC, subnet, security group and S3 lab bucket.</p></body></html>
HTML
systemctl enable --now nginx
