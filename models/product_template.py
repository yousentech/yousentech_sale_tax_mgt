# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class xx_add_fields_in_product(models.Model):
    _inherit = 'product.template'

    tax_reqiured = fields.Boolean(string="خاضع للضريبة", default=True)

 
