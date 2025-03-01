# Language Dataset Collection Crew - Example Usage

This example demonstrates how to use the Language Dataset Collection Crew to gather language-specific text data for training language models.

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

To run the example, use the CrewAI CLI:

```bash
crewai run --crew dataset_crew.crew:DatasetCrew --language French --domain business
```

### Command Line Arguments

- `--language`: The target language for text collection (default: "English")
- `--domain`: Optional domain to focus on, e.g., "government", "business", "technical" (default: None)

## What Happens

When you run the crew:

1. The Project Manager agent creates a detailed plan for collecting text data in your target language.
2. The Researcher agent finds diverse and high-quality sources of text in your target language using Serper.dev.
3. The Text Extractor agent extracts clean, well-formatted text from the sources and saves it to a CSV file.

## Output

The crew will generate a CSV file in the `output` directory named `{language}_dataset.csv` containing the extracted text data with the following columns:

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

# Example: Collecting Government Documents in English

This example demonstrates how to use the Language Dataset Collection Crew to collect English text data from government documents.

## Running the Example

```bash
crewai run --crew dataset_crew.crew:DatasetCrew --language English --domain government
```

## What Happens

1. The Project Manager agent creates a plan for collecting English government documents.
2. The Researcher agent finds relevant sources of English government documents.
3. The Text Extractor agent extracts and cleans text from these sources.

## Example Agent Interactions

### Project Manager

```
I'll create a detailed plan for collecting English government documents for our dataset.

Quality Criteria:
1. Text should be from official government sources (federal, state, local)
2. Content should be formal, well-structured, and representative of official communication
3. Documents should be recent (preferably from the last 2-3 years)
4. Text should be substantial (at least 500 words per document)
5. Content should cover diverse government functions (legislation, reports, announcements)

Researcher Guidelines:
- Focus on .gov domains and official government websites
- Prioritize reports, press releases, and policy documents
- Look for content from different government agencies
- Ensure documents are publicly accessible

Text Extractor Guidelines:
- Remove headers, footers, and navigation elements
- Preserve paragraph structure and formatting
- Include metadata about the source agency/department
- For PDFs, use the PDF Reader Tool to extract text content
```

### Researcher

```
I've found the following sources of English government documents:

1. URL: https://www.whitehouse.gov/briefing-room/statements-releases/
   Description: White House press releases and statements
   Value: Official communications from the executive branch
   Estimated text: 100+ documents, 500-1000 words each

2. URL: https://www.gao.gov/reports-testimonies
   Description: Government Accountability Office reports
   Value: Detailed analysis of government programs and spending
   Estimated text: 50+ reports, 5000+ words each

3. URL: https://www.congress.gov/congressional-record
   Description: Congressional Record transcripts
   Value: Verbatim record of congressional proceedings
   Estimated text: Daily records, thousands of words each

4. URL: https://www.gao.gov/assets/gao-25-106856.pdf
   Description: PDF report on Defense Innovation Unit
   Value: Detailed government report in PDF format
   Estimated text: 30+ pages of text
```

### Text Extractor

```
I've extracted text from the government sources. For the PDF document, I used the PDF Reader Tool:

Action: PDF Reader Tool
Input: {"pdf_url": "https://www.gao.gov/assets/gao-25-106856.pdf", "max_pages": 5}
Output: 
--- Page 1 ---
Defense Innovation Unit: Actions Needed to Assess Progress and Further Enhance Collaboration
[...extracted text content...]

--- Page 2 ---
[...more extracted text content...]

I've cleaned and formatted the text, removing headers and footers, and saved it to the dataset with appropriate metadata.

The extracted data has been saved to: output/english_dataset.csv
```

## Output

The resulting dataset is saved to `output/english_dataset.csv` with the following structure:

| text                                                         | source_url                                                                  | date_extracted | domain     | language |
| ------------------------------------------------------------ | --------------------------------------------------------------------------- | -------------- | ---------- | -------- |
| The Defense Innovation Unit (DIU) plays a crucial role in... | https://www.gao.gov/assets/gao-25-106856.pdf                                | 2023-03-01     | government | English  |
| President Biden announced today that...                      | https://www.whitehouse.gov/briefing-room/statements-releases/2023/03/01/... | 2023-03-01     | government | English  |
| ...                                                          | ...                                                                         | ...            | ...        | ...      |