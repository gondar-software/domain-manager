import subprocess

def setup_cert(domain: str, email_address: str):
    try:
        subprocess.run(["sudo", "fuser", "-k", "80/tcp"], stderr=subprocess.DEVNULL)
        subprocess.run([
            "sudo", "certbot", "certonly", "--standalone",
            "-d", domain, "-d", f"www.{domain}",
            "--non-interactive",
            "--agree-tos",
            "--email", email_address,
            "--expand",
            "--cert-name", domain,
            "--force-renewal"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(e)

def remove_cert(domain: str):
    try:
        subprocess.run(["sudo", "rm", "-r", f"/etc/letsencrypt/live/{domain}"], check=True)
    except subprocess.CalledProcessError as e:
        print(e)