from aiogram import Router

from . import start, photo, text


def setup_routers() -> Router:
    router = Router()

    router.include_router(start.router)
    router.include_router(photo.router)
    router.include_router(text.router)
    return router