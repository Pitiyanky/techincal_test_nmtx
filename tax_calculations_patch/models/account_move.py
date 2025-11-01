# -*- coding: utf-8 -*-

from odoo import models, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _compute_tax_totals(self):
        res = super(AccountMove, self)._compute_tax_totals()
        
        for move in self:
            if move.is_invoice(include_receipts=True) and move.currency_id != move.company_id.currency_id:
                tax_totals = move.tax_totals
                
                for group_key, group_data in tax_totals.get('groups_by_subtotal', {}).items():
                    subtotal_affecting_base = group_data['tax_group_subtotal_affected_by_taxes']
                    
                    for tax_line in group_data.get('tax_group_amount_details', []):
                        tax = self.env['account.tax'].browse(tax_line['tax_id'])
                        
                        base_in_company_currency = move.currency_id._convert(
                            subtotal_affecting_base,
                            move.company_id.currency_id,
                            move.company_id,
                            move.date
                        )
                        
                        tax_amount_in_company_currency = tax.amount / 100 * base_in_company_currency
                        
                        tax_line['tax_amount_in_company_currency'] = tax_amount_in_company_currency
                        
                        tax_amount_in_invoice_currency = move.company_id.currency_id._convert(
                            tax_amount_in_company_currency,
                            move.currency_id,
                            move.company_id,
                            move.date
                        )
                        tax_line['tax_amount'] = tax_amount_in_invoice_currency

        return res