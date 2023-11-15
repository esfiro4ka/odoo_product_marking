from odoo import models, fields, api


class Product(models.Model):
    _name = 'product_addition.product'
    _description = 'Description for Product'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    marked_products = fields.One2many('product_addition.marked_product',
                                      'original_product',
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


class ExpenseRevenue(models.Model):
    _name = 'product_addition.expense_revenue'
    _description = 'Expense/Revenue for Product'

    date = fields.Date(string='Date')


class MarkedProduct(models.Model):
    _name = 'product_addition.marked_product'
    _description = 'Description for Marked Product'

    original_product = fields.Many2one('product_addition.product',
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
