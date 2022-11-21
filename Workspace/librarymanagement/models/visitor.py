from odoo import api, fields, models

class LibraryVisitor(models.Model):
    _name = 'visitor.visitor'
    _description="This stores data of visitors"

    name = fields.Char(string = "visitors" , required=True)
    