# Copyright (c) 2022, Kamal Johnson and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class PlayerBoard(Document):
	def update_formation(self, formation):
		if formation:
			ship_coordinate_str = ''
			attach_coordinate_str = ''
			for ship_coordinate in formation['shipCoordinates']:
				ship_coordinate_str += ''.join(list(map(str, ship_coordinate)))
				if ship_coordinate != formation['shipCoordinates'][-1]: ship_coordinate_str += ' '
			for attach_coordinate in formation['attackCoordinates']:
				attach_coordinate_str += ''.join(list(map(str, attach_coordinate)))
				if attach_coordinate != formation['attackCoordinates'][-1]: attach_coordinate_str += ' '

			self.ship_coordinates = ship_coordinate_str
			self.attack_coordinates = attach_coordinate_str
			self.save()
		
	def get_formation(self):
		return self.get_formation_as_dict()

	def get_formation_as_dict(self):
		formation_dict = {'ship_coordinates': [], 'attack_coordinates': []}

		for ship_coordinate in self.ship_coordinates.split(' '):
			formation_dict['ship_coordinates'].append(list(ship_coordinate))
		for attack_coordinate in self.attack_coordinates.split(' '):
			formation_dict['attack_coordinates'].append(list(attack_coordinate))
		
		return formation_dict