The data portal for SNARC

Django             3.0.3  
Python             3.6.9


GCP:

Web server http://34.94.195.199/

Sql server 34.94.253.37


Cloud storage snarc-dataset

Installing
1. clone the Git repo
2. move the GCP key folder to the root
3. move the huc_data to django-mip/dataPortal/lib/huc_data
4. setup the environment in the djangoMip_uwsgi.ini
5. setup the Nginx
6. run django in Uwsgi


if the ip changed, change the setting in the Django and Nginx config