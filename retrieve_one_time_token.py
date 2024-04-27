import requests

def get_registration_token(owner, repo, pat):
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/runners/registration-token"
    headers = {
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.post(url, headers=headers)
    print(response.json())
    return response.json().get('token')

owner = "FelixSchladt"
repo = "secure_self-hosted_runners_poc"
pat ="PAT"
token = get_registration_token(owner, repo, pat)
print(token)

