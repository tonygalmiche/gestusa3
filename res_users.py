# -*- coding: utf-8 -*-

from openerp import models,fields,api
from openerp.tools.translate import _


class res_users(models.Model):
    _inherit = "res.users"

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        context=self._context
        if not args:
            args=[]
        if not context:
            context={}
        filtre=[]
        if 'etablissement_id' in context:
            print "etablissement_id"
            for etablissement in self.env['g3.etablissement'].browse(context['etablissement_id']):
                ids=[]
                for membre in etablissement.membre_ids:
                    ids.append(membre.id)
                filtre=[['name','ilike',name],['id','in',ids]]
        else:
            if name:
                filtre=['|',['name','ilike',name],['login','ilike',name]]
        recs = self.search(filtre + args, limit=limit)
        return recs.name_get()



class res_groups(models.Model):
    _inherit = "res.groups"
    _order='category_id,name'

    active = fields.Boolean('Actif')

    _defaults = {
        'active': True,
    }

