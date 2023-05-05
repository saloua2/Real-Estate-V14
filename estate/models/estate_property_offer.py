import datetime

from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner')
    property_id = fields.Many2one('estate.property')
    validity = fields.Integer()
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'The offer price should be positive.'),
    ]

    @api.depends('validity')
    def _compute_date_deadline(self):
        for rec in self:
            rec.date_deadline = fields.Date.today() + datetime.timedelta(days=rec.validity)

    def _inverse_date_deadline(self):
        for rec in self:
            rec.date_deadline = fields.Date.today() - datetime.timedelta(days=rec.validity)

    def action_accept(self):
        self.ensure_one()
        self.write({'status': 'accepted'})
        user_id = self.env['res.users'].search([('partner_id','=',self.partner_id.id)])
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = user_id.id

    def action_refuse(self):
        self.ensure_one()
        self.write({'status': 'refused'})



