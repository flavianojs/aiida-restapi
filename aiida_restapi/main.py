# -*- coding: utf-8 -*-
"""Declaration of FastAPI application."""
from fastapi import FastAPI

from aiida_restapi.routers import auth, users

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)