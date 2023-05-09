{
    'name': "Real estate",
    'version': '1.0',
    'author': "Author Name",
    'category': 'Real Estate/Brokerage',
    'description': """
    Description text
    """,
    'depends' : ['base'],
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/estate.property.type.csv',
        'data/estate_property.xml',
        'data/estate_property_offer.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/res_users_view.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        # 'demo/demo_data.xml',
    ],
}