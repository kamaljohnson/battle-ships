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
		self.participated = True
		self.save(ignore_permissions=True)

		return frappe.get_doc("Player Board", self.player_board).update_formation(formation)
	
	def get_formation(self):
		return frappe.get_doc("Player Board", self.player_board).get_formation()

	def compute_score(self):
		global_board = frappe.get_doc("Global Board")
		
		attacked_coordinates = json.loads(global_board.attacked_coordinates)

		# TODO: check how many ships sank


		# TODO: check how many best ship coordinates
		# TODO: check attack value