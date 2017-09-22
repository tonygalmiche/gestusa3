Documentation d'installation de Gestusa3
===================

Installation d'Odoo version 8.0
===================

ATTENTION : Le module gestusa3 n'est compatible qu'avec la version 8.0 d'Odoo.

Vous pouvez installer Odoo suivant la méthode de votre choix.

Exemple d'installation sur Debian Jessie : 
===================

Une méthode simple pour connaître les dépendances à installer est de simuler une installation d'Odoo avec apt-get sans valider l'installation : 

    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys DEF2A2198183CBB5
    echo "deb http://nightly.odoo.com/10.0/nightly/deb/ ./" >> /etc/apt/sources.list 
    apt-get update
    apt-get install odoo

Il suffit de copier la liste des dépendances et d'installer celles-ci sans le paquet odoo.

Une fois les dépendances installées, il est possible d'installer odoo manuellement : 

    adduser odoo
    su postgres 
    createuser -s odoo

    cd /opt/
    wget https://github.com/odoo/odoo/archive/8.0.zip
    unzip 8.0.zip 
    mv 8.0 odoo
    chown -R odoo:odoo /opt/odoo
    mkdir /etc/odoo
    chown -R odoo /etc/odoo

    mkdir /opt/addons
    chown odoo /opt/addons

    mkdir /var/log/odoo
    chown odoo /var/log/odoo

Fichier de configuration : 

    vim /etc/odoo/odoo.conf 
    [options]
    admin_passwd = xxxx
    db_host = False
    db_port = False
    db_user = odoo
    db_password = False
    addons_path = /opt/addons

Mise en place des addons
===================

    cd /opt/addons
    git clone https://github.com/tonygalmiche/gestusa3.git

Il est conseillé de télécharger et de dézipper ces addons communautaires dans « /opt/addons » pour un fonctionnement optimale : 

    https://www.odoo.com/apps/modules/8.0/auditlog/
    https://www.odoo.com/apps/modules/8.0/mass_editing/
    https://www.odoo.com/apps/modules/8.0/web_export_view/
    https://www.odoo.com/apps/modules/8.0/web_tree_many2one_clickable/
    https://www.odoo.com/apps/modules/8.0/web_widget_color/
    https://www.odoo.com/apps/modules/8.0/web_ckeditor4/
    https://www.odoo.com/apps/modules/8.0/web_m2x_options/


Lancement de Odoo
===================

    /opt/odoo/openerp-server -c /etc/odoo/odoo.conf 

Odoo sera accessible sur le port 8069 : 
    
    http://localhost:8069


Installation des addons
===================

Avec le menu « Configuration / Modules locaux », il faut donc installer ces addons : 

    gestusa3
    auditlog
    mass_editing
    web_ckeditor4
    web_export_view 
    web_m2x_options
    web_tree_many2one_clickable
    web_widget_color

