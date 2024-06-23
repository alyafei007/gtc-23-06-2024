# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class Picking(models.Model):
	_inherit = 'stock.picking'

	project_id = fields.Many2one('project.project', string='Project')
	delivery_id = fields.Char(string='Delivery No.')
	mr_no = fields.Char(string="Mr No.", readonly=True, required=True, copy=False, default='New')

	@api.model
	def create(self, vals):
		if  vals.get('mr_no','New')=='New':
			vals['mr_no']=self.env['ir.sequence'].next_by_code('material.requisition') or 'New'
			result=super(Picking, self).create(vals)
		return result

class StockMoveLine(models.Model):
	_inherit = 'stock.move.line'


	part_no = fields.Char(related='product_id.part_no', string='Part No.')
	remark = fields.Char(string='Remark')