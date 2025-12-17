from aiogram import Router
from .me import router as me_router

router = Router()

router.include_router(me_router)