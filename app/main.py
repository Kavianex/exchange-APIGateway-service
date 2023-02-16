from fastapi import FastAPI, Response
import requests
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
import auth
import settings
import uvicorn


private_methods = ["POST", "PUT", "PATCH", "DELETE"]
public_methods = ["GET", "HEAD", "OPTIONS"]
methods = private_methods + public_methods
origins = settings.ALLOWED_ORIGINS

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=methods,
    allow_headers=["*"],
)


def get_url(path: str):
    service, host = get_host(path=path)
    url = ''
    if host:
        path = path[len(service)+1:]
        url = f"{host}{path}"
    return url


def get_host(path: str):
    service = ''
    for service_name in settings.SERVICE_HOSTS:
        if path.startswith(f"/{service_name}"):
            service = service_name
            break
    return service, settings.SERVICE_HOSTS.get(service, None)


async def _reverse_proxy(request: Request):
    body = await request.body()
    path = request.url.path
    url = get_url(path)
    if not url:
        return Response(status_code=404)
    method = request.method
    authorization = request.headers.get('Authorization', '')
    wallet = request.headers.get("wallet", '')
    if method in private_methods:
        wallet = auth.authenticate(authorization=authorization)
        if not wallet:
            return Response(status_code=401)
    role = auth.authorize(wallet)
    headers = {
        "role": role,
        "wallet": wallet
    }
    response = requests.request(
        method=request.method,
        url=url,
        data=body.decode(),
        headers=headers
    )
    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=response.headers
    )

app.add_route("/{service}/{path:path}", _reverse_proxy, methods=methods)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.SERVICE_PORT,
        log_level="info"
    )
