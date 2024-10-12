from pkg.handlers import router
from pkg.handlers.get_health_status.service import get_status_message


@router.get('/health/status')
def get():
    return get_status_message()
