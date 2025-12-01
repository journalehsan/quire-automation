"""
OAuth2 authentication for Quire API
"""

import os
import requests
from typing import Dict, Optional
from datetime import datetime, timedelta


class QuireAuth:
    """Handle OAuth2 authentication with Quire"""
    
    OAUTH_AUTHORIZE_URL = "https://quire.io/oauth"
    OAUTH_TOKEN_URL = "https://quire.io/oauth/token"
    
    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        refresh_token: Optional[str] = None,
    ):
        """
        Initialize Quire OAuth handler
        
        Args:
            client_id: OAuth client ID (reads from QUIRE_CLIENT_ID if not provided)
            client_secret: OAuth client secret (reads from QUIRE_CLIENT_SECRET if not provided)
            refresh_token: OAuth refresh token (reads from QUIRE_REFRESH_TOKEN if not provided)
        """
        self.client_id = client_id or os.getenv("QUIRE_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("QUIRE_CLIENT_SECRET")
        self.refresh_token = refresh_token or os.getenv("QUIRE_REFRESH_TOKEN")
        
        self.access_token: Optional[str] = None
        self.token_expires_at: Optional[datetime] = None
        
        if not self.client_id or not self.client_secret:
            raise ValueError(
                "Client ID and Secret are required. "
                "Set QUIRE_CLIENT_ID and QUIRE_CLIENT_SECRET environment variables."
            )
    
    def get_authorization_url(self, redirect_uri: str = "https://localhost") -> str:
        """
        Get the OAuth authorization URL to start the flow
        
        Args:
            redirect_uri: Where Quire will redirect after authorization
            
        Returns:
            Authorization URL to open in browser
        """
        return f"{self.OAUTH_AUTHORIZE_URL}?client_id={self.client_id}&redirect_uri={redirect_uri}"
    
    def exchange_code_for_tokens(self, code: str) -> Dict[str, any]:
        """
        Exchange authorization code for access and refresh tokens
        
        Args:
            code: Authorization code from OAuth callback
            
        Returns:
            Token response with access_token, refresh_token, etc.
        """
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        
        response = requests.post(self.OAUTH_TOKEN_URL, data=data)
        response.raise_for_status()
        
        token_data = response.json()
        self._update_tokens(token_data)
        
        return token_data
    
    def refresh_access_token(self) -> Dict[str, any]:
        """
        Use refresh token to get a new access token
        
        Returns:
            New token data
        """
        if not self.refresh_token:
            raise ValueError("Refresh token not set. Run OAuth flow first.")
        
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        
        response = requests.post(self.OAUTH_TOKEN_URL, data=data)
        response.raise_for_status()
        
        token_data = response.json()
        self._update_tokens(token_data)
        
        return token_data
    
    def get_valid_access_token(self) -> str:
        """
        Get a valid access token, refreshing if necessary
        
        Returns:
            Valid access token
        """
        # If no token or expired, refresh
        if not self.access_token or self._is_token_expired():
            self.refresh_access_token()
        
        return self.access_token
    
    def _update_tokens(self, token_data: Dict[str, any]):
        """Update internal token state"""
        self.access_token = token_data["access_token"]
        
        # Calculate expiration (expires_in is in seconds)
        expires_in = token_data.get("expires_in", 2592000)  # Default 30 days
        self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 300)  # 5 min buffer
        
        # Update refresh token if provided
        if "refresh_token" in token_data:
            self.refresh_token = token_data["refresh_token"]
    
    def _is_token_expired(self) -> bool:
        """Check if access token is expired"""
        if not self.token_expires_at:
            return True
        return datetime.now() >= self.token_expires_at
    
    def get_auth_headers(self) -> Dict[str, str]:
        """
        Get authorization headers for API requests
        
        Returns:
            Dict with Authorization header
        """
        token = self.get_valid_access_token()
        return {"Authorization": f"Bearer {token}"}
