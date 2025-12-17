import re
from typing import List, Dict, Any
from config.settings import settings
from utils import LoggerSetup, ProcessingError
import logging


class TextChunker:
    """
    Class for splitting documents into overlapping chunks of specified size.
    """

    def __init__(self, max_chunk_size: int = None, chunk_overlap: int = None):
        self.logger = LoggerSetup.setup_logging("chunker")
        self.max_chunk_size = max_chunk_size or settings.MAX_CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP

        if self.chunk_overlap >= self.max_chunk_size:
            raise ProcessingError(
                f"Chunk overlap ({self.chunk_overlap}) must be less than chunk size ({self.max_chunk_size})",
                error_code="INVALID_CHUNK_PARAMETERS"
            )

    def chunk_text(self, text: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Split text into overlapping chunks.

        Args:
            text: The text to chunk
            metadata: Metadata to include with each chunk

        Returns:
            List of chunk dictionaries with text, metadata, and size
        """
        if not text or len(text.strip()) == 0:
            return []

        # Use a sentence-aware approach to chunking to avoid breaking sentences
        sentences = self._split_into_sentences(text)
        chunks = []
        current_chunk = ""
        current_size = 0

        for sentence in sentences:
            sentence_size = len(sentence)

            # If adding this sentence would exceed the chunk size
            if current_size + sentence_size > self.max_chunk_size and current_chunk:
                # Save the current chunk
                chunks.append({
                    "text": current_chunk.strip(),
                    "metadata": metadata or {},
                    "size": len(current_chunk)
                })

                # Start a new chunk with overlap
                if self.chunk_overlap > 0:
                    # Find the part of the current chunk that should be included as overlap
                    overlap_text = self._get_overlap_text(current_chunk, self.chunk_overlap)
                    current_chunk = overlap_text + " " + sentence
                    current_size = len(current_chunk)
                else:
                    current_chunk = sentence
                    current_size = sentence_size
            else:
                # Add sentence to current chunk
                if current_chunk:
                    current_chunk += " " + sentence
                else:
                    current_chunk = sentence
                current_size += sentence_size + 1  # +1 for the space

        # Add the final chunk if it has content
        if current_chunk.strip():
            chunks.append({
                "text": current_chunk.strip(),
                "metadata": metadata or {},
                "size": len(current_chunk)
            })

        self.logger.debug(f"Split text of {len(text)} chars into {len(chunks)} chunks")
        return chunks

    def _split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences using regex pattern.

        Args:
            text: Text to split into sentences

        Returns:
            List of sentences
        """
        # Pattern to match sentence endings: . ! ? followed by whitespace or end of string
        # This pattern handles common abbreviations and decimal numbers correctly
        sentence_pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\!|\?)\s+'
        sentences = re.split(sentence_pattern, text)

        # Clean up sentences
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences

    def _get_overlap_text(self, text: str, overlap_size: int) -> str:
        """
        Get the ending portion of text that should be used for overlap.

        Args:
            text: The text to get overlap from
            overlap_size: The desired overlap size

        Returns:
            Overlapping text
        """
        if len(text) <= overlap_size:
            return text

        # Try to find a good breaking point (like a sentence or word boundary)
        overlap_text = text[-overlap_size:]

        # If the overlap starts mid-sentence, try to expand to a word boundary
        space_idx = overlap_text.find(' ')
        if space_idx != -1:
            overlap_text = overlap_text[space_idx + 1:]

        return overlap_text

    def chunk_multiple_texts(self, texts: List[Dict[str, str]], metadata_list: List[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Chunk multiple texts with optional corresponding metadata.

        Args:
            texts: List of dictionaries with 'text' and optional 'metadata' keys
            metadata_list: Optional list of metadata to use if not provided in texts

        Returns:
            List of chunk dictionaries
        """
        all_chunks = []

        for i, item in enumerate(texts):
            text_content = item.get('content', item.get('text', ''))
            item_metadata = item.get('metadata', metadata_list[i] if metadata_list and i < len(metadata_list) else {})

            try:
                chunks = self.chunk_text(text_content, item_metadata)
                all_chunks.extend(chunks)
                self.logger.debug(f"Processed text {i+1}/{len(texts)} into {len(chunks)} chunks")
            except Exception as e:
                self.logger.error(f"Error chunking text {i+1}: {str(e)}")
                continue

        return all_chunks

    def validate_chunk_parameters(self) -> bool:
        """
        Validate that chunk parameters are reasonable.

        Returns:
            True if parameters are valid, False otherwise
        """
        if self.max_chunk_size <= 0:
            self.logger.error(f"Invalid chunk size: {self.max_chunk_size}")
            return False

        if self.chunk_overlap < 0:
            self.logger.error(f"Invalid chunk overlap: {self.chunk_overlap}")
            return False

        if self.chunk_overlap >= self.max_chunk_size:
            self.logger.error(f"Chunk overlap ({self.chunk_overlap}) must be less than chunk size ({self.max_chunk_size})")
            return False

        return True

    def get_stats(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get statistics about a list of chunks.

        Args:
            chunks: List of chunk dictionaries

        Returns:
            Dictionary with statistics
        """
        if not chunks:
            return {
                "total_chunks": 0,
                "total_chars": 0,
                "avg_chunk_size": 0,
                "min_chunk_size": 0,
                "max_chunk_size": 0
            }

        sizes = [chunk.get('size', len(chunk.get('text', ''))) for chunk in chunks]
        return {
            "total_chunks": len(chunks),
            "total_chars": sum(sizes),
            "avg_chunk_size": sum(sizes) / len(sizes),
            "min_chunk_size": min(sizes),
            "max_chunk_size": max(sizes)
        }


# Global instance for use throughout the application
text_chunker = TextChunker()