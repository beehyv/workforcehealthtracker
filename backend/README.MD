




####Mysql on docker 
Create docker image with :
 `docker run --name hcw-db -e MYSQL_ROOT_PASSWORD=beehyv123 -e MYSQL_DATABASE=hcw_test_25_03_20 -e MYSQL_USER=arnob -eMYSQL_PASSWORD=arnob  -p3306:3306 -d mysql:5.7.29`
 Access docker db with: 
 `docker exec -it hcw-db mysql -uarnob -parnob`