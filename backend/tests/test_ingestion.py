import pytest
import os
from pathlib import Path
from config.settings import settings
from data_ingestion.markdown_reader import markdown_reader
from data_ingestion.text_converter import text_converter
from data_ingestion.chunker import text_chunker
from data_ingestion.embedding_service import embedding_service
from data_ingestion.qdrant_client import qdrant_client
from data_ingestion.models import DocumentChunk, DocumentMetadata


def test_settings_loaded():
    """Test that settings are properly loaded."""
    assert settings.MAX_CHUNK_SIZE > 0
    assert settings.CHUNK_OVERLAP >= 0
    assert settings.BATCH_SIZE > 0


def test_markdown_reader():
    """Test the markdown reader functionality."""
    # This test would require actual markdown files to exist
    # For now, just test that the instance exists and methods are callable
    assert markdown_reader is not None
    assert hasattr(markdown_reader, 'read_all_markdown_files')
    assert hasattr(markdown_reader, 'get_file_list')


def test_text_converter():
    """Test the text converter functionality."""
    converter = text_converter
    assert converter is not None

    # Test basic markdown to text conversion
    markdown_text = "# Header\n\nThis is **bold** and *italic* text.\n\n- Item 1\n- Item 2"
    plain_text = converter.convert_markdown_to_text(markdown_text)

    assert "Header" in plain_text
    assert "bold" in plain_text
    assert "italic" in plain_text
    assert "Item 1" in plain_text


def test_text_chunker():
    """Test the text chunker functionality."""
    chunker = text_chunker
    assert chunker is not None

    # Test chunking with a longer text
    long_text = "This is a sentence. " * 100  # Create a long text
    chunks = chunker.chunk_text(long_text, {"source": "test"})

    assert len(chunks) > 0
    assert all(len(chunk['text']) <= settings.MAX_CHUNK_SIZE for chunk in chunks)


def test_document_chunk_model():
    """Test the DocumentChunk model validation."""
    # Valid chunk
    valid_chunk = DocumentChunk(
        text="This is a test chunk",
        embedding=[0.1] * 768,
        metadata=DocumentMetadata(
            source_file="test.md",
            relative_path="test.md",
            full_path="/path/to/test.md"
        ),
        size=19
    )

    assert valid_chunk.text == "This is a test chunk"
    assert len(valid_chunk.embedding) == 768
    assert valid_chunk.metadata.source_file == "test.md"


def test_embedding_service():
    """Test that embedding service is configured (without actually calling the API)."""
    assert embedding_service is not None
    assert hasattr(embedding_service, 'get_model_info')

    model_info = embedding_service.get_model_info()
    assert model_info['model_name'] == 'models/text-embedding-3-small'
    assert model_info['vector_size'] == 768


def test_qdrant_client():
    """Test that Qdrant client is configured (without actually connecting)."""
    assert qdrant_client is not None
    assert hasattr(qdrant_client, 'get_model_info')