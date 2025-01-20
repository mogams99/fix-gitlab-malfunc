# GitLab Commit Fetcher

This script fetches commits from multiple GitLab projects and filters them by a specific committer, in this case, `dependabot[bot]`. The script uses the GitLab API to retrieve projects and commits, then saves the filtered commit data into an Excel file.

## GitLab API Configuration

Before running the script, you need to set up the following variables:

- `GITLAB_HOST`: The base URL of your GitLab instance (e.g., `https://gitlab.com`).
- `PRIVATE_TOKEN`: Your GitLab private access token with the appropriate permissions to access project data.

Replace `<gitlab-host>` and `<access-token>` in the script with the actual values.

## How It Works

1. **Get Projects**: The script retrieves all projects from the specified GitLab instance.
2. **Get Commits by Committer**: For each project, the script fetches all commits made by a specific committer (`dependabot[bot]` in this case).
3. **Filter and Format Commits**: It filters the commits based on the committer's name and formats the commit date to a more human-readable format.
4. **Save Data**: The filtered data is saved to an Excel file named `dependabot_commits_<timestamp>.xlsx`.

## Script Details

### Functions

- **`get_projects()`**:
  - Retrieves all projects from GitLab using the GitLab API.
  - It handles pagination and collects projects until all pages are fetched.
  - **Returns**: A list of projects.

- **`get_commits_by_committer(project_id, committer_name)`**:
  - Fetches commits for a specific project, filtered by the given committer’s name (e.g., `dependabot[bot]`).
  - **Returns**: A list of commits made by the specified committer.

- **`format_datetime_with_day(iso_date)`**:
  - Converts an ISO 8601 formatted datetime string into a more human-readable format, including the day of the week.
  - **Returns**: A formatted datetime string (e.g., `Monday, 20 January 2025 14:30:00`).

## Basic Usage

1. **Set Up Configuration**: Update the `GITLAB_HOST` and `PRIVATE_TOKEN` in the script with your GitLab instance details and API token.
2. **Run the Script**:

```bash
python main.py