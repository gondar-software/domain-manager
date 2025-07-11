from src.domain_helper import GodaddyManager, NginxManager, setup_cert, remove_cert
from src.schemas import Domain, Host
from src.config import settings

class DomainService:
    def __init__(
        self,
        godaddy_api_key: str = settings.GODADDY_API_KEY,
        godaddy_api_secret: str = settings.GODADDY_API_SECRET,
        email_address: str = settings.EMAIL_ADDRESS
    ):
        self.godaddy_manager = GodaddyManager(
            godaddy_api_key,
            godaddy_api_secret
        )
        self.email_address = email_address
        self.nginx_manager = NginxManager()

    async def get_all_domains(self) -> list[Domain]:
        """
        Get all domains.
        """
        return self.nginx_manager.get_current_domains()

    async def add_domain(self, domain: str, hosts: list[Host]):
        """
        Add a new domain.
        """
        await self.remove_domain(domain)
        await self.godaddy_manager.add_records(domain)
        setup_cert(domain, self.email_address)
        new_domain = Domain(domain, hosts)
        self.nginx_manager.add_domain(new_domain)
        await self.remove_domain(domain)

    async def remove_domain(self, domain: str):
        """
        Remove an existing domain.
        """
        await self.godaddy_manager.remove_records(domain)
        remove_cert(domain)
        self.nginx_manager.remove_domain(domain)
        self.nginx_manager.restart_nginx()

    async def update_domain(self, domain: str, hosts: list[Host]):
        """
        Update an existing domain with new hosts.
        """
        await self.remove_domain(domain)
        await self.add_domain(domain, hosts)