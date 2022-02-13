from unittest import TestCase
from politetune.honorifier import Honorifier


class TestHonorifier(TestCase):

    honorifier: Honorifier
    listener: str
    visibility: str

    @classmethod
    def setUpClass(cls) -> None:
        cls.honorifier = Honorifier()
        cls.listener = "teacher"
        cls.visibility = "private"

    def test_do_honored(self):
        sent, _, _ = self.honorifier("나는 공부한다", self.listener, self.visibility)
        self.assertEqual("`저(Noun)`는 공부`해요(Verb)`", sent)
        sent, _, _ = self.honorifier("나는 수영한다", self.listener, self.visibility)
        self.assertEqual("`저(Noun)`는 수영`해요(Verb)`", sent)
        sent, _, _ = self.honorifier("나는 요구한다", self.listener, self.visibility)
        self.assertEqual("`저(Noun)`는 요구`해요(Verb)`", sent)

    def test_thirsty_honored(self):
        sent, _, _ = self.honorifier("나는 목마르다", self.listener, self.visibility)
        self.assertEqual("`저(Noun)`는 `목말라요(Adjective)`", sent)

    def test_hurts_honored(self):
        sent, _, _ = self.honorifier("나는 아프다", self.listener, self.visibility)
        self.assertEqual("`저(Noun)`는 `아파요(Adjective)`", sent)
