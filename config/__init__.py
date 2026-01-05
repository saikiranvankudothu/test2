# config/__init__.py
import os
from config.development import DevelopmentConfig
from config.production import ProductionConfig
from config.testing import TestingConfig

def get_config():
    env = os.getenv("FLASK_ENV", "development")

    if env == "production":
        return ProductionConfig
    if env == "testing":
        return TestingConfig
    return DevelopmentConfig
