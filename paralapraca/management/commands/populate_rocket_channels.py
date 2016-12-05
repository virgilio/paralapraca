# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import Q

from pymongo import MongoClient, errors
from datetime import datetime
import random

User = get_user_model()

# Connect to rocket's database
client = MongoClient('mongodb', 27017)
db = client.paralapraca
rocket_channels = db.rocketchat_room
rocket_users = db.users
rocket_subscriptions = db.rocketchat_subscription


def genMeteorID():
    return('%024x' % random.randrange(16**24))


def create_subscription(user, channel):
    new_sub = {
        "_id": genMeteorID(),
        "open": "true",
        "alert": "false",
        "unread": 0,
        "ts": datetime.now(),
        "rid": channel['id'],
        "name": channel['name'],
        "t": "c",
        "u": {
            "_id": user['id'],
            "username": user['username']
        },
        "_updatedAt": datetime.now(),
        "ls": datetime.now()
    }
    try:
        rocket_subscriptions.insert_one(new_sub)
    except errors.DuplicateKeyError:
        print("Duplicated subscription")
        pass


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

        # Populate each channel
        # Geral
        print("-----------")
        channel = {"id": "QRviDMnqyNSBTGNQh", "name": "geral"}
        usernames = []
        for user in users_geral:
            rocket_user = rocket_users.find_one({"emails": {"$elemMatch": {"address": user.email}}})
            if rocket_user is None:
                print(user.username + " " + user.email)
                continue
            usernames.append(rocket_user['username'])
            create_subscription({"id": rocket_user['_id'], "username": rocket_user['username']}, channel)
        print("Importing channel geral")
        rocket_channels.update({"_id": channel['id']}, {"$addToSet": {"usernames": {"$each": usernames}}})

        # Camaçari
        print("-----------")
        channel = {"id": "tBggre83oJSjkTA4g", "name": "camacari"}
        usernames = []
        for user in users_camacari:
            rocket_user = rocket_users.find_one({"emails": {"$elemMatch": {"address": user.email}}})
            if rocket_user is None:
                print(user.username + " " + user.email)
                continue
            usernames.append(rocket_user['username'])
            create_subscription({"id": rocket_user['_id'], "username": rocket_user['username']}, channel)
        print("Importing channel camacari")
        rocket_channels.update({"_id": channel['id']}, {"$addToSet": {"usernames": {"$each": usernames}}})

        # Maracanaú
        print("-----------")
        channel = {"id": "hTwXJ2uzsLgHzRieM", "name": "maracanau"}
        usernames = []
        for user in users_maracanau:
            rocket_user = rocket_users.find_one({"emails": {"$elemMatch": {"address": user.email}}})
            if rocket_user is None:
                print(user.username + " " + user.email)
                continue
            usernames.append(rocket_user['username'])
            create_subscription({"id": rocket_user['_id'], "username": rocket_user['username']}, channel)
        print("Importing channel maracanau")
        rocket_channels.update({"_id": channel['id']}, {"$addToSet": {"usernames": {"$each": usernames}}})

        # Natal
        print("-----------")
        channel = {"id": "ewBKkFrtg8RnSeJyw", "name": "natal"}
        usernames = []
        for user in users_natal:
            rocket_user = rocket_users.find_one({"emails": {"$elemMatch": {"address": user.email}}})
            if rocket_user is None:
                print(user.username + " " + user.email)
                continue
            usernames.append(rocket_user['username'])
            create_subscription({"id": rocket_user['_id'], "username": rocket_user['username']}, channel)
        print("Importing channel natal")
        rocket_channels.update({"_id": channel['id']}, {"$addToSet": {"usernames": {"$each": usernames}}})

        # Olinda
        print("-----------")
        channel = {"id": "GExqAwPhEoQa9n7N5", "name": "olinda"}
        usernames = []
        for user in users_olinda:
            rocket_user = rocket_users.find_one({"emails": {"$elemMatch": {"address": user.email}}})
            if rocket_user is None:
                print(user.username + " " + user.email)
                continue
            usernames.append(rocket_user['username'])
            create_subscription({"id": rocket_user['_id'], "username": rocket_user['username']}, channel)
        print("Importing channel olinda")
        rocket_channels.update({"_id": channel['id']}, {"$addToSet": {"usernames": {"$each": usernames}}})

        # Maceió
        print("-----------")
        channel = {"id": "J9o5wYiNwhxLn38GF", "name": "maceio"}
        usernames = []
        for user in users_maceio:
            rocket_user = rocket_users.find_one({"emails": {"$elemMatch": {"address": user.email}}})
            if rocket_user is None:
                print(user.username + " " + user.email)
                continue
            usernames.append(rocket_user['username'])
            create_subscription({"id": rocket_user['_id'], "username": rocket_user['username']}, channel)
        print("Importing channel maceio")
        rocket_channels.update({"_id": channel['id']}, {"$addToSet": {"usernames": {"$each": usernames}}})

        # Gestores
        print("-----------")
        channel = {"id": "8Hm5MQmTn3hxgKmH7", "name": "gestores"}
        usernames = []
        for user in users_gestores:
            rocket_user = rocket_users.find_one({"emails": {"$elemMatch": {"address": user.email}}})
            if rocket_user is None:
                print(user.username + " " + user.email)
                continue
            usernames.append(rocket_user['username'])
            create_subscription({"id": rocket_user['_id'], "username": rocket_user['username']}, channel)
        print("Importing channel gestores")
        rocket_channels.update({"_id": channel['id']}, {"$addToSet": {"usernames": {"$each": usernames}}})
