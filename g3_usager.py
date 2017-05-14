# -*- coding: utf-8 -*-

from openerp import models,fields,api
from openerp.tools.translate import _
from openerp.exceptions import Warning


class g3_usager(models.Model):
    _name='g3.usager'
    _order='nom, prenom, categorie'
    _rec_name = 'nom'


    categorie        = fields.Selection([('usager', 'Usager'), ('entourage', 'Entourage'), ('partenaire_exterieur', 'Partenaire extérieur')], 'Catégorie', select=True, required=True)
    type             = fields.Selection([('physique', 'Personne Physique'), ('morale', 'Personne Morale')], 'Type', required=False)
    sexe             = fields.Selection([('feminin', 'Féminin'), ('masculin', 'Masculin')], 'Sexe', required=False)
    nom              = fields.Char('Nom', required=True)
    nom_jeune_fille  = fields.Char('Nom de jeune fille')
    prenom           = fields.Char('Prénom', required=False)
    date_naissance   = fields.Date('Date de naissance', required=False)
    lieu_naissance   = fields.Char('Lieu de naissance')
    profession_id    = fields.Many2one('g3.profession', "Profession / Type d'établissement")
    cat_socio_id     = fields.Many2one('g3.cat.socio.professionnelle', "Catégorie socio-professionnelle")
    vit_avec_id      = fields.Many2one('g3.usager', "Vit avec", select=True)
    domicile_secours = fields.Boolean('Domicile de secours')
    adresse1         = fields.Char('Adresse')
    adresse2         = fields.Char("Complèment d'adresse")
    cp               = fields.Char('Code postal')
    ville            = fields.Char('Ville')
    telephone        = fields.Char('Téléphone')
    mobile           = fields.Char('Mobile')
    courriel         = fields.Char('Courriel')
    secours_adresse1 = fields.Char('Adresse')
    secours_adresse2 = fields.Char("Complèment d'adresse")
    secours_cp       = fields.Char('Code postal')
    secours_ville    = fields.Char('Ville')
    commentaire      = fields.Text('Commentaire')
    createur_id      = fields.Many2one('res.users', 'Créé par', readonly=True)
    

    _defaults = {
        'createur_id': lambda obj, cr, uid, ctx=None: uid,
    }

    @api.multi
    @api.depends('nom', 'prenom')
    def name_get(self):
        result = []
        for obj in self:
            name= obj.nom+u" "+(obj.prenom or u'')
            result.append((obj.id,name))
        return result


    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if args is None:
            args = []
        recs = self.browse()
        if name:
            #print args, name
            if len(args)>0:
                args=[args[0],'|',['nom','ilike',name],['prenom','ilike',name]]
            else:
                args=['|',['nom','ilike',name],['prenom','ilike',name]]
        recs = self.search(args, limit=limit)
        return recs.name_get()


    @api.model
    def create(self, vals):
        if 'vit_avec_id' in vals:
            vals=self._vit_avec_id(vals, vals['vit_avec_id'])
        obj = super(g3_usager, self).create(vals)
        self.cherche_doublon(obj)
        return obj


    @api.multi
    def write(self,vals):
        for obj in self:
            if 'vit_avec_id' in vals:
                vals=self._vit_avec_id(vals, vals['vit_avec_id'])
            res=super(g3_usager, self).write(vals)
            self.cherche_doublon(obj)
            #** Mise à jour des adresses des usagers vivants avec ce contact ***
            r=self.env['g3.usager'].search([ ['id', '!=', obj.id],['vit_avec_id', '=', obj.id]])
            for usager in r:
                usager.adresse1 = obj.adresse1
                usager.adresse2 = obj.adresse2
                usager.cp       = obj.cp
                usager.ville    = obj.ville
            #*******************************************************************
        return res






    # Blocage si nom existe déja
    @api.multi
    def cherche_doublon(self,obj):
        r=self.env['g3.usager'].search([ ['categorie', '=', obj.categorie],['type', '=', obj.type],['sexe', '=', obj.sexe],['nom', '=', obj.nom],['prenom', '=', obj.prenom],['date_naissance', '=', obj.date_naissance] ])
        if len(r)>1:
            raise Warning(u"Cet usager ou ce contact existe déjà : "+\
                str(obj.categorie or '')+" "+\
                str(obj.type or '')+" "+\
                str(obj.sexe or '')+" "+\
                obj.nom+" "+str(obj.prenom or '')+u" né le "+\
                str(obj.date_naissance or '')+u'\ncréé par '+\
                str(obj.createur_id.name or '')
            )


    @api.multi
    def onchange_vit_avec(self, vit_avec_id):
        vals = {}
        if vit_avec_id:
            vals=self._vit_avec_id(vals, vit_avec_id)
        return {'value': vals}


    @api.multi
    def _vit_avec_id(self, vals, vit_avec_id):
        usager=self.env['g3.usager'].browse(vit_avec_id)
        vals.update({'adresse1': usager.adresse1})
        vals.update({'adresse2': usager.adresse2})
        vals.update({'cp'      : usager.cp})
        vals.update({'ville'   : usager.ville})
        return vals




class g3_profession(models.Model):
    _name='g3.profession'
    _order='name'

    name              = fields.Char("Profession", required=True)




class g3_cat_socio_professionnelle(models.Model):
    _name='g3.cat.socio.professionnelle'
    _order='name'

    name = fields.Char("Catégorie socio-professionnelle", required=True)





