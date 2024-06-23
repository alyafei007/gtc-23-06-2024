# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError, Warning


class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    maintenance_ids = fields.Many2many('maintenance.equipment', 'maintenance_equipment_transaction_rel', 'product_template_id', 'maintenance_id',
                                       string='Machines & Tools', copy=False)


class MaintenanceEquipment(models.Model):
	_inherit = "maintenance.equipment"
	

	equipment_id_no= fields.Char(string='Equipment ID No.')
	equipment_part_no= fields.Char(string='Part No.')
	equipment_manufacturer= fields.Char(string='Manufacturer or Brand')
	equipment_country_id= fields.Many2one('res.country', string='Country of Origin', tracking=True)

	
class MaintenanceRequest(models.Model):
	_inherit = "maintenance.request"

	# @api.model
	# def create(self, vals):
	# 	if  vals.get('name','New')=='New':
	# 		vals['name']=self.env['ir.sequence'].next_by_code('maintenance.request') or 'New'
	# 		result=super(MaintenanceRequest, self).create(vals)
	# 	return result

	priority = fields.Selection([('0', 'Low'), ('1', 'Medium'), ('2', 'High'), ('3', 'Emergency')], string='Priority')
	order_no= fields.Char(string='Work Order No.', readonly=True, required=True, copy=False, default='New')
	breakdown = fields.Boolean('Breakdown', default=False)
	repair = fields.Boolean('Repair', default=False)
	routine = fields.Boolean('Routine', default=False)
	rework = fields.Boolean('Rework', default=False)
	installation = fields.Boolean('Installation', default=False)
	fabrication = fields.Boolean('Fabrication', default=False)
	services = fields.Boolean('Services', default=False)
	services_text = fields.Char()
	others = fields.Boolean('Others', default=False)
	others_text = fields.Char()