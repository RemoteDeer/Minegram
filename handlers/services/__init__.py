from aiogram import Router
from .aboutme_handler import router as me_router
from .requests_handler import router as requests_router

router = Router()

router.include_router(me_router)
router.include_router(requests_router)