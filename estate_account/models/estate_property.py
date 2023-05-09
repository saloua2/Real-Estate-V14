from odoo import models

class InheritedModel(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        print(" reached ".center(100, '='))
        self.env["account.move"].create(
            {
                "name": "Invoice of %s " %self.name,
                "partner_id": self.env.user.partner_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    (0,0,
                        {
                            "name": self.name,
                            "quantity": 1,
                            "account_id":1,
                            "price_unit": self.selling_price * 0.6,
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
        return super().action_sold()