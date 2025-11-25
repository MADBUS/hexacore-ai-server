"""
Centralized router configuration.
All application routers are registered here and imported into main.py.
"""
from fastapi import FastAPI

from app.social_oauth.adapter.input.web.google_oauth2_router import authentication_router
from app.user.adapter.input.web.user_router import user_router
from app.post_analysis.adapter.input.web.document_analysis_router import post_analysis_router

# Import ORM models to register them with SQLAlchemy Base
from app.user.infrastructure.orm.user_orm import UserORM  # noqa: F401


def setup_routers(app: FastAPI) -> None:
    app.include_router(authentication_router, prefix="/authentication")
    app.include_router(user_router, prefix="/user")
    app.include_router(post_analysis_router, prefix="/post-analysis")