#!/usr/bin/env python3
"""
Main ingestion script that orchestrates the entire RAG data pipeline:
1. Reads markdown files from book-site/docs
2. Converts markdown to clean plain text
3. Chunks documents with overlap
4. Generates embeddings using Google Gemini
5. Stores chunks in Qdrant vector database
"""

import time
import sys
from typing import List, Dict, Any
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# Add the backend directory to the path so imports work
sys.path.append(str(Path(__file__).parent))

from config.settings import settings
from data_ingestion.markdown_reader import markdown_reader
from data_ingestion.text_converter import text_converter
from data_ingestion.chunker import text_chunker
from data_ingestion.embedding_service import embedding_service
from data_ingestion.qdrant_client import qdrant_client
from data_ingestion.models import DocumentChunk
from utils import LoggerSetup, ProcessingError, log_info, log_error
import logging


def main():
    """
    Main ingestion pipeline function that orchestrates all components.
    """
    start_time = time.time()
    logger = LoggerSetup.setup_logging("ingest_pipeline")

    logger.info("Starting RAG data ingestion pipeline...")
    logger.info(f"Configuration: Max chunk size={settings.MAX_CHUNK_SIZE}, Overlap={settings.CHUNK_OVERLAP}")

    try:
        # Step 1: Read all markdown files
        logger.info("Step 1: Reading markdown files...")
        files_data = markdown_reader.read_all_markdown_files()
        logger.info(f"Read {len(files_data)} markdown files")

        if not files_data:
            logger.warning("No markdown files found to process")
            return

        # Step 2: Convert markdown to clean text
        logger.info("Step 2: Converting markdown to clean text...")
        processed_docs = []

        for i, file_data in enumerate(files_data):
            try:
                clean_text = text_converter.preserve_code_blocks(file_data['content'])

                doc_info = {
                    'text': clean_text,
                    'metadata': file_data['metadata'],
                    'original_file_data': file_data
                }
                processed_docs.append(doc_info)

                logger.debug(f"Processed file {i+1}/{len(files_data)}: {file_data['metadata']['source_file']}")
            except Exception as e:
                logger.error(f"Error converting file {file_data['metadata']['source_file']}: {str(e)}")
                continue  # Continue with other files

        logger.info(f"Converted {len(processed_docs)} files to clean text")

        # Step 3: Chunk documents
        logger.info("Step 3: Chunking documents...")
        all_chunks = []

        for doc in processed_docs:
            try:
                chunks = text_chunker.chunk_text(doc['text'], doc['metadata'])
                all_chunks.extend(chunks)
                logger.debug(f"Chunked document '{doc['metadata']['source_file']}' into {len(chunks)} chunks")
            except Exception as e:
                logger.error(f"Error chunking document '{doc['metadata']['source_file']}': {str(e)}")
                continue  # Continue with other documents

        logger.info(f"Created {len(all_chunks)} total chunks")

        if not all_chunks:
            logger.warning("No chunks were created, stopping pipeline")
            return

        # Step 4: Generate embeddings
        logger.info("Step 4: Generating embeddings...")
        texts_for_embedding = [chunk['text'] for chunk in all_chunks]

        # Generate embeddings in batches to respect API limits
        embeddings = embedding_service.generate_embeddings_batch(texts_for_embedding)
        logger.info(f"Generated {len(embeddings)} embeddings")

        # Associate embeddings with chunks
        for i, chunk in enumerate(all_chunks):
            if i < len(embeddings):
                chunk['embedding'] = embeddings[i]
            else:
                logger.error(f"No embedding generated for chunk {i}")
                # Skip this chunk if no embedding was generated
                continue

        # Filter out chunks without embeddings
        all_chunks = [chunk for chunk in all_chunks if 'embedding' in chunk]
        logger.info(f"Chunks with embeddings: {len(all_chunks)}")

        # Step 5: Store in Qdrant
        logger.info("Step 5: Storing chunks in Qdrant...")
        success = qdrant_client.batch_upload_chunks(all_chunks)

        if success:
            logger.info("Successfully completed ingestion pipeline!")
        else:
            logger.warning("Ingestion pipeline completed with some failures")

        # Verification step
        final_count = qdrant_client.count_chunks()
        logger.info(f"Total chunks stored in Qdrant: {final_count}")

        # Calculate and report processing time
        end_time = time.time()
        processing_time = end_time - start_time
        logger.info(f"Pipeline completed in {processing_time:.2f} seconds")

        # Create result summary
        result = {
            "success": success,
            "processed_files": len(files_data),
            "total_chunks": len(all_chunks),
            "chunks_in_qdrant": final_count,
            "processing_time": processing_time
        }

        logger.info(f"Result summary: {result}")
        return result

    except ProcessingError as e:
        log_error(e, "ingestion_pipeline")
        logger.error(f"Ingestion pipeline failed: {str(e)}")
        raise
    except Exception as e:
        log_error(e, "ingestion_pipeline")
        logger.error(f"Unexpected error in ingestion pipeline: {str(e)}")
        raise


def validate_environment():
    """
    Validate that all required environment variables and configurations are set.
    """
    logger = LoggerSetup.setup_logging("env_validation")

    errors = []

    # Check API keys
    if not settings.GEMINI_API_KEY:
        errors.append("GEMINI_API_KEY not set in environment")

    if not settings.QDRANT_API_KEY:
        errors.append("QDRANT_API_KEY not set in environment")

    if not settings.QDRANT_URL:
        errors.append("QDRANT_URL not set in environment")

    # Check docs directory exists - handle relative paths properly
    docs_path = Path(settings.DOCS_DIR)

    # If the path is relative and doesn't exist from current directory,
    # try to resolve it relative to the project root
    if not docs_path.exists() and not docs_path.is_absolute():
        # Try to find the docs directory relative to the project root
        project_root = Path(__file__).parent.parent  # Go up two levels from backend/
        full_docs_path = project_root / settings.DOCS_DIR

        if full_docs_path.exists():
            # Update the setting to use the absolute path
            import config.settings
            config.settings.settings.DOCS_DIR = str(full_docs_path.absolute())
        else:
            errors.append(f"Docs directory does not exist: {settings.DOCS_DIR}")
    elif not docs_path.exists():
        errors.append(f"Docs directory does not exist: {settings.DOCS_DIR}")

    if errors:
        for error in errors:
            logger.error(error)
        raise ProcessingError(
            f"Environment validation failed: {'; '.join(errors)}",
            error_code="ENV_VALIDATION_ERROR"
        )

    logger.info("Environment validation passed")
    return True


if __name__ == "__main__":
    try:
        # Validate environment first
        validate_environment()

        # Run the main ingestion pipeline
        result = main()

        # Exit with appropriate code
        if result and result.get("success", False):
            print("\n[SUCCESS] Ingestion pipeline completed successfully!")
            sys.exit(0)
        else:
            print("\n[WARNING] Ingestion pipeline completed with issues")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n[INTERRUPTED] Ingestion pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Ingestion pipeline failed: {str(e)}")
        sys.exit(1)