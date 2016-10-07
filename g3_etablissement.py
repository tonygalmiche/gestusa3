# -*- coding: utf-8 -*-

from openerp import models,fields,api
from openerp.tools.translate import _
from openerp.exceptions import Warning
from parametres import g3_groupes


class g3_etablissement(models.Model):
    _name='g3.etablissement'
    _order='name'

    name           = fields.Char('Nom', required=True)


    identifiant    = fields.Char('Identifiant')
    identifiant_vsb= fields.Boolean('Champ technique', store=False, compute='_compute')

    directeur_id   = fields.Many2one('res.users', 'Directeur', required=True)
    responsable_id = fields.Many2one('res.users', 'Responsable')

    membre_ids     = fields.Many2many('res.users', 'g3_etablissement_membres_rel', 'etablissement_id', 'user_id', 'Membres')

    adresse1       = fields.Char('Adresse')
    adresse1_vsb   = fields.Boolean('Champ technique', store=False, compute='_compute')

    adresse2       = fields.Char('Adresse (suite)')
    adresse2_vsb   = fields.Boolean('Champ technique', store=False, compute='_compute')

    cp             = fields.Char('CP')
    cp_vsb         = fields.Boolean('Champ technique', store=False, compute='_compute')

    ville          = fields.Char('Ville')
    ville_vsb      = fields.Boolean('Champ technique', store=False, compute='_compute')

    telephone      = fields.Char('Téléphone')
    telephone_vsb  = fields.Boolean('Champ technique', store=False, compute='_compute')

    fax            = fields.Char('Fax')
    fax_vsb        = fields.Boolean('Champ technique', store=False, compute='_compute')

    membres_line   = fields.One2many('g3.etablissement.membres', 'etablissement_id', 'Professionnels')

    _sql_constraints = [
        ('name_uniq'       , 'unique(name)'       , u"Le nom de l'établissement doit être unique !"),
    ]


    @api.depends()
    def _compute(self):
        champs=['identifiant','adresse1','adresse2','cp','ville','telephone','fax']
        for obj in self:
            for champ in champs:
                setattr(obj, champ+"_vsb", True)
            vsb=True
            for model in self.env['ir.model'].search([['model','=',self._name]]):
                for config_champ in self.env['g3.config.champ'].search([['name','=',model.id]]):
                    for line in self.env['g3.config.champ.line'].search([['model_id','=',config_champ.id]]):
                        for champ in champs:
                            if line.name.name==champ:
                                if not line.vsb:
                                    setattr(obj, champ+"_vsb", False)






    @api.multi
    def _membres_line(self):
        vals=[]
        for obj in self.env['g3.profil'].search([]):
            vals.append({
                'profil_id': obj.id,
                'group_01': obj.group_01,
                'group_02': obj.group_02,
                'group_03': obj.group_03,
                'group_04': obj.group_04,
                'group_05': obj.group_05,
                'group_06': obj.group_06,
                'group_07': obj.group_07,
                'group_08': obj.group_08,
            })
            
        return vals

    _defaults = {
        'membres_line': _membres_line,
    }




    @api.model
    def create(self, vals):
        obj = super(g3_etablissement, self).create(vals)
        self.create_profil_metier(obj)
        return obj


    @api.multi
    def write(self,vals):

        #Ajout du directeur et responsable dans la liste des membres
        #TODO : Bug à revoir
#        ids=[]
#        for obj in self:
#            if 'membre_ids' in vals:
#                ids=vals['membre_ids'][0][2]
#            else:
#                for membre in obj.membre_ids:
#                    ids.append(membre.id)
#            if 'directeur_id' in vals:
#                ids.append(vals['directeur_id'])
#            else:
#                if obj.directeur_id:
#                    ids.append(obj.directeur_id.id)
#            if 'responsable_id' in vals:
#                ids.append(vals['responsable_id'])
#            else:
#                if obj.responsable_id:
#                    ids.append(obj.responsable_id.id)
#        vals['membre_ids']=[[6, 0, ids]]
        res=super(g3_etablissement, self).write(vals)




        #Mise à jour des groupes des dossiers usagers attachés à cet établissement
        for obj in self:
            dossiers=self.env['g3.dossier.usager.accessibilite'].search([['etablissement_id','=',obj.id]])
            for dossier in dossiers:
                dossier.dossier_usager_id.gestion_groupes(dossier.dossier_usager_id.sudo(),obj.id)


        #Mise à jour du groupe des directeurs
        if 'directeur_id' in vals or 'responsable_id' in vals:
            group = self.pool.get('ir.model.data').get_object_reference(self._cr, self._uid, 'gestusa3', 'group_g3_directeur')
            etablissements=self.env['g3.etablissement'].search([])
            users=[]
            for etablissement in etablissements:
                if etablissement.directeur_id:
                    users.append(etablissement.directeur_id.id)
                if etablissement.responsable_id:
                    users.append(etablissement.responsable_id.id)
            for grp in self.env['res.groups'].browse(group[1]):
                vals2={
                    'users': [[6, 0, users]],
                }
                grp.sudo().write(vals2)

        #Mise à jour des profil metier
        for obj in self:
            self.create_profil_metier(obj)
        return res


    @api.multi
    def create_profil_metier(self,obj):
        for line in obj.membres_line:
            if not line.profil_metier_id:
                v={
                    'etablissement_id': obj.id,
                    'name': line.profil_id.name,
                    'profil_id': line.profil_id.id,
                }
                new_id=self.env['g3.profil.metier'].create(v)
                line.profil_metier_id=new_id





    @api.multi
    def copy(self,vals):
        for obj in self:
            vals.update({
                'name': obj.name + ' (copie)',
                'identifiant': '',
            })
        return super(g3_etablissement, self).copy(vals)



class g3_etablissement_membres(models.Model):
    _name='g3.etablissement.membres'
    _description = 'Groupes des membres de la structure'

    etablissement_id = fields.Many2one('g3.etablissement', 'Etablissement')
    profil_id        = fields.Many2one('g3.profil', 'Profil', required=True)
    profil_metier_id = fields.Many2one('g3.profil.metier', 'Profil Metier', readonly="1")
    group_01   = fields.Boolean(g3_groupes['01'])
    group_02   = fields.Boolean(g3_groupes['02'])
    group_03   = fields.Boolean(g3_groupes['03'])
    group_04   = fields.Boolean(g3_groupes['04'])
    group_05   = fields.Boolean(g3_groupes['05'])
    group_06   = fields.Boolean(g3_groupes['06'])
    group_07   = fields.Boolean(g3_groupes['07'])
    group_08   = fields.Boolean(g3_groupes['08'])


    @api.multi
    def onchange_profil_id(self,id):
        vals={}
        if id:
            for obj in self.env['g3.profil'].browse([id]):
                vals={
                    'group_01': obj.group_01,
                    'group_02': obj.group_02,
                    'group_03': obj.group_03,
                    'group_04': obj.group_04,
                    'group_05': obj.group_05,
                    'group_06': obj.group_06,
                    'group_07': obj.group_07,
                    'group_08': obj.group_08,
                }
        return {'value': vals}




