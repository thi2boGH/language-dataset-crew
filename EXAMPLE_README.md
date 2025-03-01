# Language Dataset Collection Crew - Example Usage

This example demonstrates how to use the Language Dataset Collection Crew to gather language-specific text data for training glirel models.

## Prerequisites

Before running the example, make sure you have:

1. Set up your API keys in the `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   SERPER_API_KEY=your_serper_api_key_here
   ```

2. Installed the required dependencies:
   ```bash
   pip install -e .
   ```

## Running the Example

To run the example, use the following command:

```bash
python example.py --language French --domain business
```

### Command Line Arguments

- `--language`: The target language for text collection (default: "English")
- `--domain`: Optional domain to focus on, e.g., "government", "business", "technical" (default: None)

## What Happens

When you run the example:

1. The Project Manager agent creates a detailed plan for collecting text data in your target language.
2. The Researcher agent finds diverse and high-quality sources of text in your target language using Serper.dev.
3. The Text Extractor agent extracts clean, well-formatted text from the sources and saves it to a CSV file.

## Output

The crew will generate a CSV file named `{language}_dataset.csv` containing the extracted text data with the following columns:

1. `text`: The extracted text content
2. `source_url`: The URL where the text was found
3. `date_extracted`: The date when the text was extracted
4. `domain`: The domain or category of the text
5. `language`: The language of the text

## Troubleshooting

If you encounter any issues:

1. Make sure your API keys are correctly set in the `.env` file.
2. Check that you have installed all the required dependencies.
3. Ensure you have a stable internet connection for the web search to work properly.

For more detailed information, refer to the main README.md file. 