# Copyright (c) 2023, Regent and contributors
# For license information, please see license.txt

# import frappe


from __future__ import unicode_literals
import frappe
from frappe import msgprint, _

def execute(filters=None):
    if not filters: filters = {}
    
    
    rpt_list = get_rpt(filters)
  
    columns = get_columns()

    if not rpt_list:
        msgprint(_("No record found"))
        return columns, rpt_list

    data = []
    
    
    for rpt in rpt_list:
        row=[
		rpt.name,
		rpt.customer,
		rpt.posting_date,
		rpt.territory,
		rpt.grand_total,
		]
        data.append(row)
        
    
    
    return columns, data 
    

def get_columns():
    columns=[
    _("Name")+":Data",
    _("Customer")+":Data",
    _("Date")+":Date",
    _("Territory")+":Data:150",
    _("Grand Total")+":Data:150"
    
    ]    
    return columns
    
    
def get_conditions(filters):
    conditions = ""
    
    if filters.get("from_date"):
        conditions += "and posting_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += "and posting_date <= %(to_date)s"
    if filters.get("territory"):
        conditions += "and territory = %(territory)s"
    # if filters.get("product"):
        # conditions += "and tx.product = %(product)s"
        
    return conditions


def get_rpt(filters):
    return frappe.db.sql(""" select name,customer,posting_date,territory,grand_total from `tabSales Invoice`""" , as_dict=1)