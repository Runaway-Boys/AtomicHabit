from django.contrib.auth import get_user_model
from django.test import TestCase


from .models import ScoreCard,ScoreCardTitle
# Create your tests here.

#User Test Case
User = get_user_model()
class UserTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user('cfe',password='abc123')

    def test_user_pw(self):
        checked = self.user_a.check_password("abc123")
        self.assertTrue(checked)
    

# Scorecard test case
class ScoreCardTestCase(TestCase):
    def setUp(self):
            self.user_a = User.objects.create_user('cfe',password='abc123')
            self.scorecard_a = ScoreCard.objects.create(
                 name = 'homework',
                 user = self.user_a
            )
            self.scorecardtitle_a = ScoreCardTitle.objects.create(
                 name = 'homework',
                 scorecard = self.scorecard_a,
                 options = 'Positive'

            )
    def test_user_count(self):
         qs = User.objects.all()
         self.assertEqual(qs.count(),1)

    #counts the amount of scorecards in the 
    #users
    def test_user_scorecard_count(self):
         user = self.user_a
         qs = user.scorecard_set.all()
         self.assertEqual(qs.count(),1)

    def test_user_scorecard_reverse_count(self):
         user = self.user_a
         qs = user.scorecard_set.all()
         self.assertEqual(qs.count(),1)

    def test_user_scorecard_foreward_count(self):
         user = self.user_a
         qs = ScoreCard.objects.filter(user=user)
         self.assertEqual(qs.count(),1)
    #counts the amount of scorecards in the 
    #users scorecard
    def test_user_scorecardtitle_reverse_count(self):
         scorecard = self.scorecard_a
         qs = scorecard.scorecardtitle_set.all()
         self.assertEqual(qs.count(),1)

    def test_user_scorecard_foreward_count(self):
         scorecard = self.scorecard_a
         qs = ScoreCardTitle.objects.filter(scorecard=scorecard)
         self.assertEqual(qs.count(),1)


class TaskModelTest(TestCase):
    def test_task_model_exist(self):

        scorecard = ScoreCard.objects.all()
        self.assertNotEqual(scorecard,0)

