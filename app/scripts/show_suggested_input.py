import logging
import json
import urllib.parse
from app.core.hubscape_adk import get_context

logger = logging.getLogger(__name__)


def show_suggested_input(target: str = "inline") -> dict:
    """Displays an interactive input widget with a dropdown menu of suggested systems.

    The suggested systems are dynamically retrieved from telemetry services and attached
    to the show_widget 'data' parameter, which are then passed into the iframe to
    pre-populate the searchable dropdown. No suggestions are hardcoded in the HTML.

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

    # URL-encode the JSON structure so it safely passes through query parameters
    encoded_suggestions = urllib.parse.quote(json.dumps(dynamic_suggestions))

    data = {
        "title": "Subsystem Search",
        "suggestions": encoded_suggestions
    }

    directive = context.show_widget(
        widget_template_id="suggested_input_widget",
        data=data,
        target="inline"
    )

    return {
        "status": "success",
        "message": "Suggested input widget displayed (target: inline).",
        "directive": directive
    }
