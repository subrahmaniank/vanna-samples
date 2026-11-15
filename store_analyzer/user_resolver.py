from typing import Optional, Dict, Any

try:
    from vanna.core.user import UserResolver, RequestContext, User
except ImportError:
    from pydantic import BaseModel
    from typing import List

    class User(BaseModel):
        id: str
        username: Optional[str] = None
        email: Optional[str] = None
        group_memberships: List[str] = []
        permissions: List[str] = []

    class RequestContext:
        def get_cookie(self, key: str) -> Optional[str]:
            return None
        def get_header(self, key: str) -> Optional[str]:
            return None

    class UserResolver:
        pass


class StoreAnalyzerUserResolver(UserResolver):
    """
    UserResolver for Store Analyzer module, migrating the simple authorization
    from Vanna 1.x into 2.0 RBAC user groups.
    """

    STORE_USERS: Dict[str, Dict[str, Any]] = {
        "admin": {
            "password": "admin#123",
            "groups": ["admin", "user"],
            "permissions": ["execute_sql", "view_sql", "manage_memory"]
        },
        "hillyer": {
            "password": "hillyer",
            "groups": ["user"],
            "permissions": ["execute_sql"]
        }
    }

    async def resolve_user(self, request_context: RequestContext) -> User:
        user_name = (
            request_context.get_cookie("user")
            or request_context.get_header("x-user")
            or "admin"
        ).lower()
        password = (
            request_context.get_cookie("password")
            or request_context.get_header("x-password")
            or "admin#123"
        )

        user_info = self.STORE_USERS.get(user_name)
        if user_info and user_info["password"] == password:
            return User(
                id=user_name,
                username=user_name,
                email=f"{user_name}@dvdrental.com",
                group_memberships=user_info["groups"],
                permissions=user_info["permissions"]
            )

        # Fallback authenticated user
        return User(
            id=user_name,
            username=user_name,
            email=f"{user_name}@dvdrental.com",
            group_memberships=["user"],
            permissions=["execute_sql"]
        )
