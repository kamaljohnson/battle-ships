# Copyright (c) 2022, Kamal Johnson and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GlobalBoard(Document):
	def start_battle(self):
		self.set_global_formation()

	def set_global_formation(self):
		all_player_boards = frappe.get_all("Player Board")

		self.ships = []
		self.attacks = []

		board_size = frappe.get_doc("Game Manager").get_board_size()

		for board in all_player_boards:
			pass