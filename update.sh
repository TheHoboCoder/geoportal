#!/bin/bash
cp -r /webapps/geoportal_project/geoportal/modules /tmp/
cp -r * /webapps/geoportal_project/geoportal
cd /webapps/geoportal_project/geoportal/geoportal
mv settings.py settings/base.py
mv /tmp/modules ../

su -l geoportal << EOF
echo "building frontend"
./build_vite.sh
./migrate.sh
EOF

echo "restarting apache2"
systemctl restart apache2.service

