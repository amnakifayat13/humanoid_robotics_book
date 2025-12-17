from typing import List
from config.settings import settings
from openai import OpenAI
import os


class EmbeddingService:
    def __init__(self):
        # Use the same API key and base URL as configured in main.py for consistency
        self.client = OpenAI(
            api_key=settings.GEMINI_API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )
        # Use the appropriate embedding model for the OpenAI-compatible endpoint
        self.model = "text-embedding-004"

    async def create_embedding(self, text: str) -> List[float]:
        """
        Create embedding for a single text
        """
        try:
            # Use OpenAI client to create embeddings via the OpenAI-compatible endpoint
            response = self.client.embeddings.create(
                input=[text],
                model=self.model
            )
            return response.data[0].embedding  # Return the first embedding
        except Exception as e:
            print(f"Error creating embedding: {e}")
            return []

    async def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings for multiple texts
        """
        embeddings = []
        for text in texts:
            embedding = await self.create_embedding(text)
            embeddings.append(embedding)
        return embeddings

    async def create_query_embedding(self, query: str) -> List[float]:
        """
        Create embedding for a query (with specific task type)
        """
        try:
            response = self.client.embeddings.create(
                input=[query],
                model=self.model
            )
            return response.data[0].embedding  # Return the first embedding
        except Exception as e:
            print(f"Error creating query embedding: {e}")
            return []