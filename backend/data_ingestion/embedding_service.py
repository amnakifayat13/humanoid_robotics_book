import google.generativeai as genai
from typing import List, Optional
from config.settings import settings
from utils import LoggerSetup, ProcessingError
import time
import logging


class EmbeddingService:
    """
    Service for generating embeddings using Google Gemini API.
    """

    def __init__(self):
        self.logger = LoggerSetup.setup_logging("embedding_service")
        if not settings.GEMINI_API_KEY:
            raise ProcessingError(
                "GEMINI_API_KEY not set in environment variables",
                error_code="MISSING_API_KEY"
            )

        genai.configure(api_key=settings.GEMINI_API_KEY)
        # Use the text-embedding-004 model (the current available embedding model in Gemini)
        self.model_name = "models/text-embedding-004"
        self.batch_size = settings.BATCH_SIZE

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate a single embedding for the given text.

        Args:
            text: Input text to generate embedding for

        Returns:
            List of floats representing the embedding vector
        """
        try:
            # Use the embeddings API to generate the embedding
            result = genai.embed_content(
                model=self.model_name,
                content=text,
                task_type="retrieval_document"  # Optimized for document retrieval
            )

            if 'embedding' in result and len(result['embedding']) > 0:
                self.logger.debug(f"Generated embedding of size {len(result['embedding'])} for text of length {len(text)}")
                return result['embedding']
            else:
                raise ProcessingError(
                    "Embedding generation returned empty result",
                    error_code="EMPTY_EMBEDDING"
                )

        except Exception as e:
            self.logger.error(f"Error generating embedding: {str(e)}")
            raise ProcessingError(
                f"Failed to generate embedding: {str(e)}",
                error_code="EMBEDDING_GENERATION_ERROR",
                original_error=e
            )

    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a batch of texts.

        Args:
            texts: List of input texts to generate embeddings for

        Returns:
            List of embedding vectors (each a list of floats)
        """
        embeddings = []

        # Process in chunks to respect API limits
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            self.logger.info(f"Processing batch {i//self.batch_size + 1} of {(len(texts)-1)//self.batch_size + 1}")

            try:
                # Generate embeddings for the batch
                batch_results = genai.embed_content(
                    model=self.model_name,
                    content=batch,
                    task_type="retrieval_document"
                )

                if 'embedding' in batch_results and len(batch_results['embedding']) == len(batch):
                    embeddings.extend(batch_results['embedding'])
                    self.logger.info(f"Generated {len(batch_results['embedding'])} embeddings in batch")
                else:
                    # Fallback: process one by one if batch failed
                    self.logger.warning("Batch embedding failed, falling back to individual processing")
                    for text in batch:
                        embedding = self.generate_embedding(text)
                        embeddings.append(embedding)

            except Exception as e:
                self.logger.error(f"Error in batch embedding: {str(e)}")
                # Fallback: process one by one if batch failed
                for text in batch:
                    try:
                        embedding = self.generate_embedding(text)
                        embeddings.append(embedding)
                    except Exception as single_error:
                        self.logger.error(f"Failed to embed single text: {str(single_error)}")
                        # Add a zero vector as fallback
                        embeddings.append([0.0] * 768)
                        continue

        return embeddings

    def validate_embedding(self, embedding: List[float]) -> bool:
        """
        Validate that the embedding is properly formatted.

        Args:
            embedding: The embedding vector to validate

        Returns:
            True if valid, False otherwise
        """
        if not isinstance(embedding, list) or len(embedding) != 768:
            self.logger.error(f"Invalid embedding: expected list of 768 floats, got {len(embedding) if isinstance(embedding, list) else type(embedding)} elements")
            return False

        # Check if all values are numbers
        if not all(isinstance(val, (int, float)) for val in embedding):
            self.logger.error("Invalid embedding: contains non-numeric values")
            return False

        return True

    def get_model_info(self) -> dict:
        """
        Get information about the embedding model.

        Returns:
            Dictionary with model information
        """
        return {
            "model_name": self.model_name,
            "vector_size": 768,  # text-embedding-004 still produces 768-dim vectors
            "batch_size": self.batch_size
        }


# Global instance for use throughout the application
embedding_service = EmbeddingService()