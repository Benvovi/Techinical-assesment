"""
Authentication and Authorization Middleware
"""
import os
import jwt
from functools import wraps
from flask import request, jsonify, g
from datetime import datetime, timedelta


JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'change-me-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_DELTA = timedelta(hours=24)


def generate_token(user_id: str, username: str) -> str:
    """
    Generate JWT token for user
    
    Args:
        user_id: User identifier
        username: Username
        
    Returns:
        JWT token string
    """
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.utcnow() + JWT_EXPIRATION_DELTA,
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> dict:
    """
    Verify JWT token
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token payload
        
    Raises:
        jwt.ExpiredSignatureError: Token has expired
        jwt.InvalidTokenError: Token is invalid
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError('Token has expired')
    except jwt.InvalidTokenError:
        raise ValueError('Invalid token')


def require_auth(f):
    """
    Decorator to require authentication for endpoints
    
    Usage:
        @require_auth
        def protected_endpoint():
            user_id = g.user_id
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'Authorization header missing'}), 401
        
        try:
            # Extract token from "Bearer <token>"
            token = auth_header.split(' ')[1] if ' ' in auth_header else auth_header
            payload = verify_token(token)
            
            # Store user info in Flask g object
            g.user_id = payload.get('user_id')
            g.username = payload.get('username')
            
        except ValueError as e:
            return jsonify({'error': str(e)}), 401
        except Exception as e:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function


def require_role(*allowed_roles):
    """
    Decorator to require specific roles
    
    Usage:
        @require_auth
        @require_role('admin', 'operator')
        def admin_endpoint():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # This would check roles from the token or database
            # For now, it's a placeholder
            if not hasattr(g, 'user_id'):
                return jsonify({'error': 'Authentication required'}), 401
            
            # Role checking logic would go here
            # For simplicity, we'll allow if authenticated
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator
