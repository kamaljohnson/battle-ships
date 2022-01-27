# Copyright (c) 2022, Kamal Johnson and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json

class PlayerBoard(Document):
	def update_formation(self, formation):
		if formation:
			game_manager = frappe.get_doc("Game Manager")
			if game_manager.season_paused:
				return 'Season Paused'

			ship_coordinates = []
			attack_coordinates = []
			for coordinate in formation['shipCoordinates']:
				ship_coordinates.append(str(coordinate))

			for coordinate in formation['attackCoordinates']:
				attack_coordinates.append(str(coordinate))

			self.ship_coordinates = json.dumps(ship_coordinates)
			self.attack_coordinates = json.dumps(attack_coordinates)
			self.save(ignore_permissions=True)
			frappe.db.commit()

			game_manager.update_session_players_left()
			return
		
	def get_formation(self):
		sc = json.loads('[]' if self.ship_coordinates == '' else self.ship_coordinates)
		ac = json.loads('[]' if self.attack_coordinates == '' else self.attack_coordinates)

		ship_coordinates = []
		attack_coordinates = []

		for c in sc:
			ship_coordinates.append(json.loads(c))

		for c in ac:
			attack_coordinates.append(json.loads(c))

		formation = {
			'ship_coordinates': ship_coordinates,
			'attack_coordinates': attack_coordinates
		}
		return formation

	def clear_board(self):
		self.ship_coordinates = ''
		self.attack_coordinates = ''
		self.save(ignore_permissions=True)
		frappe.db.commit()