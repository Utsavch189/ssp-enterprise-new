from flask import Flask
from app.router.auth_router import auth_bp
from app.router.crm_router import crm_bp
from app.router.product_router import product_bp

def register_router(app:Flask):
    app.register_blueprint(auth_bp)
    app.register_blueprint(crm_bp)
    app.register_blueprint(product_bp)