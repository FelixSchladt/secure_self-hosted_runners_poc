from fastapi import FastAPI, HTTPException, Request
import httpx
import os

app = FastAPI()

@app.get("/get-github-token/")
async def get_github_token(request: Request):
    owner = os.getenv('GITHUB_OWNER')
    repo = os.getenv('GITHUB_REPO')
    pat = os.getenv('GITHUB_PAT')

    if not owner or not repo or not pat:
        raise HTTPException(status_code=400, detail="Missing owner, repo, or PAT")

    token_response = await fetch_github_token(owner, repo, pat)
    if 'token' in token_response:
        return {"token": token_response['token']}
    else:
        raise HTTPException(status_code=500, detail="Failed to retrieve the token")

async def fetch_github_token(owner: str, repo: str, pat: str) -> dict:
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/runners/registration-token"
    headers = {
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github.v3+json"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers)
        return response.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

