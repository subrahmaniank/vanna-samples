from typing import Optional

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


class PortfolioUserResolver(UserResolver):
    """
    UserResolver for Portfolio Analyzer module.
    Resolves user identity from cookie, header, or default portfolio manager.
    """

    async def resolve_user(self, request_context: RequestContext) -> User:
        user_email = (
            request_context.get_cookie("vanna_email")
            or request_context.get_header("x-user-email")
            or "manager@portfolio.com"
        )
        username = user_email.split("@")[0] if "@" in user_email else user_email
        return User(
            id=user_email,
            username=username,
            email=user_email,
            group_memberships=["admin", "user"],
            permissions=["execute_sql"]
        )
