#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Sitemap file path from the reference project
DEFAULT_SITEMAP_FILE="$SCRIPT_DIR/ref_sitemap_generator/data/crawled_urls.txt"

# Parse command line arguments
SITEMAP_FILE=${1:-$DEFAULT_SITEMAP_FILE}
BASE_URL=${2:-""}
OUTPUT_DIR=${3:-"output/sitemap_tests_$(date +%Y%m%d_%H%M%S)"}
FRAMEWORK=${4:-"cucumber"}
LANGUAGE=${5:-"java"}
USE_VISION=${6:-"false"}
MAX_PAGES=${7:-"10"}  # Default to 10 pages to avoid long processing time

echo "Running tests with sitemap file: $SITEMAP_FILE"
echo "Base URL filter: $BASE_URL"
echo "Output directory: $OUTPUT_DIR"
echo "Test framework: $FRAMEWORK"
echo "Programming language: $LANGUAGE"
echo "Use vision: $USE_VISION"
echo "Max pages: $MAX_PAGES"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Filter sitemap if base_url is provided
if [ -n "$BASE_URL" ]; then
    FILTERED_SITEMAP="$OUTPUT_DIR/filtered_sitemap.txt"
    echo "Filtering sitemap for URLs containing $BASE_URL..."
    grep "$BASE_URL" "$SITEMAP_FILE" > "$FILTERED_SITEMAP"
    SITEMAP_FILE="$FILTERED_SITEMAP"
fi

# Limit number of URLs if needed
if [ -n "$MAX_PAGES" ]; then
    LIMITED_SITEMAP="$OUTPUT_DIR/limited_sitemap.txt"
    echo "Limiting sitemap to $MAX_PAGES URLs..."
    head -n "$MAX_PAGES" "$SITEMAP_FILE" > "$LIMITED_SITEMAP"
    SITEMAP_FILE="$LIMITED_SITEMAP"
fi

# Run the appropriate command
if [ "$USE_VISION" = "true" ]; then
    python "$SCRIPT_DIR/run.py" vision-e2e --sitemap-file "$SITEMAP_FILE" \
        -o "$OUTPUT_DIR" -f "$FRAMEWORK" -l "$LANGUAGE"
else
    python "$SCRIPT_DIR/run.py" e2e --sitemap-file "$SITEMAP_FILE" \
        -o "$OUTPUT_DIR" -f "$FRAMEWORK" -l "$LANGUAGE"
fi

echo "Test generation complete. Results saved to $OUTPUT_DIR"
