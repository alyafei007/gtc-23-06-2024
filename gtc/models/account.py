# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError, Warning


class AccountMove(models.Model):
    _inherit = "account.move"

    pm_no = fields.Char(string="PM No.", readonly=True, required=True, copy=False, default='New')

    @api.model
    def create(self, vals):
        res = super(AccountMove, self).create(vals)
        type = res.type
        if type == 'in_invoice':

            if vals.get('pm_no', 'New') == 'New':
                res.pm_no = self.env['ir.sequence'].next_by_code('account.payment.memo') or 'New'
        return res

    def action_payment_memo(self):
        if self.invoice_origin:
            purchase = self.env['purchase.order'].search([('name', '=', self.invoice_origin)])
            if purchase:
                self.po_no = purchase
        self.post()

    @api.model
    def update_po_no(self):
        for bill in self.search([('type', '=', 'in_invoice'), ('invoice_origin', '!=', False), ('po_no', '=', False)]):
            purchase = self.env['purchase.order'].search([('name', '=', bill.invoice_origin)], limit=1)
            if purchase:
                bill.po_no = purchase


    # pr_no = fields.Char(string='Pr No.')
    po_no = fields.Many2one('purchase.order', string="Purchase Order")


#Override this function becuase we have to display purchase order tags on Onchange of purchase order id
    # @api.onchange('purchase_vendor_bill_id', 'purchase_id')
    # def _onchange_purchase_auto_complete(self):
    #
    #     self.po_no = self.purchase_id.name
    #     self.pr_no = self.purchase_id.requisition_id.name
