import pytest
from app.core import hubscape_adk
from app.scripts.show_suggested_input import show_suggested_input


def test_show_suggested_input_purely_from_data():
    ctx = hubscape_adk.RemoteContext(
        user_id="riker_user_1",
        agent_id="tactical_ops"
    )

    with hubscape_adk.context_session(ctx):
        res = show_suggested_input(target="inline")

    assert res["status"] == "success"
    assert "Suggested input widget displayed" in res["message"]

    assert len(ctx.actions) == 1
    action = ctx.actions[0]
    assert action["type"] == "OPEN_AGENT_WIDGET"
    assert action["payload"]["target"] == "inline"
    assert action["payload"]["widgetId"] == "suggested_input_widget"
    assert action["payload"]["widgetConfig"]["type"] == "container"

    # Verify data contains dynamic pure python suggestions list
    data = action["payload"]["data"]
    assert "suggestions" in data
    assert isinstance(data["suggestions"], list)
    assert len(data["suggestions"]) >= 5
    assert data["suggestions"][0]["label"] == "Defensive Shields"

    # Verify iframe src is completely clean with ZERO query parameters
    iframe_child = action["payload"]["widgetConfig"]["children"][0]
    assert iframe_child["type"] == "iframe"
    src = iframe_child["props"]["src"]
    assert src == "/api/agents/tactical_ops/static/suggested_input.html"
    assert "?" not in src
