# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleReportPendingDelivery(models.Model):
    _name = 'sale.report.pending.delivery'
    _description = 'Reporte de Ventas por Despachar'
    _auto = False

    product_id = fields.Many2one('product.product', string='Producto', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Cliente', readonly=True)
    order_id = fields.Many2one('sale.order', string='Orden de Venta', readonly=True)
    invoice_id = fields.Many2one('account.move', string='Número de Factura', readonly=True)
    invoice_date = fields.Date(string='Fecha de Factura', readonly=True)
    invoiced_qty = fields.Float(string='Cantidad Facturada', readonly=True)

    def init(self):
        """
        Define la consulta SQL que poblará los datos del reporte.
        """
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW sale_report_pending_delivery AS (
                SELECT
                    sol.id AS id,
                    sol.product_id AS product_id,
                    so.partner_id AS partner_id,
                    so.id AS order_id,
                    am.id AS invoice_id,
                    am.invoice_date AS invoice_date,
                    sol.qty_invoiced AS invoiced_qty
                FROM
                    sale_order_line sol
                JOIN
                    sale_order so ON (sol.order_id = so.id)
                JOIN
                    account_move_line aml ON (sol.id = aml.sale_line_ids)
                JOIN
                    account_move am ON (aml.move_id = am.id)
                WHERE
                    so.state = 'sale'
                    AND sol.qty_invoiced > sol.qty_delivered
                    AND am.state = 'posted'
                    AND am.move_type = 'out_invoice'
            )
        """)