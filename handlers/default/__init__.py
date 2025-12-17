from aiogram import Router
from .start import router as default_router

router = Router()
router.include_router(default_router)