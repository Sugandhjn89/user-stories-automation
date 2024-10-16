import os
import requests
import logging
from jira import JIRA
from requests.auth import HTTPBasicAuth

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# JIRA configuration from environment variables
JIRA_SERVER = 'https://sugandhjn89-1728478357532.atlassian.net'  # Updated to remove /rest/api/2/serverInfo
JIRA_EMAIL = 'sugandhjn.89@gmail.com'
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')  # Get API token from environment variables
PROJECT_KEY = os.getenv('PROJECT_KEY')

def read_user_stories(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content.split('##')[1:]  # Split based on the user story header

def create_jira_issue(summary, description):
    try:
        # Authenticate to JIRA
        jira = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))
        # Create a new issue
        new_issue = jira.create_issue(
            project=PROJECT_KEY,
            summary=summary,
            description=description,
            issuetype={'name': 'Story'}
        )
        logging.info(f"Issue created: {new_issue.key}")
    except Exception as e:
        logging.error(f"Failed to create Jira issue: {e}")

def main():
    # Ensure the environment variables are set
    if not PROJECT_KEY or not JIRA_API_TOKEN:
        logging.error("PROJECT_KEY and JIRA_API_TOKEN environment variables must be set.")
        return

    user_stories = read_user_stories(r'C:\Users\MY HP\Desktop\GitHub_Requirements\GroupBillPaymentUserStories\user_stories.md')
    for story in user_stories:
        lines = story.strip().split('\n')
        if lines:
            summary = lines[0].strip().strip('*').strip()  # First line as summary
            description = '\n'.join(lines[1:]).strip()  # Rest as description
            create_jira_issue(summary, description)

if __name__ == "__main__":
    main()
