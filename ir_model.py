# -*- coding: utf-8 -*-

from openerp import models,fields,api
from openerp.tools.translate import _


class ir_model(models.Model):
    _inherit = "ir.model"


    @api.multi
    @api.depends('nom', 'prenom')
    def name_get(self):
        result = []
        for obj in self:
            result.append((obj.id, obj.model))
        return result


    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        context=self._context
        res=super(ir_model, self).name_search(name, args, operator, limit)
        if 'config_champ' in context:
            filtre=[['model','in',[
                    'g3.etablissement',
                    'g3.dossier.usager',
                    'g3.dossier.usager.accessibilite',
                    'g3.dossier.usager.etablissement',
                    'g3.dossier.usager.sejour',
                ]]]
            if name:
                filtre.append(['model','ilike',name])
            res = self.search(filtre + args, limit=limit).name_get()
        return res



class ir_model_fields(models.Model):
    _inherit = 'ir.model.fields'

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        context=self._context
        res=super(ir_model_fields, self).name_search(name, args, operator, limit)
        if 'config_champ' in context:
            filtre=[
                ['name','not in',[
                    'create_date',
                    'create_uid',
                    'display_name',
                    'id',
                    'write_date',
                    'write_uid',
                    '__last_update']
                ],
                ['readonly', '!=', True],
                ['required', '!=', True],
                ['name', 'not like', 'group_'],
                ['name', 'not like', '_vsb']
            ]


            if name:
                filtre.append(['name','ilike',name])
            res = self.search(filtre + args, limit=limit).name_get()
        return res





