# -*- coding: utf-8 -*-
from django.core.management import BaseCommand, CommandError
import random

from posts.models import Post, Comment
from django.contrib.auth.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10)

    def handle(self, *args, **options):
        count_essence = options['count']
        count_user = User.objects.all().count()
        password = '1234'
        message = """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vitae libero ac risus 
        fermentum viverra. Nunc tristique tellus velit. Nullam iaculis sodales dignissim. 
        Quisque efficitur faucibus quam, lobortis lobortis lorem ornare a. Quisque ullamcorper 
        justo et neque semper consequat. Aenean consectetur metus sed nibh mattis tristique. 
        Ut vel lectus quam. Mauris vehicula placerat orci, vel mattis ipsum finibus at. 
        Aenean nec nunc a nunc convallis lacinia sed ut arcu. Integer eget sodales tellus. 
        Nullam consectetur, metus sed semper vehicula, velit nulla accumsan felis, viverra 
        suscipit augue odio non felis.
        """

        text = """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vitae libero ac risus 
        fermentum viverra. Nunc tristique tellus velit. Nullam iaculis sodales dignissim. 
        Quisque efficitur faucibus.
        """

        for _ in range(count_essence):
            count_user += 1
            username = 'user{}'.format(count_user)
            first_name = 'Гарри{}'.format(count_user)
            last_name = 'Поттер{}'.format(count_user)
            email = 'user{}@site.net'.format(count_user)

            user = User.objects.create_user(username=username,
                                            first_name=first_name,
                                            last_name=last_name,
                                            email=email,
                                            password=password)

            user_id_list = User.objects.values_list('id', flat=True)

            for num in range(10):
                title = 'Title Post {}'.format(num)

                post = Post.objects.create(user=user,
                                           title=title,
                                           message=message)

                for _ in range(10):
                    random_user = User.objects.get(id=random.choice(user_id_list))
                    Comment.objects.create(post=post,
                                           user=random_user,
                                           text=text)
