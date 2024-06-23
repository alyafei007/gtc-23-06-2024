from odoo import api, fields, models, _

class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    maintenance_ids = fields.Many2many('maintenance.equipment', 'maintenance_equipment_transaction_rel', 'product_template_id', 'maintenance_id',
                                       string='Machines & Tools', copy=False)
    
    
class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"
    
    def show_product_template(self):
        
        return {
            'name': _('Spare Parts'),
            'view_mode': 'tree,form',
            'res_model': 'product.template',
            'view_id': False,
            'views': [(self.env.ref('product.product_template_tree_view').id, 'tree'), (self.env.ref('product.product_template_form_view').id, 'form')],
            'type': 'ir.actions.act_window',
            'domain': [('maintenance_ids', 'in', self.id)],
            'context': {'maintenance_ids':self.id}
        }