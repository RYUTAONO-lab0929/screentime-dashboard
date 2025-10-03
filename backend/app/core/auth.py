from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


bearer_scheme = HTTPBearer(auto_error=False)


def require_role(required_role: str):
    def _dep(creds: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme)):
        # 簡易RBACスタブ: 実際はOIDCのIDトークン検証やDB連携で判定
        # ここでは "X-Role: admin|researcher|participant" の代替としてBearerトークン名で判定可能
        if creds is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        token = creds.credentials
        # 例: "role:admin:<random>" のような形式を許可
        parts = token.split(":")
        role = parts[1] if len(parts) > 1 and parts[0] == "role" else None
        if role != required_role and not (required_role == "researcher" and role == "admin"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return True

    return _dep
