# Vision Analysis

Vision analysis is a powerful feature of the LLM Smoke Test Framework that utilizes AI vision capabilities to better understand web pages and generate more accurate tests.

## Overview

Traditional web testing frameworks rely solely on DOM structure to identify elements and generate tests. The LLM Smoke Test Framework goes beyond this by incorporating visual analysis of web pages using OpenAI's vision-enabled models like GPT-4o-mini.

## Benefits of Vision Analysis

- **Visual Element Detection**: Identifies elements that might be difficult to locate through DOM alone
- **Layout Understanding**: Understands the visual layout and importance of elements
- **Context Awareness**: Recognizes visual groupings and relationships between elements
- **Improved Test Coverage**: Generates tests that consider visual aspects of the application
- **Better Element Identification**: Helps identify the purpose of elements based on their appearance

## How Vision Analysis Works

1. **Screenshot Capture**: The Web Crawler captures high-quality screenshots of the page
2. **Image Optimization**: Screenshots are optimized for the best balance of quality and size
3. **Vision Model Processing**: OpenAI's vision-capable models analyze the screenshots
4. **DOM Integration**: Vision analysis is combined with DOM analysis for comprehensive understanding
5. **Testing Insights**: The combined analysis informs test scenario generation

## Using Vision Analysis

Vision analysis is enabled by default in the `vision-e2e` command:

```bash
python run.py vision-e2e https://example.com/login
```

### Customizing Vision Analysis

You can customize vision analysis with several options:

```bash
python run.py vision-e2e https://example.com/login \
  --vision-quality high \
  --model gpt-4o
```

| Option             | Description                    | Values                          |
| ------------------ | ------------------------------ | ------------------------------- |
| `--vision-quality` | Quality of images for analysis | `low`, `medium`, `high`, `auto` |
| `--model`          | OpenAI model to use            | `gpt-4o-mini`, `gpt-4o`, etc.   |
| `--dom-only`       | Disable vision (DOM only)      | `True/False`                    |

## When to Use Vision Analysis

Vision analysis is particularly valuable for:

1. **Complex UIs**: Pages with complex visual layouts
2. **Image-Heavy Pages**: Pages where visual content is important
3. **Modern Web Apps**: Applications with dynamic, visually-driven interfaces
4. **Forms**: Pages with many input fields and controls
5. **E-commerce**: Product pages and checkout processes

## Example: Vision vs DOM-Only Analysis

### Form with Visually Grouped Fields

A shipping form might have address fields visually grouped but not clearly related in the DOM structure.

**DOM-Only Analysis:**

```
Found fields:
- input#address1 (text)
- input#address2 (text)
- input#city (text)
- input#state (select)
- input#zip (text)
```

**Vision Analysis:**

```
Found shipping address section containing:
- input#address1 (Street Address)
- input#address2 (Apt/Suite)
- Group of location fields:
  - input#city (City)
  - input#state (State)
  - input#zip (ZIP Code)
```

The vision analysis correctly identifies the logical groupings and labels of fields, even when they're not explicitly grouped in the DOM.

## Performance Considerations

Vision analysis requires more processing power and API resources than DOM-only analysis:

- **API Costs**: Vision API calls typically cost more than text-only calls
- **Processing Time**: Vision analysis takes longer to complete
- **Optimization**: Screenshot quality can be adjusted to balance performance

## Best Practices

1. **Use Appropriate Quality**: Match vision quality to your needs

   - `low`: For simple UIs or when minimizing API costs
   - `medium`: Default, good for most applications
   - `high`: For visually complex or detail-rich interfaces

2. **Combine with DOM Analysis**: Use both for the best results

3. **Selective Usage**: Use vision analysis where it adds the most value

   ```bash
   python run.py vision-e2e https://example.com --page-types form,checkout,product
   ```

4. **Test Without Vision First**: If you're unsure, try DOM-only first
   ```bash
   python run.py e2e https://example.com
   ```

## Technical Implementation

Behind the scenes, the vision analysis:

1. Prepares screenshots at the appropriate quality
2. Encodes images for the OpenAI API
3. Constructs prompts that include both images and DOM context
4. Processes the multi-modal API response
5. Extracts structured insights about the page

This allows the framework to "see" the page as a human would, leading to better test generation.
