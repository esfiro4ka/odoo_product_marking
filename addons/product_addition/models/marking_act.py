import random
import string

from odoo import api, fields, models


class MarkingAct(models.Model):
    _name = 'product_addition.marking_act'
    _description = 'Marking Act'

    name = fields.Char(string='Name')
    date = fields.Date(
        string='Date', default=fields.Date.today(), required=True)
    product_line = fields.Many2one(
        'product_addition.product', string='Product', required=True)
    quantity = fields.Integer(string='Quantity', default=1, required=True)
    status = fields.Selection([
        ('purchase', 'Purchase'),
        ('sale', 'Sale'),
        ('internal displacement', 'Internal displacement'),
    ], string='Status', required=True)
    source_stock = fields.Many2one(
        'product_addition.stock', string='Source stock', create=True)
    destination_stock = fields.Many2one(
        'product_addition.stock',
        string='Destination stock',
        create=True,
        required=True)

    purchase_cost = fields.Float(string='Purchase cost')
    logistics_cost = fields.Float(string='Logistics cost')
    promotion_expense = fields.Float(string='Promotion expense')
    agent_commission = fields.Float(string='Agent commission')
    sales_price = fields.Float(string='Sales price')

    @api.model
    def _invert_value(self, field_name):
        if getattr(self, field_name) >= 0:
            setattr(self, field_name, -abs(getattr(self, field_name)))

    @api.model
    def create(self, vals):
        record = super(MarkingAct, self).create(vals)
        if vals.get('name', 'New') == 'New':
            record.name = f'Marking act #{record.id}'
        return record

    @api.onchange('promotion_expense')
    def _onchange_promotion_expense(self):
        self._invert_value('promotion_expense')

    @api.onchange('logistics_cost')
    def _onchange_logistics_cost(self):
        self._invert_value('logistics_cost')

    @api.onchange('purchase_cost')
    def _onchange_purchase_cost(self):
        self._invert_value('purchase_cost')

    @api.onchange('agent_commission')
    def _onchange_agent_commission(self):
        self._invert_value('agent_commission')

    @api.depends('quantity')
    def apply_marking_act(self):
        marked_product_obj = self.env['product_addition.marked_product']

        def generate_random_letters(length):
            return ''.join(
                random.choice(string.ascii_lowercase) for _ in range(length))

        for act in self:

            if act.status == 'purchase':

                for i in range(int(act.quantity)):

                    marked_product_id = (generate_random_letters(5) + '-' +
                                         generate_random_letters(5) + '-' +
                                         generate_random_letters(5))

                    marked_product_obj.create({
                        'name': (act.product_line.name + " #" +
                                 marked_product_id),
                        'product': act.product_line.id,
                        'last_stock': act.destination_stock.id,
                        'last_status': act.status,
                        'marked_product_id': marked_product_id,
                    })

            else:

                for marked_product in marked_product_obj.search([]):
                    if (
                        not marked_product.is_purchase_cost_set and
                        act.purchase_cost and act.purchase_cost != 0.00
                    ):
                        marked_product['purchase_cost'] = act.purchase_cost
                        marked_product['purchase_cost_date'] = fields.Datetime.now()
                        marked_product['is_purchase_cost_set'] = True

                    if (
                        not marked_product.is_logistics_cost_set and
                        act.logistics_cost and act.logistics_cost != 0.00
                    ):
                        marked_product['logistics_cost'] = act.logistics_cost
                        marked_product['logistics_cost_date'] = fields.Datetime.now()
                        marked_product['is_logistics_cost_set'] = True

                    if (
                        not marked_product.is_promotion_expense_set and
                        act.promotion_expense and act.promotion_expense != 0.00
                    ):
                        marked_product['promotion_expense'] = act.promotion_expense
                        marked_product['promotion_expense_date'] = fields.Datetime.now()
                        marked_product['is_promotion_expense_set'] = True

                    if (
                        not marked_product.is_agent_commission_set and
                        act.agent_commission and act.agent_commission != 0.00
                    ):
                        marked_product['agent_commission'] = act.agent_commission
                        marked_product['agent_commission_date'] = fields.Datetime.now()
                        marked_product['is_agent_commission_set'] = True

                    if (
                        not marked_product.is_sales_price_set and
                        act.sales_price and act.sales_price != 0.00
                    ):
                        marked_product['sales_price'] = act.sales_price
                        marked_product['sales_price_date'] = fields.Datetime.now()
                        marked_product['is_sales_price_set'] = True

                    marked_product.write({
                        'last_stock': act.destination_stock.id,
                        'last_status': act.status,
                    })

            return True
