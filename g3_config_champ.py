# -*- coding: utf-8 -*-

from openerp import models,fields,api
from openerp.tools.translate import _

class g3_config_champ(models.Model):
    _name='g3.config.champ'
    _order='name'

    name        = fields.Many2one('ir.model', 'Formulaire à paramètrer')
    champs_line = fields.One2many('g3.config.champ.line', 'model_id', 'Champs')

    _sql_constraints = [
        ('name_uniq'       , 'unique(name)'       , u"Ce formulaire existe déja !"),
    ]


class g3_config_champ_line(models.Model):
    _name='g3.config.champ.line'
    _order='model_id,name'

    model_id = fields.Many2one('g3.config.champ', 'Formulaire à paramètrer')
    name     = fields.Many2one('ir.model.fields', 'Champ')

    vsb      = fields.Boolean('Visible')
    rqr      = fields.Boolean('Requis')

    _defaults = {
        'vsb': True,
    }

