from odoo import api, fields, models
from datetime import date,datetime
from random import randint
from odoo.exceptions import  ValidationError

class BooksPurchase(models.Model):
    _name = 'book.purchase'
    _description="This model stores the data about the Book's Purchase information"
    _rec_name="book_id"
    

    book_id = fields.Many2one(comodel_name="library.book", string="Book Name")
    
    already_in_library = fields.Selection([
        ('yes','Yes'),
        ('no','No')
        ],default = "yes" ,string="Already belongs to this Library ?")
    new_name = fields.Char(string = "Enter Book Name")
    
    quantity = fields.Integer(string = "quantity")
   
    image = fields.Image(string="image")
   
    vendor_name = fields.Char(string="Vendor Name")
