# -*- coding: utf-8 -*-

from odoo import models, api
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        self._group_order_lines()
        return super(SaleOrder, self).action_confirm()

    def _group_order_lines(self):

        for order in self:
            grouped_lines = {}

            for line in order.order_line.sorted(key=lambda l: l.id):
                product_id = line.product_id.id
                
                if not product_id:
                    continue

                if product_id in grouped_lines:
                    existing_line = self.env['sale.order.line'].browse(grouped_lines[product_id])

                    if line.product_uom != existing_line.product_uom:
                        raise UserError("No se pueden agrupar líneas con diferentes unidades de medida para el mismo producto.")
                    if line.price_unit != existing_line.price_unit:
                        raise UserError("No se pueden agrupar líneas con diferentes precios unitarios para el mismo producto.")
                    
                    existing_line.product_uom_qty += line.product_uom_qty
                    
                    line.unlink()
                else:
                    grouped_lines[product_id] = line.id