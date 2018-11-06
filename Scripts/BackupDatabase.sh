!#/bin/sh
echo "Creating a version of the database to be pushed to git..."
date=`date +"%b-%d-%y-%H-%M-%S"`
mysqldump -u root -proot -x -e -A > ~/Documents/University/Fourth_Year/HCR/EE4-PostBotPat/Database/dbs.sql
git checkout dev/owen
git add dbs.sql
git commit -m "Database Backup for $date"
git push
git gc
