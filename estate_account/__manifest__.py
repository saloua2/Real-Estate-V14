{
    'name': "Account estate",
    'version': '1.0',
    'author': "Author Name",
    'category': 'Category',
    'description': """
    Description text
    """,
    'depends' : ['estate', 'account'],
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'report/estate_property_report.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        # 'demo/demo_data.xml',
    ],
}