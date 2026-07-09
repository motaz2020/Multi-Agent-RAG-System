import logging
import random
import uuid
from datetime import datetime, date, time

logger = logging.getLogger(__name__)

_RESERVATIONS: dict[str, dict] = {}
_BRANCHES = {
    "downtown": {"capacity": 80, "name": "Downtown Branch"},
    "uptown": {"capacity": 60, "name": "Uptown Branch"},
    "riverside": {"capacity": 120, "name": "Riverside Branch"},
}


def check_table_availability(branch: str, date_str: str, time_str: str) -> dict:
    branch_key = branch.lower().strip()
    if branch_key not in _BRANCHES:
        return {
            "available": False,
            "remaining_tables": 0,
            "error": f"Invalid branch '{branch}'. Available branches: downtown, uptown, riverside",
        }

    try:
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return {"available": False, "remaining_tables": 0, "error": f"Invalid date format. Use YYYY-MM-DD"}

    try:
        parsed_time = datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        return {"available": False, "remaining_tables": 0, "error": f"Invalid time format. Use HH:MM (24h)"}

    branch_capacity = _BRANCHES[branch_key]["capacity"]
    tables_per_slot = max(1, branch_capacity // 10)

    reservation_key = f"{branch_key}_{date_str}_{time_str}"
    current_bookings = sum(
        1 for r in _RESERVATIONS.values()
        if r["branch"] == branch_key and r["date"] == date_str and r["time"] == time_str
    )

    remaining = max(0, tables_per_slot - current_bookings)

    logger.info(f"Availability check: {branch} | {date_str} | {time_str} | remaining={remaining}")

    return {
        "available": remaining > 0,
        "remaining_tables": remaining,
        "branch": branch,
        "date": date_str,
        "time": time_str,
    }


def book_table(customer_name: str, branch: str, date_str: str, time_str: str) -> dict:
    availability = check_table_availability(branch, date_str, time_str)
    if not availability.get("available"):
        return {
            "reservation_id": None,
            "status": "failed",
            "error": availability.get("error", "No tables available at this time"),
        }

    if not customer_name or not customer_name.strip():
        return {"reservation_id": None, "status": "failed", "error": "Customer name is required"}

    reservation_id = f"RES-{uuid.uuid4().hex[:8].upper()}"
    branch_key = branch.lower().strip()

    _RESERVATIONS[reservation_id] = {
        "id": reservation_id,
        "customer_name": customer_name.strip(),
        "branch": branch_key,
        "date": date_str,
        "time": time_str,
        "status": "confirmed",
    }

    logger.info(f"Table booked: {reservation_id} | {customer_name} | {branch} | {date_str} | {time_str}")

    return {
        "reservation_id": reservation_id,
        "status": "confirmed",
        "customer_name": customer_name.strip(),
        "branch": branch,
        "date": date_str,
        "time": time_str,
    }


def get_today_special(branch: str) -> dict:
    branch_key = branch.lower().strip()
    if branch_key not in _BRANCHES:
        return {"error": f"Invalid branch '{branch}'. Available branches: downtown, uptown, riverside"}

    specials = {
        "downtown": {
            "meal": "Grilled Salmon with Lemon Butter Sauce",
            "price": 16.99,
            "description": "Fresh Atlantic salmon fillet grilled to perfection, served with seasonal vegetables and lemon butter sauce",
        },
        "uptown": {
            "meal": "Truffle Mushroom Risotto",
            "price": 15.99,
            "description": "Creamy arborio rice with wild mushrooms, truffle oil, and aged parmesan cheese",
        },
        "riverside": {
            "meal": "BBQ Ribs Platter",
            "price": 18.99,
            "description": "Slow-cooked pork ribs glazed with house-made BBQ sauce, served with coleslaw and cornbread",
        },
    }

    special = specials.get(branch_key, {
        "meal": "Chef's Special",
        "price": 14.99,
        "description": "Ask your server for today's special",
    })

    logger.info(f"Today's special for {branch}: {special['meal']}")

    return {
        "branch": branch,
        "meal": special["meal"],
        "price": special["price"],
        "description": special["description"],
    }
