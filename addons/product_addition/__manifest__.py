{
    'name': 'Product marking',
    'version': '1.0',
    'summary': 'Product Marking Module',
    'sequence': 1,
    'description': """Product Marking and Properties Modification Module""",
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
