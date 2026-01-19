from fastapi import FastAPI, Path
from urllib.parse import urlparse, unquote
from pydantic import BaseModel


app = FastAPI()

BLOCKED_URLS = {
    "pulse.aws/application/W7SDDK2X?p=0",
    "malware.test/bad/path",
}

ALLOWED_URLS = {
    "example.com/home",
    "es.wikipedia.org/wiki/Wikipedia:Portada"
}




@app.get("/urlinfo/1/{hostname_and_port}/{encoded_path:path}")
def obtener_info_url(hostname_and_port: str, 
                     encoded_path: str = Path(...)
                     ):
    decoded_path = unquote(encoded_path)
    full_url = f"{hostname_and_port}{decoded_path}"
    parsed = urlparse(full_url)
    

    if full_url in BLOCKED_URLS:
        verdict = "DENY"
        reason = "URL found in blocked list"
    elif full_url in ALLOWED_URLS:
        verdict = "ALLOW"
        reason = "URL explicitly allowed"
    else:
        verdict = "UNKNOWN"
        reason = "URL not found in any list"


    return {
        "original_url": full_url,
        "scheme": parsed.scheme,
        "host": parsed.hostname,
        "port": parsed.port,
        "path": parsed.path,
        "query": parsed.query,
        "verdict": verdict,
        "reason": reason
    }