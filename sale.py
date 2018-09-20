# This file is part of sale_salesman module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import ModelSQL, fields
from trytond.pool import PoolMeta

__all__ = ['PartyEmployee', 'Party', 'Employee', 'Sale']


class PartyEmployee(ModelSQL):
    'Party - Employee'
    __name__ = 'party.party-company.employee'
    __metaclass__ = PoolMeta
    party = fields.Many2One('party.party', 'Party', required=True,
        select=True, ondelete='CASCADE')
    employee = fields.Many2One('company.employee', 'Salesman', required=True,
        select=True, ondelete='CASCADE')


class Party:
    __name__ = 'party.party'
    __metaclass__ = PoolMeta
    salesmans = fields.Many2Many('party.party-company.employee', 'party',
        'employee', 'Salesmans')


class Employee:
    __name__ = 'company.employee'
    __metaclass__ = PoolMeta
    sale_parties = fields.Many2Many('party.party-company.employee', 'employee',
        'party', 'Sale Parties')


class Sale:
    __name__ = 'sale.sale'
    __metaclass__ = PoolMeta

    @fields.depends('party')
    def on_change_party(self):
        super(Sale, self).on_change_party()
        if self.party:
            if len(self.party.salesmans) == 1:
                self.employee = self.party.salesmans[0]
            else:
                self.employee = None
