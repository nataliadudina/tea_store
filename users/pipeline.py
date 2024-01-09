from django.contrib.auth.models import Group

""" Identifies users logged in via social network by group. """


def new_users_handler(backend, user, response, *args, **kwargs):
    group = Group.objects.filter(name='social')
    if len(group):
        user.groups.add(group[0])