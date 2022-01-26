# Copyright (c) 2022, Kamal Johnson and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GameManager(Document):
	@frappe.whitelist()
	def start_battle(self):
		print("------------------- BATTLE STARTED --------------------")
		self.season_paused = True
		self.save()

		global_board = frappe.get_doc("Global Board")
		global_board.start_battle()

	def get_board_size(self):
		return list(map(int, self.board_size.split(' ')))