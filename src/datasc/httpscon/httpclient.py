import requests
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context


class HTTPSClient:
    """HTTP client with SSL configuration and bearer token authentication"""

    def __init__(self, base_url, token, verify_ssl=True, cert_path=None):
        """
        Initialize HTTPS client

        Args:
            base_url: Base URL for the API endpoint
            token: Bearer token for authentication
            verify_ssl: Whether to verify SSL certificates (default: True)
            cert_path: Path to custom CA certificate bundle (optional)
        """
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.verify_ssl = verify_ssl
        self.cert_path = cert_path

        # Create session with custom configuration
        self.session = requests.Session()
        self._configure_ssl()
        self._set_headers()

    def _configure_ssl(self):
        """Configure SSL settings for the session"""
        if self.cert_path:
            # Use custom certificate
            self.session.verify = self.cert_path
        elif not self.verify_ssl:
            # Disable SSL verification (not recommended for production)
            self.session.verify = False
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # Optional: Configure custom SSL context with specific TLS version
        class SSLAdapter(HTTPAdapter):
            def init_poolmanager(self, *args, **kwargs):
                context = create_urllib3_context()
                context.minimum_version = urllib3.util.ssl_.TLSVersion.TLSv1_2
                kwargs['ssl_context'] = context
                return super().init_poolmanager(*args, **kwargs)

        self.session.mount('https://', SSLAdapter())

    def _set_headers(self):
        """Set default headers including bearer token"""
        self.session.headers.update({
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def get(self, endpoint, params=None):
        """Make GET request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, data=None, json=None):
        """Make POST request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.post(url, data=data, json=json)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint, data=None, json=None):
        """Make PUT request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.put(url, data=data, json=json)
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint):
        """Make DELETE request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.delete(url)
        response.raise_for_status()
        return response.json() if response.content else None

    def close(self):
        """Close the session"""
        self.session.close()


# Example usage
if __name__ == "__main__":
    # Configuration
    API_URL = "https://api.example.com"
    BEARER_TOKEN = "your-bearer-token-here"

    # Create client with SSL verification enabled
    client = HTTPSClient(
        base_url=API_URL,
        token=BEARER_TOKEN,
        verify_ssl=True  # Set to False to disable SSL verification
    )

    try:
        # Example GET request
        response = client.get("/users", params={"page": 1})
        print("GET response:", response)

        # Example POST request
        new_user = {"name": "John Doe", "email": "john@example.com"}
        response = client.post("/users", json=new_user)
        print("POST response:", response)

        # Example PUT request
        updated_user = {"name": "Jane Doe"}
        response = client.put("/users/1", json=updated_user)
        print("PUT response:", response)

        # Example DELETE request
        response = client.delete("/users/1")
        print("DELETE response:", response)

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.SSLError as e:
        print(f"SSL Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
    finally:
        client.close()