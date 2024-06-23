# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


class HR_Expense(models.Model):
	_inherit = 'hr.expense'
	
	supplier_name= fields.Char(string='Supplier Name')
	supplier_trn= fields.Char(string='TRN.')


class HrExpenseSheet(models.Model):
	_inherit = 'hr.expense.sheet'

	trans_no = fields.Char(string="Trans No.", readonly=True, required=True, copy=False, default='New')
	project_id = fields.Many2one('account.analytic.account', string='Project')

	@api.model
	def create(self, vals):
		if  vals.get('trans_no','New')=='New':
			vals['trans_no']=self.env['ir.sequence'].next_by_code('transaction.number') or 'New'
			result=super(HrExpenseSheet, self).create(vals)
		return result