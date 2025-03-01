#!/usr/bin/env python
import sys
import warnings
import argparse
from datetime import datetime

from dataset_crew.crew import DatasetCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Run the DatasetCrew to collect language-specific text data."
    )
    parser.add_argument(
        "--language",
        type=str,
        default="English",
        help="Target language for text collection",
    )
    parser.add_argument(
        "--domain",
        type=str,
        default=None,
        help="Optional domain to focus on (e.g., government, business)",
    )
    return parser.parse_args()


def run():
    """
    Run the crew.
    """
    args = parse_args()

    inputs = {
        "language": args.language,
        "domain": args.domain if args.domain else "general",
        "current_year": str(datetime.now().year),
    }

    print(f"Starting DatasetCrew to collect {inputs['language']} text data")
    if inputs["domain"] != "general":
        print(f"Focusing on domain: {inputs['domain']}")

    try:
        result = DatasetCrew().crew().kickoff(inputs=inputs)
        print(
            f"DatasetCrew completed successfully. Output saved to {inputs['language']}_dataset.csv"
        )
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    args = parse_args()

    inputs = {
        "language": args.language,
        "domain": args.domain if args.domain else "general",
    }

    try:
        DatasetCrew().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        DatasetCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    args = parse_args()

    inputs = {
        "language": args.language,
        "domain": args.domain if args.domain else "general",
    }

    try:
        DatasetCrew().crew().test(
            n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


if __name__ == "__main__":
    run()
