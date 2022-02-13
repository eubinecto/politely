from unittest import TestCase
from politetune.honorifier import Honorifier


class TestHonorifier(TestCase):

    honorifier: Honorifier

    @classmethod
    def setUpClass(cls) -> None:
        cls.honorifier = Honorifier()
        cls.unhonored = ("friend", "private")
        cls.honored = ("friend", "public")

    def test_do_unhonored(self):
        """
        한다 -> 해
        :return:
        """
        listener, visibility = self.unhonored
        sent, _, _ = self.honorifier("나는 공부한다", listener, visibility)
        self.assertEqual("`나`는 공부`해`", sent)
        sent, _, _ = self.honorifier("나는 수영한다", listener, visibility)
        self.assertEqual("`나`는 수영`해`", sent)
        sent, _, _ = self.honorifier("나는 요구한다", listener, visibility)
        self.assertEqual("`나`는 요구`해`", sent)

    def test_do_honored(self):
        """
        한다 -> 해요
        :return:
        """
        listener, visibility = self.honored
        sent, _, _ = self.honorifier("나는 공부한다", listener, visibility)
        self.assertEqual("`저`는 공부`해요`", sent)
        sent, _, _ = self.honorifier("나는 수영한다", listener, visibility)
        self.assertEqual("`저`는 수영`해요`", sent)
        sent, _, _ = self.honorifier("나는 요구한다", listener, visibility)
        self.assertEqual("`저`는 요구`해요`", sent)

    def test_thirsty_unhonored(self):
        """
        목마르다 -> 목말라
        :return:
        """
        listener, visibility = self.unhonored
        sent, _, _ = self.honorifier("나는 목마르다", listener, visibility)
        self.assertEqual("`나`는 `목말라`", sent)

    def test_thirsty_honored(self):
        """
        목마르다 -> 목말라요
        :return:
        """
        listener, visibility = self.honored
        sent, _, _ = self.honorifier("나는 목마르다", listener, visibility)
        self.assertEqual("`저`는 `목말라요`", sent)

    def test_hurts_unhonored(self):
        """
        아프다 -> 아파, 아파요
        :return:
        """
        listener, visibility = self.unhonored
        sent, _, _ = self.honorifier("나는 아프다", listener, visibility)
        self.assertEqual("`나`는 `아파`", sent)

    def test_hurts_honored(self):
        """
        아프다 -> 아파, 아파요
        :return:
        """
        listener, visibility = self.honored
        sent, _, _ = self.honorifier("나는 아프다", listener, visibility)
        self.assertEqual("`저`는 `아파요`", sent)
