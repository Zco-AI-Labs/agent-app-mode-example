import logging
from typing import Optional
from app.core.hubscape_adk import get_context

logger = logging.getLogger(__name__)


def save_tactical_state(
    alert_level: str = "GREEN",
    shields_power: int = 100,
    warp_power: int = 80,
    sensors_power: int = 90
) -> dict:
    """Persists current tactical console settings and subsystem power allocations to the user's scoped database.
    
    Data is stored under scope='user' at platform_users/{userId}/agent_data/{agentId}/tactical_console/settings.

    Args:
        alert_level: Current condition status ('GREEN', 'YELLOW', or 'RED'). Defaults to 'GREEN'.
        shields_power: Shields subsystem power percentage (0-100). Defaults to 100.
        warp_power: Warp core power percentage (0-100). Defaults to 80.
        sensors_power: Sensor array power percentage (0-100). Defaults to 90.

    Returns:
        dict: Confirmation containing the saved record, version, and timestamp metadata.
    """
    context = get_context()
    
    settings_data = {
        "alert_level": alert_level.upper(),
        "shields_power": int(shields_power),
        "warp_power": int(warp_power),
        "sensors_power": int(sensors_power)
    }
    
    saved_record = context.save(
        scope="user",
        collection_name="tactical_console",
        doc_id="settings",
        data=settings_data
    )
    
    return {
        "status": "success",
        "message": f"Tactical configuration saved to user profile (Version {saved_record.get('version', 1)}).",
        "saved_settings": saved_record
    }
