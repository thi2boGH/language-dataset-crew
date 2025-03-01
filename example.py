#!/usr/bin/env python
"""
Example script to run the Language Dataset Collection Crew.
"""
import os
import argparse
from dotenv import load_dotenv
from dataset_crew.main import run


def main():
    """
    Run the Language Dataset Collection Crew with command line arguments.
    """
    # Load environment variables from .env file
    load_dotenv()

    # Check if API keys are set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY is not set in the .env file.")
        return

    if not os.getenv("SERPER_API_KEY"):
        print("Error: SERPER_API_KEY is not set in the .env file.")
        return

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Run the Language Dataset Collection Crew."
    )
    parser.add_argument(
        "--language",
        type=str,
        default="English",
        help="Target language for text collection (e.g., French, German, Spanish)",
    )
    parser.add_argument(
        "--domain",
        type=str,
        default=None,
        help="Optional domain to focus on (e.g., government, business, technical)",
    )

    args = parser.parse_args()

    print(f"Starting Language Dataset Collection Crew")
    print(f"Language: {args.language}")
    if args.domain:
        print(f"Domain: {args.domain}")

    # Run the crew
    result = run()

    print(
        f"Dataset collection complete. Check the {args.language}_dataset.csv file for results."
    )


if __name__ == "__main__":
    main()
