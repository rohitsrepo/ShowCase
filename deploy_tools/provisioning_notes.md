Provisioning a new site
=======================

## Required packages:

* nginx
* python
* Git
* pip
* virtualenv
* python-dev
* rabbitmq-server
* OpenCV (Generate outline and graysclae things)
* libjpeg-dev (Image optimization with pillow)
* solr for search -> java

eg, on Ubuntu:

    sudo apt-get install nginx git python python-pip
    sudo pip3 install virtualenv

## Nginx Virtual Host config

* see nginx.template.conf
* replace SITENAME with, eg, staging.my-domain.com

## Upstart Job

* see gunicorn-upstart.template.conf
* replace SITENAME with, eg, staging.my-domain.com

## Folder structure:
Assume we have a user account at /home/username

/home/username
└── sites
    └── SITENAME
         ├── database
         ├── source
         ├── static
         └── virtualenv
         --- logs
         	--- celery
         	--- flower
