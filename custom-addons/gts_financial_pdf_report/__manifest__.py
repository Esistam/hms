# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Financial PDF Reports | Odoo12 Financial Reports in PDF(BS,P&L,GL,Trial Balance) | Odoo 12 Accounting reports | odoo12 accounting report',
    'version' : '12.0.0.1',
    'summary': 'GTS Financial PDF Reports in community odoo v12',
    'sequence': 1,
    'description': """
        ALL Financial PDF Reports or Finance report  or Financial Reports - Balance Sheet, Profit and Loss, General Ledger,
        Trial Balance, Aged Partner balance, Partner Ledger, Sale/Purchase Journal 
        in odoo version 12 odoo 12 Financial Reports odoo 12 accounting reports odoo 12 reports odoo12 reports
        12 accounting reports BS P&L GL Trial Balance Missing Accounting reports on Odoo12 Community Edition
        Print Balance Sheet Report,Print Profit Loss Report, Print Trial Balance Report,Print General Ledger Report in PDF format 
        using all the filters i.e Date Range filter, Journal filter, Posted/Unposted entry etc. 
        We have also developed the other deprecated reports and modules of Odoo for v12,
        Odoo 12 Missing Financial Reports odoo12 accounting report odoo12 financial accounting report odoo 12 accounting report
        Odoo 12 Accounting Management Odoo12 ALL Financial Reports(BS,P&L,GL,Trial Balance)(PDF)
    """,
    'category': 'Accounting',
    'website': 'https://www.geotechnosoft.com',
    'author': 'Geo Technosoft',
    'depends' : ['account'],
    'data': [
        'security/account_security.xml',
        'security/ir.model.access.csv',
        'views/account_financial_report_view.xml',
        'views/account_report.xml',
        'views/account_financial_report_data.xml',
        'views/report_trialbalance.xml',
        'views/report_generalledger.xml',
        'views/report_partnerledger.xml',
        'views/report_financial.xml',
        'views/report_agedpartnerbalance.xml',
        'views/account_menuitem.xml',
        'wizard/account_report_print_journal_view.xml',
        'wizard/account_report_partner_ledger_view.xml',
        'wizard/account_report_general_ledger_view.xml',
        'wizard/account_report_trial_balance_view.xml',
        'wizard/account_financial_report_view.xml',
        'wizard/account_report_aged_partner_balance_view.xml',

    ],
    'qweb': [],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    # 'price': 15.00,
    # 'currency': 'EUR',
    'license': 'OPL-1',
}
