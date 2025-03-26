# -*- coding: utf-8 -*-

from odoo import models, fields

class Clientes(models.Model):
    _inherit = 'res.partner'
    
    
    codigo_cliente = fields.Char(string="Código Cliente")
    codigo_contable = fields.Char(string="Código Contable")
    provincia = fields.Char(string="Provincia")
    fax = fields.Char(string="Fax", help="Número de fax del cliente")
    forma_pago = fields.Many2one(
        'account.payment.term', 
        string="Forma de Pago", 
        ondelete='cascade'  # Permite eliminar correctamente si es necesario
    )
    nombre_comercial = fields.Char(string="Nombre de Comercial")
    telefono2 = fields.Char(string="Teléfono Secundario", size=15)