#!/bin/bash
DOMAINNAME=$1
SUBDOMEN=$2
# 1. clone repository
 #git clone https://github.com/TheHoboCoder/deploy-geodjango.git ../deploy-geodjango
# 2. remove all in modules just in case
mkdir modules || rm -R modules/*
mkdir static/dist
cd ../deploy-geodjango/
chmod u+x deploy.sh common_funcs.sh
pwd
# 3. run script
./deploy.sh geoportal $DOMAINNAME $SUBDOMEN
# 4. change ownership of media
chown geoportal:www-data /webapps/geoportal_project/geoportal/modules
chmod g+w /webapps/geoportal_project/geoportal/modules

cat > /webapps/geoportal_project/build_vite.sh << EOF
#!/bin/bash
cd geoportal
npm install
export NODE_OPTIONS="--max-old-space-size=4096"
npx vite build
EOF

chown geoportal:webapps /webapps/geoportal_project/build_vite.sh
chmod u+x /webapps/geoportal_project/build_vite.sh

su -l geoportal << EOF
echo "building frontend"
./build_vite.sh
./migrate.sh
EOF

echo "restarting apache2"
systemctl restart apache2.service

echo "DEPLOYMENT DONE!!!"