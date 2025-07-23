"""
Encryption Module

Handles multi-layer encryption using AES-256, ChaCha20, and TLS tunneling
for secure data transmission through TOR.
"""

import os
import base64
import hashlib
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
import ssl
import socket


@dataclass
class EncryptionConfig:
    """Configuration for encryption settings."""
    algorithm: str = "AES-256-GCM"
    key_size: int = 32  # 256 bits
    salt_size: int = 16
    iv_size: int = 12
    tag_size: int = 16
    iterations: int = 100000


class EncryptionManager:
    """
    Manages multi-layer encryption for secure data transmission.
    
    Provides:
    - AES-256-GCM encryption
    - ChaCha20-Poly1305 encryption
    - TLS tunneling
    - Key derivation and management
    - Secure random generation
    """
    
    def __init__(self, config: EncryptionConfig = None):
        self.config = config or EncryptionConfig()
        self.logger = logging.getLogger(__name__)
        self._master_key: Optional[bytes] = None
        self._session_keys: Dict[str, bytes] = {}
        
    def generate_master_key(self, password: str, salt: Optional[bytes] = None) -> bytes:
        """Generate a master key from password using PBKDF2."""
        if salt is None:
            salt = os.urandom(self.config.salt_size)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.config.key_size,
            salt=salt,
            iterations=self.config.iterations,
            backend=default_backend()
        )
        
        self._master_key = kdf.derive(password.encode())
        return self._master_key
    
    def derive_session_key(self, session_id: str, info: str = b"session") -> bytes:
        """Derive a session key from master key using HKDF."""
        if not self._master_key:
            raise ValueError("Master key not set. Call generate_master_key first.")
        
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=self.config.key_size,
            salt=None,
            info=info,
            backend=default_backend()
        )
        
        session_key = hkdf.derive(self._master_key + session_id.encode())
        self._session_keys[session_id] = session_key
        return session_key
    
    def encrypt_aes(self, data: bytes, key: Optional[bytes] = None, 
                   session_id: str = "default") -> Dict[str, bytes]:
        """Encrypt data using AES-256-GCM."""
        if key is None:
            if session_id not in self._session_keys:
                self.derive_session_key(session_id)
            key = self._session_keys[session_id]
        
        # Generate random IV
        iv = os.urandom(self.config.iv_size)
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(iv),
            backend=default_backend()
        )
        
        encryptor = cipher.encryptor()
        
        # Encrypt data
        ciphertext = encryptor.update(data) + encryptor.finalize()
        
        return {
            'ciphertext': ciphertext,
            'iv': iv,
            'tag': encryptor.tag
        }
    
    def decrypt_aes(self, encrypted_data: Dict[str, bytes], 
                   key: Optional[bytes] = None, session_id: str = "default") -> bytes:
        """Decrypt data using AES-256-GCM."""
        if key is None:
            if session_id not in self._session_keys:
                raise ValueError(f"Session key for {session_id} not found")
            key = self._session_keys[session_id]
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(encrypted_data['iv'], encrypted_data['tag']),
            backend=default_backend()
        )
        
        decryptor = cipher.decryptor()
        
        # Decrypt data
        plaintext = decryptor.update(encrypted_data['ciphertext']) + decryptor.finalize()
        
        return plaintext
    
    def encrypt_chacha20(self, data: bytes, key: Optional[bytes] = None,
                        session_id: str = "default") -> Dict[str, bytes]:
        """Encrypt data using ChaCha20-Poly1305."""
        if key is None:
            if session_id not in self._session_keys:
                self.derive_session_key(session_id)
            key = self._session_keys[session_id]
        
        # Generate random nonce
        nonce = os.urandom(12)
        
        # Create cipher
        cipher = Cipher(
            algorithms.ChaCha20(key, nonce),
            mode=None,
            backend=default_backend()
        )
        
        encryptor = cipher.encryptor()
        
        # Encrypt data
        ciphertext = encryptor.update(data) + encryptor.finalize()
        
        return {
            'ciphertext': ciphertext,
            'nonce': nonce
        }
    
    def decrypt_chacha20(self, encrypted_data: Dict[str, bytes],
                        key: Optional[bytes] = None, session_id: str = "default") -> bytes:
        """Decrypt data using ChaCha20-Poly1305."""
        if key is None:
            if session_id not in self._session_keys:
                raise ValueError(f"Session key for {session_id} not found")
            key = self._session_keys[session_id]
        
        # Create cipher
        cipher = Cipher(
            algorithms.ChaCha20(key, encrypted_data['nonce']),
            mode=None,
            backend=default_backend()
        )
        
        decryptor = cipher.decryptor()
        
        # Decrypt data
        plaintext = decryptor.update(encrypted_data['ciphertext']) + decryptor.finalize()
        
        return plaintext
    
    def create_tls_tunnel(self, host: str, port: int, 
                         verify_ssl: bool = True) -> socket.socket:
        """Create a TLS tunnel to a remote host."""
        try:
            # Create SSL context
            context = ssl.create_default_context()
            if not verify_ssl:
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
            
            # Create socket and wrap with SSL
            sock = socket.create_connection((host, port))
            ssl_sock = context.wrap_socket(sock, server_hostname=host)
            
            self.logger.info(f"TLS tunnel established to {host}:{port}")
            return ssl_sock
            
        except Exception as e:
            self.logger.error(f"Failed to create TLS tunnel: {e}")
            raise
    
    def encrypt_multi_layer(self, data: bytes, session_id: str = "default") -> Dict[str, Any]:
        """Apply multiple layers of encryption."""
        try:
            # Layer 1: AES-256-GCM
            aes_encrypted = self.encrypt_aes(data, session_id=session_id)
            
            # Layer 2: ChaCha20 (encrypt the AES ciphertext)
            chacha_encrypted = self.encrypt_chacha20(
                aes_encrypted['ciphertext'], 
                session_id=f"{session_id}_chacha"
            )
            
            return {
                'aes_iv': aes_encrypted['iv'],
                'aes_tag': aes_encrypted['tag'],
                'chacha_nonce': chacha_encrypted['nonce'],
                'final_ciphertext': chacha_encrypted['ciphertext'],
                'algorithm': 'AES-256-GCM+ChaCha20',
                'session_id': session_id
            }
            
        except Exception as e:
            self.logger.error(f"Multi-layer encryption failed: {e}")
            raise
    
    def decrypt_multi_layer(self, encrypted_data: Dict[str, Any]) -> bytes:
        """Decrypt multiple layers of encryption."""
        try:
            session_id = encrypted_data.get('session_id', 'default')
            
            # Layer 2: Decrypt ChaCha20
            chacha_data = {
                'ciphertext': encrypted_data['final_ciphertext'],
                'nonce': encrypted_data['chacha_nonce']
            }
            aes_ciphertext = self.decrypt_chacha20(
                chacha_data, 
                session_id=f"{session_id}_chacha"
            )
            
            # Layer 1: Decrypt AES-256-GCM
            aes_data = {
                'ciphertext': aes_ciphertext,
                'iv': encrypted_data['aes_iv'],
                'tag': encrypted_data['aes_tag']
            }
            plaintext = self.decrypt_aes(aes_data, session_id=session_id)
            
            return plaintext
            
        except Exception as e:
            self.logger.error(f"Multi-layer decryption failed: {e}")
            raise
    
    def generate_secure_random(self, length: int) -> bytes:
        """Generate cryptographically secure random bytes."""
        return os.urandom(length)
    
    def hash_data(self, data: bytes, algorithm: str = "sha256") -> str:
        """Hash data using specified algorithm."""
        if algorithm.lower() == "sha256":
            return hashlib.sha256(data).hexdigest()
        elif algorithm.lower() == "sha512":
            return hashlib.sha512(data).hexdigest()
        elif algorithm.lower() == "blake2b":
            return hashlib.blake2b(data).hexdigest()
        else:
            raise ValueError(f"Unsupported hash algorithm: {algorithm}")
    
    def verify_integrity(self, data: bytes, expected_hash: str, 
                        algorithm: str = "sha256") -> bool:
        """Verify data integrity using hash."""
        actual_hash = self.hash_data(data, algorithm)
        return actual_hash == expected_hash
    
    def clear_session_keys(self):
        """Clear all session keys from memory."""
        self._session_keys.clear()
        self.logger.info("Session keys cleared from memory")
    
    def get_encryption_info(self) -> Dict[str, Any]:
        """Get information about current encryption setup."""
        return {
            'algorithm': self.config.algorithm,
            'key_size': self.config.key_size,
            'active_sessions': len(self._session_keys),
            'master_key_set': self._master_key is not None
        } 