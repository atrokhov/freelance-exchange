# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from .models import Notice, Profile

def create_notice(author, title, body, done, price, executor, days):
        time = timezone.now() + datetime.timedelta(days=days)
        return Notice.objects.create(author=author, title=title, body=body, done=done, price=price, executor=executor, pub_date=time)

    
class NoticeIndexTests(TestCase):

    def create_user(self, username, password):
        self.user = User.objects.create_user(username=username, password=password)
        login = self.client.login(username=username, password=password)

    def test_index_view_with_no_notices(self):
        response = self.client.get(reverse('exchange:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Нет объявлений")
        self.assertQuerysetEqual(response.context['latest_notice_list'], [])

    def test_index_view_with_a_past_question(self):
        user1 = self.create_user(username='testuser1', password='12345')
        user2 = self.create_user(username='testuser2', password='12345')
        create_notice(author=user1, title="Past notice.", body="Past notice.", done=False, price=100, executor=user2, days=-30)
        response = self.client.get(reverse('exchange:index'))
        self.assertQuerysetEqual(
            response.context['latest_notice_list'],
            ['<Notice: Past notice.>']
        )

    def test_index_view_with_two_past_questions(self):
        user1 = self.create_user(username='testuser1', password='12345')
        user2 = self.create_user(username='testuser2', password='12345')
        create_notice(author=user1, title="Past notice 1.", body="Past notice.", done=False, price=100, executor=user2, days=-30)
        create_notice(author=user2, title="Past notice 2.", body="Past notice.", done=False, price=100, executor=user1, days=-5)
        response = self.client.get(reverse('exchange:index'))
        self.assertQuerysetEqual(
            response.context['latest_notice_list'],
            ['<Notice: Past notice 2.>', '<Notice: Past notice 1.>']
        )


class NoticeUserNoticesTests(TestCase):
    def create_user(self, username, password):
        self.user = User.objects.create_user(username=username, password=password)
        login = self.client.login(username=username, password=password)
    
    def test_index_view_with_no_notices(self):
        response = self.client.get(reverse('exchange:your_notices'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Нет объявлений")
        self.assertQuerysetEqual(response.context['notices'], [])

    def test_index_view_with_a_past_question(self):
        user1 = self.create_user(username='testuser1', password='12345')
        user2 = self.create_user(username='testuser2', password='12345')
        create_notice(author=user1, title="Past notice.", body="Past notice.", done=False, price=100, executor=user2, days=-30)
        response = self.client.get(reverse('exchange:your_notices'))
        self.assertQuerysetEqual(
            response.context['notices'],
            ['<Notice: Past notice.>']
        )

    def test_index_view_with_two_past_questions(self):
        user1 = self.create_user(username='testuser1', password='12345')
        user2 = self.create_user(username='testuser2', password='12345')
        create_notice(author=user1, title="Past notice 1.", body="Past notice.", done=False, price=100, executor=user2, days=-30)
        create_notice(author=user2, title="Past notice 2.", body="Past notice.", done=False, price=100, executor=user1, days=-5)
        response = self.client.get(reverse('exchange:your_notices'))
        self.assertQuerysetEqual(
            response.context['notices'],
            ['<Notice: Past notice 2.>', '<Notice: Past notice 1.>']
        )