# Auth/utils.py
import jwt
from datetime import datetime, timedelta
from django.conf import settings

# Clé secrète
SECRET_KEY = settings.SECRET_KEY  # ou une autre constante privée

def generate_jwt_token(user_id):
    expiration = datetime.utcnow() + timedelta(days=1)  # Token valide 1 jour
    payload = {
        'user_id': user_id,
        'exp': expiration,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
