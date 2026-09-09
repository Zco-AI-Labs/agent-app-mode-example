import logging
from app.core.hubscape_adk import get_context

logger = logging.getLogger(__name__)


def open_tactical_sidebar() -> dict:
    """Docks the tactical systems console in the persistent 384px Side Bar.
    
    Provides continuous monitoring and quick power diversion controls for defensive shields,
    warp engines, sensor telemetry, and structural integrity.

    Returns:
        dict: Confirmation of sidebar docking.
    """
    context = get_context()
    data = {
        "shields_power": 90,
        "warp_power": 65,
        "sensors_power": 85
    }
    
    directive = context.show_widget(
        widget_template_id="tactical_systems_sidebar",
        data=data,
        target="sidebar"
    )
    
    return {
        "status": "success",
        "message": "Tactical systems console docked in the Side Bar.",
        "directive": directive
    }
