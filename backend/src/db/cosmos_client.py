"""
CosmosDB client and connection management.
Provides async context managers for database operations.
"""

import os
from typing import Optional
from azure.cosmos.aio import CosmosClient, ContainerProxy, DatabaseProxy


class CosmosDBClient:
    """Async CosmosDB client wrapper."""
    
    _instance: Optional["CosmosDBClient"] = None
    
    def __init__(self, endpoint: str, key: str, database_id: str = "pianotracker"):
        """Initialize CosmosDB client."""
        self.endpoint = endpoint
        self.key = key
        self.database_id = database_id
        self.client: Optional[CosmosClient] = None
        self.database: Optional[DatabaseProxy] = None
    
    async def connect(self) -> None:
        """Establish connection to Cosmos DB."""
        self.client = CosmosClient(self.endpoint, credential=self.key)
        self.database = self.client.get_database_client(self.database_id)
    
    async def disconnect(self) -> None:
        """Close connection to Cosmos DB."""
        if self.client:
            await self.client.close()
    
    def get_users_container(self) -> ContainerProxy:
        """Get users container."""
        if not self.database:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.database.get_container_client("users")
    
    def get_sessions_container(self) -> ContainerProxy:
        """Get practice_sessions container."""
        if not self.database:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.database.get_container_client("practice_sessions")
    
    @classmethod
    def get_instance(cls) -> "CosmosDBClient":
        """Get singleton instance."""
        if cls._instance is None:
            endpoint = os.getenv("COSMOSDB_ENDPOINT")
            key = os.getenv("COSMOSDB_KEY")
            if not endpoint or not key:
                raise ValueError("COSMOSDB_ENDPOINT and COSMOSDB_KEY must be set")
            cls._instance = cls(endpoint, key)
        return cls._instance


# Global client instance
_cosmos_client: Optional[CosmosDBClient] = None


async def get_cosmos_client() -> CosmosDBClient:
    """Get or create global CosmosDB client instance."""
    global _cosmos_client
    if _cosmos_client is None:
        _cosmos_client = CosmosDBClient.get_instance()
        await _cosmos_client.connect()
    return _cosmos_client


async def close_cosmos_client() -> None:
    """Close global CosmosDB client instance."""
    global _cosmos_client
    if _cosmos_client:
        await _cosmos_client.disconnect()
        _cosmos_client = None
