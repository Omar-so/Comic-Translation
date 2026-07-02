#alembic/env.py
from alembic import context

config = context.config

from config import settings
from app.models.base import Base
import app.models.user
import app.models.chapter

print("DB URL:", settings.db_url)
config.set_main_option("sqlalchemy.url", settings.db_url)

target_metadata = Base.metadata