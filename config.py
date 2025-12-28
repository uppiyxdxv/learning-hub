import os

class Config:
    SECRET_KEY = 'learning-platform-secret-key-2025'
    # FIXED: Use simple path in project root
    SQLALCHEMY_DATABASE_URI = 'sqlite:///learning.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
