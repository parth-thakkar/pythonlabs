import httpx

class SimpleMCPClient:
    def __init__(self, base_url: str, api_key: str | None = None):
        self.base_url = base_url
        self.headers = {}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

        self.client = httpx.Client(headers=self.headers)

        # MCP handshake (mandatory)
        self.client.post(
            f"{self.base_url}/initialize",
            json={
                "protocolVersion": "2024-11-05",
                "clientInfo": {
                    "name": "langgraph-client",
                    "version": "1.0.0",
                },
            },
        )

    def list_tools(self):
        resp = self.client.post(f"{self.base_url}/tools/list", json={})
        resp.raise_for_status()
        return resp.json()["tools"]

    def call_tool(self, name: str, arguments: dict | None = None):
        resp = self.client.post(
            f"{self.base_url}/tools/call",
            json={
                "name": name,
                "arguments": arguments or {},
            },
        )
        resp.raise_for_status()
        return resp.json()["content"]
