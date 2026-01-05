# encoding=utf-8
import sys
import arrow
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Union

# 导入原有工具函数
from mid_url import url_to_mid, mid_to_url
from pingyin_tool import get_pingyin
from ip_tool import int2ip, ip2int
from domain_tool import evaluate
from base64_tool import base64_encode, base64_decode

app = FastAPI(title="Tool Service", description="Migrated from Tornado to FastAPI")

# 配置 CORS，替代原有的 options 方法
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],  # 原代码只允许 POST 和 OPTIONS
    allow_headers=["*"],
)

# --- Request Models ---

class MidURLRequest(BaseModel):
    mid: Optional[str] = None
    url: Optional[str] = None

class PinyinRequest(BaseModel):
    content: str

class TimeStampRequest(BaseModel):
    date: Optional[str] = None
    sec: Optional[Union[str, int, float]] = None

class IPRequest(BaseModel):
    ip: Optional[str] = None
    integer: Optional[Union[str, int]] = None

class DomainRequest(BaseModel):
    domain: str

class Base64Request(BaseModel):
    originalString: Optional[str] = None
    encodedString: Optional[str] = None

class UpperLowerRequest(BaseModel):
    upperString: Optional[str] = None
    lowerString: Optional[str] = None

# --- Route Handlers ---

@app.post("/api/mid_url")
async def handle_mid_url(params: MidURLRequest):
    if params.mid:
        print('mid', params.mid)
        ss = mid_to_url(params.mid)
        return {'url': ss}
    else:
        ss = params.url
        mid = url_to_mid(ss)
        print('mid', mid)
        return {'mid': mid}

@app.post("/api/pinyin")
async def handle_pinyin(params: PinyinRequest):
    return {'pinyin': get_pingyin(params.content)}

@app.post("/api/timestamp")
async def handle_timestamp(params: TimeStampRequest):
    if params.date:
        d = params.date
        print(d)
        d += "+08:00"
        sec = int(arrow.get(d).timestamp())
        return {'sec': sec}
    else:
        ss = params.sec
        ss = float(ss)
        t = arrow.get(ss)
        t = t.to("+08:00")
        return {'date': t.format('YYYY-MM-DD HH:mm:ss')}

@app.post("/api/ip")
async def handle_ip(params: IPRequest):
    if params.ip:
        return {'integer': ip2int(params.ip)}
    else:
        integer = params.integer
        print(integer)
        return {'ip': int2ip(integer)}

@app.post("/api/domain")
def handle_domain(params: DomainRequest):
    """
    注意：这里使用普通 def 而不是 async def。
    因为 evaluate 函数内部使用 requests 发起同步网络请求，
    FastAPI 会自动在线程池中运行此函数，避免阻塞事件循环。
    """
    domain = params.domain.strip()
    return evaluate(domain)

@app.post("/api/base64")
async def handle_base64(params: Base64Request):
    if params.originalString:
        return {'encodedString': base64_encode(params.originalString)}
    else:
        return {'originalString': base64_decode(params.encodedString)}

@app.post("/api/upper_lower_case")
async def handle_base64(params: UpperLowerRequest):
    if params.lowerString:
        return {'upperString': params.lowerString.upper()}
    else:
        return {'lowerString': params.upperString.lower()}


if __name__ == "__main__":
    print('starting....')
    port = 9099
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    
    # workers=2 模拟原有的 server.start(2)
    uvicorn.run("tool_server:app", host="0.0.0.0", port=port, workers=2)

