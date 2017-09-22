# -*- coding: utf-8 -*-

from openerp import models,fields,api
from openerp.tools.translate import _
from openerp.exceptions import Warning
from parametres import g3_groupes, g3_couleurs
#import parametres
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

#TODO : 
# - Lors de la création d'un dossier, n'afficher que les contacts de type 'usager' dans la liste de choix
# - Pour les contacts ou personnes exetérieur,  afficher les contacts de type 'usager' dans le cas ou l'usager est responsable de lui-même
# -> Dans la liste de choix, il faudra proposer l'usager' en plus de pere, mere,...
# - Voir pour mettre la fonction _comput commune à tous les modèles et pour stocker les tableaux des champs dans les parametres
# - Voir pour adapter 'web_widget_color' pour mettre une liste de choix à la place du sélecteur de couleurs
# - Pour l'onglet accessibilité qui sera commun à toutes les tables, voir pour créer un objet hérité par tous les autres
# - Voir pour mettre les 8 groupes dans un modèle qui sera hérité des autres
# - Faire fonctionner mon module permettant de créer des listes peronnalisées
# - Dans la vue liste, voir s'il est possible d'afficher ou masquer les colonnes suivant le paramétrage des champs
# -> Il faut peut-être recontruire la vue liste xml à chaque modification du paramètrage des champs

# Ajouter un bouton sur l'usager pour créer directement un dossier depuis celui-ci
# Voir s'il est possible de récupérer en lecture seule les structures indiquées dans le dossier usager au niveau de l'usager 
# => pour que la secreétait puisse contacter l'autre structure pour avoir l'accès au dossier usager

# - Faire une doc au fur et à mesure
# - Mettre en place un script (tache plannifiée dans Odoo) qui recalculera les dossiers usagers en fonction de la date d'entrée ou de sortie de celui-ci


def set_visibility(self, champs):
    for obj in self:
        for champ in champs:
            setattr(obj, champ+"_vsb", True)
        for model in self.env['ir.model'].search([['model','=',self._name]]):
            for config_champ in self.env['g3.config.champ'].search([['name','=',model.id]]):
                for line in self.env['g3.config.champ.line'].search([['model_id','=',config_champ.id]]):
                    for champ in champs:
                        if line.name.name==champ:
                            if not line.vsb:
                                setattr(obj, champ+"_vsb", False)



class g3_dossier_usager(models.Model):
    _name='g3.dossier.usager'
    _description = 'Dossier usager'
    _order='usager_id'

    usager_id                 = fields.Many2one('g3.usager', 'Personne accompagnée', required=True)
    usager_adresse1           = fields.Text("Identité", store=False, compute='_usager_adresse1')
    identifiant               = fields.Char("Identifiant dossier")
    identifiant_vsb           = fields.Boolean('Champ technique', store=False, compute='_compute')
    photo                     = fields.Binary("Photo")
    photo_vsb                 = fields.Boolean('Champ technique', store=False, compute='_compute')
    etablissement_line        = fields.One2many('g3.dossier.usager.etablissement', 'dossier_usager_id', u"Etablissements")
    etablissement_ids         = fields.Many2many('g3.etablissement', 'g3_dossier_usager_etablissement_rel', 'dossier_id', 'etablissement_id', u"Etablissements", store=True, compute='_compute_etablissement_ids')
    code_couleur              = fields.Selection(g3_couleurs, "Code couleur")
    code_couleur_vsb          = fields.Boolean('Champ technique', store=False, compute='_compute')

    #color                     = fields.Char(string="Color", help="Choose your color")
    color = fields.Selection([
        ('#FF0000','rouge'),
        ('#FFA500','orange'),
        ('#0000FF','bleu'),
        ('#008000','vert'),
        ('#FFFF00','jaune'),
        ('#FFC0CB','rose'),
        ('#FF00FF','fuchsia'),
        ('#800000','marron'),
        ('#000000','noir'),
        ('#FFFFFF','blanc'),
    ], "Code Couleur")

    nationalite_id            = fields.Many2one('g3.nationalite', 'Nationalité')
    nationalite_id_vsb        = fields.Boolean('Champ technique', store=False, compute='_compute')

    document_line             = fields.One2many('g3.dossier.usager.document', 'dossier_usager_id', u"Documents")
    document_line_vsb         = fields.Boolean('Champ technique', store=False, compute='_compute')

    num_secu                  = fields.Char("N° de sécurité sociale")
    num_secu_vsb              = fields.Boolean('Champ technique', store=False, compute='_compute')

    notification_line         = fields.One2many('g3.dossier.usager.notification', 'dossier_usager_id', u"Notifications")
    notification_line_vsb     = fields.Boolean('Champ technique', store=False, compute='_compute')

    affiliation_line          = fields.One2many('g3.dossier.usager.affiliation', 'dossier_usager_id', u"Affiliations")
    affiliation_line_vsb      = fields.Boolean('Champ technique', store=False, compute='_compute')

    sejour_line               = fields.One2many('g3.dossier.usager.sejour', 'dossier_usager_id', u"Séjours")
    sejour_line_vsb           = fields.Boolean('Champ technique', store=False, compute='_compute')

    genogramme                = fields.Binary('Génogramme')
    genogramme_vsb            = fields.Boolean('Champ technique', store=False, compute='_compute')

    mesure_protection_line    = fields.One2many('g3.dossier.usager.mesure.protection', 'dossier_usager_id', u"Mesure de protection")
    mesure_protection_vsb     = fields.Boolean('Champ technique', store=False, compute='_compute')

    contact_line              = fields.One2many('g3.dossier.usager.contact', 'dossier_usager_id', u"Contacts")
    situation_parent_id       = fields.Many2one('g3.situation.familiale', 'Situation des parents')
    situation_parent_id_vsb   = fields.Boolean('Champ technique', store=False, compute='_compute')
    situation_usager_id       = fields.Many2one('g3.situation.familiale', "Situation de l'usager")
    situation_usager_id_vsb   = fields.Boolean('Champ technique', store=False, compute='_compute')
    info_pratique_line        = fields.One2many('g3.dossier.usager.info.pratique', 'dossier_usager_id', u"Informations pratiques")
    info_pratique_line_vsb    = fields.Boolean('Champ technique', store=False, compute='_compute')
    autorisation_line         = fields.One2many('g3.dossier.usager.autorisation', 'dossier_usager_id', u"Autorisations")
    autorisation_line_vsb     = fields.Boolean('Champ technique', store=False, compute='_compute')
    partenaire_line           = fields.One2many('g3.dossier.usager.partenaire', 'dossier_usager_id', u"Partenaires extérieurs")
    partenaire_line_vsb       = fields.Boolean('Champ technique', store=False, compute='_compute')
    parcours_line             = fields.One2many('g3.dossier.usager.parcours', 'dossier_usager_id', u"Parcours")
    parcours_line_vsb         = fields.Boolean('Champ technique', store=False, compute='_compute')
    diplome_line              = fields.One2many('g3.dossier.usager.diplome', 'dossier_usager_id', u"Diplomes / attestations")
    diplome_line_vsb          = fields.Boolean('Champ technique', store=False, compute='_compute')
    formation_line            = fields.One2many('g3.dossier.usager.formation', 'dossier_usager_id', u"Formations")
    formation_line_vsb        = fields.Boolean('Champ technique', store=False, compute='_compute')

    accessibilite_line = fields.One2many('g3.dossier.usager.accessibilite', 'dossier_usager_id', u"Accessibilités")
    group_01_id   = fields.Many2one('g3.groupe', g3_groupes['01'])
    group_02_id   = fields.Many2one('g3.groupe', g3_groupes['02'])
    group_03_id   = fields.Many2one('g3.groupe', g3_groupes['03'])
    group_04_id   = fields.Many2one('g3.groupe', g3_groupes['04'])
    group_05_id   = fields.Many2one('g3.groupe', g3_groupes['05'])
    group_06_id   = fields.Many2one('g3.groupe', g3_groupes['06'])
    group_07_id   = fields.Many2one('g3.groupe', g3_groupes['07'])
    group_08_id   = fields.Many2one('g3.groupe', g3_groupes['08'])

    createur_id   = fields.Many2one('res.users', 'Créé par', readonly=True)
    active        = fields.Boolean('Actif',default=True)


    _defaults = {
        'createur_id': lambda obj, cr, uid, ctx=None: uid,
    }



    def run_desactiver_dossier_action(self, cr, uid, use_new_cursor=False, company_id = False, context=None):
        self.run_desactiver_dossier(cr, uid, context)


    @api.multi
    def run_desactiver_dossier(self):
        date_limite=datetime.now()+relativedelta(months=-36)
        date_limite=date_limite.strftime('%Y-%m-%d')
        print "#### DEBUT recherche des dossiers à désactiver ####"
        dossier_obj = self.env['g3.dossier.usager']
        dossiers=dossier_obj.search([
            ('id','>',0),
        ])
        for dossier in dossiers:
            lines=dossier.etablissement_line
            date_sortie='2000-01-01'
            for line in lines:
                date=line.date_sortie_prevue
                if date==False:
                    date=datetime.now().strftime('%Y-%m-%d')
                if date>date_sortie:
                    date_sortie=date
            if date_sortie<date_limite:
                print "### Dossier à désactiver ###", dossier,date_limite,date_sortie
                dossier.active=False
        print "#### FIN ####"




    @api.depends('usager_id')
    def _usager_adresse1(self):
        #** Adresse de l'usager ************************************************
        for obj in self:
            if obj.usager_id:
                adresse = \
                    (obj.usager_id.prenom or '')+u' '    + \
                    (obj.usager_id.nom or '')+u' '
                date_naissance=obj.usager_id.date_naissance
                if date_naissance:
                    date_naissance=datetime.strptime(date_naissance, '%Y-%m-%d').strftime('%d/%m/%Y')
                    if obj.usager_id.sexe=='feminin':
                        adresse = adresse + u'née le '
                    else:
                        adresse = adresse + u'né le '
                    adresse = adresse + date_naissance+u'\n'
                adresse = adresse + \
                    (obj.usager_id.adresse1 or '')+u' '  + \
                    (obj.usager_id.adresse2 or '')+u'\n' + \
                    (obj.usager_id.cp       or '')+u' '  + \
                    (obj.usager_id.ville    or '')
                if obj.usager_id.secours_adresse1:
                    adresse = adresse + u'\nAdresse de secours : \n' + \
                        (obj.usager_id.secours_adresse1 or '')+u' '  + \
                        (obj.usager_id.secours_adresse2 or '')+u'\n' + \
                        (obj.usager_id.secours_cp       or '')+u' '  + \
                        (obj.usager_id.secours_ville    or '')
                obj.usager_adresse1 = adresse
        #***********************************************************************



    @api.depends('etablissement_line')
    def _compute_etablissement_ids(self):
        for obj in self:
            etablissement_ids  = []
            for line in obj.etablissement_line:
                etablissement_ids.append(line.etablissement_id.id)
            obj.etablissement_ids=[(6,0,etablissement_ids)]




    @api.depends('usager_id')
    def _compute(self):
        """Visibilité des champs"""
        champs=[
            'identifiant',
            'photo',
            'code_couleur',
            'nationalite_id',
            'situation_parent_id',
            'situation_usager_id',
            'info_pratique_line',
            'autorisation_line',
            'partenaire_line',
            'parcours_line',
            'diplome_line',
            'formation_line',
            'document_line',
            'num_secu',
            'notification_line',
            'affiliation_line',
            'regime_hebergement_id',
            'referent_usager_id',
            'genogramme',
        ]
        set_visibility(self, champs)


    @api.multi
    @api.depends('usager_id')
    def name_get(self):
        result = []
        for obj in self:
            result.append((obj.id, obj.usager_id.name_get()[0][1]))
        return result


#    # Blocage si dossier existe déjà pour cet usager
#    @api.multi
#    def cherche_doublon(self,usager_id):
#        print "cherche_doublon=",usager_id
#        dossiers=self.env['g3.dossier.usager'].search([ ['usager_id', '=', usager_id] ])
#        if len(dossiers)>1:

#            #Nom des structures ou cet usager est présent
#            etb=[]
#            for dossier in dossiers:
#                for line in dossier.etablissement_line:
#                    etb.append(line.etablissement_id.name)
#            raise Warning(u"Ce dossier usager existe déjà dans ces établissements : "+", ".join(etb))


    # Contraintes sur le dossier
    @api.multi
    def contraintes(self,obj):
        # Blocage si un dossier existe pour cet usager
        obj=obj.sudo()
        usager_id=obj.usager_id.id
        dossiers=self.env['g3.dossier.usager'].search([ ['usager_id', '=', usager_id] ])
        if len(dossiers)>1:
            #Nom des structures ou cet usager est présent
            etb=[]
            for dossier in dossiers:
                for line in dossier.etablissement_line:
                    etb.append(line.etablissement_id.name)
            raise Warning(u"Cette personne accompagnée existe déjà dans ces établissements : "+", ".join(etb))

        t=[]

        # Blocage si aucun établissement
        if not obj.etablissement_line:
            raise Warning("Il est obligatoire de sélectionner un établissement")

        # Blocage si la liste contient plusieurs fois le même établissement
        for row in obj.etablissement_line:
            id=row.etablissement_id.id
            if id in t:
                raise Warning("Il ne peut pas y avoir plusieurs fois le même établissement dans la liste")
            t.append(row.etablissement_id.id)
        # Blocage si plus de 5 contacts
        if len(obj.contact_line)>5:
            raise Warning("Il ne faut pas mettre plus de 5 contacts par personne accompagnée")

        # Blocage si plus de 2 responsable legal
        ct=0
        for row in obj.contact_line:
            if row.responsable_legal:
                ct=ct+1
        if ct>2:
            raise Warning("Il ne faut pas mettre plus de 2 responsable légal par personne accompagnée")







    @api.multi
    def gestion_accessibilites(self,obj):

        obj=obj.sudo()

        # Blocage si la date de fin est inférieur à la date de début
        for etablissement in obj.etablissement_line:
            date_entree = etablissement.date_entree
            date_sortie = etablissement.date_sortie_prevue
            if date_entree and date_sortie and date_sortie<date_entree:
                raise Warning("La date de sortie ne peut pas être inférieur à la date d'entrée pour l'établissement "+
                    str(etablissement.etablissement_id.name))
        #Suppression des établissements qui ne sont plus dans la liste
        for accessibilite in obj.accessibilite_line:
            accessibilite.sudo().unlink()
        #Creation des etablissements
        for etablissement in obj.etablissement_line:
            vals2={
                'dossier_usager_id': obj.id,
                'etablissement_id': etablissement.etablissement_id.id,
            }
            r=self.env['g3.dossier.usager.accessibilite'].sudo().create(vals2)
        for etablissement in obj.etablissement_line:
            date_entree = etablissement.date_entree
            date_sortie = etablissement.date_sortie_prevue
            now         = time.strftime('%Y-%m-%d',time.gmtime())
            datetime_object = datetime.now()
            new_date = datetime_object + relativedelta(years=-3)
            now3=new_date.strftime('%Y-%m-%d')
            for accessibilite in obj.accessibilite_line:
                if etablissement.etablissement_id==accessibilite.etablissement_id:
                    accessibilite.group_01 = False
                    accessibilite.group_02 = False
                    accessibilite.group_03 = False
                    accessibilite.group_04 = False
                    accessibilite.group_05 = False
                    accessibilite.group_06 = False
                    accessibilite.group_07 = False
                    accessibilite.group_08 = False
                    # Avant le séjour : Tous les droits sauf validation (DIV et DMV)
                    if(date_entree and date_entree<now):
                        accessibilite.group_01 = True
                        accessibilite.group_02 = True
                        accessibilite.group_03 = True
                        accessibilite.group_04 = True
                        accessibilite.group_05 = False
                        accessibilite.group_06 = True
                        accessibilite.group_07 = True
                        accessibilite.group_08 = False
                    # Pendant le séjour : Tous les droits 
                    if(date_entree and date_sortie and now>=date_entree and now<=date_sortie):
                        accessibilite.group_01 = True
                        accessibilite.group_02 = True
                        accessibilite.group_03 = True
                        accessibilite.group_04 = True
                        accessibilite.group_05 = True
                        accessibilite.group_06 = True
                        accessibilite.group_07 = True
                        accessibilite.group_08 = True
                    # Après le séjour : Lecture seule pour DA et DI et droits complets pour DM (DM, DMM et DMV)
                    if(date_sortie and now>date_sortie):
                        accessibilite.group_01 = True
                        accessibilite.group_02 = False
                        accessibilite.group_03 = True
                        accessibilite.group_04 = False
                        accessibilite.group_05 = False
                        accessibilite.group_06 = True
                        accessibilite.group_07 = True
                        accessibilite.group_08 = True
                    # Aprés 3 ans de séjour => Aucun droits
                    if(date_sortie and date_sortie<now3):
                        accessibilite.group_01 = False
                        accessibilite.group_02 = False
                        accessibilite.group_03 = False
                        accessibilite.group_04 = False
                        accessibilite.group_05 = False
                        accessibilite.group_06 = False
                        accessibilite.group_07 = False
                        accessibilite.group_08 = False

        # Création ou mise à jour des goupes
        self.gestion_groupes(obj)



    @api.multi
    def gestion_groupes(self,obj,etablissement_id=False):

        obj=obj.sudo()

        #for obj in self.sudo():
        for groupe in g3_groupes:
            #Recherche des membres des groupes en fonction des access dans l'établissement et dans la personne accompagnée
            users=[]
            for accessibilite in obj.accessibilite_line:
                if etablissement_id==False or accessibilite.etablissement_id.id==etablissement_id:
                    for line in accessibilite.etablissement_id.membres_line:
                        for user in line.profil_metier_id.membre_ids:
                            if user.id not in users:
                                for groupe2 in g3_groupes:
                                    if getattr(accessibilite, "group_"+groupe2) and getattr(line, "group_"+groupe2) and groupe==groupe2:
                                        users.append(user.id)
            vals2={
                'name': g3_groupes[groupe],
                'code': groupe,
                'dossier_usager_id': obj.id,
                'membre_ids': [[6, 0, users]],
            }
            for groupe2 in g3_groupes:
                group_xx=getattr(obj, "group_"+groupe2+"_id")
                #Création du groupe s'il n'existe pas
                if groupe==groupe2 and not group_xx:
                    obj2=self.env['g3.groupe'].sudo().create(vals2)
                    setattr(obj, "group_"+groupe2+"_id",obj2.id)
                #Mise à jour du groupe s'il existe
                if groupe==groupe2 and group_xx:
                    for grp in self.env['g3.groupe'].browse(group_xx.id):
                        setattr(obj, "group_"+groupe2+"_id",grp.id)
                        grp.sudo().write(vals2)


    # http://fr.wikipedia.org/wiki/Numero_de_Securite_sociale#Unicit.C3.A9
    def validInsee(self, vals):
        if 'num_secu' in vals:
            num_secu=vals['num_secu']
            if num_secu:
                msg=False
                if len(num_secu)<15:
                    msg="Le numéro de sécurité sociale doit faire au moins 15 caractères"
                else:
                    num_secu = num_secu.replace(' ', '')
                    insee = num_secu[0:len(num_secu)-2]
                    cle   = num_secu[-2:]
                    # gestion numeros corses
                    insee = insee.replace('A', '0')
                    insee = insee.replace('B', '0')
                    reste = int(insee) % 97
                    r=((97 - reste) == int(cle))
                    if not r:
                        msg="Numero de sécurité sociale non valide"
                if msg:
                    raise Warning(msg)



    @api.model
    def create(self, vals):
        obj = super(g3_dossier_usager, self).create(vals)
        self.contraintes(obj)
        self.gestion_accessibilites(obj)
        self.validInsee(vals)
        return obj


    @api.multi
    def write(self,vals):
        #self.run_desactiver_dossier()
        res=super(g3_dossier_usager, self).write(vals)
        for obj in self:
            self.contraintes(obj)
            if 'etablissement_line' in vals or 'accessibilite_line' in vals:
                self.gestion_accessibilites(obj)

        self.validInsee(vals)
        return res


    @api.multi
    def unlink(self):
        #Suppression des groupes associés au dossier
        for obj in self:
            for groupe in g3_groupes:
                grp=getattr(obj, "group_"+groupe+"_id")
                grp.unlink()
        res=super(g3_dossier_usager, self).unlink()
        return res




class g3_dossier_usager_etablissement(models.Model):
    _name='g3.dossier.usager.etablissement'
    _order='dossier_usager_id,date_entree'

    dossier_usager_id  = fields.Many2one('g3.dossier.usager', 'Personne accompagnée', required=True, ondelete='cascade')
    etablissement_id   = fields.Many2one('g3.etablissement', 'Etablissement'  , required=True)
    provenance         = fields.Char('Provenance')
    date_entree        = fields.Date("Date d'entrée", required=True)
    date_sortie_prevue = fields.Date("Date de sortie prévue")
    destination        = fields.Char('Destination')


class g3_dossier_usager_sejour(models.Model):
    _name='g3.dossier.usager.sejour'
    _order='dossier_usager_id,date_entree'

    dossier_usager_id         = fields.Many2one('g3.dossier.usager', 'Personne accompagnée', required=True, ondelete='cascade')
    etablissement_id          = fields.Many2one('g3.etablissement', 'Etablissement'  , required=True)
    date_entree               = fields.Date("Date d'entrée", required=True)
    date_sortie               = fields.Date("Date de sortie")

    regime_hebergement_id     = fields.Many2one('g3.regime.hebergement', "Régime d'hébergement")
    regime_hebergement_id_vsb = fields.Boolean('Champ technique', store=False, compute='_compute')

    referent_usager_id        = fields.Many2one('res.users', 'Référent personne accompagnée')
    referent_usager_id_vsb    = fields.Boolean('Champ technique', store=False, compute='_compute')

    referent_line             = fields.One2many('g3.dossier.usager.referent', 'sejour_id', u"Référents")
    referent_line_vsb         = fields.Boolean('Champ technique', store=False, compute='_compute')

    groupe_educatif_line      = fields.One2many('g3.dossier.usager.groupe.educatif', 'sejour_id', u"Groupe(s) éducatif(s)")
    groupe_educatif_line_vsb  = fields.Boolean('Champ technique', store=False, compute='_compute')

    atelier_line              = fields.One2many('g3.dossier.usager.atelier', 'sejour_id', u"Atelier(s)")
    atelier_line_vsb          = fields.Boolean('Champ technique', store=False, compute='_compute')

    classe_line               = fields.One2many('g3.dossier.usager.classe', 'sejour_id', u"Classe(s)")
    classe_line_vsb           = fields.Boolean('Champ technique', store=False, compute='_compute')


    @api.depends('etablissement_id')
    def _compute(self):
        """Visibilité des champs"""
        champs=[
            'regime_hebergement_id',
            'referent_usager_id',
            'referent_line',
            'groupe_educatif_line',
            'atelier_line',
            'classe_line',
        ]
        set_visibility(self, champs)




class g3_dossier_usager_mesure_protection(models.Model):
    _name='g3.dossier.usager.mesure.protection'
    _order='dossier_usager_id,date_debut'

    dossier_usager_id = fields.Many2one('g3.dossier.usager', 'Personne accompagnée', required=True, ondelete='cascade')
    type_mesure       = fields.Selection([('tutelle','Tutelle'),('curatelle','Curatelle')], "Type de mesure")
    date_debut        = fields.Date("Date de début", required=True)
    date_fin          = fields.Date("Date de fin")
    fichier_ids       = fields.Many2many('ir.attachment', 'g3_dossier_usager_mesure_protection_attachment_rel', 'mesure_protection_id', 'attachment_id', u'Pièces jointes')
    commentaire       = fields.Char("Commentaire")
    #piece_jointe     = fields.Binary('Pièce jointe')


class g3_dossier_usager_document(models.Model):
    _name='g3.dossier.usager.document'
    _order='name'

    dossier_usager_id  = fields.Many2one('g3.dossier.usager', 'Personne accompagnée', required=True, ondelete='cascade')
    name               = fields.Many2one('g3.type.document', 'Type de document', required=True)
    date               = fields.Date("Date de validité")
    fichier_ids        = fields.Many2many('ir.attachment', 'g3_dossier_usager_document_attachment_rel', 'document_id', 'attachment_id', u'Pièces jointes')
    #piece_jointe      = fields.Binary('Pièce jointe')

class g3_dossier_usager_notification(models.Model):
    _name='g3.dossier.usager.notification'
    _order='type_notification_id, date_debut'

    dossier_usager_id    = fields.Many2one('g3.dossier.usager', 'Personne accompagnée', required=True, ondelete='cascade')
    type_notification_id = fields.Many2one('g3.type.notification', "Type de notification")
    numero               = fields.Char("Numéro")
    en_date              = fields.Date("En date")
    date_debut           = fields.Date("Date de début")
    date_fin             = fields.Date("Date de fin")
    fichier_ids          = fields.Many2many('ir.attachment', 'g3_dossier_usager_notification_attachment_rel', 'notification_id', 'attachment_id', u'Pièces jointes')
    prescripteur         = fields.Many2one('g3.usager', 'Prescripteur',  domain=[('categorie', '=', 'partenaire_exterieur')])
    commentaire          = fields.Char("Commentaire")
    #piece_jointe        = fields.Binary('Pièce jointe')

class g3_dossier_usager_affiliation(models.Model):
    _name='g3.dossier.usager.affiliation'
    _order='type_affiliation_id, date_debut'

    dossier_usager_id    = fields.Many2one('g3.dossier.usager', 'Personne accompagnée', required=True, ondelete='cascade')
    type_affiliation_id  = fields.Many2one('g3.type.affiliation', "Type d'affiliation")
    type_assure_id       = fields.Many2one('g3.type.assure',"Assuré")
    nom_assure_autre     = fields.Char("Nom de l'assuré (si Assuré=Autre)")
    numero               = fields.Char("Numéro")
    en_date              = fields.Date("En date")
    date_debut           = fields.Date("Date de début")
    date_fin             = fields.Date("Date de fin")
    fichier_ids          = fields.Many2many('ir.attachment', 'g3_dossier_usager_affiliation_attachment_rel', 'affiliation_id', 'attachment_id', u'Pièces jointes')
    affiliateur          = fields.Many2one('g3.usager', 'Affiliateur',  domain=[('categorie', '=', 'partenaire_exterieur')])
    code_organisme       = fields.Char("Code organisme")
    code_gestion         = fields.Char("Code gestion")
    commentaire          = fields.Char("Commentaire")
    #piece_jointe        = fields.Binary('Pièce jointe')






class g3_dossier_usager_contact(models.Model):
    _name='g3.dossier.usager.contact'
    _order='name'

    dossier_usager_id  = fields.Many2one('g3.dossier.usager', 'Personne accompagnée', required=True, ondelete='cascade')
    name               = fields.Many2one('g3.usager', 'Contact', required=True)
    lien_id            = fields.Many2one('g3.lien', "Lien avec la personne accompagnée")
    responsable_legal  = fields.Boolean('Responsable légal')
    commentaire        = fields.Char('Commentaire')




class g3_dossier_usager_autorisation(models.Model):
    _name='g3.dossier.usager.autorisation'
    _order='name'

    dossier_usager_id  = fields.Many2one('g3.dossier.usager', 'Personne accompagnée', required=True, ondelete='cascade')
    name               = fields.Many2one('g3.type.autorisation', "Type d'autorisation", required=True)
    date               = fields.Date('Date')
    #fichier            = fields.Binary('Fichier')
    fichier_ids        = fields.Many2many('ir.attachment', 'g3_dossier_usager_autorisation_attachment_rel', 'autorisation_id', 'attachment_id', u'Pièces jointes')
    commentaire        = fields.Char('Commentaire')


class g3_dossier_usager_partenaire(models.Model):
    _name='g3.dossier.usager.partenaire'
    _order='name'

    dossier_usager_id       = fields.Many2one('g3.dossier.usager', 'Personne accompagnée', required=True, ondelete='cascade')
    name                    = fields.Many2one('g3.usager', 'Partenaire', required=True)
    categorie_partenaire_id = fields.Many2one('g3.categorie.partenaire', "Catégorie de partenaire")
    commentaire             = fields.Char('Commentaire')

class g3_dossier_usager_parcours(models.Model):
    _name='g3.dossier.usager.parcours'
    _order='dossier_usager_id,date_entree'

    dossier_usager_id       = fields.Many2one('g3.dossier.usager', 'Personne accompagnée', required=True, ondelete='cascade')
    date_entree             = fields.Date("Date d'entrée")
    type_structure_id       = fields.Many2one('g3.type.structure', 'Type de structure')
    nom_structure           = fields.Char('Nom de la structure')
    date_sortie             = fields.Date("Date de sortie")
    commentaire             = fields.Char('Commentaire')

class g3_dossier_usager_diplome(models.Model):
    _name='g3.dossier.usager.diplome'
    _order='name'

    dossier_usager_id = fields.Many2one('g3.dossier.usager', 'Personne accompagnée', required=True, ondelete='cascade')
    name              = fields.Char("Diplome / attestation")
    date              = fields.Date("Date")
    fichier_ids       = fields.Many2many('ir.attachment', 'g3_dossier_usager_diplome_attachment_rel', 'diplome_id', 'attachment_id', u'Pièces jointes')
    #piece_jointe     = fields.Binary('Pièce jointe')

class g3_dossier_usager_formation(models.Model):
    _name='g3.dossier.usager.formation'
    _order='name'

    dossier_usager_id = fields.Many2one('g3.dossier.usager', 'Personne accompagnée', required=True, ondelete='cascade')
    name              = fields.Char("Ecole")
    date_debut        = fields.Date("Date de début")
    date_fin          = fields.Date("Date de fin")

class g3_dossier_usager_accessibilite(models.Model):
    _name='g3.dossier.usager.accessibilite'
    _order='dossier_usager_id,etablissement_id'

    dossier_usager_id  = fields.Many2one('g3.dossier.usager', 'Personne accompagnée', required=True, ondelete='cascade')
    etablissement_id   = fields.Many2one('g3.etablissement', 'Etablissement'  , required=True)
    group_01   = fields.Boolean(g3_groupes['01'])
    group_02   = fields.Boolean(g3_groupes['02'])
    group_03   = fields.Boolean(g3_groupes['03'])
    group_04   = fields.Boolean(g3_groupes['04'])
    group_05   = fields.Boolean(g3_groupes['05'])
    group_06   = fields.Boolean(g3_groupes['06'])
    group_07   = fields.Boolean(g3_groupes['07'])
    group_08   = fields.Boolean(g3_groupes['08'])


class g3_dossier_usager_info_pratique(models.Model):
    _name='g3.dossier.usager.info.pratique'
    _order='name'
    dossier_usager_id  = fields.Many2one('g3.dossier.usager', 'Personne accompagnée', required=True, ondelete='cascade')
    name               = fields.Many2one('g3.info.pratique', 'Information pratique', required=True)
    commentaire        = fields.Char('Commentaire')


class g3_dossier_usager_referent(models.Model):
    _name='g3.dossier.usager.referent'
    _order='accompagnement_id'
    sejour_id          = fields.Many2one('g3.dossier.usager.sejour', 'Personne accompagnée', required=True, ondelete='cascade')
    referent_id        = fields.Many2one('res.users', 'Référent')
    accompagnement_id  = fields.Many2one('g3.accompagnement', 'Accompagnement')
    nom                = fields.Char('Commentaire')


class g3_dossier_usager_groupe_educatif(models.Model):
    _name='g3.dossier.usager.groupe.educatif'
    _order='name'
    dossier_usager_id  = fields.Many2one('g3.dossier.usager.sejour', 'Personne accompagnée', required=True, ondelete='cascade')
    name = fields.Char('Nom')

class g3_dossier_usager_groupe_educatif(models.Model):
    _name='g3.dossier.usager.groupe.educatif'
    _order='name'
    sejour_id  = fields.Many2one('g3.dossier.usager.sejour', 'Personne accompagnée', required=True, ondelete='cascade')
    name = fields.Char('Nom')

class g3_dossier_usager_atelier(models.Model):
    _name='g3.dossier.usager.atelier'
    _order='name'
    sejour_id  = fields.Many2one('g3.dossier.usager.sejour', 'Personne accompagnée', required=True, ondelete='cascade')
    name = fields.Char('Nom')

class g3_dossier_usager_classe(models.Model):
    _name='g3.dossier.usager.classe'
    _order='name'
    sejour_id  = fields.Many2one('g3.dossier.usager.sejour', 'Personne accompagnée', required=True, ondelete='cascade')
    name = fields.Char('Nom')


class g3_groupe(models.Model):
    _name='g3.groupe'
    _order='name'
    name              = fields.Char("Nom du groupe", required=True)
    code              = fields.Char("Code", required=True)
    dossier_usager_id = fields.Many2one('g3.dossier.usager', 'Personne accompagnée', required=True)
    membre_ids        = fields.Many2many('res.users', 'g3_groupe_membres_rel', 'groupe_id', 'user_id', 'Membres')


class g3_nationalite(models.Model):
    _name='g3.nationalite'
    _order='name'
    name              = fields.Char("Nationalité", required=True)


class g3_lien(models.Model):
    _name='g3.lien'
    _order='name'
    name              = fields.Char("Lien avec la personne accompagnée", required=True)


class g3_situation_familiale(models.Model):
    _name='g3.situation.familiale'
    _order='name'
    name              = fields.Char("Situation familiale", required=True)


class g3_info_pratique(models.Model):
    _name='g3.info.pratique'
    _order='name'
    name              = fields.Char("Information pratique", required=True)


class g3_type_autorisation(models.Model):
    _name='g3.type.autorisation'
    _order='name'
    name              = fields.Char("Type d'autorisation", required=True)

class g3_categorie_partenaire(models.Model):
    _name='g3.categorie.partenaire'
    _order='name'
    name              = fields.Char("Catégorie de partenaire", required=True)


class g3_type_structure(models.Model):
    _name='g3.type.structure'
    _order='name'
    name              = fields.Char("Type de structure", required=True)


class g3_type_document(models.Model):
    _name='g3.type.document'
    _order='name'
    name = fields.Char("Type de document", required=True)


class g3_type_notification(models.Model):
    _name='g3.type.notification'
    _order='name'
    name = fields.Char("Type de notification", required=True)

class g3_type_affiliation(models.Model):
    _name='g3.type.affiliation'
    _order='name'
    name = fields.Char("Type d'affiliation", required=True)


class g3_type_assure(models.Model):
    _name='g3.type.assure'
    _order='name'
    name = fields.Char("Type d'assuré", required=True)

class g3_regime_hebergement(models.Model):
    _name='g3.regime.hebergement'
    _order='name'
    name = fields.Char("Régime d'hébergement", required=True)


class g3_accompagnement(models.Model):
    _name='g3.accompagnement'
    _order='name'
    name = fields.Char("Accompagnement", required=True)


