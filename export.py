

import asyncio
import logging
from functools import wraps
from typing import TypeVar, Callable, Any, cast

# Configure a module-level logger
logger = logging.getLogger(__name__)


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
            print("\ FATAL: Could not retrieve data after all retries.")

    asyncio.run(main())

"""
core/event_bus.py

Enterprise-grade Asynchronous Event Bus (Publisher/Subscriber Pattern).
Decouples domain logic from background tasks to ensure high-performance API response times.
"""

import asyncio
import logging
import uuid
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Callable, Dict, List, TypeVar, Awaitable, Any

# Configure logging
logger = logging.getLogger(__name__)

# ==========================================
# 📦 1. EVENT SCHEMA DEFINITION
# ==========================================

@dataclass
class Event:
    """Base class for all system events. Immutable by design."""
    name: str
    payload: Dict[str, Any]
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

# Type hinting for subscriber callbacks
# A subscriber must be an async function that takes an Event and returns nothing
SubscriberCallback = Callable[[Event], Awaitable[None]]

# ==========================================
# 🚦 2. THE EVENT BUS (THE BROKER)
# ==========================================

class AsyncEventBus:
    """
    A Singleton Event Bus that manages topics and routes messages to subscribers.
    """
    _instance = None

    def __new__(cls):
        # Ensure only one Event Bus exists in the entire application (Singleton Pattern)
        if cls._instance is None:
            cls._instance = super(AsyncEventBus, cls).__new__(cls)
            cls._instance.subscribers: Dict[str, List[SubscriberCallback]] = {}
            cls._instance.queue: asyncio.Queue = asyncio.Queue()
        return cls._instance

    def subscribe(self, event_name: str, callback: SubscriberCallback) -> None:
        """Registers a function to listen for a specific event."""
        if event_name not in self.subscribers:
            self.subscribers[event_name] = []
        self.subscribers[event_name].append(callback)
        logger.info(f"Subscribed '{callback.__name__}' to event: {event_name}")

    async def publish(self, event: Event) -> None:
        """Puts an event onto the queue immediately and frees up the main thread."""
        await self.queue.put(event)
        logger.debug(f"Event published to queue: {event.name} ({event.event_id})")

    async def _process_event(self, event: Event) -> None:
        """Routes the event to all interested subscribers concurrently."""
        if event.name not in self.subscribers:
            logger.warning(f"No subscribers found for event: {event.name}")
            return

        # Gather all subscriber functions for this event
        callbacks = self.subscribers[event.name]
        
        # Execute all subscribers concurrently using asyncio.gather
        tasks = [callback(event) for callback in callbacks]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Expert Error Handling: Log errors without crashing the whole bus
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Subscriber failed processing event '{event.name}': {result}")

    async def start_worker(self) -> None:
        """Background loop that constantly watches the queue for new events."""
        logger.info("Event Bus Worker Started. Listening for events...")
        while True:
            # This will pause the loop until an event is actually in the queue
            event: Event = await self.queue.get()
            
            try:
                # Process the event
                await self._process_event(event)
            finally:
                # Tell the queue this task is fully complete
                self.queue.task_done()


# ==========================================
# 🚀 3. USAGE EXAMPLE (SIMULATING AN API)
# ==========================================
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | [%(levelname)s] %(message)s")

    bus = AsyncEventBus()

    # --- THE SUBSCRIBERS (Background Workers) ---
    async def send_welcome_email(event: Event) -> None:
        """Simulates a slow email API call."""
        user = event.payload.get("username")
        logger.info(f"[Email Worker] Preparing email for {user}...")
        await asyncio.sleep(2)  # Simulating network delay
        logger.info(f"[Email Worker] ✅ Welcome email sent to {user}!")

    async def update_analytics_dashboard(event: Event) -> None:
        """Simulates writing to a data warehouse."""
        user = event.payload.get("username")
        logger.info(f"[Analytics Worker] Updating daily sign-up metrics for {user}...")
        await asyncio.sleep(0.5)
        logger.info(f"[Analytics Worker] ✅ Metrics updated!")

    # Register the workers to listen for the "USER_REGISTERED" shout
    bus.subscribe("USER_REGISTERED", send_welcome_email)
    bus.subscribe("USER_REGISTERED", update_analytics_dashboard)

    # --- THE PUBLISHER (Your API Route) ---
    async def api_create_user(username: str) -> dict:
        """Simulates a FastAPI POST route."""
        logger.info(f"--- API Request: Create User '{username}' ---")
        
       
        
        new_event = Event(name="USER_REGISTERED", payload={"username": username})
        await bus.publish(new_event)
        
        # 3. Return to the user instantly! (0.01 seconds)
        return {"status": "success", "message": "User created instantly!"}


    async def main():
       
        worker_task = asyncio.create_task(bus.start_worker())

    
        response = await api_create_user("Awonders_Dev")
        logger.info(f"API Response Sent to Browser: {response}")

       
        await bus.queue.join()
        worker_task.cancel() # Shut down the worker

    asyncio.run(main())