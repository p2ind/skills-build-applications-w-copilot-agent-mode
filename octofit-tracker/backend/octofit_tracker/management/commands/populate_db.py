from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection
from djongo import models as djongo_models

from octofit_tracker import models as app_models

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete all data from collections
        User = get_user_model()
        User.objects.all().delete()
        Team = self.get_or_create_model('Team')
        Activity = self.get_or_create_model('Activity')
        Leaderboard = self.get_or_create_model('Leaderboard')
        Workout = self.get_or_create_model('Workout')
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create users
        users = [
            User.objects.create_user(username='ironman', email='ironman@marvel.com', password='password', team=marvel),
            User.objects.create_user(username='spiderman', email='spiderman@marvel.com', password='password', team=marvel),
            User.objects.create_user(username='batman', email='batman@dc.com', password='password', team=dc),
            User.objects.create_user(username='superman', email='superman@dc.com', password='password', team=dc),
        ]

        # Create activities
        activities = [
            Activity.objects.create(user=users[0], type='run', duration=30, distance=5),
            Activity.objects.create(user=users[1], type='cycle', duration=45, distance=15),
            Activity.objects.create(user=users[2], type='swim', duration=60, distance=2),
            Activity.objects.create(user=users[3], type='run', duration=25, distance=4),
        ]

        # Create workouts
        workouts = [
            Workout.objects.create(user=users[0], name='Chest Day', description='Bench press, push-ups'),
            Workout.objects.create(user=users[1], name='Leg Day', description='Squats, lunges'),
            Workout.objects.create(user=users[2], name='Back Day', description='Pull-ups, rows'),
            Workout.objects.create(user=users[3], name='Cardio', description='Running, cycling'),
        ]

        # Create leaderboard
        Leaderboard.objects.create(team=marvel, points=100)
        Leaderboard.objects.create(team=dc, points=90)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))

    def get_or_create_model(self, name):
        # Dynamically create simple models if not present
        from django.apps import apps
        try:
            return apps.get_model('octofit_tracker', name)
        except LookupError:
            class Meta:
                app_label = 'octofit_tracker'
            attrs = {'__module__': 'octofit_tracker.models', 'Meta': Meta}
            return type(name, (djongo_models.Model,), attrs)
