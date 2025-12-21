from aiogram import Router
from .error_handler import router as error_router
from .start_handler import router as start_router
from .admin_handler import router as admin_router
from .services import router as services_router

router = Router()

router.include_router(admin_router)
router.include_router(error_router)
router.include_router(start_router)
router.include_router(services_router)