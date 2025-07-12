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
        try:
            try:
                await self.remove_domain(domain)
            except:
                pass
            setup_cert(domain, self.email_address)
            new_domain = Domain(domain=domain, hosts=hosts)
            self.nginx_manager.add_domain(new_domain)
        except Exception as e:
            print(f"Error adding domain {domain}: {e}")
            await self.remove_domain(domain)
            raise

    async def remove_domain(self, domain: str):
        """
        Remove an existing domain.
        """
        # await self.godaddy_manager.remove_records(domain)
        remove_cert(domain)
        summary = self.nginx_manager.get_hosting_summary()
        old_domain = summary['domains'].get(domain, None)
        if old_domain:
            self.nginx_manager.remove_domain(old_domain)
        

    async def update_domain(self, domain: str, hosts: list[Host]):
        """
        Update an existing domain with new hosts.
        """
        try:
            await self.remove_domain(domain)
            await self.add_domain(domain, hosts)
        except:
            await self.remove_domain(domain)
            raise