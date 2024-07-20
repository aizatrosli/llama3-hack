import json
import os
import asyncio
from datetime import datetime
from typing import List, Optional
from fastapi import Form, File, UploadFile, Request, APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from app import index
router = APIRouter()
API_TIMEOUT = 30

@router.get("/say_hello_world", name="Sanity check", status_code=status.HTTP_201_CREATED)
async def say_hello_world(
    text: str,
    overwrite: Optional[bool] = False,
):
    content = {'text': text}
    if overwrite:
        return JSONResponse(status_code=200, content=content)
    else:
        content['test'] = True
        return JSONResponse(status_code=200, content=content)
    

@router.get("/query", name="Query RAG", status_code=status.HTTP_201_CREATED)
async def query_llm(
    query: str,
):
    response = await asyncio.wait_for(index.query_index(query), timeout=API_TIMEOUT)
    return JSONResponse(status_code=200, content={'answer': response.response})

    
