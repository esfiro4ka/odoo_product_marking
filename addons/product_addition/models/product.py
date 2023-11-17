# import uuid
import random
import string
from odoo import models, fields, api


class Product(models.Model):
    _name = 'product_addition.product'
    _description = 'Description for Product'

    name = fields.Char(string='Name')
    description = fields.Text(string='Description')
    marked_products = fields.One2many('product_addition.marked_product',
                                      'product',
                                      string='Marked Products')


class Stock(models.Model):
    _name = 'product_addition.stock'
    _description = 'Description for Stock'

    name = fields.Char(string='Stock Name', required=True)


class ExpenseRevenueItem(models.Model):
    _name = 'product_addition.expense_revenue_item'
    _description = 'Expense/Revenue Item for Product'

    purchase_cost = fields.Float(string='Purchase Cost')
    logistics_cost = fields.Float(string='Logistics Cost')
    promotion_expense = fields.Float(string='Promotion Expense')
    agent_commission = fields.Float(string='Agent Commission')
    sales_price = fields.Float(string='Sales Price')

    profit = fields.Float(
        string='Profit', compute='_compute_profit', store=True)

    date = fields.Date(string='Date')

    marking_act_id = fields.Many2one(
        'product_addition.marking_act', string='Marking Act')

    @api.model
    def _invert_value(self, field_name):
        if getattr(self, field_name) >= 0:
            setattr(self, field_name, -abs(getattr(self, field_name)))

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

    @api.depends('purchase_cost', 'logistics_cost', 'promotion_expense',
                 'agent_commission', 'sales_price')
    def _compute_profit(self):
        for record in self:
            record.profit = (record.purchase_cost + record.logistics_cost +
                             record.promotion_expense +
                             record.agent_commission + record.sales_price)


# class ExpenseRevenue(models.Model):
#     _name = 'product_addition.expense_revenue'
#     _description = 'Expense/Revenue for Product'

#     date = fields.Date(string='Date')


class MarkedProduct(models.Model):
    _name = 'product_addition.marked_product'
    _description = 'Description for Marked Product'
    _inherit = 'product_addition.product'

    last_stock = fields.Many2one('product_addition.stock', string='Last Stock')
    last_status = fields.Selection([
        ('purchase', 'Purchase'),
        ('sale', 'Sale'),
        ('internal_displacement', 'Internal Displacement'),
    ], string='Last Status')

    product = fields.Many2one('product_addition.product',
                              string='Product')
    marking_act = fields.Many2one('product_addition.marking_act',
                                  string='Marking Act')
    marked_product_id = fields.Char(string='Marked Product Identifier')


class MarkingAct(models.Model):
    _name = 'product_addition.marking_act'
    _description = 'Marking Act'

    name = fields.Char(string='Reference',
                       required=True, readonly=True, copy=False, default='New')
    date = fields.Date(string='Date',
                       default=fields.Date.today(), required=True)
    product_line = fields.Many2one('product_addition.product',
                                   string='Product', required=True)
    quantity = fields.Float(string='Quantity', default=1, required=True)
    status = fields.Selection([
        ('purchase', 'Purchase'),
        ('sale', 'Sale'),
        ('internal displacement', 'Internal displacement'),
    ], string='Status', required=True)
    source_stock = fields.Many2one('product_addition.stock',
                                   string='Source stock',
                                   create=True)
    destination_stock = fields.Many2one('product_addition.stock',
                                        string='Destination stock',
                                        create=True,
                                        required=True)
    expense_revenue_item = fields.One2many(
        'product_addition.expense_revenue_item',
        'marking_act_id',
        string='Expense/Revenue Items'
    )

    @api.depends('quantity')
    def apply_marking_act(self):
        marked_product_obj = self.env['product_addition.marked_product']

        def generate_random_letters(length):
            return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

        for act in self:
            for i in range(int(act.quantity)):

                # marked_product_id = str(uuid.uuid4())[:5] + '-' + str(uuid.uuid4())[:5] + '-' + str(uuid.uuid4())[:5]

                marked_product_id = generate_random_letters(5) + '-' + generate_random_letters(5) + '-' + generate_random_letters(5)

                marked_product_obj.create({
                    'product': act.product_line.id,
                    'last_stock': act.destination_stock.id,
                    'last_status': act.status,
                    'marked_product_id': marked_product_id,
                })

        return True
