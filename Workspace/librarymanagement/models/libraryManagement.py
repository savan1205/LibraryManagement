from odoo import api, fields, models

class libraryManagement(models.Model):
    _name = 'library.management'
    _inherit=['mail.thread','mail.activity.mixin']
    _description="This is master Table to store the libraries"

    name=fields.Char(string="Libraries", tracking=True)
    property_type=fields.Selection([
        ('public','Public'),
        ('private','Private')
        ],string="Property Type")
    librarians_ids=fields.Many2many(comodel_name="librarian.librarian", string="Librarians")