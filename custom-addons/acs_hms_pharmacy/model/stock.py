# -*- coding: utf-8 -*-

from odoo import api, fields, models,_
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime, timedelta


class StockProductionLot(models.Model):
    _name = 'stock.production.lot'
    _inherit = ['stock.production.lot', 'mail.thread']

    @api.one
    @api.depends('removal_date', 'alert_date', 'life_date', 'use_date')
    def _get_product_state(self):
        now = fields.Datetime.now()
        self.expiry_state = 'normal'
        if self.life_date and self.life_date < now:
            self.expiry_state = 'expired'
        elif (self.alert_date and self.removal_date and
                self.removal_date >= now > self.alert_date):
            self.expiry_state = 'alert'
        elif (self.removal_date and self.use_date and
                self.use_date >= now > self.removal_date):
            self.expiry_state = 'to_remove'
        elif (self.use_date and self.life_date and
                self.life_date >= now > self.use_date):
            self.expiry_state = 'best_before'


    def _get_locked_value(self):
        return self._get_product_locked(self.product_id)

    mrp = fields.Float(string='MRP', help="If we get lot price different set this price to set invoice price")
    expiry_state = fields.Selection(
        compute=_get_product_state,
        selection=[('expired', 'Expired'),
                   ('alert', 'In alert'),
                   ('normal', 'Normal'),
                   ('to_remove', 'To remove'),
                   ('best_before', 'After the best before')],
        string='Expiry state')
    locked = fields.Boolean(string='Blocked', default='_get_locked_value', readonly=True)

    @api.onchange('life_date')
    def _onchange_life_date(self):
        if self.life_date:
            self.removal_date = (self.life_date + timedelta(days= -90)).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
            self.use_date = (self.life_date + timedelta(days= -90)).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
            self.alert_date = (self.life_date + timedelta(days= -90)).strftime(DEFAULT_SERVER_DATETIME_FORMAT)

    def _get_product_locked(self, product):
        """Should create locked? (including categories and parents)

        @param product: browse-record for product.product
        @return True when the category of the product or one of the parents
                demand new lots to be locked"""
        _locked = product.categ_id.lot_default_locked
        categ = product.categ_id.parent_id
        while categ and not _locked:
            _locked = categ.lot_default_locked
            categ = categ.parent_id
        return _locked

    @api.onchange('product_id')
    def onchange_product_id(self):
        self.locked = self._get_product_locked(self.product_id)

    @api.multi
    def button_lock(self):
        stock_quant_obj = self.env['stock.quant']
        for lot in self:
            for quant in stock_quant_obj.search([('lot_id', '=', lot.id)]):
                quant.locked = True
            lot.locked = True

    @api.multi
    def button_unlock(self):
        for lot in self:
            lot.locked = False

    @api.model
    def create(self, vals):
        product = self.env['product.product'].browse(vals.get('product_id'))
        vals['locked'] = self._get_product_locked(product)
        return super(StockProductionLot, self).create(vals)

    @api.one
    def write(self, values):
        if 'product_id' in values:
            product = self.env['product.product'].browse(
                values.get('product_id'))
            values['locked'] = self._get_product_locked(product)
        return super(StockProductionLot, self).write(values)


class StockQuant(models.Model):
    _inherit = "stock.quant"

    expiry_state = fields.Selection(string="Expiry State",
                                    related="lot_id.expiry_state")
    locked = fields.Boolean(string='Blocked', related="lot_id.locked", default=False, store=True)

    @api.model
    def quants_get(self, location, product, qty, domain=None,
                   restrict_lot_id=False, restrict_partner_id=False):
        if domain is None:
            domain = []
        domain += [('locked', '=', False)]
        return super(StockQuant, self).quants_get(
            location, product, qty, domain=domain,
            restrict_lot_id=restrict_lot_id,
            restrict_partner_id=restrict_partner_id)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: