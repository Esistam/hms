# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import Warning,UserError, ValidationError
	
class AccountInvoiceInherit(models.Model):
	_inherit = 'account.invoice'

	def delete_entry(self):
		for mv in self:
			mv.with_context(force_delete=True).unlink()
		return {
				'name': _('Journal Entries'),
				'type': 'ir.actions.act_window',
				'view_mode': 'tree,form',
				'res_model': 'account.invoice',
			}
