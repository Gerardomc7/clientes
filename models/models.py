# -*- coding: utf-8 -*-
import re
from odoo import api, models, fields
import logging
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class Clientes(models.Model):
    _inherit = 'res.partner'
    _order = "codigo_cliente asc"

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

    @api.constrains('codigo_cliente', 'codigo_contable')
    def _check_codes(self):
        """
        Valida que:
        - codigo_cliente tenga exactamente 6 dígitos y comience con "00" (ejemplo: '004416').
        - codigo_contable tenga exactamente 7 dígitos (ejemplo: 4304416).
        """
        # Expresiones regulares para validar el formato
        regex_cliente = re.compile(r'^00[0-9]{4}$')
        regex_contable = re.compile(r'^[0-9]{7}$')

        for record in self:
            # Validación para codigo_cliente
            if record.codigo_cliente:
                if not regex_cliente.match(record.codigo_cliente):
                    raise ValidationError(
                        "El 'Código Cliente' debe contener exactamente 6 dígitos y comenzar con '00' (ejemplo: '004416')."
                    )
                else:
                    _logger.info("Código Cliente generado correctamente: %s", record.codigo_cliente)

            # Validación para codigo_contable
            if record.codigo_contable:
                if not regex_contable.match(record.codigo_contable):
                    raise ValidationError(
                        "El 'Código Contable' debe contener exactamente 7 dígitos (ejemplo: 4304416)."
                    )
                else:
                    _logger.info("Código Contable generado correctamente: %s", record.codigo_contable)
    
    _sql_constraints = [
        ('codigo_cliente_unique', 'unique(codigo_cliente)', 'El Código Cliente ya existe.'),
        ('codigo_contable_unique', 'unique(codigo_contable)', 'El Código Contable ya existe.')
    ]

    #-- Preparación para la base de datos
    #ALTER TABLE res_partner
    #ADD COLUMN codigo_cliente VARCHAR,
    #ADD COLUMN codigo_contable VARCHAR,
    #ADD COLUMN provincia VARCHAR,
    #ADD COLUMN fax VARCHAR,
    #ADD COLUMN forma_pago INTEGER,  -- Campo Many2one que referenciará a account_payment_term
    #ADD COLUMN nombre_comercial VARCHAR,
    #ADD COLUMN telefono2 VARCHAR;

