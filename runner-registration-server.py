from fastapi import FastAPI, HTTPException, Request
import httpx
import os
import uuid
import libvirt

app = FastAPI()

domain_name = "runner-base-img"
snapshot_name = "base-image-v4"
default_workflow_timeout = 3*60 # 3 minute timeout

def reset_runner():
    try:
        # Connect to the local libvirt system
        if (conn:=libvirt.open("qemu:///system")) is None:
            print("Failed to open connection to the local libvirt system")
            return False

        # Find the domain by name
        if (dom := conn.lookupByName(domain_name)) is None:
            print(f"No domain found with name: {domain_name}")
            return False

        # Look up the snapshot by name
        if (snap := dom.snapshotLookupByName(snapshot_name, 0)) is None:
            print(f"No snapshot found with name: {snapshot_name}")
            return False

        # Revert to the snapshot
        if dom.revertToSnapshot(snap, 0) < 0:
            print(f"Failed to revert to snapshot: {snapshot_name}")
            return False
        else:
            print(f"Successfully reverted to snapshot: {snapshot_name}")

        # Start the domain if it is not already running
        if dom.isActive() == 0:
            if dom.create() < 0:
                print("Failed to start the domain")
                return False
            else:
                print(f"Domain {domain_name} has been started.")

        # Close the connection
        conn.close()

    except libvirt.libvirtError as e:
        print(f"Error: {e}")
        return False

@app.get("/api/reset-runner/")
async def get_reset_runner():
    print("Runner reset")
    reset_runner()

@app.get("/api/register-runner/")
async def get_register_run():
    print("register runner")
    # Put some logic here to reset the runner after timeout
    # in case it did not reset itself

@app.get("/api/get-github-token/")
async def get_github_token(request: Request):
    owner = os.getenv('GITHUB_OWNER')
    repo = os.getenv('GITHUB_REPO')
    pat = os.getenv('GITHUB_PAT')
    print("One time token requested")

    if not owner or not repo or not pat:
        raise HTTPException(status_code=400, detail="Missing owner, repo, or PAT")

    token_response = await fetch_github_token(owner, repo, pat)
    if 'token' in token_response:
        return token_response['token'].strip('"')
    else:
        raise HTTPException(status_code=500, detail="Failed to retrieve the token")

async def fetch_github_token(owner: str, repo: str, pat: str) -> dict:
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/runners/registration-token"
    print(pat)
    headers = {
        "Authorization": f"Bearer {pat}",
        "Accept": "application/vnd.github.v3+json"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers)
        return response.json()
