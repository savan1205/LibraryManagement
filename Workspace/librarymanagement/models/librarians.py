from odoo import api, fields, models
from datetime import date,datetime

class libraryLibrarians(models.Model):
    _name = 'librarian.librarian'
    _description = "This is master Table to store the librarian"

    name = fields.Char(string = "librarian")
    
    gender = fields.Selection([
                            ('male','Male'),
                            ('female','Female')
                            ],string = "gender")
    
    dob = fields.Datetime(string = "date of birth")
    
    age = fields.Integer(compute ="_compute_age",string = "Age")  
    
    date_of_joining = fields.Date(string = "date of joining")
    
    current_experience = fields.Char(compute = "_compute_exp",string = "current experience(in years)")


    @api.depends('dob')
    def _compute_age(self):
        for rec in self:
            rec.age = 0
            if rec.dob:
                dob = rec.dob
                today = date.today()
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                rec.age = age


    @api.depends('date_of_joining')
    def _compute_exp(self):
        for rec in self:
            rec.current_experience = " "
            if rec.date_of_joining:
                date_of_joining = rec.date_of_joining
                today = date.today()
                current_experience = today.year - date_of_joining.year - ((today.month, today.day) < (date_of_joining.month, date_of_joining.day))
                months = today.month - date_of_joining.month
               
                print("______________--------------------",months )
                rec.current_experience = str(current_experience) + " years" + ", " + str(abs(months)) + " months"

       