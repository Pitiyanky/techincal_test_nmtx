# -*- coding: utf-8 -*-
{
    'name': "Reporte de Ventas Facturadas por Despachar",

    'summary': "Añade un reporte de productos facturados pendientes de despacho.",

    'author': "Jesus Machado",
    'website': "https://www.linkedin.com/in/jesusdavidmachado",

    'category': 'Sale',
    'version': '17.0.0.0.1',
    'depends': ['sale'],

    'data': [
        'security/ir.model.access.csv',
        'views/sale_report_pending_delivery_views.xml',
    ],

}

