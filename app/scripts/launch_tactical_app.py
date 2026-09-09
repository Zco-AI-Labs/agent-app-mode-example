import json
import logging
import os
from typing import Optional
from app.core.hubscape_adk import get_context

logger = logging.getLogger(__name__)


def _load_widget_json(filename: str) -> dict:
    """Helper to locate and load widget JSON from app/ui/widgets or app/widgets."""
    app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_name = filename if filename.endswith(".json") else f"{filename}.json"
    
    primary_path = os.path.join(app_dir, "ui", "widgets", target_name)
    fallback_path = os.path.join(app_dir, "widgets", target_name)
    
    selected_path = primary_path if os.path.exists(primary_path) else fallback_path
    if not os.path.exists(selected_path):
        raise FileNotFoundError(f"Widget template {target_name} not found in {primary_path} or {fallback_path}")
        
    with open(selected_path, "r", encoding="utf-8") as f:
        return json.load(f)


def launch_tactical_app(alert_level: str = "GREEN") -> dict:
    """Launches full-screen App Mode for the Tactical Operations Console.
    
    Transitions the client interface to a dual-surface tactical console:
    1. Full-screen canvas stage with deep subsystem monitoring gauges and telemetry graphs.
    2. Companion remote dock pinned to the top 65% of the Side Bar with quick tactical actions.
    3. Integrated chat feed pinned in the bottom 35% of the Side Bar for real-time interaction.
    4. Top application bar featuring title, Command icon, and state persistence save action.

    Args:
        alert_level: Operational condition ('GREEN', 'YELLOW', or 'RED'). Defaults to 'GREEN'.

    Returns:
        dict: Confirmation of App Mode launch directive.
    """
    context = get_context()
    
    canvas_config = _load_widget_json("tactical_canvas")
    remote_config = _load_widget_json("tactical_remote")
    
    canvas_widget = {
        "widgetId": "tactical_canvas",
        "widgetConfig": canvas_config,
        "data": {
            "alert_level": alert_level.upper(),
            "shields_power": 100,
            "warp_power": 80,
            "sensors_power": 90
        }
    }
    
    remote_widget = {
        "widgetId": "tactical_remote",
        "widgetConfig": remote_config,
        "data": {
            "alert_level": alert_level.upper()
        }
    }
    
    actions = [
        {
            "id": "save_state",
            "label": "Save Console Settings",
            "icon": "Save",
            "actionType": "chat_command",
            "command": "Save current tactical settings",
            "showFeedback": True
        }
    ]
    
    directive = context.launch_app_mode(
        app_id="tactical_console",
        canvas_widget=canvas_widget,
        remote_widget=remote_widget,
        title="Tactical Operations Console",
        icon="Command",
        actions=actions
    )
    
    return {
        "status": "success",
        "message": f"Tactical Operations Console launched in App Mode (Condition {alert_level.upper()}).",
        "directive": directive
    }
