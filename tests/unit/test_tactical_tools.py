import pytest
from unittest.mock import MagicMock
from app.core import hubscape_adk
from app.scripts.show_tactical_status import show_tactical_status
from app.scripts.open_tactical_sidebar import open_tactical_sidebar
from app.scripts.launch_tactical_app import launch_tactical_app
from app.scripts.save_tactical_state import save_tactical_state


def test_show_tactical_status_tool():
    ctx = hubscape_adk.RemoteContext(
        user_id="riker_user_1",
        agent_id="tactical_ops"
    )
    
    with hubscape_adk.context_session(ctx):
        res = show_tactical_status()
        
    assert res["status"] == "success"
    assert "briefing displayed inline" in res["message"]
    
    # Verify action registered on context
    assert len(ctx.actions) == 1
    action = ctx.actions[0]
    assert action["type"] == "OPEN_AGENT_WIDGET"
    assert action["payload"]["target"] == "inline"
    assert action["payload"]["widgetId"] == "tactical_status_card"
    
    # Check data interpolation
    data = action["payload"]["data"]
    assert data["shields_level"] == "100%"
    assert data["warp_status"] == "ONLINE"
    assert data["sensors_status"] == "ACTIVE"


def test_open_tactical_sidebar_tool():
    ctx = hubscape_adk.RemoteContext(
        user_id="riker_user_1",
        agent_id="tactical_ops"
    )
    
    with hubscape_adk.context_session(ctx):
        res = open_tactical_sidebar()
        
    assert res["status"] == "success"
    assert "docked in the Side Bar" in res["message"]
    
    assert len(ctx.actions) == 1
    action = ctx.actions[0]
    assert action["type"] == "OPEN_AGENT_WIDGET"
    assert action["payload"]["target"] == "sidebar"
    assert action["payload"]["widgetId"] == "tactical_systems_sidebar"
    
    data = action["payload"]["data"]
    assert data["shields_power"] == 90
    assert data["warp_power"] == 65
    assert data["sensors_power"] == 85


def test_launch_tactical_app_tool():
    ctx = hubscape_adk.RemoteContext(
        user_id="riker_user_1",
        agent_id="tactical_ops"
    )
    
    with hubscape_adk.context_session(ctx):
        res = launch_tactical_app(alert_level="YELLOW")
        
    assert res["status"] == "success"
    assert "App Mode (Condition YELLOW)" in res["message"]
    
    assert len(ctx.actions) == 1
    action = ctx.actions[0]
    assert action["type"] == "OPEN_AGENT_WIDGET"
    assert action["payload"]["target"] == "app_mode"
    assert action["payload"]["widgetId"] == "tactical_console"
    assert action["payload"]["title"] == "Tactical Operations Console"
    assert action["payload"]["icon"] == "Command"
    
    app_config = action["payload"]["appConfig"]
    assert app_config["appId"] == "tactical_console"
    assert app_config["canvasWidget"]["widgetId"] == "tactical_canvas"
    assert app_config["canvasWidget"]["data"]["alert_level"] == "YELLOW"
    assert app_config["remoteWidget"]["widgetId"] == "tactical_remote"
    assert app_config["remoteWidget"]["data"]["alert_level"] == "YELLOW"
    
    # Check toolbar save action
    assert len(app_config["actions"]) == 1
    save_act = app_config["actions"][0]
    assert save_act["id"] == "save_state"
    assert save_act["actionType"] == "chat_command"
    assert save_act["showFeedback"] is True


def test_save_tactical_state_tool():
    ctx = hubscape_adk.RemoteContext(
        user_id="riker_user_1",
        agent_id="tactical_ops"
    )
    
    mock_db = MagicMock()
    mock_doc = MagicMock()
    mock_snap = MagicMock()
    mock_snap.exists = False
    mock_doc.get.return_value = mock_snap
    mock_db.document.return_value = mock_doc
    ctx._db = mock_db
    
    with hubscape_adk.context_session(ctx):
        res = save_tactical_state(
            alert_level="RED",
            shields_power=100,
            warp_power=50,
            sensors_power=75
        )
        
    assert res["status"] == "success"
    assert "saved to user profile" in res["message"]
    
    saved = res["saved_settings"]
    assert saved["alert_level"] == "RED"
    assert saved["shields_power"] == 100
    assert saved["warp_power"] == 50
    assert saved["sensors_power"] == 75
    assert saved["version"] == 1
    assert saved["created_by"] == "riker_user_1"
    
    expected_doc_path = ctx.get_agent_db_path("user", "tactical_console", "settings")
    mock_db.document.assert_called_with(expected_doc_path)
    mock_doc.set.assert_called_once()
