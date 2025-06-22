// Copyright (c) 2025, none and contributors
// For license information, please see license.txt

frappe.ui.form.on('Weather Log', {
	 refresh(frm) {
        frm.add_custom_button("Fetch Weather", function () {
            frappe.prompt([
                {
                    label: "City",
                    fieldname: "city",
                    fieldtype: "Data",
                    reqd: 1
                }
            ], function (values) {
                frappe.call({
                    method: "promotor.promotor.api_integration.fetch_weather_data",
                    args: {
                        city: values.city
                    },
                    callback: function (r) {
                        if (r.message) {
                            frm.set_value("city", values.city);
                            frm.set_value("temperature", r.message.temperature);
                            frm.set_value("description", r.message.description);
                            frm.set_value("response_json", JSON.stringify(r.message.response_json));
                        }
                    }
                });
            });
        });
    }
});
