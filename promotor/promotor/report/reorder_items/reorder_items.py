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
		rpt.item_code,
		rpt.warehouse,
		rpt.actual_qty,
		rpt.count
		]
        data.append(row)
        
    
    
    return columns, data 
    

def get_columns():
    columns=[
    _("Item_code")+":Data",
    _("Warehouse")+":Data",
    _("Stock Qty")+":Data",
    _("Count")+":Integer"
    # _("Item Name")+":Data:150",
    # _("Warehouse")+":Data:150",
    # _("Actual Qty")+":Float:150",
    # _("Safety Stock")+":Float:150"
    
    ]    
    return columns
    
    
def get_conditions(filters):
    conditions = ""
    
    if filters.get("warehouse"):
        conditions += "and b.warehouse = %(warehouse)s"
        
    return conditions

# def get_rpt(filters):
    # conditions = get_conditions(filters)
    # return frappe.db.sql(""" select 'Reorder Items' as item,sum(below_reorder_level) as below_reorder_level,sum(above_reorder_level)  as above_reorder_level from (
 # SELECT 0 as below_reorder_level,count(i.item_code) as above_reorder_level  FROM `tabBin` b RIGHT JOIN `tabItem` i ON b.item_code = i.item_code WHERE NVL(b.actual_qty,0) > nvl(i.safety_stock,0)
 # union all
 # SELECT count(i.item_code) as below_reorder_level,0 as above_reorder_level FROM `tabBin` b RIGHT JOIN `tabItem` i ON b.item_code = i.item_code WHERE NVL(b.actual_qty,0) <= nvl(i.safety_stock,0)) as x where 1=1 %s """ %
        # conditions, filters, as_dict=1)
def get_rpt(filters):
    conditions = get_conditions(filters)
    return frappe.db.sql(""" SELECT i.item_code,i.item_name,1 as count,b.warehouse,NVL(b.actual_qty,0) actual_qty,nvl(i.safety_stock,0) as safety_stock FROM `tabBin` b RIGHT JOIN `tabItem` i ON b.item_code = i.item_code WHERE NVL(b.actual_qty,0) <= nvl(i.safety_stock,0) %s """ %
        conditions, filters, as_dict=1)