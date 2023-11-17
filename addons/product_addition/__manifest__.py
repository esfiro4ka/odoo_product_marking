{
    'name': 'Product Marking',
    'version': '1.0',
    'summary': 'Module for marking a product',
    'sequence': 1,
    'description': """Module for marking a product and changing its characteristics""",
    'author': 'Olga Rotbardt',
    'depends': ['base'],
    'data': [
        'views/menu.xml',
        'views/product.xml',
        'views/marking_act.xml',
        'views/marked_product.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
