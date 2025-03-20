import os
import logging
import base64
from PIL import Image
import io

logger = logging.getLogger(__name__)

def optimize_screenshot(
    screenshot_path,
    max_dimension=1280,
    quality=75,
    format="JPEG"
):
    """
    Optimize a screenshot for API usage by:
    1. Resizing to stay within max_dimension while preserving aspect ratio
    2. Converting to specified format with quality setting
    3. Returning as base64 string

    Args:
        screenshot_path (str): Path to the screenshot file
        max_dimension (int): Maximum width/height in pixels
        quality (int): JPEG quality (1-100)
        format (str): Image format (JPEG, PNG)

    Returns:
        tuple: (base64_string, format_name)
    """
    try:
        if not os.path.exists(screenshot_path):
            logger.error(f"Screenshot file not found: {screenshot_path}")
            return None, None

        # Open the image
        with Image.open(screenshot_path) as img:
            # Check if resizing is needed
            width, height = img.size
            should_resize = width > max_dimension or height > max_dimension

            if should_resize:
                # Calculate new dimensions while preserving aspect ratio
                if width > height:
                    new_width = max_dimension
                    new_height = int(height * (max_dimension / width))
                else:
                    new_height = max_dimension
                    new_width = int(width * (max_dimension / height))

                # Resize the image
                img = img.resize((new_width, new_height), Image.LANCZOS)
                logger.info(f"Resized image from {width}x{height} to {new_width}x{new_height}")

            # Convert to desired format in memory
            buffer = io.BytesIO()
            img.save(buffer, format=format, optimize=True, quality=quality)
            buffer.seek(0)

            # Get base64 string
            base64_string = base64.b64encode(buffer.read()).decode('utf-8')
            format_lower = format.lower()

            logger.info(f"Optimized image: format={format}, quality={quality}, size={len(base64_string) // 1024}KB")

            return base64_string, format_lower

    except Exception as e:
        logger.error(f"Error optimizing screenshot {screenshot_path}: {str(e)}", exc_info=True)
        return None, None
