from imp import reload
from fastapi import FastAPI
from core.configs import settings
from api.v1.api import api_router

app = FastAPI(title='Course API - Security')
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level='info', reload=True)


"""
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNjYxMjg5ODQzLCJpYXQiOjE2NjA2ODUwNDMsInN1YiI6IjQifQ.HVxxAqVgEAdokfJB1A2KgewyY7KCo7WBVSxrtS5XTBw
Type: bearer
"""