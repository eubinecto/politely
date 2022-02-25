from unittest import TestCase
from politetune.processors import Tuner


class TestTuner(TestCase):

    tuner: Tuner

    @classmethod
    def setUpClass(cls) -> None:
        cls.tuner = Tuner()
        cls.ban = ("adult family", "private")
        cls.jon = ("adult family", "public")
        cls.formal = ("boss at work", "public")

    def test_banmal(self):
        listener, visibility = self.ban
        tuned = self.tuner("나는 공부한다", listener, visibility)
        self.assertEqual("나는 공부해", tuned)
        tuned = self.tuner("나는 수영한다", listener, visibility)
        self.assertEqual("나는 수영해", tuned)
        tuned = self.tuner("나는 요구한다", listener, visibility)
        self.assertEqual("나는 요구해", tuned)
        tuned = self.tuner("나는 목마르다", listener, visibility)
        self.assertEqual("나는 목말라", tuned)
        tuned = self.tuner("나는 아프다", listener, visibility)
        self.assertEqual("나는 아파", tuned)
        tuned = self.tuner("나는 내 목표를 향해 달린다", listener, visibility)
        self.assertEqual("나는 내 목표를 향해 달려", tuned)
        tuned = self.tuner("나는 내 트로피를 들었다", listener, visibility)
        self.assertEqual("나는 내 트로피를 들었어", tuned)

    def test_jondemal(self):
        listener, visibility = self.jon
        tuned = self.tuner("나는 내 목표를 향해 달린다", listener, visibility)
        self.assertEqual("저는 제 목표를 향해 달려요", tuned)
        tuned = self.tuner("나는 공부한다", listener, visibility)
        self.assertEqual("저는 공부해요", tuned)
        tuned = self.tuner("나는 수영한다", listener, visibility)
        self.assertEqual("저는 수영해요", tuned)
        tuned = self.tuner("나는 요구한다", listener, visibility)
        self.assertEqual("저는 요구해요", tuned)
        tuned = self.tuner("나는 목마르다", listener, visibility)
        self.assertEqual("저는 목말라요", tuned)
        tuned = self.tuner("나는 내 트로피를 들었다", listener, visibility)
        self.assertEqual("저는 제 트로피를 들었어요", tuned)

    def test_formal(self):
        listener, visibility = self.formal
        tuned = self.tuner("나는 내 목표를 향해 달린다", listener, visibility)
        self.assertEqual("저는 제 목표를 향해 달립니다", tuned)


