from odoo import fields, models, api, _
from odoo.exceptions import ValidationError,UserError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.today())
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north', 'North'),('south', 'South'),('east', 'East'),('west', 'West')])
    active = fields.Boolean("Active", default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ], string='Status', default='new')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    salesperson_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True, default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.users', string='Buyer',copy=False)
    property_tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Integer(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price')

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)','The expected price should be positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling_price should be positive.'),
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            # print(record.offer_ids.mapped('price'))
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = False

    @api.onchange("garden")
    def _onchange_garden(self):
        for rec in self:
            if rec.garden:
                rec.garden_area = 10
                rec.garden_orientation = "north"
            else:
                rec.garden_area = 0
                rec.garden_orientation = False

    def action_sold(self):
        self.ensure_one()
        if self.state == 'canceled':
            raise UserError(_("Cancelled properties cannot be sold!"))
        self.write({'state': 'sold'})

    def action_cancel(self):
        self.ensure_one()
        self.write({'state': 'canceled'})

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.expected_price:
                amount = record.expected_price * 0.9
                if float_compare(record.selling_price, amount, precision_rounding=4) <= 0:
                    raise ValidationError("the selling price cannot be lower than 90% of the expected price")


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('uniq_name', 'UNIQUE(name)', 'The property tag name must be unique.'),
    ]


