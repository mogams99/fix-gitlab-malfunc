import requests
from datetime import datetime
import pandas as pd

#? GitLab API Config
GITLAB_HOST = "https://<gitlab-host>/api/v4/projects"  
PRIVATE_TOKEN = "<access-token>" 

def get_projects():
    """Mengambil semua project dari GitLab."""
    url = f"{GITLAB_HOST}/api/v4/projects"
    headers = {"PRIVATE-TOKEN": PRIVATE_TOKEN}
    projects = []
    page = 1

    while True:
        params = {"per_page": 100, "page": page}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error fetching projects: {response.status_code}")
            break

        data = response.json()
        if not data:
            break

        projects.extend(data)
        page += 1

    return projects

def get_commits_by_committer(project_id, committer_name):
    """Mengambil commit dari project berdasarkan committer_name."""
    url = f"{GITLAB_HOST}/api/v4/projects/{project_id}/repository/commits"
    headers = {"PRIVATE-TOKEN": PRIVATE_TOKEN}
    params = {"per_page": 100}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Error fetching commits for project {project_id}: {response.status_code}")
        return []

    all_commits = response.json()
    filtered_commits = [
        commit for commit in all_commits
        if commit.get("committer_name") == committer_name
    ]

    return filtered_commits

def format_datetime_with_day(iso_date):
    """Mengonversi waktu ISO 8601 ke format manusiawi dengan hari."""
    date_obj = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
    return date_obj.strftime("%A, %d %B %Y %H:%M:%S")

if __name__ == "__main__":
    committer_name = "dependabot[bot]"
    projects = get_projects()
    filtered_projects = 0  # Untuk menghitung proyek yang memiliki commit dari dependabot[bot]

    #? List untuk menyimpan data yang akan ditulis ke file Excel
    all_data = []

    for project in projects:
        project_id = project["id"]
        project_name = project["name"]
        commits = get_commits_by_committer(project_id, committer_name)

        if commits:
            filtered_projects += 1  # Menambah hitungan proyek dengan commit dari dependabot[bot]
            for commit in commits:
                commit_id = commit["id"]
                commit_title = commit["title"]
                committed_date = format_datetime_with_day(commit["committed_date"])

                # ? Tambahkan data ke list
                all_data.append({
                    "Project Name": project_name,
                    "Project ID": project_id,
                    "Commit ID": commit_id,
                    "Commit Title": commit_title,
                    "Committed Date": committed_date,
                    "Committer Name": committer_name,
                })

    #? Menambahkan tanggal saat file diekspor
    export_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = f"dependabot_commits_{export_date}.xlsx"

    #? Buat DataFrame dari list data
    if all_data:
        df = pd.DataFrame(all_data)

        #? Simpan ke file Excel
        df.to_excel(output_file, index=False)
        print(f"Found {filtered_projects} projects with commits from {committer_name}.")
        print(f"Data saved to {output_file}")
    else:
        print(f"No commits found for {committer_name}.")
