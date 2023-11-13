from odoo import models, fields


class Product(models.Model):
    _name = 'product_addition.product'
    _description = 'Description for product'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
