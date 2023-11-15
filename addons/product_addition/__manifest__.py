{
    'name': 'Product Addition',
    'version': '1.0',
    'summary': 'Module for adding a product',
    'sequence': 1,
    'description': """Module for adding a product and its characteristics""",
    'author': 'Olga Rotbardt',
    'depends': ['base'],
    'data': [
        'views/menu.xml',
        'views/product.xml',
        'views/marking_act.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
