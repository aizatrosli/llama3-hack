import json
from datetime import datetime
from typing import List, Optional
from fastapi import Form, File, UploadFile, Request, APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

router = APIRouter()

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