// Copyright (c) 2022, Kamal Johnson and contributors
// For license information, please see license.txt

frappe.ui.form.on('Game Manager', {
	refresh: function(frm) {
		frm.add_custom_button(
			__("Battle Now"),
			() => {
				frappe.confirm(
					`Are you sure you want to start a battle now?`,
					() => frm.call('start_battle').then((r) => console.log('battle started!!'))
				);
			},
		);
	}
});
