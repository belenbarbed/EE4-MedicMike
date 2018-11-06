#!/bin/sh
read -p "This action will overwrite Baxter's database with the version stored on this branch on git. Are you sure you wish to continue?" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
  #Pull and overwrite database
  git fetch
  git pull
  mysqldump -u root -proot < ~/Documents/University/Fourth_Year/HCR/EE4-PostBotPat/Database/dbs.sql
  echo "Done"
fi
