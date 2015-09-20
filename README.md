
                          Catalog App

  What is this?
  -----------

  The Catalog App is a web application created by Roberto 
  Zanchi as a stage 3 project for the Full Stack Web Developer
  Nanodegree. Catalog app is coded in Python using the Flask
  framework and runs on a Vagrant virtual machine.
  

  Installation
  ------------------

  1) Install Vagrant https://www.vagrantup.com/

  2) Install VirtualBox https://www.virtualbox.org/

  3) Clone the content of GitHub repository https://github.com/robertozanchi/catalog-web-application
     into your local vagrant folder

  4) Flask and Werkzeug versions. This app was coded on a system using:
     Werkzeug 0.8.3
     Flask 0.9
     Flask-Login 0.1.3


  Run the Catalog App
  ------------------

  1) Initiate vagrant and launch the virtual machine with the command "vagrant ssh"

  2) Once in the virtual machine, change directory to the "catalog" folder

  3) Create catalog.db database by running "python database_setup.py"

  4) Populate database with item categories and sample items by running "python sample_data.py"

  5) Run the Catalog web application by running "python application.py"

  6) Visit http://localhost:5000/ in your browser


  APIs
  ------------------

  JSON: A JSON catalog of items is available at /application/JSON

  XML: An XML catalog of items is available at /application/xml 