import httpx

class GodaddyManager:
    def __init__(self, key: str, secret: str):
        self.key = key
        self.secret = secret

    async def add_record(self, domain: str, subdomain_name: str):
        url = f"https://api.godaddy.com/v1/domains/{domain}/records"
        try:
            async with httpx.AsyncClient() as client:
                ip_response = await client.get("https://api.ipify.org")
                ip_response.raise_for_status()
                public_ip = ip_response.text
                headers = {
                    "Authorization": f"sso-key {self.key}:{self.secret}",
                    "Content-Type": "application/json"
                }
                data = [
                    {
                        "data": public_ip, 
                        "name": subdomain_name, 
                        "type": "A"
                    },
                    {
                        "data": f"{subdomain_name}.{domain}.",
                        "name": f"www.{subdomain_name}", 
                        "type": "CNAME"
                    }
                ]
                response = await client.patch(
                    url,
                    headers=headers,
                    json=data
                )
                response.raise_for_status()
            return True
        except httpx.HTTPStatusError as e:
            print(f"GoDaddy API error: {e}")
            return False

    async def remove_record(self, domain: str, subdomain_name: str):
        url1 = f"https://api.godaddy.com/v1/domains/{domain}/records/A/{subdomain_name}"
        url2 = f"https://api.godaddy.com/v1/domains/{domain}/records/CNAME/www.{subdomain_name}"
        try:
            async with httpx.AsyncClient() as client:
                response1 = await client.delete(url1)
                response1.raise_for_status()
                response2 = await client.delete(url2)
                response2.raise_for_status()
            return True
        except httpx.HTTPStatusError as e:
            print(f"GoDaddy API error: {e}")
            return False