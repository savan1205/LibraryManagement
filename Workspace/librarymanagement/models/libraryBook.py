from odoo import api, fields, models
from datetime import date,datetime
from random import randint
from odoo.exceptions import  ValidationError

class libraryBooks(models.Model):
    _name = 'library.book'
    _description="This model stores the data about the Book information"
    _rec_name="name"

    
    sequence_number=fields.Char(String="Lm Order ",readonly=True, default = lambda self: ('New'))

    @api.model 
    def create(self,vals):
        if vals.get('sequence_number', ('New')) == ('New'):
            vals['sequence_number'] = self.env['ir.sequence'].next_by_code(
           'library.book') or ('New')            
        res = super(libraryBooks, self).create(vals)
        return res

    sale_history_ids=fields.One2many(comodel_name="sale.history",inverse_name="book_id",string="Sale History")
    name = fields.Char(string = "Book")


    Author = fields.Char(string = "Author")
    image = fields.Image(string="image")


    def __get_default_name(self):
        return randint(10**(8-1),(10**8-1))


    isbn_number = fields.Integer(default = __get_default_name , string = "ISBN Number")
    
    state=fields.Selection([
        ('good condition','Good Condition'),
        ('scrapped','Scrapped')
        ],string="State") 

    total=fields.Float(compute ="total_sales",string="total")

    ratings=fields.Selection([
        ('very low','very Low'),
        ('low','Low'),
        ('med','Med'),
        ('high','High'),
        ('very high','Very High')],string="Rating",help="Give Your Ratings On this Book")



    stock = fields.Selection([
        ('available','Available'),
        ('ordered','Ordered'),
        ('not available','Not Available')
        ], default="available", required=True , string = "Stock Available")



    book_type = fields.Selection([
        ('eBook','Ebook'),
        ('physical','Physical'),
        ],string = "select book type", default="physical")


    set_password = fields.Char(string = "Set Password for Pdf", size=8)

    confirm_password = fields.Char(string = "Confirm Password", size=8)

    partner_id=fields.Many2one('res.partner',string="customer")
    user_id=fields.Many2one('res.users',string="users")



    


    #    A l l   F u n c t i o n s  f o r   Library Book
 


    def send_mail(self):
        template_id = self.env.ref('librarymanagement.email_template_edit_library')

        print("--------------------==========",template_id)
        ctx = {
            'default_model': 'library.book',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id.id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "mail.mail_notification_paynow",
           
            'force_email': True,
            
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    
    @api.constrains('book_type','set_password','confirm_password')
    def check_pass(self):
       for pass_rec in self:
            if pass_rec.book_type != "physical":
                if not pass_rec.set_password or not pass_rec.confirm_password :
                    raise ValidationError("Password fields cannot be Empty")

            if pass_rec.book_type == 'eBook' and pass_rec.set_password != pass_rec.confirm_password:
                raise ValidationError("Both entered password should be same")

    # @api.model
    # def create(self,vals):
    #     vals['isbn_number']=randint(10**(8-1),(10**8)-1)               
    #     return super(libraryBooks,self).create(vals)


    def move_to_scrap(self):
        for rec in self:
            if rec.state == "good condition":
                rec.state = "scrapped"

    def total_sales(self):
        sums = 0
        for rec in self:
        #     totalSale=self.env['sale.history'].search([('id','=',rec.sale_history_ids.ids)])
        #     print("-------------------------",totalSale)
            # print("===============================",rec.sale_history_ids)
            for res in rec.sale_history_ids:
                sums+=res.subtotal

        rec.total= sums


    def action_total_sales(self):
        print("______________________total of all sale history line")    


    @api.model
    def default_get(self,fields):
        res = super(libraryBooks,self).default_get(fields)
        # print("_____________________________fields",fields)
        print("-----------------------------res",res)
        res['state'] = "good condition"
        return res

    def action_discount(self):
        # print("------------------------------",date.today())
        for record in self.sale_history_ids:
            for fields in record:
        #         today=date.today()
                if fields.purchase_date == date.today():
                    record.price -= (record.price*10)/100
                    print("------------------------Done")

    def action_scheduled_book_action(self):
        print("____________________________",self)
        records = self.env['sale.history'].search([('submission_date','<',date.today())])
        print("----------------------",records)
        for rec in records:
            rec.unlink()
        # for record in self.sale_history_ids:
        #     for fields in record:
        #         fields.quantity=0

                # if fields.submission_date == date.today():
                    # print("d____e____l____e__t__e")
                    # record.unlink()
        #         today=date.today()
                 # objectt=self.env['sale.history'].search([(submission_date <= date.today())]):
                            












 #             S a l e        H i s t o r y       c l a s s

class SaleHistory(models.Model):
    _name = 'sale.history'
    _description = "This is sale history"

    book_id = fields.Many2one(comodel_name="library.book",string="Book" )
    visitor_id = fields.Many2one(comodel_name="visitor.visitor",string="Visitor")
    quantity = fields.Integer(string="Quantity")
    price = fields.Integer(string="price")
    
    subtotal = fields.Integer(compute="total_price",string="Sub Total")

    sell_type = fields.Selection([
        ('purchased','Purchased'),
        ('on rent','On Rent')
        ],string = "Selling Type",default = "purchased")

    purchase_date = fields.Date(string = "Purchase Date",default=datetime.today())
    submission_date = fields.Date(string = "Submisiion Date")
    
    days_left = fields.Integer(compute="gett_daysLeft",string = "Days Left" )


    total=fields.Float(compute ="total_sales",string="total")
    
            

    # @api.constrains('submission_date', 'sell_type')
    # def check_submission_validity(self):
    #     for history_rec in self:
    #         if history_rec.sell_type == 'on rent' and not history_rec.submission_date > date.today():
    #             raise ValidationError("Invalid Date Entered")




    @api.depends('submission_date')
    def gett_daysLeft(self):
        for rec in self:
            rec.days_left = 0
            if rec.submission_date:
                submission_date = rec.submission_date
                today = date.today()
                dleft = today.day - submission_date.day
                rec.days_left = abs(dleft)




    @api.depends('quantity','price')
    def total_price(self):
        for recc in self:
            recc.subtotal=0
            prce=0
            if recc.price and recc.quantity:
                prce=((recc.price)*(recc.quantity))
        recc.subtotal=prce