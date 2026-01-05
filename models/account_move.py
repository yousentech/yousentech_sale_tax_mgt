# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

 

class xx_account_move_tax_required(models.Model):
    _inherit = 'account.move'

    # *******************************************************************************************************
    disallow_modify_product_tax_in_invoice = fields.Boolean(
        default=lambda self: self._default_disallow_modify_product_tax_in_invoice(),
        compute="_get_disallow_modify_product_tax_in_invoice")

    # @api.depends('company_id')
    def _get_disallow_modify_product_tax_in_invoice(self):
        for rec in self:
            rec.disallow_modify_product_tax_in_invoice = self.user_has_groups(
                'yousentech_invoicing_tax_mgt.group_disallow_modify_product_tax_in_invoice')

    def _default_disallow_modify_product_tax_in_invoice(self):
        return self.user_has_groups('yousentech_invoicing_tax_mgt.group_disallow_modify_product_tax_in_invoice')
    # *******************************************************************************************************

    @api.constrains('invoice_line_ids')
    def check_tax_required(self):
        for rec in self:

            if rec.move_type in ('out_invoice','out_refund'):
                for line in rec.invoice_line_ids:
                    if line.product_id:
                        if line.product_id.tax_reqiured and not line.tax_ids:
                            raise ValidationError(
                                 "تنبيه .. لا يمكن الاستمرار لوجود ضريبة للمنتج (%s) " % line.product_id.name)

    def post(self):
        self.check_tax_required()
        return super(xx_account_move_tax_required, self).post()
    
class xx_account_move_line_tax_required(models.Model):
    _inherit = 'account.move.line'

    l_tax_reqiured = fields.Boolean()

    @api.onchange('product_id')
    def check_tax_required(self):
        for rec in self:
            if rec.product_id:
                rec.l_tax_reqiured = rec.product_id.tax_reqiured

 