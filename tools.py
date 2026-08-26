from datetime import datetime

from data import orders, policy_sections, REFERENCE_DATE

#TOOL 1 - to get order

def get_order(order_id):
    for order in orders:
        if order["order_id"] == order_id:
            return order

    return {
        "error": "Order not found"
    }

#TOOL 2 - to search policy

def search_policy(topic):
    topic = topic.lower()

    keywords = {
        "shipping": "## 1. Shipping",
        "delivery": "## 1. Shipping",
        "delayed": "## 1. Shipping",
        "lost": "## 1. Shipping",
        "address": "## 1. Shipping",

        "return": "## 2. Returns",
        "non-returnable": "## 2. Returns",
        "final sale": "## 2. Returns",

        "refund": "## 3. Refunds",
        "cash": "## 3. Refunds",

        "exchange": "## 4. Exchanges",
        "size": "## 4. Exchanges",

        "pickup": "## 5. Return pickup",

        "damaged": "## 6. Damaged or wrong items",
        "wrong item": "## 6. Damaged or wrong items"
    }

    section_name = None

    for keyword, section in keywords.items():
        if keyword in topic:
            section_name = section
            break

    if not section_name:
        return {
            "error": "The policy does not contain information about this topic."
        }

    for section in policy_sections:
        if section.startswith(section_name):
            return section

    return {
        "error": "The policy section could not be found."
    }

#TOOL 3 - Check the return or exchange eligibility

def check_eligibility(order_id, item_sku, action):
    order = get_order(order_id)

    if "error" in order:
        return order

    if order["status"] == "cancelled":
        return {

            "eligible": False,
            "reason": "Cancelled orders cannot have a return raised."
        }

    if order["status"] == "lost_in_transit":
        return {

            "eligible": False,
            "reason": "This is a lost-parcel claim and must be handled by a human."
        }

    

    # Order must have been delivered
    if not order.get("delivered_at"):
        return {
            "eligible": False,
            "reason": "The order has not been delivered yet."
        }

    # Find the item
    item = None

    for product in order["items"]:
        if product["sku"] == item_sku:
            item = product
            break

    if item is None:
        return {
            "eligible": False,
            "reason": "The item was not found in this order."
        }

    # Check 30-day return/exchange window
    delivered_date = datetime.fromisoformat(
        order["delivered_at"].replace("Z", "+00:00")
    ).date()


    days_since_delivery = (REFERENCE_DATE - delivered_date).days

    if days_since_delivery > 30:
        return {
            "eligible": False,
            "reason": "The 30-day return/exchange window has expired."
        }

    # Non-returnable categories
    non_returnable = [
        "innerwear",
        "jewellery",
        "beauty",
        "fragrance",
        "face_masks",
        "gift_cards"
    ]

    if item["category"] in non_returnable:
        return {
            "eligible": False,
            "reason": f"{item['category']} items cannot be returned or exchanged."
        }

    # Final sale items
    if item.get("final_sale", False):
        if action == "size_exchange":
            return {
                "eligible": True,
                "reason": "Final-sale items are eligible for size exchange only."
            }

        return {
            "eligible": False,
            "reason": "Final-sale items are eligible for size exchange only."
        }

    # Colour/style exchanges are not allowed
    if action in ["colour_exchange", "style_exchange"]:
        return {
            "eligible": False,
            "reason": "Trendly only supports size exchanges."
        }

    # Normal return or size exchange
    if action in ["return", "size_exchange"]:
        return {
            "eligible": True,
            "reason": "The item is eligible."
        }

    return {
        "eligible": False,
        "reason": "This type of request is not supported."
    }

#TOOL 4 - Creating the return

def create_return(order_id, item_sku, action):
    eligibility = check_eligibility(
        order_id,
        item_sku,
        action
    )

    if not eligibility.get("eligible"):
        return {
            "success": False,
            "reason": eligibility.get("reason")
        }

    return {
        "success": True,
        "request_id": f"RET-{order_id[-4:]}",
        "order_id": order_id,
        "item_sku": item_sku,
        "action": action
    }

#TOOL 5 - Escalate to human

def escalate(order_id, reason):
    return {
        "escalated": True,
        "order_id": order_id,
        "reason": reason,
        "message": "This issue has been escalated to a human support agent."
    }

