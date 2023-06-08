#!/bin/bash
cp -r /webapps/geoportal_project/geoportal/modules /tmp/
rm -r /webapps/geoportal_project/geoportal/modules
cp -r * /webapps/geoportal_project/geoportal
cd /webapps/geoportal_project/geoportal/geoportal
mv settings.py settings/base.py
mv  /tmp/modules ../

chown -R geoportal:www-data ../modules
chmod -R g+w ../modules

su -l geoportal << EOF
echo "building frontend"
./build_vite.sh
./migrate.sh
EOF

echo "restarting apache2"
systemctl restart apache2.service

