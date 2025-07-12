import httpx
import tldextract

class GodaddyManager:
    def __init__(self, key: str, secret: str):
        self.key = key
        self.secret = secret

    def split_domain(self, full_domain: str):
        """
        Split a full domain into subdomain and primary domain.
        """
        extracted = tldextract.extract(full_domain)
        subdomain = extracted.subdomain
        primary_domain = f"{extracted.domain}.{extracted.suffix}"
        return subdomain, primary_domain

    async def process_records(self, full_domain: str, record_types: list, action: str):
        """
        Process DNS records for a domain or subdomain with multiple types (A and CNAME).
        :param full_domain: Full domain name (e.g., "blog.example.com").
        :param record_types: List of record types to process (e.g., ["A", "CNAME"]).
        :param action: Action to perform ("add" or "remove").
        """
        subdomain, primary_domain = self.split_domain(full_domain)
        
        headers = {
            "Authorization": f"sso-key {self.key}:{self.secret}",
            "Content-Type": "application/json"
        }
        if action == "add":
            async with httpx.AsyncClient() as client:
                ip_response = await client.get("https://api.ipify.org")
                ip_response.raise_for_status()
                public_ip = ip_response.text
                data = [{
                    "data": public_ip if record_type == "A" else f"{full_domain}.",
                    "name": (subdomain if subdomain else "@") if record_type == "A" else (f"www.{subdomain}" if subdomain else "www"),
                    "type": record_type
                } for record_type in record_types]
                url = f"https://api.ote-godaddy.com/v1/domains/{primary_domain}/records"
                response = await client.patch(url, headers=headers, json=data)
                response.raise_for_status()
        for record_type in record_types:
            if action == "remove":
                async with httpx.AsyncClient() as client:
                    url = f"https://api.ote-godaddy.com/v1/domains/{primary_domain}/records/{record_type}/{subdomain if subdomain else '@'}"
                    response = await client.delete(url, headers=headers)
                    response.raise_for_status()

    async def add_records(self, full_domain: str, record_types: list = ["A", "CNAME"]):
        """
        Add DNS records for a domain or subdomain with multiple types.
        """
        return await self.process_records(full_domain, record_types, action="add")

    async def remove_records(self, full_domain: str, record_types: list = ["A", "CNAME"]):
        """
        Remove DNS records for a domain or subdomain with multiple types.
        """
        return await self.process_records(full_domain, record_types, action="remove")