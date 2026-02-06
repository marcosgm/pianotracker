#!/usr/bin/env python3
"""
Initialize Azure CosmosDB database and containers.
Creates the database and required containers with proper partition keys.

Usage:
    python backend/src/db/initialize.py

Environment Variables:
    COSMOSDB_ENDPOINT: CosmosDB endpoint URL
    COSMOSDB_KEY: CosmosDB primary key
    COSMOSDB_DATABASE: Database name (default: pianotracker)
"""

import asyncio
import sys
from azure.cosmos.aio import CosmosClient
from azure.cosmos import PartitionKey

# Configuration
DATABASE_ID = "pianotracker"
USERS_CONTAINER_ID = "users"
SESSIONS_CONTAINER_ID = "practice_sessions"

# Indexes for performance
USERS_INDEXES = [
    {
        "key": [{"path": "/email"}],
        "unique": True
    }
]

SESSIONS_INDEXES = [
    {
        "key": [{"path": "/user_id"}, {"path": "/date", "order": "descending"}]
    },
    {
        "key": [{"path": "/user_id"}, {"path": "/practice_type"}]
    }
]


async def initialize_database():
    """Initialize Cosmos DB database and containers."""
    import os
    
    endpoint = os.getenv("COSMOSDB_ENDPOINT")
    key = os.getenv("COSMOSDB_KEY")
    
    if not endpoint or not key:
        print("Error: COSMOSDB_ENDPOINT and COSMOSDB_KEY must be set")
        sys.exit(1)
    
    # Create client and database
    client = CosmosClient(endpoint, credential=key)
    
    try:
        # Create or get database
        database = client.get_database_client(DATABASE_ID)
        print(f"✓ Using database: {DATABASE_ID}")
    except Exception:
        # Database doesn't exist, create it
        database = await client.create_database(DATABASE_ID)
        print(f"✓ Created database: {DATABASE_ID}")
    
    # Create users container
    try:
        users_container = database.get_container_client(USERS_CONTAINER_ID)
        print(f"✓ Using container: {USERS_CONTAINER_ID}")
    except Exception:
        users_container = await database.create_container(
            id=USERS_CONTAINER_ID,
            partition_key=PartitionKey(path="/partition_key"),
            offer_throughput=400  # Minimum for non-free tier
        )
        print(f"✓ Created container: {USERS_CONTAINER_ID}")
    
    # Create sessions container
    try:
        sessions_container = database.get_container_client(SESSIONS_CONTAINER_ID)
        print(f"✓ Using container: {SESSIONS_CONTAINER_ID}")
    except Exception:
        sessions_container = await database.create_container(
            id=SESSIONS_CONTAINER_ID,
            partition_key=PartitionKey(path="/partition_key"),
            offer_throughput=400
        )
        print(f"✓ Created container: {SESSIONS_CONTAINER_ID}")
    
    # Note: Composite indexes and unique indexes typically require
    # updating the indexing policy on existing containers.
    # For MVP, let's keep it simple and use default indexing.
    
    print("\n✓ Database initialization complete!")
    print(f"  Endpoint: {endpoint}")
    print(f"  Database: {DATABASE_ID}")
    print(f"  Containers: {USERS_CONTAINER_ID}, {SESSIONS_CONTAINER_ID}")


if __name__ == "__main__":
    asyncio.run(initialize_database())
