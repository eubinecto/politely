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
        sent = self.tuner("나는 공부한다", listener, visibility)
        self.assertEqual("나는 공부해", sent)
        sent = self.tuner("나는 수영한다", listener, visibility)
        self.assertEqual("나는 수영해", sent)
        sent = self.tuner("나는 요구한다", listener, visibility)
        self.assertEqual("나는 요구해", sent)

    def test_do_honored(self):
        """
        한다 -> 해요
        :return:
        """
        listener, visibility = self.honored
        sent = self.tuner("나는 공부한다", listener, visibility)
        self.assertEqual("저는 공부해요", sent)
        sent = self.tuner("나는 수영한다", listener, visibility)
        self.assertEqual("저는 수영해요", sent)
        sent = self.tuner("나는 요구한다", listener, visibility)
        self.assertEqual("저는 요구해요", sent)

    def test_thirsty_unhonored(self):
        """
        목마르다 -> 목말라
        :return:
        """
        listener, visibility = self.unhonored
        sent = self.tuner("나는 목마르다", listener, visibility)
        self.assertEqual("나는 목말라", sent)

    def test_thirsty_honored(self):
        """
        목마르다 -> 목말라요
        :return:
        """
        listener, visibility = self.honored
        sent = self.tuner("나는 목마르다", listener, visibility)
        self.assertEqual("저는 목말라요", sent)

    def test_hurts_unhonored(self):
        """
        아프다 -> 아파
        :return:
        """
        listener, visibility = self.unhonored
        sent = self.tuner("나는 아프다", listener, visibility)
        self.assertEqual("나는 아파", sent)

    def test_hurts_honored(self):
        """
        아프다 -> 아파요
        :return:
        """
        listener, visibility = self.honored
        sent = self.tuner("나는 아프다", listener, visibility)
        self.assertEqual("저는 아파요", sent)
