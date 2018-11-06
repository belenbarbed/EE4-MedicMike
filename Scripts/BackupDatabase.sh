!#/bin/sh
cd $(dirname $0)
echo "Creating a version of the database to be pushed to git..."
date=`date +"%b-%d-%y-%H-%M-%S"`
mysqldump -u root -proot -x -e -A > ../Database/dbs.sql
git checkout dev/owen
git add dbs.sql
git commit -m "Database Backup for $date"
git push
git gc
