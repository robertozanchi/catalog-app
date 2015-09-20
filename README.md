
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

  3) Clone the content of GitHub repository into your local vagrant folder


  Run the Catalog App
  ------------------

  1) Initiate vagrant and launch the virtual machine with the command "vagrant ssh"

  2) Once in the virtual machine, change directory to the "catalog" folder

  3) Create catalog.db database by running "python database_setup.py"

  4) Populate database with item categories and sample items by running "python sample_data.py"

  5) Run the Catalog web application by running "python application.py"

  6) Visit http://localhost:5000/ in your browser