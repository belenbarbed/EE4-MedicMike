
#!/bin/sh
cd $(dirname $0)
read -p "This action will overwrite Baxter's database with the version stored on this branch on git. Are you sure you wish to continue?" -n 1 -r
echo
password="root"
if [[ $REPLY =~ ^[Yy]$ ]]
then
  #Pull and overwrite database
  git fetch
  git pull
  mysqldump -u root -p Baxter< ../Database/dbs.sql
  echo "Done"
fi
