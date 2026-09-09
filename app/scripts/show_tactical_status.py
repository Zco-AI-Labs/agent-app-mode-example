import logging
from app.core.hubscape_adk import get_context

logger = logging.getLogger(__name__)


def show_tactical_status() -> dict:
    """Displays a tactical status briefing card inline in the chat flow.
    
    Reports the primary readiness and operational state of the USS Hubscape defensive shields,
    warp drive, and sensor arrays.

    Returns:
        dict: Confirmation of widget rendering and tactical status parameters.
    """
    context = get_context()
    data = {
        "shields_level": "100%",
        "warp_status": "ONLINE",
        "sensors_status": "ACTIVE"
    }
    
    directive = context.show_widget(
        widget_template_id="tactical_status_card",
        data=data,
        target="inline"
    )
    
    return {
        "status": "success",
        "message": "Tactical status briefing displayed inline in the chat log.",
        "directive": directive
    }
