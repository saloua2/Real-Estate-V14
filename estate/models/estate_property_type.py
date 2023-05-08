from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name"


    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer('Sequence', default=1)
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_count_offer')


    _sql_constraints = [
        ('uniq_name', 'UNIQUE(name)', 'The property type name must be unique.'),
    ]
    @api.depends('offer_ids')
    def _count_offer(self):
        self.offer_count = sum(self.offer_ids)