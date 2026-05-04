import time
from functools import wraps


def retry(max_retries=3, delay=5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)

                except Exception as e:
                    last_exception = e
                    print(f"[RETRY] Attempt {attempt} failed: {e}")

                    if attempt < max_retries:
                        time.sleep(delay)

            raise last_exception

        return wrapper
    return decorator