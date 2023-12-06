<h1>Arms-tracker App</h1>

This repository is part of the arms-tracker app, an interactive web-application visualising the flow of arms ex- and imports and the impact on global conflict.

You can visit the app at <a href=https://www.arms-tracker.app>www.arms-tracker.app</a>

For a full documentation please go to <a href=https://github.com/Kafkaese/taro> this repository </a>, which serves as a landing page and gives a better overview of the entire project. Below you can find the section of the documentation that refers to this repository in particular.

<h2>Backend Repository</h2>
This repository contains the backend of the arms-tracker app. This includes:

<h4>EDA Jupyter Notebooks</h4>
Every data  projects  starts with the collection and exploration of data. Here you can find EDA notebooks as well as notebooks containing the first code for data pipelines.
Since some of the additional data is scraped from Wikipedia, you can also find notebooks with web scrapers in this section.

<h4>API Code</h4>
The REST API was written in python using the <a href=https://fastapi.tiangolo.com/>FastAPI</a> package. It is served by a <a href=https://www.uvicorn.org/>Uvicorn Web Server</a>. The API serves as the interface between the <a href=https://www.postgresql.org/>Postgresql</a> Database and the Frontend. It contains various endpoints for get requests to retrieve data in a safe way and encapsulates the complexity of the sql queries. The whole API is containerized with <a href=https://www.docker.com/>Docker</a> for fast and easy deployment.

 <h4>Pipeline</h4>
 In order to get the raw data preprocessed into the Postgresql Database that the API queries, there are various data pipelines. They are in the form of a custom python package named 'taro'. This way they can easily be containerized and quickly run from said container.

 <h4>Tests</h4>
 In order to ensure a good devlopment workflow, the code for both the API, as well as the Pipelines, comes with a number of tests. The <a href=https://docs.pytest.org/en/7.4.x/>Pytest</a> package was used to write these. The tests are crucial for the CI workflow discussed later.

 <h4>Development Environment</h4>
 For local development there are a number of files for a convinient development environment. This includes a <a href=https://docs.docker.com/compose/>Docker Compose</a> configuration. 
The configuration consists of services for the API, a postgresql server and the pipelines. Optionally, a frontend container can be enabled, but it it often turned out to be more convinient to have the frontend run on a seperate development server.
 In order to be able to have ssl encryption in the development stage already, the neccesary files for this are also in this repository. This ssl certificate and key are locally trusted only and serve allow the development of ssl-encrypted content locally. The cerficate and key were created with <a href=https://github.com/FiloSottile/mkcert>mkcert</a>.

 <h4>Continious Integration</h4>
 Due to the microservice architecture of the appllication and the subsequent splitting of the code into several repositories, part of the CI pipeline is in this repository. Specifically, a Test Environment that is run every time a non-draft pull-request into the main branch of the taro-data respository is opened or synchronized. For this purpose a Github Actions workflow is used.
 The workflow uses <a href=https://www.terraform.io/>Terraform</a> to provision a Test Environment on <a href=https://www.terraform.io/>Microsoft Azure</a>. This includes:
 <br></br>

 - A Resource Group.
 - A Container Registry. 
 - A Postgresql Flexible Server
 - A Container Group

After the environment has been provisioned, the images for the API and the Data Pipelines are build and pushed to the container registry and the Pipeline is run.  Then the  Container Group starts an instance of the API image and the tests can be run. In a final step, no matter what the outcome of any previous  steps, the Test Environment is destroyed. This is in  order to minimize the costs of the infrastructure. 
 
