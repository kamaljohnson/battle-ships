import frappe

@frappe.whitelist(allow_guest=True)
def upload_result(player_id, result):
    print(f"PLAYER ID: {player_id}")
    print(f"RESULT: {result}")

@frappe.whitelist(allow_guest=True)
def create_session_player():
    new_player = frappe.new_doc("Player")
    new_player.insert()
    return new_player.name