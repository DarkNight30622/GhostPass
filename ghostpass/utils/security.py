"""
Security Utilities

Provides security-related utilities for GHOST PASS.
"""

import hashlib
import secrets
import logging
from typing import Dict, List, Optional
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class SecurityUtils:
    """
    Security utilities for GHOST PASS.
    
    Provides:
    - Password hashing and verification
    - Secure random generation
    - Hash verification
    - Security checks
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def hash_password(self, password: str, salt: Optional[bytes] = None) -> Dict[str, bytes]:
        """
        Hash a password using PBKDF2.
        
        Args:
            password: Password to hash
            salt: Optional salt (generated if not provided)
        
        Returns:
            Dictionary with hash and salt
        """
        if salt is None:
            salt = secrets.token_bytes(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        password_hash = kdf.derive(password.encode())
        
        return {
            'hash': password_hash,
            'salt': salt
        }
    
    def verify_password(self, password: str, password_hash: bytes, salt: bytes) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            password: Password to verify
            password_hash: Stored password hash
            salt: Salt used for hashing
        
        Returns:
            True if password matches, False otherwise
        """
        try:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            
            kdf.verify(password.encode(), password_hash)
            return True
            
        except Exception:
            return False
    
    def generate_secure_token(self, length: int = 32) -> str:
        """
        Generate a secure random token.
        
        Args:
            length: Length of token in bytes
        
        Returns:
            Hex-encoded secure token
        """
        return secrets.token_hex(length)
    
    def generate_strong_password(self, length: int = 16) -> str:
        """
        Generate a strong random password.
        
        Args:
            length: Length of password
        
        Returns:
            Strong password string
        """
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    def verify_file_integrity(self, file_path: str, expected_hash: str, 
                            algorithm: str = "sha256") -> bool:
        """
        Verify file integrity using hash.
        
        Args:
            file_path: Path to file
            expected_hash: Expected hash value
            algorithm: Hash algorithm to use
        
        Returns:
            True if hash matches, False otherwise
        """
        try:
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            if algorithm.lower() == "sha256":
                actual_hash = hashlib.sha256(file_data).hexdigest()
            elif algorithm.lower() == "sha512":
                actual_hash = hashlib.sha512(file_data).hexdigest()
            elif algorithm.lower() == "md5":
                actual_hash = hashlib.md5(file_data).hexdigest()
            else:
                raise ValueError(f"Unsupported hash algorithm: {algorithm}")
            
            return actual_hash == expected_hash
            
        except Exception as e:
            self.logger.error(f"File integrity check failed: {e}")
            return False
    
    def sanitize_filename(self, filename: str) -> str:
        """
        Sanitize a filename for safe storage.
        
        Args:
            filename: Original filename
        
        Returns:
            Sanitized filename
        """
        # Remove or replace dangerous characters
        dangerous_chars = '<>:"/\\|?*'
        for char in dangerous_chars:
            filename = filename.replace(char, '_')
        
        # Limit length
        if len(filename) > 255:
            filename = filename[:255]
        
        return filename
    
    def check_password_strength(self, password: str) -> Dict[str, any]:
        """
        Check password strength.
        
        Args:
            password: Password to check
        
        Returns:
            Dictionary with strength analysis
        """
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 8:
            score += 1
        else:
            feedback.append("Password should be at least 8 characters long")
        
        # Uppercase check
        if any(c.isupper() for c in password):
            score += 1
        else:
            feedback.append("Password should contain uppercase letters")
        
        # Lowercase check
        if any(c.islower() for c in password):
            score += 1
        else:
            feedback.append("Password should contain lowercase letters")
        
        # Digit check
        if any(c.isdigit() for c in password):
            score += 1
        else:
            feedback.append("Password should contain numbers")
        
        # Special character check
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if any(c in special_chars for c in password):
            score += 1
        else:
            feedback.append("Password should contain special characters")
        
        # Strength rating
        if score <= 2:
            strength = "Weak"
        elif score <= 3:
            strength = "Fair"
        elif score <= 4:
            strength = "Good"
        else:
            strength = "Strong"
        
        return {
            'score': score,
            'strength': strength,
            'feedback': feedback,
            'max_score': 5
        } 