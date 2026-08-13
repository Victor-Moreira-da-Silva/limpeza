from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import User
from app.schemas import LoginIn,TokenOut
from app.services.security import verify_password,token
router=APIRouter(prefix='/auth',tags=['auth'])
@router.post('/login',response_model=TokenOut)
def login(data:LoginIn,db:Session=Depends(get_db)):
    u=db.query(User).filter(User.email==data.email).first()
    if not u or not u.active or not verify_password(data.password,u.password_hash): raise HTTPException(401,'credenciais inválidas')
    return TokenOut(access_token=token({'sub':str(u.id),'tenant_id':u.tenant_id,'role_id':u.role_id},30),refresh_token=token({'sub':str(u.id),'type':'refresh'},60*24*7))
@router.post('/recover-password')
def recover_password(email:str): return {'message':'se o e-mail existir, instruções serão enviadas'}
