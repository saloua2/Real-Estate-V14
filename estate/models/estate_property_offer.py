import datetime

from odoo import fields, models, api, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    state = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner')
    property_id = fields.Many2one('estate.property')
    validity = fields.Integer()
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

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
        self.write({'state': 'accepted'})
        user_id = self.env['res.users'].search([('partner_id','=',self.partner_id.id)])
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = user_id.id

    def action_refuse(self):
        self.ensure_one()
        self.write({'state': 'refused'})
    @api.model
    def create(self, vals):
        print(self.env['estate.property'].browse(vals['property_id']))
        active = self.env['estate.property'].browse(vals['property_id'])
        if active.state == 'new' and active.best_price != 0.0:
            active.write({'state': 'offer_received'})
        return super(EstatePropertyOffer, self).create(vals)




