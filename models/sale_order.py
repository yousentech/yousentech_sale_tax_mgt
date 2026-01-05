# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

 
class xx_sale_order_line_tax_required(models.Model):
    _inherit = 'sale.order.line'

    l_tax_reqiured = fields.Boolean()

    @api.onchange('product_id')
    def check_tax_required(self):
        for rec in self:
            if rec.product_id:
                rec.l_tax_reqiured = rec.product_id.tax_reqiured


class xx_sale_order_tax_required(models.Model):
    _inherit = 'sale.order'

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
 
    @api.constrains('order_line')
    def check_tax_required(self):
        for rec in self:
            for line in rec.order_line:
                if line.product_id:
                    if line.product_id.tax_reqiured and not line.tax_ids:
                        raise ValidationError(
                                "تنبيه .. لا يمكن الاستمرار لوجود ضريبة للمنتج (%s) " % line.product_id.name)

    def action_confirm(self):
        self.check_tax_required()
        return super(xx_sale_order_tax_required, self).post()
    
 