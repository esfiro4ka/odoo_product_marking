from odoo import models, fields


class Product(models.Model):
    _name = 'product_addition.product'
    _description = 'Description for Product'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    marked_products = fields.One2many('product_addition.marked_product',
                                      'original_product',
                                      string='Marked Products')


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
    # если разные товары в одном акте:
    # product_lines = fields.Many2many('product_addition.product',
    #                                  string='Product Lines')
    product_line = fields.Many2one('product_addition.product',
                                   string='Product')
    quantity = fields.Float(string='Quantity', default=1)
