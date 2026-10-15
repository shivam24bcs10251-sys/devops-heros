#!/usr/bin/env bash
set -euo pipefail
dnf install -y nginx
cat > /usr/share/nginx/html/index.html <<'HTML'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Session 19 Terraform cloud lab</title>
  <style>
    * { box-sizing: border-box; }
    body { margin: 0; background: #f3f6fb; color: #172238; font-family: system-ui, sans-serif; }
    main { max-width: 1000px; margin: 8vh auto; padding: 40px; }
    .eyebrow { color: #3d63b8; font-size: 13px; font-weight: 700; letter-spacing: .16em; text-transform: uppercase; }
    h1 { font-size: clamp(28px, 4vw, 44px); line-height: 1.2; margin: 18px 0; letter-spacing: -.03em; }
    .intro { color: #54627b; max-width: 680px; line-height: 1.8; }
    .status { display: inline-block; background: #e0f3e8; color: #256443; border-radius: 20px; padding: 8px 14px; margin: 14px 0 30px; font-size: 13px; font-weight: 600; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 16px; }
    article { background: white; border: 1px solid #e0e6f0; border-radius: 14px; padding: 24px; }
    h2 { font-size: 17px; margin: 0 0 12px; }
    article p, footer { color: #64718a; font-size: 14px; line-height: 1.6; }
    footer { margin-top: 28px; }
  </style>
</head>
<body><main>
  <div class="eyebrow">DevOps · Infrastructure as Code</div>
  <h1>Shivam Jaiswal — Session 19</h1>
  <p class="intro">Terraform provisioned this EC2 web server, VPC, subnet, security group and S3 lab bucket. This page is served by Nginx on Amazon Linux 2023.</p>
  <div class="status">● HTTP request reached the cloud web server</div>
  <section class="grid">
    <article><h2>Network</h2><p>Dedicated VPC, public subnet, internet gateway and route table.</p></article>
    <article><h2>Compute</h2><p>EC2 t3.micro with an encrypted gp3 root disk and IMDSv2.</p></article>
    <article><h2>Storage</h2><p>Private S3 bucket with AES256 encryption and versioning.</p></article>
    <article><h2>Access</h2><p>HTTP restricted to the workstation's public IPv4 /32. No SSH ingress.</p></article>
  </section>
  <footer>Session 19 cloud lab · Terraform-managed infrastructure · Verified before teardown</footer>
</main></body></html>
HTML
systemctl enable --now nginx
