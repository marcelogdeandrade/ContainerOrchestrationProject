#! /usr/bin/python
# -*- coding: utf-8 -*-

import click
import json
import requests
import pprint
import os
import os.path

base = 'http://localhost:3000/'
headers = {'Content-type': 'application/json'}

filename = "config"
directory = os.path.expanduser('~/.marcelao')
config_path = os.path.join(directory, filename)

@click.group()
def all():
    """CLI para gerencimento dos servicos"""
    pass


#Get Service
@all.command()
def get_service(**kwargs):
    """Retorna inforações do serviço"""
    url = base + 'getService'
    if(_check_config_exists()):
        with open(config_path, 'r') as output:
            _id = output.readline().strip().split('=')[1]
            username = output.readline().strip().split('=')[1]
            response = requests.get(
                url, headers=headers, data=json.dumps({'username': username}))
            click.echo(response.text)

#Credentials config
@all.command()
@click.option('--username', prompt=True, help='Username desejado')
@click.option('--password', prompt=True, hide_input=True,
              confirmation_prompt=True, help='Senha desejada')
def configure(username, password):
    """Cadastra um usuario no servico"""
    if(_check_config_exists()):
        click.confirm('Ja foi cadastrado um usuario, voce quer sobreescrever o usuario existente?', abort=True)
    url = base + 'adduser'
    response = requests.post(url, headers=headers, data=json.dumps({'username': username, 'password': password}))
    if (response.status_code == 200):
        data = json.loads(response.content)
        text = _format_config_file(data['_id'], data['username'])
        with open(config_path, 'w') as output:
            output.write(text)
        click.echo('Usuario criado com sucesso!')
    elif (response.status_code == 400):
        data = json.loads(response.content)
        click.echo('Houve um erro ao criar o usuario.')
        click.echo(data['errmsg'])

#Add Service
@all.command()
@click.option('--username', help='Username do usuario')
def create_service(username):
    """Cria um serviço com Load Balancer e Escalabilidade Horizontal"""
    url = base + 'createService'
    if(_check_config_exists()):
        with open(config_path, 'r') as output:
            _id = output.readline().strip().split('=')[1]
            username = output.readline().strip().split('=')[1]
            response = requests.post(url, headers=headers, data=json.dumps({'username': username}))
            click.echo(response.text)

#Delete Service
@all.command()
@click.option('--username', help="Username do usuario")
def delete_service(username):
    """Deleta um serviço criado"""
    url = base + 'deleteService'
    if(_check_config_exists()):
        with open(config_path, 'r') as output:
            _id = output.readline().strip().split('=')[1]
            username = output.readline().strip().split('=')[1]
            response = requests.post(
                url, headers=headers, data=json.dumps({'username': username}))
            click.echo(response.text)

#Auxiliary functions
def _check_config_exists():
    return os.path.isfile(config_path)

def _format_config_file(id, username):
    return "id={0}\nusername={1}\n".format(id, username)

if __name__ == '__main__':
    if not os.path.exists(directory):
        os.makedirs(directory)
    all()