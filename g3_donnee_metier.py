# -*- coding: utf-8 -*-

from openerp import models,fields,api
from openerp.tools.translate import _
import uuid
from appy.pod.renderer import Renderer



class g3_donnee_metier(models.Model):
    _name='g3.donnee.metier'
    _order='dossier_usager_id,titre'

    dossier_usager_id = fields.Many2one('g3.dossier.usager', "Dossier usager", required=True)
    titre              = fields.Char('Titre', required=True)
    contenu           = fields.Text('Contenu')


    @api.multi
    def name_get(self):
        result = []
        for obj in self:
            name=obj.dossier_usager_id.name_get()[0][1]+u' - '+obj.titre
            result.append((obj.id, name))
        return result


    @api.multi
    def generation_odt(self):
        for obj in self:
            print obj


            alea=str(uuid.uuid4())
            appy_model    = "/tmp/appy_model_"+alea+".odt"
            appy_model    = "/tmp/model.odt"

            appy_dest     = "/tmp/appy_dest_"+alea+".odt"
            appy_dest_pdf = "/tmp/appy_dest_"+alea+".pdf"
            #f = open(appy_model,'wb')
            #f.write(contenu.decode('base64'))
            #f.close()

            v = {}
            v["o"]    = obj
            v['test'] = 'Ceci est un test'

            # ** Génération du fichier avec Appy ***********************
            renderer = Renderer(appy_model, v, appy_dest)
            renderer.run()
            # **********************************************************

#        # ** Transformation en PDF *********************************
#        if type=="PDF":
#            cde="soffice --headless   --convert-to pdf:writer_pdf_Export "+appy_dest+" --outdir /tmp"
#            os.system(cde)
#        #***********************************************************

#        # ** Recherche si une pièce jointe est déja associèe *******
#        name=nom[:-4]
#        if type=="PDF":
#            name=name+".pdf"
#        else:
#            name=name+".odt"
#        obj = self.pool.get('ir.attachment')
#        model=str(self)
#        ids = obj.search(cr, uid, [('res_model','=',model),('res_id','=',id),('name','=',name)], context=context)
#        # **********************************************************

#        # ** Creation ou modification de la pièce jointe ***********
#        #r = open(appy_dest,'rb').read().encode('base64')
#        dest=appy_dest
#        if type=="PDF":
#            dest=appy_dest_pdf
#        r = open(dest,'rb').read().encode('base64')

#        vals = {
#            'name':        name,
#            'datas_fname': name,
#            'type':        'binary',
#            'res_model':   model,
#            'res_id':      id,
#            'datas':       r,
#        }
#        if ids:
#            obj.write(cr, SUPERUSER_ID, ids[0], vals, context=context)
#            print "Modification ir.attachment id="+str(ids[0])
#        else:
#            id = obj.create(cr, SUPERUSER_ID, vals, context=context)
#            print "Création ir.attachment id="+str(id)
#        os.system("rm -f "+appy_model)
#        os.system("rm -f "+appy_dest)
#        os.system("rm -f "+appy_dest_pdf)
#        #***********************************************************************



