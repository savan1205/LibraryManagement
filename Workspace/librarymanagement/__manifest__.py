{
    'name': 'Library',
    'version': '1.0',
    'category': 'Library management',
    'summary': 'Library management',
    'sequence': -500,
    'description': """
This module contains all the common features of Library management.
    """,
    'depends': ['mail'],
    'data': [
    'security/ir.model.access.csv',

    # 'report/book_report.xml',
    
    'data/library_mail.xml',
    'data/data_sequence.xml',
    
    'views/libraryManagement.xml',
    'views/librarians.xml',
    'views/visitor.xml',
    'views/libraryBook.xml',
    'views/purchaseView.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    
       
    'license': 'LGPL-3',

}
