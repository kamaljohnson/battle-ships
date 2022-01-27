import frappe

@frappe.whitelist(allow_guest=True)
def upload_formation(player_id, formation):
    player = frappe.get_doc("Player", player_id)
    return player.update_formation(formation)

@frappe.whitelist(allow_guest=True)
def fetch_formation(player_id):
    player = frappe.get_doc("Player", player_id)
    return player.get_formation()

@frappe.whitelist(allow_guest=True)
def create_session_player():
    new_player = frappe.new_doc("Player").insert(ignore_permissions=True)
    return new_player.name

@frappe.whitelist(allow_guest=True)
def fetch_board_size():
    return frappe.get_doc("Game Manager").get_board_size()

@frappe.whitelist(allow_guest=True)
def check_and_fetch_battle_results(player_id):
    return frappe.get_doc("Player", player_id).check_and_get_battle_results()

@frappe.whitelist(allow_guest=True)
def play_again(player_id):
    return frappe.get_doc("Player", player_id).play_again()

@frappe.whitelist(allow_guest=True)
def fetch_session_players_left():
    return frappe.get_doc("Game Manager").get_session_players_left()