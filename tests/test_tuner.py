from unittest import TestCase
from politetune.tuner import Tuner


class TestTuner(TestCase):

    tuner: Tuner

    @classmethod
    def setUpClass(cls) -> None:
        cls.tuner = Tuner()
        cls.unhonored = ("friend", "private")
        cls.honored = ("friend", "public")

    def test_do_unhonored(self):
        """
        한다 -> 해
        :return:
        """
        listener, visibility = self.unhonored
        res = self.tuner("나는 공부한다", listener, visibility)
        self.assertEqual("나는 공부해", res['tuned'])
        res = self.tuner("나는 수영한다", listener, visibility)
        self.assertEqual("나는 수영해", res['tuned'])
        res = self.tuner("나는 요구한다", listener, visibility)
        self.assertEqual("나는 요구해", res['tuned'])

    def test_do_honored(self):
        """
        한다 -> 해요
        :return:
        """
        listener, visibility = self.honored
        res = self.tuner("나는 공부한다", listener, visibility)
        self.assertEqual("저는 공부해요", res['tuned'])
        res = self.tuner("나는 수영한다", listener, visibility)
        self.assertEqual("저는 수영해요", res['tuned'])
        res = self.tuner("나는 요구한다", listener, visibility)
        self.assertEqual("저는 요구해요", res['tuned'])

    def test_thirsty_unhonored(self):
        """
        목마르다 -> 목말라
        :return:
        """
        listener, visibility = self.unhonored
        res = self.tuner("나는 목마르다", listener, visibility)
        self.assertEqual("나는 목말라", res['tuned'])

    def test_thirsty_honored(self):
        """
        목마르다 -> 목말라요
        :return:
        """
        listener, visibility = self.honored
        res = self.tuner("나는 목마르다", listener, visibility)
        self.assertEqual("저는 목말라요", res['tuned'])

    def test_hurts_unhonored(self):
        """
        아프다 -> 아파
        :return:
        """
        listener, visibility = self.unhonored
        res = self.tuner("나는 아프다", listener, visibility)
        self.assertEqual("나는 아파", res['tuned'])

    def test_hurts_honored(self):
        """
        아프다 -> 아파요
        :return:
        """
        listener, visibility = self.honored
        res = self.tuner("나는 아프다", listener, visibility)
        self.assertEqual("저는 아파요", res['tuned'])

    def test_run_unhonored(self):
        """
        달리다 -> 달려
        :return:
        """
        listener, visibility = self.unhonored
        res = self.tuner("나는 내 목표를 향해 달린다", listener, visibility)
        self.assertEqual("나는 내 목표를 향해 달려", res['tuned'])

    def test_run_honored(self):
        """
        달리다 -> 달려
        :return:
        """
        listener, visibility = self.honored
        res = self.tuner("나는 내 목표를 향해 달린다", listener, visibility)
        self.assertEqual("저는 제 목표를 향해 달려요", res['tuned'])

    def test_listen_unhonored(self):
        """
        달리다 -> 달려
        :return:
        """
        listener, visibility = self.unhonored
        res = self.tuner("나는 내 트로피를 들었다", listener, visibility)
        self.assertEqual("나는 내 트로피를 들었어", res['tuned'])

    def test_listen_honored(self):
        """
        달리다 -> 달려
        :return:
        """
        listener, visibility = self.honored
        res = self.tuner("나는 내 트로피를 들었다", listener, visibility)
        self.assertEqual("저는 제 트로피를 들었어요", res['tuned'])
