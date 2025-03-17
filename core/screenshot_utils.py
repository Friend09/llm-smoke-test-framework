from PIL import Image
import io
import os
import logging

logger = logging.getLogger(__name__)

def optimize_screenshot(screenshot_path, max_dimension=1280, quality=75):
    """
    Optimize screenshot by resizing and compressing it.
    
    Args:
        screenshot_path (str): Path to the original screenshot
        max_dimension (int): Maximum dimension (width or height) in pixels
        quality (int): JPEG compression quality (1-100)
        
    Returns:
        str: Base64 encoded optimized image
    """
    if not os.path.exists(screenshot_path):
        logger.error(f"Screenshot file not found: {screenshot_path}")
        return None
        
    try:
        # Get original file size for logging
        original_size = os.path.getsize(screenshot_path)
        
        # Open and optimize image
        img = Image.open(screenshot_path)
        
        # Get original dimensions
        original_width, original_height = img.size
        
        # Resize if needed
        if original_width > max_dimension or original_height > max_dimension:
            if original_width > original_height:
                new_width = max_dimension
                new_height = int((max_dimension / original_width) * original_height)
            else:
                new_height = max_dimension
                new_width = int((max_dimension / original_height) * original_width)
            
            img = img.resize((new_width, new_height), Image.LANCZOS)
            logger.info(f"Resized image from {original_width}x{original_height} to {new_width}x{new_height}")
        else:
            logger.info(f"Image dimensions are already optimal: {original_width}x{original_height}")
            
        # Compress image
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=quality)
        buffer.seek(0)
        compressed_data = buffer.read()
        
        # Log compression stats
        compressed_size = len(compressed_data)
        compression_ratio = original_size / compressed_size if compressed_size > 0 else 0
        logger.info(f"Compressed image from {original_size/1024:.1f}KB to {compressed_size/1024:.1f}KB (ratio: {compression_ratio:.1f}x)")
        
        # Base64 encode
        import base64
        return base64.b64encode(compressed_data).decode(), "jpeg"
        
    except Exception as e:
        logger.error(f"Error optimizing screenshot: {str(e)}", exc_info=True)
        
        # Fallback to original image if optimization fails
        try:
            with open(screenshot_path, "rb") as f:
                import base64
                return base64.b64encode(f.read()).decode(), "png"
        except Exception as fallback_error:
            logger.error(f"Fallback to original image failed: {str(fallback_error)}")
            return None, None
