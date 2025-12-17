import os
import glob
from typing import List, Dict, Any, Optional
from pathlib import Path
from config.settings import settings
from utils import LoggerSetup, ProcessingError
import logging


class MarkdownReader:
    """
    Class for reading markdown files from the book-site/docs directory.
    """

    def __init__(self):
        self.logger = LoggerSetup.setup_logging("markdown_reader")
        self.docs_dir = Path(settings.DOCS_DIR)
        self.supported_extensions = ['.md', '.mdx']

    def read_all_markdown_files(self) -> List[Dict[str, Any]]:
        """
        Read all markdown files from the configured docs directory.

        Returns:
            List of dictionaries containing file content and metadata
        """
        files_data = []
        self.logger.info(f"Reading markdown files from: {self.docs_dir.absolute()}")

        if not self.docs_dir.exists():
            raise ProcessingError(
                f"Docs directory does not exist: {self.docs_dir.absolute()}",
                error_code="DOCS_DIR_NOT_FOUND"
            )

        # Find all markdown files recursively
        for ext in self.supported_extensions:
            pattern = f"**/*{ext}"
            markdown_files = list(self.docs_dir.glob(pattern))

            for file_path in markdown_files:
                try:
                    file_data = self._read_single_file(file_path)
                    files_data.append(file_data)
                    self.logger.debug(f"Successfully read file: {file_path}")
                except Exception as e:
                    self.logger.error(f"Error reading file {file_path}: {str(e)}")
                    # Continue processing other files even if one fails
                    continue

        self.logger.info(f"Successfully read {len(files_data)} markdown files")
        return files_data

    def _read_single_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Read a single markdown file and return its content with metadata.

        Args:
            file_path: Path to the markdown file

        Returns:
            Dictionary containing file content and metadata
        """
        try:
            # Read the file content
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Create metadata
            relative_path = file_path.relative_to(self.docs_dir)
            metadata = {
                "source_file": file_path.name,
                "relative_path": str(relative_path),
                "full_path": str(file_path.absolute()),
                "size": len(content)
            }

            return {
                "content": content,
                "metadata": metadata,
                "file_path": str(file_path)
            }

        except UnicodeDecodeError:
            raise ProcessingError(
                f"File {file_path} is not a valid UTF-8 text file",
                error_code="INVALID_ENCODING"
            )
        except PermissionError:
            raise ProcessingError(
                f"Permission denied reading file: {file_path}",
                error_code="PERMISSION_DENIED"
            )
        except Exception as e:
            raise ProcessingError(
                f"Error reading file {file_path}: {str(e)}",
                error_code="FILE_READ_ERROR",
                original_error=e
            )

    def get_file_list(self) -> List[str]:
        """
        Get a list of all markdown file paths without reading their content.

        Returns:
            List of file paths
        """
        file_paths = []

        if not self.docs_dir.exists():
            raise ProcessingError(
                f"Docs directory does not exist: {self.docs_dir.absolute()}",
                error_code="DOCS_DIR_NOT_FOUND"
            )

        for ext in self.supported_extensions:
            pattern = f"**/*{ext}"
            markdown_files = list(self.docs_dir.glob(pattern))
            file_paths.extend([str(path) for path in markdown_files])

        return file_paths

    def validate_file_access(self, file_path: str) -> bool:
        """
        Validate that a file can be accessed for reading.

        Args:
            file_path: Path to the file to validate

        Returns:
            True if file can be accessed, False otherwise
        """
        try:
            path = Path(file_path)
            if not path.exists():
                self.logger.warning(f"File does not exist: {file_path}")
                return False

            if not os.access(path, os.R_OK):
                self.logger.warning(f"No read permission for file: {file_path}")
                return False

            return True
        except Exception:
            return False


# Global instance for use throughout the application
markdown_reader = MarkdownReader()