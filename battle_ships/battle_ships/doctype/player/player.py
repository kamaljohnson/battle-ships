# Copyright (c) 2022, Kamal Johnson and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document
import json

class Player(Document):
	def before_insert(self):
		if not self.player_board:
			self.player_board = frappe.new_doc("Player Board").insert().name

	def update_formation(self, formation):
		formation = json.loads(formation)

		frappe.get_doc("Player Board", self.player_board).update_formation(formation)