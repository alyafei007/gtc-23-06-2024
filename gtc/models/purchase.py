# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from num2words import num2words


PURCHASE_REQUISITION_STATES = [
	('draft', 'Draft'),
	('submitted', 'Summitted'),
	('ongoing', 'Ongoing'),
	('in_progress', 'Confirmed'),
	('open', 'Bid Selection'),
	('done', 'Closed'),
	('cancel', 'Cancelled')
]

class PurchaseRequisition(models.Model):
	_inherit = 'purchase.requisition'

	department_id = fields.Many2one('hr.department', string='Department')
	project_id = fields.Many2one('project.project', string='Project')
	justification = fields.Text(string='Justification')
	supplier = fields.Text(string='Supplier')
	recommendation = fields.Text(string='Recommendation')

	state = fields.Selection(PURCHASE_REQUISITION_STATES,
							  'Status', tracking=True, required=True,
							  copy=False, default='draft') 
	state_blanket_order = fields.Selection(PURCHASE_REQUISITION_STATES)

	def purchase_requisition_submitted(self):
		self.ensure_one()
		if not all(obj.line_ids for obj in self):
			raise UserError(_("You cannot confirm agreement '%s' because there is no product line.") % self.name)

		if self.type_id.quantity_copy == 'none' and self.vendor_id:
			for requisition_line in self.line_ids:
				if requisition_line.price_unit <= 0.0:
					raise UserError(_('You cannot confirm the blanket order without price.'))
				if requisition_line.product_qty <= 0.0:
					raise UserError(_('You cannot confirm the blanket order without quantity.'))
				requisition_line.create_supplier_info()
			self.write({'state': 'draft'})
		else:
			self.write({'state': 'submitted'})

class PurchaseRequisitionLine(models.Model):
	_inherit = 'purchase.requisition.line'

	brand = fields.Char(string='Brand')
	part_no = fields.Char(related="product_id.part_no")
	categ_id = fields.Many2one(related="product_id.categ_id")
	account_analytic_id = fields.Many2one(compute='_compute_account_analytic', store=True)
	product_qty_available = fields.Float(string='Quantity On Hand', related='product_id.qty_available', readonly=True)
	
	@api.depends('requisition_id.project_id')
	def _compute_account_analytic(self):
		for line in self:
			if line.requisition_id.project_id.analytic_account_id:
				line.account_analytic_id = line.requisition_id.project_id.analytic_account_id

class PurchaseOrder(models.Model):
	_inherit = 'purchase.order'

	total_in_words = fields.Text('Total in Words', compute="_defiend_words")

	@api.depends('amount_total')
	def _defiend_words(self):
		lang = self.partner_id and self.partner_id.lang[:2]
		try:
			test = num2words(42, lang=lang, to='currency')
		except NotImplementedError:
			lang = 'en'
		total_in_words = num2words(self.amount_total,lang=lang, to='currency').title()
		total_in_words = total_in_words.replace('Euro', self.currency_id.currency_unit_label + 's')
		if self.currency_id.name == 'AED':
			self.total_in_words = total_in_words.replace('Cents', 'Fills')
		else:
			self.total_in_words = total_in_words

	delivary_mod = fields.Text(string='Delivery mode & Address')
	project_id = fields.Many2one('project.project', related="requisition_id.project_id")

class PurchaseOrderLine(models.Model):
	_inherit = 'purchase.order.line'

	part_no = fields.Char(related="product_id.part_no")
	account_analytic_id = fields.Many2one(compute='_compute_account_analytic', store=True)
	
	@api.depends('order_id.project_id')
	def _compute_account_analytic(self):
		for line in self:
			if line.order_id.project_id.analytic_account_id:
				line.account_analytic_id = line.order_id.project_id.analytic_account_id


