from crewai.tools import BaseTool
from typing import Type, Optional, List, Dict, Any
from pydantic import BaseModel, Field
import csv
import os
import json
import pandas as pd
from datetime import datetime


class DatasetToolInput(BaseModel):
    """Input schema for DatasetTool."""

    action: str = Field(
        ...,
        description="The action to perform: 'create', 'append', 'stats', or 'validate'.",
    )
    file_path: str = Field(..., description="The path to the CSV file.")
    data: Optional[List[Dict[str, Any]]] = Field(
        None, description="Data to append (for 'append' action)."
    )
    language: Optional[str] = Field(
        None, description="The language of the dataset (for 'create' action)."
    )


class DatasetTool(BaseTool):
    name: str = "Dataset Management Tool"
    description: str = (
        "Manage the text dataset CSV file. This tool can create a new dataset, "
        "append data to an existing dataset, get statistics about the dataset, "
        "or validate the dataset for quality issues."
    )
    args_schema: Type[BaseModel] = DatasetToolInput

    def _run(
        self,
        action: str,
        file_path: str,
        data: Optional[List[Dict[str, Any]]] = None,
        language: Optional[str] = None,
    ) -> str:
        """
        Manage the dataset CSV file.

        Args:
            action: The action to perform ('create', 'append', 'stats', or 'validate')
            file_path: The path to the CSV file
            data: Data to append (for 'append' action)
            language: The language of the dataset (for 'create' action)

        Returns:
            A JSON string containing the result of the operation
        """
        try:
            # Create output directory if it doesn't exist
            output_dir = os.path.join(os.getcwd(), "output")
            os.makedirs(output_dir, exist_ok=True)

            # Normalize and validate file path
            if not file_path or not file_path.endswith(".csv"):
                # Use a default file path based on language if provided
                if language:
                    file_name = f"{language.lower()}_dataset.csv"
                else:
                    file_name = "dataset.csv"
                file_path = os.path.join(output_dir, file_name)
            elif not os.path.isabs(file_path):
                # If it's a relative path but not in the output directory, put it there
                if not file_path.startswith(output_dir):
                    file_path = os.path.join(output_dir, os.path.basename(file_path))

            if action == "create":
                return self._create_dataset(file_path, language)
            elif action == "append":
                if data is None:
                    return json.dumps(
                        {
                            "error": "No data provided for 'append' action",
                            "action": action,
                            "file_path": file_path,
                        },
                        indent=2,
                    )
                return self._append_to_dataset(file_path, data)
            elif action == "stats":
                return self._get_dataset_stats(file_path)
            elif action == "validate":
                return self._validate_dataset(file_path)
            else:
                return json.dumps(
                    {
                        "error": f"Invalid action: {action}. Must be one of: 'create', 'append', 'stats', 'validate'."
                    },
                    indent=2,
                )
        except Exception as e:
            return json.dumps(
                {
                    "error": f"Dataset operation failed: {str(e)}",
                    "action": action,
                    "file_path": file_path,
                },
                indent=2,
            )

    def _create_dataset(self, file_path: str, language: Optional[str]) -> str:
        """Create a new dataset CSV file."""
        if os.path.exists(file_path):
            return json.dumps(
                {
                    "warning": f"File already exists: {file_path}. Not creating a new file.",
                    "file_path": file_path,
                },
                indent=2,
            )

        fieldnames = ["text", "source_url", "date_extracted", "domain", "language"]

        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

        return json.dumps(
            {
                "success": True,
                "message": f"Created new dataset file: {file_path}",
                "file_path": file_path,
                "language": language,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            },
            indent=2,
        )

    def _append_to_dataset(self, file_path: str, data: List[Dict[str, Any]]) -> str:
        """Append data to an existing dataset CSV file."""
        if not os.path.exists(file_path):
            return self._create_dataset(
                file_path, data[0].get("language") if data else None
            )

        fieldnames = ["text", "source_url", "date_extracted", "domain", "language"]

        with open(file_path, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for item in data:
                writer.writerow(
                    {
                        "text": item.get("text", ""),
                        "source_url": item.get("source_url", ""),
                        "date_extracted": item.get(
                            "date_extracted", datetime.now().strftime("%Y-%m-%d")
                        ),
                        "domain": item.get("domain", "general"),
                        "language": item.get("language", ""),
                    }
                )

        return json.dumps(
            {
                "success": True,
                "message": f"Appended {len(data)} records to dataset file: {file_path}",
                "file_path": file_path,
                "records_added": len(data),
            },
            indent=2,
        )

    def _get_dataset_stats(self, file_path: str) -> str:
        """Get statistics about the dataset."""
        if not os.path.exists(file_path):
            return json.dumps(
                {"error": f"File does not exist: {file_path}", "file_path": file_path},
                indent=2,
            )

        try:
            df = pd.read_csv(file_path)

            # Calculate statistics
            total_records = len(df)
            total_text_length = (
                df["text"].str.len().sum() if "text" in df.columns else 0
            )
            avg_text_length = (
                df["text"].str.len().mean()
                if "text" in df.columns and total_records > 0
                else 0
            )

            # Count by domain
            domain_counts = (
                df["domain"].value_counts().to_dict() if "domain" in df.columns else {}
            )

            # Count by language
            language_counts = (
                df["language"].value_counts().to_dict()
                if "language" in df.columns
                else {}
            )

            # Count by date
            date_counts = (
                df["date_extracted"].value_counts().to_dict()
                if "date_extracted" in df.columns
                else {}
            )

            return json.dumps(
                {
                    "success": True,
                    "file_path": file_path,
                    "total_records": total_records,
                    "total_text_length": total_text_length,
                    "avg_text_length": avg_text_length,
                    "domain_counts": domain_counts,
                    "language_counts": language_counts,
                    "date_counts": date_counts,
                },
                indent=2,
            )

        except Exception as e:
            return json.dumps(
                {
                    "error": f"Failed to get dataset stats: {str(e)}",
                    "file_path": file_path,
                },
                indent=2,
            )

    def _validate_dataset(self, file_path: str) -> str:
        """Validate the dataset for quality issues."""
        if not os.path.exists(file_path):
            return json.dumps(
                {"error": f"File does not exist: {file_path}", "file_path": file_path},
                indent=2,
            )

        try:
            df = pd.read_csv(file_path)

            # Check for missing values
            missing_values = df.isnull().sum().to_dict()

            # Check for empty text
            empty_text_count = (
                (df["text"].str.len() == 0).sum() if "text" in df.columns else 0
            )

            # Check for very short text (less than 100 characters)
            short_text_count = (
                (df["text"].str.len() < 100).sum() if "text" in df.columns else 0
            )

            # Check for duplicate text
            duplicate_text_count = (
                df["text"].duplicated().sum() if "text" in df.columns else 0
            )

            # Check for missing URLs
            missing_url_count = (
                (df["source_url"].isnull() | (df["source_url"] == "")).sum()
                if "source_url" in df.columns
                else 0
            )

            issues_found = any(
                [
                    any(count > 0 for count in missing_values.values()),
                    empty_text_count > 0,
                    short_text_count > 0,
                    duplicate_text_count > 0,
                    missing_url_count > 0,
                ]
            )

            return json.dumps(
                {
                    "success": True,
                    "file_path": file_path,
                    "issues_found": issues_found,
                    "missing_values": missing_values,
                    "empty_text_count": empty_text_count,
                    "short_text_count": short_text_count,
                    "duplicate_text_count": duplicate_text_count,
                    "missing_url_count": missing_url_count,
                },
                indent=2,
            )

        except Exception as e:
            return json.dumps(
                {
                    "error": f"Failed to validate dataset: {str(e)}",
                    "file_path": file_path,
                },
                indent=2,
            )
