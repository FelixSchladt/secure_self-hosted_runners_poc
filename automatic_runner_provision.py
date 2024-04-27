import requests
import time

owner = os.getenv('GITHUB_OWNER')
repo = os.getenv('GITHUB_REPO')
pat = os.getenv('GITHUB_PAT')

def fetch_workflow_runs():
    url = "https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/actions/runs"
    headers = {
        'Authorization': f'token {GITHUB_PAT}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(url, headers=headers)
    runs = response.json().get('workflow_runs', [])
    return [run for run in runs if run['status'] == 'queued']

def fetch_workflow_file(owner, repo, path_to_workflow_file, github_token):
    """
    Fetch the workflow file from GitHub repository and check if it requires a self-hosted runner.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path_to_workflow_file}"
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3.raw'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch the workflow file: {response.status_code}")
        return None

def check_for_self_hosted_runner(workflow_content):
    """
    Check the content of the workflow file to determine if it uses a self-hosted runner.
    """
    if 'runs-on: self-hosted' in workflow_content:
        return True
    return False

def main():
    while True:
        queued_runs = fetch_workflow_runs()
        if queued_runs:
            print("There are queued workflow runs:")
            for run in queued_runs:
                print(run)
        else:
            print("No queued runs at this time.")
        time.sleep(300)  # Poll every 5 minutes

if __name__ == "__main__":
    main()
