

//Cette fonction est importée automatiquement, car elle porte le même nom que le module
openerp.gestusa3 = function(instance) {

    //Surcharge de la fonction fournie par le module web_ckeditor4 pour configurer ckeditor

    instance.web_ckeditor4.FieldCKEditor4 = instance.web_ckeditor4.FieldCKEditor4.extend({

        ckeditor_config: {
            removePlugins: 'iframe,flash,forms,smiley,pagebreak,stylescombo',
            filebrowserImageUploadUrl: 'dummy',

            //Permet de désactiver certains plugins pour éviter les bugs par exemple
            //Cela permmet de supprimer également les icones de ces plugins
            removePlugins: 'iframe,flash,forms,smiley,pagebreak,stylescombo',

            filebrowserImageUploadUrl: 'dummy',

            //TODO : J'ai du ajouter manuellement le plugin tableresize pour pouvoir modifier la largeur des colonnes
            //http://ckeditor.com/addon/tableresize
            extraPlugins: 'filebrowser,button,colorbutton,floatpanel,panel,panelbutton,dialogui,tableresize',

            allowedContent: true,
            /*
            allowedContent:
              'h1 h2 h3 p blockquote strong em;' +
              'a[!href];' +
              'img(left,right)[!src,alt,width,height];' +
              'table tr th td caption;' +
              'span{!font-family};' +
              'span{!color};' +
              'span(!marker);' +
              'del ins',
            */


            // this is '#39' per default which screws up single quoted text in ${}
            entities_additional: '',

            //Permet de forcer la langue, mais normalement, celle-ci est sélectionnée automatiquement
            language : 'fr',
            defaultLanguage : 'fr',

            //Permet de changer la couleur de l'interface => Complètement inutile, mais ca fonctionne :)
            //uiColor : '#AADC6E',


            //Ces lignes permettent de paramètrer la barre d'outils
            /*
            toolbar: [
              { name: 'clipboard', groups: [ 'clipboard', 'undo' ], items: [ 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo' ] },
              { name: 'editing', groups: [ 'find', 'selection', 'spellchecker' ], items: [ 'Scayt' ] },
              { name: 'links', items: [ 'Link', 'Unlink' ] },
              { name: 'insert', items: [ 'Table', 'HorizontalRule', 'SpecialChar' ] },
              { name: 'tools', items: [ 'Maximize' ] },
              { name: 'document', groups: [ 'mode', 'document', 'doctools' ], items: [ 'Source' ] },
              { name: 'others', items: [ '-' ] },
              '/',
              { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ], items: [ 'Bold', 'Italic', 'Underline', '-', 'RemoveFormat' ] },
              { name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi' ], items: [ 'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote' ] },
              { name: 'styles', items: [ 'Styles', 'Format', 'Subscript','Superscript' ] }
            ],
            */

            //Il est possible aussi d'indique la liste des icones à supprimer
            //Liste des icones : http://ckeditor.com/forums/CKEditor/Complete-list-of-toolbar-items
            //removeButtons : 'About,Image,Anchor',


            //Configurateur de la barre d'outils en ligne : http://ckeditor.com/latest/samples/toolbarconfigurator/index.html#advanced
            toolbar : [
                { name: 'clipboard', items: [ 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo' ] },
                { name: 'editing', items: [ 'Scayt' ] },
                { name: 'basicstyles', items: [ 'Bold', 'Italic', 'Underline',  'Subscript', 'Superscript', '-', 'CopyFormatting', 'RemoveFormat' ] },
                { name: 'paragraph', items: [ 'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock' ] },
                { name: 'links', items: [ 'Link', 'Unlink', 'Anchor' ] },
                { name: 'insert', items: [ 'Table', 'Image', 'HorizontalRule','SpecialChar' ] },
                { name: 'styles', items: [ 'Styles', 'Format', 'Font', 'FontSize' ] },
                { name: 'colors', items: [ 'TextColor', 'BGColor' ] },
                { name: 'tools', items: [ 'Maximize', 'ShowBlocks' ] },
                { name: 'document', items: [ 'Source' ] },
            ],


            //Style apparaissant dans la liste de choix des styles
            format_tags : 'p;h1;h2;h3;h4;h5;pre',

            //Permet de supprimer les onglets 'Avancé' de certianes boites de dialogue
            //removeDialogTabs : 'image:advanced;link:advanced',
            removeDialogTabs : 'image:advanced',

        },


    });

}

