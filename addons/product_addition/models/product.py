from odoo import fields, models


class Product(models.Model):
    _name = 'product_addition.product'
    _description = 'Description for Product'

    name = fields.Char(string='Name')
    description = fields.Text(string='Description')
    marked_products = fields.One2many(
        'product_addition.marked_product',
        'product',
        string='Marked products')


class Stock(models.Model):
    _name = 'product_addition.stock'
    _description = 'Description for Stock'

    name = fields.Char(string='Name', required=True)
