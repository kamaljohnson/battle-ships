import frappe

@frappe.whitelist(allow_guest=True)
def upload_result(player_id, result):
    print(f"PLAYER ID: {player_id}")
    print(f"RESULT: {result}")