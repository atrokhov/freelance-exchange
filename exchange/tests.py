# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from .models import Notice, Profile

from django.test import Client

csrf_client = Client(enforce_csrf_checks=True)

def create_notice(author, title, body, done, price, executor, days):
        time = timezone.now() + datetime.timedelta(days=days)
        return Notice.objects.create(author=author, title=title, body=body, done=done, price=price, executor=executor, pub_date=time)

    
class NoticeIndexTests(TestCase):

    def create_user(self, username, password):
        self.user = User.objects.create_user(username=username, password=password)

    def test_index_view_with_no_notices(self):
        response = self.client.get(reverse('exchange:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Нет объявлений")
        self.assertQuerysetEqual(response.context['latest_notice_list'], [])

    def test_index_view_with_a_past_notice(self):
        user1 = self.create_user(username='testuser1', password='12345')
        user2 = self.create_user(username='testuser2', password='12345')
        create_notice(author=user1, title="Past notice.", body="Past notice.", done=False, price=100, executor=user2, days=-30)
        response = self.client.get(reverse('exchange:index'))
        self.assertQuerysetEqual(
            response.context['latest_notice_list'],
            ['<Notice: Past notice.>']
        )

    def test_index_view_with_two_past_notices(self):
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
        self.user = User.objects.create_user(username=username, password=password, is_active=True)
        self.user.save()
        return self.user

    def test_user_notices_view_with_no_notices(self):
        user1 = self.create_user(username="testuser1", password="12345")
        self.client.login(username="testuser1", password="12345")
        response = self.client.get(reverse('exchange:your_notices'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Notice")
        self.assertQuerysetEqual(response.context['notices'], [])

    def test_user_notices_view_with_a_notice(self):
        user1 = self.create_user(username='testuser1', password='12345')
        user2 = self.create_user(username='testuser2', password='12345')
        self.client.login(username='testuser2', password='12345')
        create_notice(author=user2, title="Notice.", body="Notice.", done=False, price=100, executor=user1, days=0)
        response = self.client.get(reverse('exchange:your_notices'))
        self.assertQuerysetEqual(
            response.context['notices'],
            ['<Notice: Notice.>']
        )

class NoticeUserTasksTests(TestCase):

    def create_user(self, username, password):
        self.user = User.objects.create_user(username=username, password=password, is_active=True)
        self.user.save()
        return self.user

    def test_user_notices_view_with_no_notices(self):
        user1 = self.create_user(username="testuser1", password="12345")
        self.client.login(username="testuser1", password="12345")
        response = self.client.get(reverse('exchange:your_notices'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Notice")
        self.assertQuerysetEqual(response.context['notices'], [])

    def test_user_notices_view_with_a_notice(self):
        user1 = self.create_user(username='testuser1', password='12345')
        user2 = self.create_user(username='testuser2', password='12345')
        self.client.login(username='testuser2', password='12345')
        create_notice(author=user1, title="Notice.", body="Notice.", done=False, price=100, executor=user2, days=0)
        response = self.client.get(reverse('exchange:your_tasks'))
        self.assertQuerysetEqual(
            response.context['notices'],
            ['<Notice: Notice.>']
        )

class NoticeDetailTests(TestCase):

    def create_user(self, username, password):
        self.user = User.objects.create_user(username=username, password=password, is_active=True)
        self.user.save()
        return self.user

    def test_detail_view(self):
        user1 = self.create_user(username="testuser1", password="12345")
        user2 = self.create_user(username='testuser2', password='12345')
        self.client.login(username='testuser2', password='12345')
        notice = create_notice(author=user2, title="Notice.", body="Notice.", done=False, price=100, executor=user1, days=0)
        response = self.client.get(reverse('exchange:detail', args=(notice.id,)))
        self.assertContains(response, notice.body, status_code=200)

class NoticeCreateTests(TestCase):

    def create_user(self, username, password):
        self.user = User.objects.create_user(username=username, password=password, is_active=True)
        self.user.save()
        return self.user

    def test_published_post(self):
        user1 = self.create_user(username="testuser1", password="12345")
        user2 = self.create_user(username='testuser2', password='12345')
        self.client.login(username='testuser2', password='12345')
        self.client.post('/notice/new/', { 'author': user2, 'title': "Notice.", 'body': "Notice.", 'done': False, 'price': 100, 'executor': user1, 'days': 0 })
        self.assertEqual(Notice.objects.last().title, "Notice.")

    def test_display_post(self):
        user1 = self.create_user(username="testuser1", password="12345")
        user2 = self.create_user(username='testuser2', password='12345')
        self.client.login(username='testuser2', password='12345')
        notice = create_notice(author=user2, title="Notice.", body="Notice.", done=False, price=100, executor=user1, days=0)
        response = self.client.get(reverse('exchange:detail', args=(notice.id,)))
        self.assertContains(response, "Notice.")

class UpdateFormTest(TestCase):

    def create_user(self, username, password):
        self.user = User.objects.create_user(username=username, password=password, is_active=True)
        self.user.save()
        return self.user

    def test_update_notice(self):
        user1 = self.create_user(username="testuser1", password="12345")
        user2 = self.create_user(username='testuser2', password='12345')
        self.client.login(username='testuser2', password='12345')
        notice = create_notice(author=user2, title="Notice.", body="Notice.", done=False, price=100, executor=user1, days=0)

        response = self.client.post(
            reverse('exchange:edit', kwargs={'pk': notice.id}), 
            {'title': 'The Catcher in the Rye', 'body': 'Hello world!!!'})

        self.assertEqual(response.status_code, 302)

        notice.refresh_from_db()
        self.assertEqual(notice.body, 'Hello world!!!')

class AddMoneyFormTest(TestCase):

    def create_user(self, username, password):
        self.user = User.objects.create_user(username=username, password=password, is_active=True)
        self.user.save()
        return self.user

    def test_add_money(self):
        user = self.create_user(username="testuser1", password="12345")
        self.client.login(username='testuser1', password='12345')

        response = self.client.post(reverse('exchange:add_money', kwargs={'pk': user.id}), {'transaction_sum': 40})

        self.assertEqual(response.status_code, 302)

        user.profile.refresh_from_db()
        self.assertEqual(user.profile.current_balance, 40)

class SetExecutorFormTest(TestCase):

    def create_user(self, username, password):
        self.user = User.objects.create_user(username=username, password=password, is_active=True)
        self.user.save()
        return self.user

    def test_set_executor(self):
        user1 = self.create_user(username="testuser1", password="12345")
        user2 = self.create_user(username='testuser2', password='12345')
        self.client.login(username='testuser2', password='12345')
        notice = create_notice(author=user1, title="Notice.", body="Notice.", done=False, price=100, executor=None, days=0)
    
        response = self.client.post(reverse('exchange:set_executor', kwargs={'pk': notice.id}))

        self.assertEqual(response.status_code, 302)

        notice.refresh_from_db()
        self.assertEqual(notice.executor, user2)

class DoneFormTest(TestCase):

    def create_user(self, username, password):
        self.user = User.objects.create_user(username=username, password=password, is_active=True)
        self.user.save()
        return self.user

    def test_done(self):
        user1 = self.create_user(username="testuser1", password="12345")
        user2 = self.create_user(username='testuser2', password='12345')
        self.client.login(username='testuser1', password='12345')
        notice = create_notice(author=user1, title="Notice.", body="Notice.", done=False, price=100, executor=user2, days=0)
        self.client.post(reverse('exchange:add_money', kwargs={'pk': user1.id}), {'transaction_sum': 1000})
    
        response = self.client.post(reverse('exchange:done', kwargs={'pk': notice.id}))

        self.assertEqual(response.status_code, 302)

        notice.refresh_from_db()
        user1.profile.refresh_from_db()
        user2.profile.refresh_from_db()

        self.assertEqual(user1.profile.current_balance, 900)
        self.assertEqual(user2.profile.current_balance, 100)
        self.assertEqual(notice.done, True)
        
