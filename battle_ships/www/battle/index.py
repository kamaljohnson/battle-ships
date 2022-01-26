import frappe

@frappe.whitelist(allow_guest=True)
def upload_formation(player_id, formation):
    player = frappe.get_doc("Player", player_id)
    player.update_formation(formation)

@frappe.whitelist(allow_guest=True)
def create_session_player():
    new_player = frappe.new_doc("Player").insert()
    return new_player.name