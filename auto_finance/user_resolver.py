"""Demo identity for the auto finance sample."""

from vanna.core.user import RequestContext, User, UserResolver


class AutoFinanceUserResolver(UserResolver):
    async def resolve_user(self, request_context: RequestContext) -> User:
        email = (
            request_context.get_cookie("vanna_email")
            or request_context.get_header("x-user-email")
            or "analyst@auto-finance.example"
        )
        return User(
            id=email,
            username=email.split("@")[0],
            email=email,
            group_memberships=["admin", "user"],
            permissions=["execute_sql"],
        )
