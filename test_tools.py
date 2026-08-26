from tools import (
    get_order,
    search_policy,
    check_eligibility,
    create_return,
    escalate
)


print("\n--- ORDER LOOKUP ---")
print(get_order("TR-4530"))


print("\n--- POLICY ---")
print(search_policy("shipping"))


print("\n--- VALID RETURN ---")
print(
    check_eligibility(
        "TR-4530",
        "TR-KRT-033",
        "return"
    )
)


print("\n--- JEWELLERY ---")
print(
    check_eligibility(
        "TR-4527",
        "TR-EAR-042",
        "return"
    )
)


print("\n--- FINAL SALE ---")
print(
    check_eligibility(
        "TR-4528",
        "TR-SHR-009",
        "return"
    )
)


print("\n--- LOST ORDER ---")
print(get_order("TR-4526"))


print("\n--- CREATE RETURN ---")
print(
    create_return(
        "TR-4530",
        "TR-KRT-033",
        "return"
    )
)


print("\n--- ESCALATE ---")
print(
    escalate(
        "TR-4526",
        "Lost parcel must be handled by a human."
    )
)

print("\n--- EXPIRED RETURN ---")
print(
    check_eligibility(
        "TR-4523",
        "TR-JKT-008",
        "return"
    )
)


print("\n--- CANCELLED ORDER ---")
print(
    check_eligibility(
        "TR-4529",
        "TR-SCF-027",
        "return"
    )
)


print("\n--- LOST PARCEL ELIGIBILITY ---")
print(
    check_eligibility(
        "TR-4526",
        "TR-BAG-011",
        "return"
    )
)