# Copyright (c) 2022, Kamal Johnson and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class PlayerBoard(Document):
	def update_formation(self, formation):
		if(formation):
			ship_coordinate_str = ''
			attach_coordinate_str = ''
			for ship_coordinate in formation['shipCoordinates']:
				ship_coordinate_str += ''.join(list(map(str, ship_coordinate))) + ' '
			for attach_coordinate in formation['attackCoordinates']:
				attach_coordinate_str += ''.join(list(map(str, attach_coordinate))) + ' '

			self.ship_coordinates = ship_coordinate_str
			self.attack_coordinates = attach_coordinate_str
			self.save()