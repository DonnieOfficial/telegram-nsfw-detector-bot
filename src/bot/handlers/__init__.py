from aiogram import Router

from . import start, photo


def setup_routers() -> Router:
    router = Router()

    router.include_router(start.router)
    router.include_router(photo.router)
    return router