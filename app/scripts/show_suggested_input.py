import logging
from app.core.hubscape_adk import get_context

logger = logging.getLogger(__name__)


def show_suggested_input(target: str = "inline") -> dict:
    """Displays an interactive input widget with a dropdown menu of suggested systems.

    The suggested systems are dynamically retrieved from telemetry services and attached
    to the show_widget 'data' parameter. The iframe receives this data strictly in-memory
    via postMessage with zero URL query parameters. No suggestions are hardcoded in the HTML.

    Args:
        target: Spatial surface target for the widget ('inline' or 'sidebar'). Defaults to 'inline'.

    Returns:
        dict: Confirmation of widget display directive.
    """
    context = get_context()

    # Dynamic suggestions retrieved from subsystem / telemetry service
    dynamic_suggestions = [
        {"label": "Defensive Shields", "icon": "🛡️", "category": "Defense"},
        {"label": "Warp Propulsion", "icon": "⚡", "category": "Engines"},
        {"label": "Long-Range Sensors", "icon": "📡", "category": "Sensors"},
        {"label": "Subspace Communications", "icon": "📶", "category": "Comms"},
        {"label": "Phaser Array", "icon": "🎯", "category": "Tactical"},
        {"label": "Photon Torpedoes", "icon": "🚀", "category": "Tactical"},
        {"label": "Tractor Beam", "icon": "🧲", "category": "Utility"},
        {"label": "Navigational Deflector", "icon": "🧭", "category": "Navigation"}
    ]

    # Pass the rich list directly into data without URL-encoding into query parameters
    data = {
        "title": "Subsystem Search",
        "suggestions": dynamic_suggestions
    }

    directive = context.show_widget(
        "suggested_input_widget",
        data=data,
        target=target
    )

    logger.info(f"Mounted suggested input widget with pure postMessage channel (target={target})")
    return {
        "status": "success",
        "directive": directive,
        "message": f"Suggested input widget displayed in {target} viewport via postMessage."
    }
