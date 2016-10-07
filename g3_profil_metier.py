# -*- coding: utf-8 -*-

from openerp import models,fields,api
from openerp.tools.translate import _
from openerp.exceptions import Warning

from parametres import g3_groupes

class g3_profil(models.Model):
    _name='g3.profil'
    _order='name'

    name       = fields.Char('Nom du profil', required=True)
    group_id   = fields.Many2one('res.groups', 'Groupe', help="Groupe associé à ce profil pour la gestion des l'affichage des onglets")

    group_01   = fields.Boolean(g3_groupes['01'])
    group_02   = fields.Boolean(g3_groupes['02'])
    group_03   = fields.Boolean(g3_groupes['03'])
    group_04   = fields.Boolean(g3_groupes['04'])
    group_05   = fields.Boolean(g3_groupes['05'])
    group_06   = fields.Boolean(g3_groupes['06'])
    group_07   = fields.Boolean(g3_groupes['07'])
    group_08   = fields.Boolean(g3_groupes['08'])

    _sql_constraints = [
        ('name_uniq'       , 'unique(name)'       , u"Le nom doit être unique !"),
    ]


class g3_profil_metier(models.Model):
    _name='g3.profil.metier'
    _order='etablissement_id,name'

    name              = fields.Char('Nom du profil', required=True)
    etablissement_id  = fields.Many2one('g3.etablissement', 'Etablissement')
    membre_ids        = fields.Many2many('res.users', 'g3_profil_metier_membres_rel', 'profil_metier_id', 'user_id', 'Membres')
    profil_id         = fields.Many2one('g3.profil', 'Profil Parent')

    _sql_constraints = [
    ]
    

    @api.multi
    def write(self,vals):
        res=super(g3_profil_metier, self).write(vals)
        for obj in self:
            #Recherche les membres des profil_metier ayant le même parent et alimente le groupe d'utilisateurs correspondant
            profils=self.env['g3.profil.metier'].search([['profil_id', '=', obj.profil_id.id]])
            users=[]
            for profil in profils:
                for membre in profil.membre_ids:
                    if membre.id not in users:
                        users.append(membre.id)
            for group in self.env['res.groups'].browse(obj.profil_id.group_id.id):
                group.sudo().write({'users': [(6, 0,  users)]})

            #Mise à jour des groupes des dossiers usagers attachés à cet établissement
            dossiers=self.env['g3.dossier.usager.accessibilite'].search([['etablissement_id','=',obj.etablissement_id.id]])
            for dossier in dossiers:
                print "Mise à jour",dossier.dossier_usager_id
                #dossier.dossier_usager_id.update_groupes()
                dossier.dossier_usager_id.gestion_groupes(dossier.dossier_usager_id,obj.etablissement_id.id)

        return res

                #    r=self.env['g3.dossier.usager.accessibilite'].sudo().create(vals2)




