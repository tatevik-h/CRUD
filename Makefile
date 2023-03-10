IMAGE_NAME ?= app

##
##start
## 			info  |  --> Start project.
## 			usage |  --> make start
##
start: buildDB buildImage startContainer insertData insertFeedback

##
##stop
## 			info  |  --> Stop project.
## 			usage |  --> make stop
##
stop: stopContainer removeImage downDB

##
##destroy
## 			info  |  --> Destroy all.
## 			usage |  --> make destroy
##
destroy: stopContainer removeImage destroyDB 

##
##fullreload
## 			info  |  --> Reload all project. 
## 			usage |  --> make fullreload
##
fullreload: reloadInfra reload

##
##reload
## 			info  |  --> Reload app.
## 			usage |  --> make reload
##
reload: removeContainer buildImage startContainer insertData insertFeedback

##
##buildDB
## 			info  |  --> Build database. 
## 			usage |  --> make buildDB
##
buildDB:
	docker-compose -f infra/docker-compose.yml up -d

##
##buildImage
## 			info  |  --> Build image with given name. 
## 			usage |  --> make buildImage IMAGE_NAME=<IMAGE_NAME>
##
buildImage:
	docker build -t ${IMAGE_NAME} .

##
##startContainer
## 			info  |  --> Start container. 
## 			usage |  --> make startContainer IMAGE_NAME=<IMAGE_NAME>
##
startContainer: 
	docker run -dp 8000:8000 --name app --env-file ./config/variables/.env -v "$$(PWD):/code" ${IMAGE_NAME}

##
##stopContainer
## 			info  |  --> Stop container using image name.
## 			usage |  --> make stopContainer IMAGE_NAME=<IMAGE_NAME>
##
stopContainer:
	docker stop $$(docker ps -a | grep "${IMAGE_NAME} " | sed 's/ .*//' | xargs) 2> /dev/null || (tput setaf 1 && echo "No such running container using ${IMAGE_NAME} image name." && tput setaf 0)

##
##removeContainer
## 			info  |  --> Remove container using image name.
## 			usage |  --> make removeContainer IMAGE_NAME=<IMAGE_NAME>
##
removeContainer: stopContainer
	docker rm $$(docker ps -a | grep "${IMAGE_NAME} " | sed 's/ .*//'| xargs) 2> /dev/null || (tput setaf 1 && echo "No such container using ${IMAGE_NAME} image name." && tput sgr0)
	
##
##removeImage
## 			info  |  --> Remove image using image name.
## 			usage |  --> make removeImage IMAGE_NAME=<IMAGE_NAME>
##
removeImage: removeContainer 
	docker rmi $$(docker images --format="{{.Repository}} {{.ID}}" | grep "^${IMAGE_NAME} " | sed 's/${IMAGE_NAME} //' | xargs) 2> /dev/null || (tput setaf 1 && echo "No such image: ${IMAGE_NAME}" && tput sgr0) 

##
##downDB
## 			info  |  --> Down database.
## 			usage |  --> make downDB
##
downDB:
	docker-compose -f infra/docker-compose.yml down

##
##destroyDB
## 			info  |  --> Down database.
## 			usage |  --> make destroyDB
##
destroyDB:
	docker-compose -f infra/docker-compose.yml down -v

##
##reloadInfra
## 			info  |  --> Reload databases.
## 			usage |  --> make reloadInfra
##
reloadInfra:
	cd infra/ && docker-compose down -v && docker-compose up -d

##
##insertData
## 			info  |  --> Insert data into  'waiters' table.
## 			usage |  --> make insertData
##
insertData: 
	@sleep 5
	docker cp scripts/insert_waiters.sql postgres:/insert_waiters.sql
	docker exec -u postgres postgres psql db postgres -f insert_waiters.sql

##
##insertFeedback
## 			info  |  --> Insert data into  'feedback' table.
## 			usage |  --> make insertFeedback
##
insertFeedback:
	@sleep 5
	docker exec -it app python scripts/insert_feedback.py

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
