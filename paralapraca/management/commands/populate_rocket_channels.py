# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import Q

from pymongo import MongoClient

User = get_user_model()


class Command(BaseCommand):
    help = 'Synchronize Django user groups with Rocket Chat Channels taking specific grouping rules into account.'

    def handle(self, **options):

        # Retrieve the admin superuser
        User = get_user_model()

        # Get the users list for each room
        users_geral = User.objects.all().exclude(groups__name="Gestores")

        users_camacari = (
            User.objects.filter(Q(groups__name="Camaçari") |
                                Q(groups__name="Assessoras Camaçari") |
                                Q(groups__name="Avante") |
                                Q(groups__name="Entremeios"))
                        .exclude(Q(groups__name="Gestores") |
                                 Q(groups__name="Gestores Camaçari"))
                        .distinct()
        )

        users_maracanau = (
            User.objects.filter(Q(groups__name="Maracanaú") |
                                Q(groups__name="Assessoras Maracanaú") |
                                Q(groups__name="Avante") |
                                Q(groups__name="Entremeios"))
                        .exclude(Q(groups__name="Gestores") |
                                 Q(groups__name="Gestores Maracanaú"))
                        .distinct()
        )

        users_natal = (
            User.objects.filter(Q(groups__name="Natal") |
                                Q(groups__name="Assessoras Natal") |
                                Q(groups__name="Avante") |
                                Q(groups__name="Entremeios"))
                        .exclude(Q(groups__name="Gestores") |
                                 Q(groups__name="Gestores Natal"))
                        .distinct()
        )

        users_olinda = (
            User.objects.filter(Q(groups__name="Olinda") |
                                Q(groups__name="Assessoras Olinda") |
                                Q(groups__name="Avante") |
                                Q(groups__name="Entremeios"))
                        .exclude(Q(groups__name="Gestores") |
                                 Q(groups__name="Gestores Olinda"))
                        .distinct()
        )

        users_maceio = (
            User.objects.filter(Q(groups__name="Maceió") |
                                Q(groups__name="Assessoras Maceió") |
                                Q(groups__name="Avante") |
                                Q(groups__name="Entremeios"))
                        .exclude(Q(groups__name="Gestores") |
                                 Q(groups__name="Gestores Maceió"))
                        .distinct()
        )

        users_gestores = (
            User.objects.filter(Q(groups__name="Gestores") |
                                Q(groups__name="Gestores Camçari") |
                                Q(groups__name="Gestores Maceió") |
                                Q(groups__name="Gestores Maracanaú") |
                                Q(groups__name="Gestores Natal") |
                                Q(groups__name="Gestores Olinda") |
                                Q(groups__name="Avante") |
                                Q(groups__name="Entremeios"))
                        .distinct()
        )

        # Connect to rocket's database
        client = MongoClient('mongo-paralapraca.docker', 27017)
        db = client.paralapraca
        rocket_channels = db.rocketchat_room
        rocket_users = db.users

        # Populate each channel
        # Geral
        print("-----------")
        usernames = []
        for user in users_geral:
            rocket_user = rocket_users.find_one({"emails": {"$elemMatch": {"address": user.email}}})
            if rocket_user is None:
                print(user.username + " " + user.email)
                continue
            usernames.append(rocket_user['username'])
        print("Importing channel geral")
        rocket_channels.update({"_id": "QRviDMnqyNSBTGNQh"}, {"$addToSet": {"usernames": {"$each": usernames}}})

        # Camaçari
        print("-----------")
        usernames = []
        for user in users_camacari:
            rocket_user = rocket_users.find_one({"emails": {"$elemMatch": {"address": user.email}}})
            if rocket_user is None:
                print(user.username + " " + user.email)
                continue
            usernames.append(rocket_user['username'])
        print("Importing channel camacari")
        rocket_channels.update({"_id": "tBggre83oJSjkTA4g"}, {"$addToSet": {"usernames": {"$each": usernames}}})

        # Maracanaú
        print("-----------")
        usernames = []
        for user in users_maracanau:
            rocket_user = rocket_users.find_one({"emails": {"$elemMatch": {"address": user.email}}})
            if rocket_user is None:
                print(user.username + " " + user.email)
                continue
            usernames.append(rocket_user['username'])
        print("Importing channel maracanau")
        rocket_channels.update({"_id": "hTwXJ2uzsLgHzRieM"}, {"$addToSet": {"usernames": {"$each": usernames}}})

        # Natal
        print("-----------")
        usernames = []
        for user in users_natal:
            rocket_user = rocket_users.find_one({"emails": {"$elemMatch": {"address": user.email}}})
            if rocket_user is None:
                print(user.username + " " + user.email)
                continue
            usernames.append(rocket_user['username'])
        print("Importing channel natal")
        rocket_channels.update({"_id": "ewBKkFrtg8RnSeJyw"}, {"$addToSet": {"usernames": {"$each": usernames}}})

        # Olinda
        print("-----------")
        usernames = []
        for user in users_olinda:
            rocket_user = rocket_users.find_one({"emails": {"$elemMatch": {"address": user.email}}})
            if rocket_user is None:
                print(user.username + " " + user.email)
                continue
            usernames.append(rocket_user['username'])
        print("Importing channel olinda")
        rocket_channels.update({"_id": "GExqAwPhEoQa9n7N5"}, {"$addToSet": {"usernames": {"$each": usernames}}})

        # Maceió
        print("-----------")
        usernames = []
        for user in users_maceio:
            rocket_user = rocket_users.find_one({"emails": {"$elemMatch": {"address": user.email}}})
            if rocket_user is None:
                print(user.username + " " + user.email)
                continue
            usernames.append(rocket_user['username'])
        print("Importing channel maceio")
        rocket_channels.update({"_id": "J9o5wYiNwhxLn38GF"}, {"$addToSet": {"usernames": {"$each": usernames}}})

        # Gestores
        print("-----------")
        usernames = []
        for user in users_gestores:
            rocket_user = rocket_users.find_one({"emails": {"$elemMatch": {"address": user.email}}})
            if rocket_user is None:
                print(user.username + " " + user.email)
                continue
            usernames.append(rocket_user['username'])
        print("Importing channel gestores")
        rocket_channels.update({"_id": "LZxQypGvjoM6uvmcZ"}, {"$addToSet": {"usernames": {"$each": usernames}}})
