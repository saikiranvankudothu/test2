# config/testing.py
from config.base import BaseConfig

class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = False
