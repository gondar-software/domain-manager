from typing import List, Dict

from .godaddy_manager import GodaddyManager
from .nginx_manager import NginxManager
from .types import Domain, Host
from .cert_helper import setup_cert, remove_cert
from .config import settings

class DomainManager:
    def __init__(
        self,
        godaddy_api_key: str = settings.GODADDY_API_KEY,
        godaddy_api_secret: str = settings.GODADDY_API_SECRET,
        domain: str = settings.DOMAIN,
        email_address: str = settings.EMAIL_ADDRESS
    ):
        self.godaddy_manager = GodaddyManager(
            godaddy_api_key,
            godaddy_api_secret
        )
        self.domain = domain
        self.email_address = email_address
        self.nginx_manager = NginxManager()
        self.subdomain_dict: Dict[str, Domain] = {}

    async def add_new_subdomain(self, subdomain: str, hosts: List[Host]):
        next = True

        old_subdomain = self.subdomain_dict.get(subdomain, None)
        if old_subdomain:
            next = await self.remove_subdomain(subdomain)

        if next:
            next = await self.godaddy_manager.add_record(
                self.domain,
                subdomain
            )

        if next:
            next = setup_cert(
                f"{subdomain}.{self.domain}", 
                self.email_address
            )

        if next:
            new_subdomain = Domain(
                f"{subdomain}.{self.domain}",
                hosts
            )
            next = self.nginx_manager.add_domain(new_subdomain)

        if next:
            self.subdomain_dict[subdomain] = new_subdomain
        else:
            await self.remove_subdomain(subdomain)

        return next

    async def remove_subdomain(self, subdomain: str):
        next = True

        if next:
            next = await self.godaddy_manager.remove_record(
                self.domain,
                subdomain
            )

        if next:
            next = remove_cert(
                f"{subdomain}.{self.domain}"
            )

        if next:
            old_subdomain = self.subdomain_dict.get(subdomain, None)
            if old_subdomain:
                next = self.nginx_manager.remove_domain(
                    old_subdomain
                )
                if not next:
                    next = self.nginx_manager.restart_nginx()

        return next