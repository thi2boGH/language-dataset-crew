# Language Dataset Collection Crew

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.102.0-green.svg)](https://crewai.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A CrewAI-powered tool to collect language-specific text data for training language models.

## Overview

This project uses CrewAI to create a crew of AI agents that work together to collect high-quality text data in various languages. The crew consists of:

1. **Project Manager**: Coordinates the collection effort and defines quality criteria
2. **Researcher**: Finds diverse and high-quality text sources on the web
3. **Text Extractor**: Extracts and cleans text from the sources for inclusion in the dataset

## Features

- Collect text data in any language
- Focus on specific domains (government, business, technical, etc.)
- Extract text from various web sources including PDFs
- Automatic PDF page limiting (first 10 pages) to handle large documents
- Clean and format text for language model training
- Save data to CSV files with appropriate metadata

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/language-dataset-crew.git
cd language-dataset-crew

# Install the package
pip install -e .
```

## Configuration

Create a `.env` file in the root directory with your API keys:

```
MODEL=gpt-4o-mini  # or another OpenAI model
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
```

You can copy the `.env.example` file and fill in your API keys.

## Usage

Run the crew using the CrewAI CLI:

```bash
# Collect English text data
crewai run --crew dataset_crew.crew:DatasetCrew --language English

# Collect French text data with a focus on government documents
crewai run --crew dataset_crew.crew:DatasetCrew --language French --domain government
```

The collected data will be saved to the `output` directory in CSV format:
- `output/english_dataset.csv`
- `output/french_dataset.csv`
- etc.

## Tools

The crew uses several powerful tools to collect and process text data:

### Search Tools
- **SerperDevTool**: Used to search the web for relevant content
- **WebsiteSearchTool**: Specialized tool for searching within specific websites

### Content Extraction Tools
- **ScrapeWebsiteTool**: Extracts content from web pages with high accuracy
- **PDFSearchTool**: Specialized tool for extracting and searching text in PDF documents
- **PDFReaderTool**: Custom tool for PDF text extraction that automatically limits extraction to the first 10 pages of large PDFs

### Data Management Tools
- **DatasetTool**: Custom tool for managing the dataset CSV files
- **FileReadTool**: Reads and processes various file formats
- **DirectoryReadTool**: Manages directory structures and file organization

## Troubleshooting

### Common Issues

1. **PDF Text Extraction**: If you encounter issues with PDF text extraction, try using the PDFSearchTool first, which is more robust. The custom PDFReaderTool is available as a fallback and will automatically limit extraction to the first 10 pages for large PDFs.

2. **Dataset Tool Path Issues**: If you encounter issues with the Dataset Management Tool, make sure you're using a valid file path. The tool now automatically normalizes file paths and uses default values when needed.

3. **Missing Dependencies**: If you get import errors, make sure you've installed all the required dependencies with `pip install -e .`

## Advanced Usage

CrewAI provides additional CLI commands for working with your crew:

```bash
# Train your crew (useful for fine-tuning)
crewai train --crew dataset_crew.crew:DatasetCrew --n-iterations 5 --filename training_results.json --language Spanish

# Replay a specific task execution
crewai replay --crew dataset_crew.crew:DatasetCrew --task-id extraction_task

# Test your crew with different models
crewai test --crew dataset_crew.crew:DatasetCrew --n-iterations 3 --model gpt-4o --language German
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [CrewAI](https://crewai.com) for the multi-agent framework
- [Serper.dev](https://serper.dev) for web search capabilities
- [OpenAI](https://openai.com) for the language models

## 📧 Contact

For questions or feedback, please open an issue on this repository.
