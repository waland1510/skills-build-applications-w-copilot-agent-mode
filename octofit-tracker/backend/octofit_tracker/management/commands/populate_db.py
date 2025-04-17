import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from pymongo import MongoClient
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activity, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        try:
            logger.debug('Clearing existing data using raw MongoDB commands...')
            client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
            db = client[settings.DATABASES['default']['NAME']]

            db.users.delete_many({})
            db.teams.delete_many({})
            db.activity.delete_many({})
            db.leaderboard.delete_many({})
            db.workouts.delete_many({})

            logger.debug('Creating users...')
            user_data = [
                {'email': 'thundergod@mhigh.edu', 'name': 'Thor', 'age': 25},
                {'email': 'metalgeek@mhigh.edu', 'name': 'Tony Stark', 'age': 35},
                {'email': 'zerocool@mhigh.edu', 'name': 'Steve Rogers', 'age': 30},
                {'email': 'crashoverride@mhigh.edu', 'name': 'Natasha Romanoff', 'age': 28},
                {'email': 'sleeptoken@mhigh.edu', 'name': 'Bruce Banner', 'age': 40},
            ]
            for data in user_data:
                User.objects.create(**data)

            # Fetch the created users
            users = list(User.objects.all())
            logger.debug(f'Created {len(users)} users')

            logger.debug('Creating teams...')
            teams = [
                Team(name='Blue Team', members=[users[0].email, users[1].email]),
                Team(name='Gold Team', members=[users[2].email, users[3].email, users[4].email]),
            ]
            Team.objects.bulk_create(teams)
            
            # Fetch the created teams
            teams = list(Team.objects.all())
            logger.debug(f'Created {len(teams)} teams')

            logger.debug('Creating activities...')
            activities = [
                Activity(user_id=str(users[0]._id), type='Cycling', duration=60, date='2025-04-17'),
                Activity(user_id=str(users[1]._id), type='Crossfit', duration=120, date='2025-04-16'),
                Activity(user_id=str(users[2]._id), type='Running', duration=90, date='2025-04-15'),
                Activity(user_id=str(users[3]._id), type='Strength', duration=30, date='2025-04-14'),
                Activity(user_id=str(users[4]._id), type='Swimming', duration=75, date='2025-04-13'),
            ]
            Activity.objects.bulk_create(activities)

            logger.debug('Creating leaderboard entries...')
            leaderboard_entries = [
                Leaderboard(team_id=str(teams[0]._id), points=200),
                Leaderboard(team_id=str(teams[1]._id), points=300),
            ]
            Leaderboard.objects.bulk_create(leaderboard_entries)

            logger.debug('Creating workouts...')
            workouts = [
                Workout(name='Cycling Training', description='Training for a road cycling event'),
                Workout(name='Crossfit', description='Training for a crossfit competition'),
                Workout(name='Running Training', description='Training for a marathon'),
                Workout(name='Strength Training', description='Training for strength'),
                Workout(name='Swimming Training', description='Training for a swimming competition'),
            ]
            Workout.objects.bulk_create(workouts)

            logger.debug('Database population complete.')
            self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
        except Exception as e:
            logger.error(f'Error occurred: {e}')
            raise