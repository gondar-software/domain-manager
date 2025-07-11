from fastapi import APIRouter, Depends, HTTPException
from src.dependencies import get_domain_service, get_auth_service
from src.services import DomainService
from src.schemas import Domain, Host

domain_router = APIRouter()

@domain_router.get("/", response_model=list[Domain])
async def list_domains(
    payload: dict = Depends(get_auth_service),
    domain_service: DomainService = Depends(get_domain_service)
):
    """
    Endpoint to list all domains.
    """
    try:
        if not payload:
            return await domain_service.get_all_domains()
        else:
            raise HTTPException(status_code=403, detail="Unauthorized access")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@domain_router.post("/")
async def create_domain(
    domain: Domain,
    payload: dict = Depends(get_auth_service),
    domain_service: DomainService = Depends(get_domain_service)
):
    """
    Endpoint to create a new domain.
    """
    try:
        if not payload:
            await domain_service.add_domain(domain.domain, domain.hosts)
        else:
            raise HTTPException(status_code=403, detail="Unauthorized access")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@domain_router.delete("/{domain}")
async def delete_domain(
    domain: str,
    payload: dict = Depends(get_auth_service),
    domain_service: DomainService = Depends(get_domain_service)
):
    """
    Endpoint to delete a domain.
    """
    try:
        if not payload:
            await domain_service.remove_domain(domain)
        else:
            raise HTTPException(status_code=403, detail="Unauthorized access")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@domain_router.put("/{domain}")
async def update_domain(
    domain: str,
    hosts: list[Host],
    payload: dict = Depends(get_auth_service),
    domain_service: DomainService = Depends(get_domain_service)
):
    """
    Endpoint to update an existing domain.
    """
    try:
        if not payload:
            await domain_service.update_domain(domain, hosts)
        else:
            raise HTTPException(status_code=403, detail="Unauthorized access")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))