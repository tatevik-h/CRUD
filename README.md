# cfm-techdojo-survey-project

## Requirements
* Docker +20.10.12
* docker-compose +2.2.3

## Docker Compose for External Dependencies

**Build**
* Go to infra and execute:

`docker-compose build`

**Start**
* Go to infra and execute:

`docker-compose up -d`

**Stop**
* Go to infra and execute:

`docker-compose down -v`
* `-v` removes the volumes.

# Run the Application
The following instructions will enable you to build and run the cfm-techdojo-survey-project:
* Build the image:
    `docker build -t ${IMAGE_NAME} .`

* Run the docker image:
        `docker run -dp 8000:8000 ${IMAGE_NAME}`

## Swagger UI
For swagger ui, navigate to ------> `http://localhost:8000/docs`

## Automated run and test project
A `Makefile` has been created in order to automate build in the project.

The make file is composed by blocks that performs a specific checks. The following table explains the available blocks in the `Makefile`:

| Name            | Description                                             |
|-----------------|---------------------------------------------------------|
| start           | Create db, build image and start docker container.      |
| stop            | Stop db, remove image and down database.                |
| destroy         | Stop db, remove image, down database and clean data.    |
| buildDB         | First command will build db.                            |
| buildImage      | First command will build main image.                    |
| startContainer  | First command will start main container.                |
| stopContainer   | First command will stop main container.                 |
| removeContainer | First command will remove main container of main image. |
| removeImage     | First command will remove main image.                   |
| removeDB        | First command will remove main db.                      |
| downDB          | First command will down db.                             |
| destroyDB       | First command will destroy database.                    |
| reload          | First command will reload the main project.             |
| reloadInfra     | First command will reload database.                     |
| fullreload      | First command will reload the project.                  |
| insertData      | First command will insert data into 'waiter' table.     |
| insertFeedback  | First command will insert data into 'feedback' table.   |
| help            | First command will print help message.                  |

To execute one block of `Makefile`, run the command:

```bash
make <block_name>
```

- In order to run the development environment run the following command:
```bash
make start
```
- In order to stop the development environment run the following command:
```bash
make stop
```
- In order to destroy environment run the following command:
```bash
make destroy
```
