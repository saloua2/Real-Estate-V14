from odoo import models

class InheritedModel(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        res = super().action_sold()
        print(" reached ".center(100, '='))
        for rec in self:
            self.env["account.move"].create(
                {
                    "name": "Invoice of %s " %rec.name,
                    "partner_id": self.env.user.partner_id.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        (0,0,
                            {
                                "name": rec.name,
                                "quantity": 1,
                                "account_id":1,
                                "price_unit": rec.selling_price * 0.6,
                            },
                        ),
                        (0,0,
                            {
                                "name": "administrative fees",
                                "quantity": 1,
                                "account_id": 1,
                                "price_unit": 100.00,
                            },
                        )
                    ],
                }
            )
            return res