from aiogram import Router
from .errors import router as error_router
from .default import router as default_router
from .services import router as services_router

router = Router()

router.include_router(error_router)
router.include_router(default_router)
router.include_router(services_router)