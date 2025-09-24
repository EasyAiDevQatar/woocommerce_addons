import frappe
from erpnext.selling.doctype.sales_order.sales_order import make_sales_invoice


def on_update(doc, method):
    """
    On update event for Sales Order
    Automatically create Sales Invoice for WooCommerce orders
    """
    if doc.woocommerce_id and doc.docstatus == 1:
        existing_invoice = frappe.db.exists("Sales Invoice", {"sales_order": doc.name})
        
        if not existing_invoice:
            try:
                sales_invoice = make_sales_invoice(doc.name, ignore_permissions=True)
                
                # sales_invoice.woocommerce_id = doc.woocommerce_id
                
                sales_invoice.save()
                
                sales_invoice.submit()
                
                frappe.msgprint(f"Sales Invoice {sales_invoice.name} created automatically for WooCommerce order {doc.woocommerce_id}")
                
            except Exception as e:
                frappe.log_error(f"Error creating sales invoice for WooCommerce order {doc.woocommerce_id}: {str(e)}")
                frappe.msgprint(f"Error creating sales invoice: {str(e)}", alert=True)
