from fastapi import Depends,HTTPException,Header
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import User,Role,role_permissions,Permission
from app.services.security import decode_token
def current_user(authorization:str=Header(None),db:Session=Depends(get_db)):
    if not authorization or not authorization.startswith('Bearer '): raise HTTPException(401,'não autenticado')
    try: data=decode_token(authorization.split()[1])
    except Exception: raise HTTPException(401,'sessão inválida')
    user=db.get(User,int(data['sub']))
    if not user or not user.active: raise HTTPException(403,'usuário inativo')
    return user
def require(code):
    def dep(user:User=Depends(current_user),db:Session=Depends(get_db)):
        if user.role and user.role.name=='Administrador': return user
        q=db.query(Permission.code).join(role_permissions,Permission.id==role_permissions.c.permission_id).filter(role_permissions.c.role_id==user.role_id)
        if code not in {x[0] for x in q}: raise HTTPException(403,'permissão insuficiente')
        return user
    return dep
