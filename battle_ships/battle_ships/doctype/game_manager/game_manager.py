# Copyright (c) 2022, Kamal Johnson and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import enqueue

class GameManager(Document):
	@frappe.whitelist()
	def start_battle(self):
		print("\n\n------------------- BATTLE STARTED --------------------\n")
		self.stop_season()
		
		global_board = frappe.get_doc("Global Board")
		global_board.start_battle()

		print("\n------------------- BATTLE ENDED --------------------\n\n")

	def update_player_score(self):
		pass

	def get_board_size(self):
		return list(map(int, self.board_size.split(' ')))

	def stop_season(self):
		print("STOPPING SEASON")
		self.season_paused = True
		self.save()
		frappe.db.commit()

	def start_season(self):
		print("STARTING SEASON")
		self.season_paused = False
		self.save()
		frappe.db.commit()