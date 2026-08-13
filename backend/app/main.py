from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import router as auth_router
from app.routers.crud import router as crud_router
from app.routers.analytics import router as analytics_router
app=FastAPI(title='Limpeza360 API',version='0.1.0',description='SaaS multi-tenant para gestão de limpeza, higienização e lavanderia')
app.add_middleware(CORSMiddleware,allow_origins=['*'],allow_methods=['*'],allow_headers=['*'])
app.include_router(auth_router)
app.include_router(analytics_router)
app.include_router(crud_router)
@app.get('/health')
def health(): return {'status':'ok'}
