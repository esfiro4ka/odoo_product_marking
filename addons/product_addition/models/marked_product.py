from odoo import api, fields, models

from .product import models


class MarkedProduct(models.Model):
    _name = 'product_addition.marked_product'
    _description = 'Description for Marked Product'
    _inherit = 'product_addition.product'

    last_stock = fields.Many2one(
        'product_addition.stock', string='Last stock')
    last_status = fields.Selection([
        ('purchase', 'Purchase'),
        ('sale', 'Sale'),
        ('internal_displacement', 'Internal displacement'),
    ], string='Last status')

    product = fields.Many2one(
        'product_addition.product', string='Product')
    marking_act = fields.Many2one(
        'product_addition.marking_act', string='Marking Act')
    marked_product_id = fields.Char(string='Marked product ID')

    purchase_cost = fields.Float(string='Purchase cost', readonly=True)
    logistics_cost = fields.Float(string='Logistics cost', readonly=True)
    promotion_expense = fields.Float(string='Promotion expense', readonly=True)
    agent_commission = fields.Float(string='Agent commission', readonly=True)
    sales_price = fields.Float(string='Sales price', readonly=True)
    profit = fields.Float(
        string='Profit', compute='_compute_profit', store=True)

    purchase_cost_date = fields.Datetime(
        string='Purchase Date', readonly=True)
    logistics_cost_date = fields.Datetime(
        string='Logistics Cost Date', readonly=True)
    promotion_expense_date = fields.Datetime(
        string='Promotion Expense Date', readonly=True)
    agent_commission_date = fields.Datetime(
        string='Agent Commission Date', readonly=True)
    sales_price_date = fields.Datetime(
        string='Sales Price Date', readonly=True)

    is_purchase_cost_set = fields.Boolean(
        string='Is Purchase Cost Set', default=False)
    is_logistics_cost_set = fields.Boolean(
        string='Is Logistic Cost Set', default=False)
    is_promotion_expense_set = fields.Boolean(
        string='Is Promotion Expense Set', default=False)
    is_agent_commission_set = fields.Boolean(
        string='Is Agent Commission Set', default=False)
    is_sales_price_set = fields.Boolean(
        string='Is Sales Price Set', default=False)

    @api.depends('purchase_cost', 'logistics_cost', 'promotion_expense',
                 'agent_commission', 'sales_price')
    def _compute_profit(self):
        for record in self:
            record.profit = (record.purchase_cost + record.logistics_cost +
                             record.promotion_expense +
                             record.agent_commission + record.sales_price)
