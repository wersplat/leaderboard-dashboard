def is_admin(user_id: int) -> bool:
    # Check if the user is an admin
    return user_id in ADMIN_IDS

def is_on_cooldown(user_id: int) -> bool:
    # Check if the user is on cooldown
    return user_id in COOLDOWN_USERS
