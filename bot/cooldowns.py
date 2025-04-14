import time
import logging
from config.config import COOLDOWN_TIME

logger = logging.getLogger("discord")

# Replace hardcoded cooldown time with centralized configuration
COOLDOWN_SECONDS = COOLDOWN_TIME

# Store cooldowns by user ID
user_cooldowns = {}


def is_on_cooldown(user_id: int) -> bool:
    """
    Returns True if the user is still on cooldown.

    Args:
        user_id (int): The ID of the user.

    Returns:
        bool: True if the user is on cooldown, False otherwise.
    """
    now = time.time()
    last_used = user_cooldowns.get(user_id, 0)
    return (now - last_used) < COOLDOWN_SECONDS


def update_cooldown(user_id: int) -> None:
    """
    Resets the cooldown timer for a user.

    Args:
        user_id (int): The ID of the user.
    """
    user_cooldowns[user_id] = time.time()
    logger.info(f"Cooldown updated for user {user_id}.")
