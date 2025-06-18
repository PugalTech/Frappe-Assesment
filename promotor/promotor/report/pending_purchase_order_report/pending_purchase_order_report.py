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
        row=[rpt.count]
        data.append(row)
        
    
    
    return columns, data 
    

def get_columns():
    columns=[
    _("Count")+":Data",
    # _("Item Code")+":Data",
    # _("Order Qty")+":Data",
    # _("Qty")+":Data:150"
    
    ]    
    return columns
    


def get_rpt(filters):
    return frappe.db.sql("""  select x.name,count(x.item_code) as count,x.qty as order_qty,nvl(x.qty,0)-nvl(y.received_qty,0) as qty from
 (select tm.name,tx.item_code,sum(tx.qty) as qty from `tabPurchase Order` tm left join `tabPurchase Order Item` tx on tm.name=tx.parent where tm.status = 'To Receive and Bill' and date(now()) > tm.schedule_date group by tm.name,tx.item_code) as x left join (select purchase_order,item_code,sum(received_qty) as received_qty from `tabPurchase Receipt Item` where 1=1 group by purchase_order,item_code ) as y on x.name=y.purchase_order and x.item_code=y.item_code""" , as_dict=1)