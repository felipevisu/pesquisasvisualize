# Pesquisas Visualize

Form creator developed in Python with the Django framework. Focused on generating statistics for election polls and collecting feedback for corporate purposes.

## Key features
* Creation of forms;
* Goals and objectives;
* Visualization and filters.

### Creating forms

The form designer allows you to define several types of custom fields;

![Screenshot from 2023-07-05 20-26-27](https://github.com/felipevisu/pesquisasvisualize/assets/9272668/490fe4af-54d1-498f-92cd-797ba43a7b8b)

**Options:**
* Selection;
* Multiple selection;
* Number;
* Text.

In addition to ordering the questions, marking questions as mandatory and validating the answers when submitting a new form.

### Goals and objectives

Definition of goals to be achieved in the collection of forms.

![Screenshot from 2023-07-05 20-48-14](https://github.com/felipevisu/pesquisasvisualize/assets/9272668/5b9f5332-45ca-4459-958e-f23f9633f28f)

**Options:**
* Neighborhoods;
* Groups of neighborhoods;
* Age group;
* Gender;
* Age.

### Visualization and filters

Visualization of results in graphs and possibility to apply filters and combine results.

![Screenshot from 2023-07-05 20-27-03](https://github.com/felipevisu/pesquisasvisualize/assets/9272668/be322c1c-c782-44e7-958c-4bbecbb02ff1)]

## Localhost execution

In an envirounment with Linux start and excecute a python virtualenv `venv`
```
virtualenv venv
source venv bin activate
```
Install the dependencies
```
pip install -r requirements.txt
```
Configure the .env file
```
SECRET_KEY=
DEBUG=
ALLOWED_HOSTS=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
FTP_USER=
FTP_PASSWORD=
FTP_HOST=
FTP_PATH=
```
Run in localhost
```
python manage.py runserver
```
