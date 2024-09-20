import time

from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/run_command")
async def run_command(cmd: str):
    if cmd == "time":
        res = f"time: {time.ctime()}"
    elif cmd == "hello":
        res = "Hi"
    else:
        res = f"run {cmd} success!"
    return {"result": res}


@app.get("/manifest.json")
def manifest(request: Request):
    server_url = request.base_url
    manifest_dict = {
        "api": [],
        "openapi": f"{server_url}openapi.json",
        "author": "HYD",
        "createdAt": "2024-06-13",
        "identifier": "test",
        "meta": {
            "avatar": "🚀",
            "tags": ["test"],
            "title": "test",
            "description": "This plugin can run a command in test.",
        },
        "version": "1",
    }
    manifest_dict["openapi"] = manifest_dict["openapi"].format(server_url=server_url)
    return manifest_dict


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=12345, reload=True)
