import uuid
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct
from config.settings import settings
from utils import LoggerSetup, ProcessingError
import logging


class QdrantClientWrapper:
    """
    Wrapper class for Qdrant client with methods for document chunk storage and retrieval.
    """

    def __init__(self):
        self.logger = LoggerSetup.setup_logging("qdrant_client")
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            prefer_grpc=True  # Use gRPC for better performance
        )
        self.collection_name = settings.COLLECTION_NAME
        self._ensure_collection_exists()

    def _ensure_collection_exists(self) -> None:
        """
        Ensure the required collection exists in Qdrant.
        Creates it if it doesn't exist.
        """
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_exists = any(col.name == self.collection_name for col in collections.collections)

            if not collection_exists:
                # Create collection with 768-dimensional vectors (for Gemini embeddings)
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=768,  # Gemini text-embedding-3-small produces 768-dim vectors
                        distance=models.Distance.COSINE
                    )
                )
                self.logger.info(f"Created new collection: {self.collection_name}")
            else:
                self.logger.info(f"Collection {self.collection_name} already exists")
        except Exception as e:
            self.logger.error(f"Error ensuring collection exists: {str(e)}")
            raise ProcessingError(
                f"Failed to ensure Qdrant collection exists: {str(e)}",
                error_code="QDRANT_COLLECTION_ERROR",
                original_error=e
            )

    def upload_chunks(self, chunks: List[Dict[str, Any]]) -> bool:
        """
        Upload document chunks to Qdrant vector database.

        Args:
            chunks: List of chunks to upload, each with 'text', 'embedding', and 'metadata'

        Returns:
            True if upload was successful, False otherwise
        """
        try:
            points = []
            for chunk in chunks:
                # Validate required fields
                if 'text' not in chunk or 'embedding' not in chunk:
                    raise ProcessingError(
                        "Chunk missing required fields: 'text' and 'embedding'",
                        error_code="CHUNK_VALIDATION_ERROR"
                    )

                # Validate embedding format
                if not self._validate_embedding_format(chunk['embedding']):
                    raise ProcessingError(
                        f"Invalid embedding format in chunk. Expected 768 elements, got {len(chunk['embedding']) if isinstance(chunk['embedding'], list) else 'non-list'}",
                        error_code="EMBEDDING_FORMAT_ERROR"
                    )

                point_id = str(uuid.uuid4())
                payload = {
                    "text": chunk['text'],
                    "metadata": chunk.get('metadata', {}),
                    "size": chunk.get('size', len(chunk['text']))
                }

                point = PointStruct(
                    id=point_id,
                    vector=chunk['embedding'],
                    payload=payload
                )
                points.append(point)

            # Upload in batches
            batch_size = settings.BATCH_SIZE
            for i in range(0, len(points), batch_size):
                batch = points[i:i + batch_size]
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=batch
                )
                self.logger.info(f"Uploaded batch of {len(batch)} chunks to Qdrant")

            self.logger.info(f"Successfully uploaded {len(points)} chunks to Qdrant")
            return True

        except Exception as e:
            self.logger.error(f"Error uploading chunks to Qdrant: {str(e)}")
            raise ProcessingError(
                f"Failed to upload chunks to Qdrant: {str(e)}",
                error_code="QDRANT_UPLOAD_ERROR",
                original_error=e
            )

    def _validate_embedding_format(self, embedding: List[float]) -> bool:
        """
        Validate that the embedding is properly formatted for Qdrant.

        Args:
            embedding: The embedding vector to validate

        Returns:
            True if valid, False otherwise
        """
        if not isinstance(embedding, list) or len(embedding) != 768:
            return False

        # Check if all values are numbers
        if not all(isinstance(val, (int, float)) for val in embedding):
            return False

        return True

    def batch_upload_chunks(self, chunks: List[Dict[str, Any]], batch_size: int = None) -> bool:
        """
        Enhanced batch upload functionality with better error handling and reporting.

        Args:
            chunks: List of chunks to upload
            batch_size: Size of batches (defaults to settings)

        Returns:
            True if all chunks were uploaded successfully
        """
        batch_size = batch_size or settings.BATCH_SIZE
        total_chunks = len(chunks)
        successful_uploads = 0

        try:
            # Process chunks in batches
            for i in range(0, len(chunks), batch_size):
                batch = chunks[i:i + batch_size]

                # Prepare points for this batch
                points = []
                for chunk in batch:
                    if 'text' not in chunk or 'embedding' not in chunk:
                        self.logger.warning(f"Skipping chunk due to missing required fields: {chunk.get('metadata', {}).get('source_file', 'unknown')}")
                        continue

                    if not self._validate_embedding_format(chunk['embedding']):
                        self.logger.warning(f"Skipping chunk due to invalid embedding format: {chunk.get('metadata', {}).get('source_file', 'unknown')}")
                        continue

                    point_id = str(uuid.uuid4())
                    payload = {
                        "text": chunk['text'],
                        "metadata": chunk.get('metadata', {}),
                        "size": chunk.get('size', len(chunk['text']))
                    }

                    point = PointStruct(
                        id=point_id,
                        vector=chunk['embedding'],
                        payload=payload
                    )
                    points.append(point)

                # Upload the batch
                if points:  # Only upload if there are valid points
                    self.client.upsert(
                        collection_name=self.collection_name,
                        points=points
                    )
                    successful_uploads += len(points)
                    self.logger.info(f"Batch upload: {len(points)} chunks uploaded successfully. Progress: {min(i + batch_size, len(chunks))}/{len(chunks)}")

            self.logger.info(f"Batch upload completed: {successful_uploads}/{total_chunks} chunks uploaded")
            return successful_uploads == total_chunks

        except Exception as e:
            self.logger.error(f"Error in batch upload: {str(e)}")
            raise ProcessingError(
                f"Failed to batch upload chunks: {str(e)}",
                error_code="QDRANT_BATCH_UPLOAD_ERROR",
                original_error=e
            )

    def get_chunk_by_id(self, chunk_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific chunk by its ID.

        Args:
            chunk_id: The ID of the chunk to retrieve

        Returns:
            The chunk data if found, None otherwise
        """
        try:
            records = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[chunk_id]
            )

            if records:
                record = records[0]
                chunk_data = {
                    "id": record.id,
                    "text": record.payload.get("text", ""),
                    "metadata": record.payload.get("metadata", {}),
                    "size": record.payload.get("size", 0),
                    "vector": record.vector
                }
                return chunk_data
            return None

        except Exception as e:
            self.logger.error(f"Error retrieving chunk by ID: {str(e)}")
            raise ProcessingError(
                f"Failed to retrieve chunk by ID: {str(e)}",
                error_code="QDRANT_RETRIEVE_ERROR",
                original_error=e
            )

    def count_chunks(self) -> int:
        """
        Get the total number of chunks in the collection.

        Returns:
            The number of chunks in the collection
        """
        try:
            collection_info = self.client.get_collection(self.collection_name)
            return collection_info.points_count
        except Exception as e:
            self.logger.error(f"Error counting chunks: {str(e)}")
            raise ProcessingError(
                f"Failed to count chunks: {str(e)}",
                error_code="QDRANT_COUNT_ERROR",
                original_error=e
            )

    def search_similar(self, query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar chunks in the vector database.

        Args:
            query_embedding: The embedding vector to search for similarity
            limit: Maximum number of results to return

        Returns:
            List of similar chunks with their metadata
        """
        try:
            # Using the correct search method for current Qdrant client version
            search_results = self.client.search_points(
                collection_name=self.collection_name,
                query=query_embedding,
                limit=limit,
                with_payload=True,
            )

            results = []
            for result in search_results:
                chunk_data = {
                    "id": result.id,
                    "text": result.payload.get("text", "") if hasattr(result, 'payload') else getattr(result, 'document', ''),
                    "metadata": result.payload.get("metadata", {}) if hasattr(result, 'payload') else {},
                    "score": result.score
                }
                results.append(chunk_data)

            self.logger.info(f"Found {len(results)} similar chunks for query")
            return results

        except Exception as e:
            self.logger.error(f"Error searching Qdrant: {str(e)}")
            raise ProcessingError(
                f"Failed to search Qdrant: {str(e)}",
                error_code="QDRANT_SEARCH_ERROR",
                original_error=e
            )

    def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the collection.

        Returns:
            Dictionary with collection information
        """
        try:
            collection_info = self.client.get_collection(self.collection_name)
            info = {
                "name": collection_info.config.params.vectors.size,
                "vector_size": collection_info.config.params.vectors.size,
                "distance": collection_info.config.params.vectors.distance,
                "points_count": collection_info.points_count
            }
            return info
        except Exception as e:
            self.logger.error(f"Error getting collection info: {str(e)}")
            raise ProcessingError(
                f"Failed to get collection info: {str(e)}",
                error_code="QDRANT_INFO_ERROR",
                original_error=e
            )

    def delete_collection(self) -> bool:
        """
        Delete the collection (useful for testing/resetting).

        Returns:
            True if deletion was successful, False otherwise
        """
        try:
            self.client.delete_collection(self.collection_name)
            self.logger.info(f"Deleted collection: {self.collection_name}")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting collection: {str(e)}")
            raise ProcessingError(
                f"Failed to delete collection: {str(e)}",
                error_code="QDRANT_DELETE_ERROR",
                original_error=e
            )


# Global instance for use throughout the application
qdrant_client = QdrantClientWrapper()