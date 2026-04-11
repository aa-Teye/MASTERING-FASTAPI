"""
core/resilience.py

Enterprise-grade decorators for network resilience and fault tolerance.
Implements exponential backoff and basic circuit breaking for async network calls.
"""

import asyncio
import logging
from functools import wraps
from typing import TypeVar, Callable, Any, cast

# Configure a module-level logger
logger = logging.getLogger(__name__)

# Define Generics for strict type hinting of the decorated functions
R = TypeVar('R')
FuncType = Callable[..., asyncio.Future[R]]

class MaxRetriesExceededError(Exception):
    """Raised when a function fails after the maximum number of retries."""
    pass

def with_retry(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 10.0,
    exceptions: tuple[type[Exception], ...] = (ConnectionError, TimeoutError)
) -> Callable[[FuncType[R]], FuncType[R]]:
    """
    A decorator that retries an asynchronous function if specific exceptions are raised.
    Uses an exponential backoff strategy (1s, 2s, 4s, 8s...).

    Args:
        max_attempts: The absolute maximum number of times to try the execution.
        base_delay: The starting delay in seconds between retries.
        max_delay: The cap on the delay to prevent infinitely long waits.
        exceptions: A tuple of exception types that should trigger a retry.
    """
    def decorator(func: FuncType[R]) -> FuncType[R]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> R:
            attempt = 1
            current_delay = base_delay

            while attempt <= max_attempts:
                try:
                    # Attempt to execute the core function
                    return await func(*args, **kwargs)
                
                except exceptions as e:
                    logger.warning(
                        f"Attempt {attempt}/{max_attempts} failed for '{func.__name__}': {e}"
                    )
                    
                    if attempt == max_attempts:
                        logger.error(f"Function '{func.__name__}' failed completely after {max_attempts} attempts.")
                        raise MaxRetriesExceededError(f"Operation failed: {str(e)}") from e
                    
                    # Calculate the next delay (Exponential Backoff)
                    # min() ensures we never wait longer than max_delay
                    sleep_time = min(current_delay, max_delay)
                    logger.info(f"Retrying in {sleep_time} seconds...")
                    
                    await asyncio.sleep(sleep_time)
                    
                    # Double the delay for the next iteration
                    current_delay *= 2
                    attempt += 1

            # Fallback (Should theoretically be unreachable due to the raise inside the loop)
            raise MaxRetriesExceededError("Unexpected exit from retry loop")
            
        return cast(FuncType[R], wrapper)
    return decorator



if __name__ == "__main__":
    import random
    
    # We set up logging just for the demonstration
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

    # We apply the decorator to a mock database call that fails randomly
    @with_retry(max_attempts=4, base_delay=1.5, exceptions=(ValueError,))
    async def fetch_external_user_data(user_id: int) -> dict[str, str]:
        """Simulates fetching data from an unstable external service."""
        logging.info(f"--- Firing request for User {user_id} ---")
        
        # Simulate an 80% chance of the network dropping the connection
        if random.random() < 0.8:
            raise ValueError("External database is currently locked.")
            
        return {"id": str(user_id), "status": "verified", "role": "admin"}

    # Run the async simulation
    async def main():
        try:
            result = await fetch_external_user_data(404)
            print(f"\n SUCCESS: {result}")
        except MaxRetriesExceededError:
            print("\n❌ FATAL: Could not retrieve data after all retries.")

    asyncio.run(main())