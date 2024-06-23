# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class ResPartner(models.Model):
	_inherit = "res.partner"
	
	fax_no = fields.Char(string='Fax No')
	approved_supplier = fields.Boolean(string='Approved Supplier?')
	not_approved_supplier = fields.Text(string='specify the reason making purchase')