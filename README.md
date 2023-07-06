# Pesquisas Visualize

Criador de formulários desenvolvido em Python com o framework Django. Focado em gerar estatísticas para pesquisas eleitorais e coleta de feedback para fins corporativos.

## Principais recursos
* Criação de formulários;
* Metas e objectivos;
* Visualização e filtros.

### Criação de formulários

O criador de formulários permite definir diversos tipos de campos customizados;

![Screenshot from 2023-07-05 20-26-27](https://github.com/felipevisu/pesquisasvisualize/assets/9272668/490fe4af-54d1-498f-92cd-797ba43a7b8b)

**Opções:**
* Seleção;
* Seleção múltipla;
* Número;
* Texto.

Além de ordenar as questões, marcar questões como obrigatórias e validação das respostas na submição de um novo formulário.

### Metas e objectivos

Definição de metas a serem atigindas na coleta de formulários.

![Screenshot from 2023-07-05 20-48-14](https://github.com/felipevisu/pesquisasvisualize/assets/9272668/5b9f5332-45ca-4459-958e-f23f9633f28f)

**Opções:**
* Bairros;
* Grupos de bairros;
* Faixa etária;
* Gênero;
* Idade.

### Visualização e filtros

Visualização dos resultaros em gráficos e possibilidade de aplicar filtros e combinar resultados.

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
