from datetime import datetime,timedelta,timezone
from hashlib import pbkdf2_hmac
import base64,hmac,hashlib,json,os
from app.config import settings
def hash_password(p,salt=None):
    salt=salt or os.urandom(16); dk=pbkdf2_hmac('sha256',p.encode(),salt,120000); return base64.b64encode(salt+dk).decode()
def verify_password(p,h):
    raw=base64.b64decode(h); return hmac.compare_digest(raw[16:],pbkdf2_hmac('sha256',p.encode(),raw[:16],120000))
def token(data,minutes=30):
    payload={**data,'exp':(datetime.now(timezone.utc)+timedelta(minutes=minutes)).timestamp()}; body=base64.urlsafe_b64encode(json.dumps(payload).encode()).rstrip(b'='); sig=hmac.new(settings.secret_key.encode(),body,hashlib.sha256).digest(); return (body+b'.'+base64.urlsafe_b64encode(sig).rstrip(b'=')).decode()
def decode_token(t):
    body,sig=t.encode().split(b'.'); good=base64.urlsafe_b64encode(hmac.new(settings.secret_key.encode(),body,hashlib.sha256).digest()).rstrip(b'=')
    if not hmac.compare_digest(sig,good): raise ValueError('token inválido')
    data=json.loads(base64.urlsafe_b64decode(body+b'=='))
    if data['exp']<datetime.now(timezone.utc).timestamp(): raise ValueError('token expirado')
    return data
