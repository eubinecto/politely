from unittest import TestCase
from politetune.tuner import Tuner


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
        tuned = self.tuner("그 아이는 참 예의가 바르다", listener, visibility)
        self.assertEqual("그 아이는 참 예의가 발라", tuned)
        tuned = self.tuner("나는 내가 제일 좋아하는 노래를 듣는다", listener, visibility)
        self.assertEqual("나는 내가 제일 좋아하는 노래를 들어", tuned)
        tuned = self.tuner("그 단어는 이 물건을 일컫는다", listener, visibility)
        self.assertEqual("그 단어는 이 물건을 일컬어", tuned)
        # this ambiguity is sort of the problem.
        # how do you solve this ambiguity? -> This is sort of what's impossible.
        # this is probably the case where you need predictive models. Rules cannot cover edge cases.
        # tuned = self.tuner("나는 지나가던 행인에게 길을 물었다", listener, visibility)
        # self.assertEqual("나는 지나가던 행인에게 길을 물었어", tuned)
        # # this is sort of the problem.
        # tuned = self.tuner("나는 주체할수 없는 슬픔을 내 가슴에 묻었다", listener, visibility)
        # self.assertEqual("나는 주체할수 없는 슬픔을 내 가슴에 묻었어", tuned)

    def test_jondemal(self):
        listener, visibility = self.jon
        tuned = self.tuner("나는 내 목표를 향해 달린다", listener, visibility)
        self.assertEqual("저는 제 목표를 향해 달려요", tuned)
        tuned = self.tuner("나는 공부한다", listener, visibility)
        self.assertEqual("저는 공부해요", tuned)
        tuned = self.tuner("나는 공부해", listener, visibility)
        self.assertEqual("저는 공부해요", tuned)
        tuned = self.tuner("나는 공부할래", listener, visibility)
        self.assertEqual("저는 공부해요", tuned)
        tuned = self.tuner("나는 수영한다", listener, visibility)
        self.assertEqual("저는 수영해요", tuned)
        tuned = self.tuner("나는 요구한다", listener, visibility)
        self.assertEqual("저는 요구해요", tuned)
        tuned = self.tuner("나는 목마르다", listener, visibility)
        self.assertEqual("저는 목말라요", tuned)
        tuned = self.tuner("나는 내 트로피를 들었다", listener, visibility)
        self.assertEqual("저는 제 트로피를 들었어요", tuned)
        tuned = self.tuner("그 아이는 참 예의가 바르다", listener, visibility)
        self.assertEqual("그 아이는 참 예의가 발라요", tuned)
        tuned = self.tuner("나는 내가 제일 좋아하는 노래를 듣는다", listener, visibility)
        self.assertEqual("저는 제가 제일 좋아하는 노래를 들어요", tuned)
        tuned = self.tuner("그 단어는 이 물건을 일컫는다", listener, visibility)
        self.assertEqual("그 단어는 이 물건을 일컬어요", tuned)

    def test_formal(self):
        listener, visibility = self.formal
        tuned = self.tuner("나는 내 목표를 향해 달린다", listener, visibility)
        self.assertEqual("저는 제 목표를 향해 달립니다", tuned)
        tuned = self.tuner("나는 공부한다", listener, visibility)
        self.assertEqual("저는 공부합니다", tuned)
        tuned = self.tuner("나는 수영한다", listener, visibility)
        self.assertEqual("저는 수영합니다", tuned)
        tuned = self.tuner("나는 요구한다", listener, visibility)
        self.assertEqual("저는 요구합니다", tuned)
        tuned = self.tuner("나는 목마르다", listener, visibility)
        self.assertEqual("저는 목마릅니다", tuned)
        tuned = self.tuner("나는 내 트로피를 들었다", listener, visibility)
        self.assertEqual("저는 제 트로피를 들었습니다", tuned)
        tuned = self.tuner("그 아이는 참 예의가 바르다", listener, visibility)
        self.assertEqual("그 아이는 참 예의가 바릅니다", tuned)
        tuned = self.tuner("나는 내가 제일 좋아하는 노래를 듣는다", listener, visibility)
        self.assertEqual("저는 제가 제일 좋아하는 노래를 듣습니다", tuned)
        tuned = self.tuner("그 단어는 이 물건을 일컫는다", listener, visibility)
        self.assertEqual("그 단어는 이 물건을 일컫습니다", tuned)


