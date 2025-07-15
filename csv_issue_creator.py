#!/usr/bin/env python3
"""
CSV to GitHub Issues Creator

This script processes a CSV file containing paper information and automatically
creates GitHub issues for each unique Paper ID. It tracks processed IDs to avoid
creating duplicate issues.
"""

import os
import sys
import json
import pandas as pd
from datetime import datetime
from github import Github
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('csv_issue_creator.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class CSVIssueCreator:
    def __init__(self, csv_file_path, processed_ids_file="processed_ids.json"):
        """
        Initialize the CSV Issue Creator
        
        Args:
            csv_file_path (str): Path to the CSV file
            processed_ids_file (str): Path to store processed Paper IDs
        """
        self.csv_file_path = csv_file_path
        self.processed_ids_file = processed_ids_file
        self.processed_ids = self.load_processed_ids()
        
        # GitHub configuration
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.repo_name = os.getenv('GITHUB_REPOSITORY')
        
        if not self.github_token:
            raise ValueError("GITHUB_TOKEN environment variable is required")
        if not self.repo_name:
            raise ValueError("GITHUB_REPOSITORY environment variable is required")
        
        # Initialize GitHub client
        try:
            self.github = Github(self.github_token)
            self.repo = self.github.get_repo(self.repo_name)
            logger.info(f"Initialized CSV Issue Creator for repository: {self.repo_name}")
        except Exception as e:
            logger.error(f"Failed to initialize GitHub client: {e}")
            raise
    
    def load_processed_ids(self):
        """Load previously processed Paper IDs from JSON file"""
        try:
            if os.path.exists(self.processed_ids_file):
                with open(self.processed_ids_file, 'r') as f:
                    return set(json.load(f))
            return set()
        except Exception as e:
            logger.warning(f"Error loading processed IDs: {e}")
            return set()
    
    def save_processed_ids(self):
        """Save processed Paper IDs to JSON file"""
        try:
            with open(self.processed_ids_file, 'w') as f:
                json.dump(list(self.processed_ids), f)
            logger.info(f"Saved {len(self.processed_ids)} processed IDs")
        except Exception as e:
            logger.error(f"Error saving processed IDs: {e}")
    
    def read_csv_file(self):
        """Read and validate the CSV file"""
        try:
            df = pd.read_csv(self.csv_file_path)
            
            # Check if required columns exist
            required_columns = ['Paper ID', 'Paper Title', 'Coder', 'Supervisor', 'Collection']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            # Remove rows with empty Paper ID
            df = df.dropna(subset=['Paper ID'])
            df['Paper ID'] = df['Paper ID'].astype(str).str.strip()
            
            logger.info(f"Successfully loaded CSV with {len(df)} rows")
            return df
            
        except Exception as e:
            logger.error(f"Error reading CSV file: {e}")
            raise
    
    def create_issue_body(self, row):
        """Create the body content for a GitHub issue"""
        body_parts = []
        
        # Add Collection
        if 'Collection' in row and pd.notna(row['Collection']):
            body_parts.append(f"**Collection:** {row['Collection']}")
        
        # Add Coder and Supervisor as Authors
        coder = row['Coder'] if 'Coder' in row and pd.notna(row['Coder']) else ''
        supervisor = row['Supervisor'] if 'Supervisor' in row and pd.notna(row['Supervisor']) else ''
        authors = ', '.join(filter(None, [coder, supervisor]))
        if authors:
            body_parts.append(f"**Authors:** {authors}")
        
        # Add metadata
        body_parts.append(f"\n---\n*Issue created automatically from CSV on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        
        return "\n".join(body_parts)
    
    def create_github_issue(self, paper_id, title, body):
        """Create a GitHub issue"""
        try:
            # Check if issue with this title already exists
            existing_issues = self.repo.get_issues(state='all')
            for issue in existing_issues:
                if issue.title == title:
                    logger.info(f"Issue already exists for Paper ID {paper_id}: {title}")
                    return issue.number
            
            # Create new issue
            issue = self.repo.create_issue(
                title=title,
                body=body,
                labels=['paper', 'auto-generated']
            )
            
            logger.info(f"Created issue #{issue.number} for Paper ID {paper_id}: {title}")
            return issue.number
            
        except Exception as e:
            logger.error(f"Error creating issue for Paper ID {paper_id}: {e}")
            return None
    
    def process_csv(self):
        """Main method to process the CSV file and create issues"""
        try:
            # Read CSV file
            df = self.read_csv_file()
            
            new_issues_created = 0
            skipped_issues = 0
            
            for index, row in df.iterrows():
                paper_id = row['Paper ID']
                title = paper_id  # Use Paper ID as the issue title
                
                # Skip if already processed
                if paper_id in self.processed_ids:
                    logger.debug(f"Skipping already processed Paper ID: {paper_id}")
                    skipped_issues += 1
                    continue
                
                # Create issue body
                body = self.create_issue_body(row)
                
                # Create GitHub issue
                issue_number = self.create_github_issue(paper_id, title, body)
                
                if issue_number:
                    # Mark as processed
                    self.processed_ids.add(paper_id)
                    new_issues_created += 1
            
            # Save processed IDs
            self.save_processed_ids()
            
            logger.info(f"Processing complete. Created {new_issues_created} new issues, skipped {skipped_issues} already processed.")
            return new_issues_created
            
        except Exception as e:
            logger.error(f"Error processing CSV: {e}")
            raise

def main():
    """Main function"""
    try:
        # Get CSV file path from command line argument or use default
        csv_file = sys.argv[1] if len(sys.argv) > 1 else "sample_papers.csv"
        
        # Check if CSV file exists
        if not os.path.exists(csv_file):
            logger.error(f"CSV file not found: {csv_file}")
            sys.exit(1)
        
        # Create and run the issue creator
        creator = CSVIssueCreator(csv_file)
        new_issues = creator.process_csv()
        
        print(f"Successfully processed CSV file. Created {new_issues} new issues.")
        
    except Exception as e:
        logger.error(f"Script failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
