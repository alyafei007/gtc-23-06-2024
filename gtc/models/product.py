# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError, Warning

class ProductTemplate(models.Model):
	_inherit = "product.template"
	
	part_no = fields.Char(string='Part No.')
	


class ProductProduct(models.Model):
	_inherit = "product.product"
	
	part_no = fields.Char(related="product_tmpl_id.part_no", store=True)
        