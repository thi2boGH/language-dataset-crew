# Language Dataset Collection Crew

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.102.0-green.svg)](https://crewai.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A CrewAI-powered tool to collect high-quality text data in specific languages for training glirel models or other NLP applications.

## 🌟 Features

- **Multi-language Support**: Collect text data in any language
- **Domain Specific**: Optionally focus on specific domains (business, government, technical, etc.)
- **Intelligent Extraction**: Uses LLMs to extract clean, relevant text from web sources
- **Structured Output**: Saves data to CSV with metadata for easy processing

## 🤖 How It Works

This crew helps you gather language-specific text data from the web through three specialized AI agents:

1. **Planning**: The Project Manager agent creates a detailed plan for collecting text data in your target language, defining quality criteria and guidelines.
2. **Research**: The Researcher agent finds diverse and high-quality sources of text in your target language using Serper.dev, optionally focusing on a specific domain.
3. **Extraction**: The Text Extractor agent extracts clean, well-formatted text from the sources and saves it to a CSV file with metadata.

The resulting dataset can be used to train language-specific glirel models or other NLP applications.

## 🛠️ Installation

### Prerequisites

- Python 3.10 or higher
- API keys for OpenAI and Serper.dev

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/language-dataset-crew.git
   cd language-dataset-crew
   ```

2. Install the package:
   ```bash
   pip install -e .
   ```

3. Create a `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   SERPER_API_KEY=your_serper_api_key_here
   ```

## 🚀 Usage

Run the crew with the following command:

```bash
crewai run --language French --domain business
```

### Command Line Arguments

- `--language`: The target language for text collection (default: "English")
- `--domain`: Optional domain to focus on, e.g., "government", "business", "technical" (default: None)

## 📊 Output

The crew will generate a CSV file named `{language}_dataset.csv` containing the extracted text data with the following columns:

1. `text`: The extracted text content
2. `source_url`: The URL where the text was found
3. `date_extracted`: The date when the text was extracted
4. `domain`: The domain or category of the text
5. `language`: The language of the text

## 📝 Example

See the [EXAMPLE_README.md](EXAMPLE_README.md) for a detailed example of how to use this tool.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [CrewAI](https://crewai.com) for the multi-agent framework
- [Serper.dev](https://serper.dev) for web search capabilities
- [OpenAI](https://openai.com) for the language models

## 📧 Contact

For questions or feedback, please open an issue on this repository.
