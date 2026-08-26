import json
import re
from pathlib import Path
from datetime import date

BASE_DIR = Path(__file__).parent

REFERENCE_DATE = date(2026, 7, 29)

# Load orders
with open(BASE_DIR / "orders.json", "r", encoding="utf-8") as file:
    orders_data = json.load(file)

orders = orders_data["orders"]

# Load policy
with open(BASE_DIR / "trendly_policy.md", "r", encoding="utf-8") as file:
    policy = file.read()

policy_sections = re.split(r"\n(?=## )", policy)