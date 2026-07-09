import pytest

from ai.tools.restaurant_tools import check_table_availability, book_table, get_today_special
from ai.tools.registry import ToolRegistry, get_registry


class TestCheckAvailability:
    def test_valid_branch(self):
        result = check_table_availability("downtown", "2026-07-10", "19:00")
        assert "available" in result
        assert "remaining_tables" in result

    def test_invalid_branch(self):
        result = check_table_availability("invalid_branch", "2026-07-10", "19:00")
        assert result["available"] is False
        assert "error" in result

    def test_invalid_date(self):
        result = check_table_availability("downtown", "not-a-date", "19:00")
        assert result["available"] is False
        assert "error" in result


class TestBookTable:
    def test_successful_booking(self):
        result = book_table("John Doe", "uptown", "2026-07-11", "20:00")
        assert result["status"] == "confirmed"
        assert result["reservation_id"].startswith("RES-")
        assert result["customer_name"] == "John Doe"

    def test_empty_name(self):
        result = book_table("", "downtown", "2026-07-11", "20:00")
        assert result["status"] == "failed"
        assert "error" in result

    def test_invalid_branch(self):
        result = book_table("John Doe", "invalid", "2026-07-11", "20:00")
        assert result["status"] == "failed"


class TestTodaySpecial:
    def test_valid_branch_special(self):
        result = get_today_special("downtown")
        assert "meal" in result
        assert "price" in result
        assert "description" in result

    def test_all_branches_have_specials(self):
        for branch in ["downtown", "uptown", "riverside"]:
            result = get_today_special(branch)
            assert result["meal"] is not None
            assert isinstance(result["price"], float)

    def test_invalid_branch(self):
        result = get_today_special("unknown")
        assert "error" in result


class TestToolRegistry:
    def test_registry_initialization(self):
        registry = ToolRegistry()
        assert registry.list_tools() == []

    def test_register_and_execute(self):
        registry = ToolRegistry()

        def mock_tool(**kwargs):
            return {"result": "success"}

        registry.register("test_tool", mock_tool)
        assert "test_tool" in registry.list_tools()

        result = registry.execute("test_tool", key="value")
        assert result.status == "success"

    def test_execute_unknown_tool(self):
        registry = ToolRegistry()
        result = registry.execute("nonexistent")
        assert result.status == "error"

    def test_default_registry_has_three_tools(self):
        registry = get_registry()
        tools = registry.list_tools()
        assert "check_table_availability" in tools
        assert "book_table" in tools
        assert "get_today_special" in tools
