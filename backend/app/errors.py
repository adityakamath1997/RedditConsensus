from fastapi import HTTPException


class BaseAppError(Exception):
    def __init__(self, code: str, message: str, status_code: int):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class BadRequestError(BaseAppError):
    def __init__(self, message: str = "Invalid request."):
        super().__init__("BAD_REQUEST", message, 400)


class UnauthorizedError(BaseAppError):
    def __init__(self, message: str = "Unauthorized."):
        super().__init__("UNAUTHORIZED", message, 401)


class ForbiddenError(BaseAppError):
    def __init__(self, message: str = "Forbidden."):
        super().__init__("FORBIDDEN", message, 403)


class RateLimitError(BaseAppError):
    def __init__(self, message: str = "Service rate limited. Please try again shortly."):
        super().__init__("RATE_LIMITED", message, 429)


class UpstreamError(BaseAppError):
    def __init__(self, message: str = "Upstream service error. Please try again later."):
        super().__init__("UPSTREAM_ERROR", message, 502)


class ServiceUnavailableError(BaseAppError):
    def __init__(self, message: str = "Service temporarily unavailable. Please try again later."):
        super().__init__("SERVICE_UNAVAILABLE", message, 503)


class InternalServerError(BaseAppError):
    def __init__(self, message: str = "Unexpected server error. Please try again later."):
        super().__init__("INTERNAL_ERROR", message, 500)


