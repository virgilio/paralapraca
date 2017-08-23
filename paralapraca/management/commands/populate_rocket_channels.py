# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import Q
from core.models import Class

from random import random
import requests
import os


User = get_user_model()
rocket = os.getenv('ROCKET_CHAT_API')
api_user = {
    'username': os.getenv('ROCKET_CHAT_USER'),
    'password': os.getenv('ROCKET_CHAT_PASS')
}

def create_chat_user(username):
    user = User.objects.get(username=username)
    create_req = requests.post(rocket + 'users.create', headers=auth_headers, json={
        'name'    : user.username,
        'email'   : user.email,
        'password': '%d%f' % (user.id, random()),
        'username': user.username,
        'verified': True,
    })
    return create_req

def sync_room(user_list, group):
    rocket_group_req = requests.get(rocket + 'groups.info?roomName=' + group, headers=auth_headers)
    rocket_group = rocket_group_req.json()

    # For compatibility reasons with the Rocket Chat permissions system, the user making the requests needs to be a member of the room to control it
    # The next line ensures that the main user won't be removed from any group by this script
    user_list += [api_user['username']]

    # Anyone that is in the group, but isn't in the user_list, must be removed
    for group_member in rocket_group['group']['usernames']:
        if group_member not in user_list:
            # Get the userId
            user = requests.get(rocket + 'users.info?username=' + group_member, headers=auth_headers)
            
            # Kick him from the room
            kick = requests.post(rocket + 'groups.kick', headers=auth_headers, json={
                'roomId': rocket_group['group']['_id'],
                'userId': user.json()['user']['_id']
            })
            if not kick.ok:
                print("Couldn't kick " + group_member + " from " + rocket_group['group']['name'])

    # Anyone in the user_list that isn't in the group, must be invited
    for timtec_user in user_list:
        if timtec_user not in rocket_group['group']['usernames']:
            
            # Get the userId
            user = requests.get(rocket + 'users.info?username=' + timtec_user, headers=auth_headers)
            if not user.ok:
                # If Rocket.Chat couldn't find the user, he probably isn't there yet
                # So create a profile for him now
                user = create_chat_user(timtec_user)
                if not user.ok:
                    # If creation failed as well, human attention is needed for him
                    print("Couldn't locate or create " + timtec_user)
                    continue
            
            # Include him in the room
            invite = requests.post(rocket + 'groups.invite', headers=auth_headers, json={
                'roomId': rocket_group['group']['_id'],
                'userId': user.json()['user']['_id']
            })
            if not invite.ok:
                print("Couldn't invite " + group_member + " for " + rocket_group['group']['name'])


class Command(BaseCommand):
    help = 'Synchronize Django user groups with Rocket Chat Rooms taking specific grouping rules into account.'

    def handle(self, **options):

        global api_user_data
        api_user_data = requests.post(rocket + 'login', json=api_user).json()
        
        global auth_headers
        auth_headers = {
            'X-Auth-Token': api_user_data['data']['authToken'],
            'X-User-Id': api_user_data['data']['userId']
        }

        ### Get the users list for each room ###
        # Group 'geral'
        users = User.objects.all().exclude(
            Q(groups__name="Gestores") |
            Q(groups__name="Gestores Camaçari") |
            Q(groups__name="Gestores Maceió") |
            Q(groups__name="Gestores Maracanaú") |
            Q(groups__name="Gestores Natal") |
            Q(groups__name="Gestores Olinda")
        ).distinct().values_list('username')
        sync_room([u[0] for u in users], 'geral')
        
        # Group 'natal'
        users = User.objects.filter(
            Q(groups__name="Avante") |
            Q(groups__name="Entremeios") |
            Q(groups__name="Assessoras Natal") |
            Q(groups__name="Natal") |
            Q(groups__name="Mediadoras")
        ).distinct().values_list('username')
        sync_room([u[0] for u in users], 'natal')

        # Group 'camacari'
        users = User.objects.filter(
            Q(groups__name="Avante") |
            Q(groups__name="Entremeios") |
            Q(groups__name="Assessoras Camaçari") |
            Q(groups__name="Camaçari") |
            Q(groups__name="Mediadoras")
        ).distinct().values_list('username')
        sync_room([u[0] for u in users], 'camacari')

        # Group 'maracanau'
        users = User.objects.filter(
            Q(groups__name="Avante") |
            Q(groups__name="Entremeios") |
            Q(groups__name="Assessoras Maracanaú") |
            Q(groups__name="Maracanaú") |
            Q(groups__name="Mediadoras")
        ).distinct().values_list('username')
        sync_room([u[0] for u in users], 'maracanau')

        # Group 'maceio'
        users = User.objects.filter(
            Q(groups__name="Avante") |
            Q(groups__name="Entremeios") |
            Q(groups__name="Assessoras Maceió") |
            Q(groups__name="Maceió") |
            Q(groups__name="Mediadoras")
        ).distinct().values_list('username')
        sync_room([u[0] for u in users], 'maceio')
        
        # Group 'olinda'
        users = User.objects.filter(
            Q(groups__name="Avante") |
            Q(groups__name="Entremeios") |
            Q(groups__name="Assessoras Olinda") |
            Q(groups__name="Olinda") |
            Q(groups__name="Mediadoras")
        ).distinct().values_list('username')
        sync_room([u[0] for u in users], 'olinda')
        

        # Classes must be synchronized also
        users = Class.objects.get(name='Turma FIRMEZA - Maracanaú').students.all().values_list('username')
        sync_room([u[0] for u in users], 'turma_firmeza')

        users = Class.objects.get(name='Turma IRINÉIA - Maceió').students.all().values_list('username')
        sync_room([u[0] for u in users], 'turma_irineia')

        users = Class.objects.get(name='Turma PRA TODO CANTO - Camaçari').students.all().values_list('username')
        sync_room([u[0] for u in users], 'turma_pratodocanto')

        users = Class.objects.get(name='Turma AQUI E ACOLÁ - Olinda').students.all().values_list('username')
        sync_room([u[0] for u in users], 'turma_aquieacola')

        users = Class.objects.get(name='Turma JUAQUINA - Natal').students.all().values_list('username')
        sync_room([u[0] for u in users], 'turma_juaquina')

        users = Class.objects.get(name='Turma DORIAN - Natal').students.all().values_list('username')
        sync_room([u[0] for u in users], 'turma_dorian')

        users = Class.objects.get(name='Turma NAVARRO - Natal').students.all().values_list('username')
        sync_room([u[0] for u in users], 'turma_navarro')