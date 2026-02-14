import logging
from functools import wraps

logger = logging.getLogger("api.calls")

def log_api_exceptions(func):
    """
    Decorator to log exceptions in Ninja API endpoints.
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except Exception as e:
            # Log full traceback and extra info
            logger.exception(
                f"Error in API call: {str(e)}",
                extra={
                    "user": str(request.user) if request.user.is_authenticated else "Anonymous",
                    "method": request.method,
                    "path": request.get_full_path(),
                }
            )
            # Return safe JSON error response
            return {
                "success": False,
                "message": "An internal error occurred."
            }
    return wrapper
