import re
from typing import List
from bs4 import BeautifulSoup
from utils import LoggerSetup, ProcessingError
import logging


class MarkdownToTextConverter:
    """
    Class for converting markdown content to clean plain text.
    """

    def __init__(self):
        self.logger = LoggerSetup.setup_logging("text_converter")

    def convert_markdown_to_text(self, markdown_content: str) -> str:
        """
        Convert markdown content to clean plain text.

        Args:
            markdown_content: Raw markdown content to convert

        Returns:
            Clean plain text with formatting removed
        """
        try:
            # First, handle common markdown patterns with regex
            text = self._remove_markdown_headers(markdown_content)
            text = self._remove_markdown_links_and_images(text)
            text = self._remove_markdown_formatting(text)
            text = self._remove_markdown_code_blocks(text)
            text = self._remove_markdown_lists(text)
            text = self._remove_extra_whitespace(text)

            # Use BeautifulSoup to handle any remaining HTML that might be in the markdown
            soup = BeautifulSoup(text, 'html.parser')
            clean_text = soup.get_text(separator=' ', strip=True)

            self.logger.debug(f"Converted markdown to text: {len(markdown_content)} chars -> {len(clean_text)} chars")
            return clean_text

        except Exception as e:
            self.logger.error(f"Error converting markdown to text: {str(e)}")
            raise ProcessingError(
                f"Failed to convert markdown to text: {str(e)}",
                error_code="TEXT_CONVERSION_ERROR",
                original_error=e
            )

    def _remove_markdown_headers(self, text: str) -> str:
        """Remove markdown headers (lines starting with #)."""
        # Remove ATX headers (e.g., # Header, ## Header, etc.)
        text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
        # Remove Setext headers (underlined headers)
        text = re.sub(r'\n[=\-]{2,}\s*\n', '\n', text)
        return text

    def _remove_markdown_links_and_images(self, text: str) -> str:
        """Remove markdown links and images."""
        # Remove links: [text](url) or [text][id] or [id]
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        # Remove reference-style links: [text][id]
        text = re.sub(r'\[([^\]]+)\]\[[^\]]*\]', r'\1', text)
        # Remove images: ![alt text](url)
        text = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'\1', text)
        return text

    def _remove_markdown_formatting(self, text: str) -> str:
        """Remove bold, italic, and other inline formatting."""
        # Remove bold: **text** or __text__
        text = re.sub(r'\*{2}([^*]+)\*{2}', r'\1', text)
        text = re.sub(r'_{2}([^_]+)_{2}', r'\1', text)
        # Remove italic: *text* or _text_
        text = re.sub(r'(?<!\*)\*([^\*]+)\*(?!\*)', r'\1', text)
        text = re.sub(r'(?<!_)_([^_]+)_(?!_)', r'\1', text)
        # Remove code: `text`
        text = re.sub(r'`([^`]+)`', r'\1', text)
        # Remove strikethrough: ~~text~~
        text = re.sub(r'~{2}([^~]+)~{2}', r'\1', text)
        return text

    def _remove_markdown_code_blocks(self, text: str) -> str:
        """Remove markdown code blocks."""
        # Remove fenced code blocks: ```language\ncontent\n```
        text = re.sub(r'```.*?\n(.*?)```', r'\1', text, flags=re.DOTALL)
        # Remove indented code blocks (4 spaces or 1 tab)
        text = re.sub(r'^(\s{4}|\t).*$', '', text, flags=re.MULTILINE)
        return text

    def _remove_markdown_lists(self, text: str) -> str:
        """Remove markdown list items."""
        # Remove unordered list items: - item, * item, + item
        text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)
        # Remove ordered list items: 1. item, 2. item, etc.
        text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
        return text

    def _remove_extra_whitespace(self, text: str) -> str:
        """Remove extra whitespace and normalize line breaks."""
        # Replace multiple newlines with single newlines
        text = re.sub(r'\n\s*\n', '\n\n', text)
        # Replace multiple spaces with single spaces
        text = re.sub(r' +', ' ', text)
        # Remove leading/trailing whitespace
        text = text.strip()
        return text

    def convert_multiple_markdown(self, markdown_contents: List[str]) -> List[str]:
        """
        Convert multiple markdown contents to clean plain text.

        Args:
            markdown_contents: List of markdown contents to convert

        Returns:
            List of clean plain texts
        """
        converted_texts = []
        for i, content in enumerate(markdown_contents):
            try:
                converted = self.convert_markdown_to_text(content)
                converted_texts.append(converted)
                self.logger.debug(f"Converted markdown {i+1}/{len(markdown_contents)}")
            except Exception as e:
                self.logger.error(f"Error converting markdown {i+1}: {str(e)}")
                # Add empty string as fallback
                converted_texts.append("")
                continue

        return converted_texts

    def preserve_code_blocks(self, markdown_content: str) -> str:
        """
        Convert markdown to text while preserving code blocks.

        Args:
            markdown_content: Raw markdown content

        Returns:
            Plain text with code blocks preserved
        """
        # Extract code blocks and store them temporarily
        code_blocks = []
        def replace_code_block(match):
            code_blocks.append(match.group(0))
            return f" [CODE_BLOCK_{len(code_blocks)-1}] "

        # Find and replace fenced code blocks
        text = re.sub(r'```.*?\n(.*?)```', replace_code_block, markdown_content, flags=re.DOTALL)
        # Find and replace inline code
        text = re.sub(r'`(.*?)`', replace_code_block, text)

        # Convert the remaining markdown to text
        converted_text = self.convert_markdown_to_text(text)

        # Restore code blocks
        for i, code_block in enumerate(code_blocks):
            # Extract just the content from the code block
            content_match = re.search(r'```.*?\n(.*?)```', code_block, flags=re.DOTALL)
            if content_match:
                content = content_match.group(1).strip()
            else:
                # For inline code, extract content between backticks
                content_match = re.search(r'`(.*?)`', code_block)
                content = content_match.group(1) if content_match else code_block

            converted_text = converted_text.replace(f"[CODE_BLOCK_{i}]", content)

        return converted_text


# Global instance for use throughout the application
text_converter = MarkdownToTextConverter()