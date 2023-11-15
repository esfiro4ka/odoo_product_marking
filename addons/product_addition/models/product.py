from odoo import models, fields


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
