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
        tuned = self.tuner("그는 경주를 즐긴다", listener, visibility)
        self.assertEqual("그는 경주를 즐겨", tuned)
        tuned = self.tuner("물티슈가 말라 버렸다", listener, visibility)
        self.assertEqual("물티슈가 말라 버렸어", tuned)
        tuned = self.tuner("난 가끔 노래를 부른다", listener, visibility)
        self.assertEqual("난 가끔 노래를 불러", tuned)
        tuned = self.tuner("아무도 모른다", listener, visibility)
        self.assertEqual("아무도 몰라", tuned)
        tuned = self.tuner("새로운 소리에 놀랐다", listener, visibility)
        self.assertEqual("새로운 소리에 놀랐어", tuned)

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
        tuned = self.tuner("어제 채점을 다 했다", listener, visibility)
        self.assertEqual("어제 채점을 다 했어요", tuned)
        tuned = self.tuner("대강 훑어만 봤다", listener, visibility)
        self.assertEqual("대강 훑어만 봤어요", tuned)
        tuned = self.tuner("그는 경주를 즐긴다", listener, visibility)
        self.assertEqual("그는 경주를 즐겨요", tuned)
        tuned = self.tuner("물티슈가 말라 버렸다", listener, visibility)
        self.assertEqual("물티슈가 말라 버렸어요", tuned)
        tuned = self.tuner("난 가끔 노래를 부른다", listener, visibility)
        self.assertEqual("전 가끔 노래를 불러요", tuned)
        tuned = self.tuner("아무도 모른다", listener, visibility)
        self.assertEqual("아무도 몰라요", tuned)
        tuned = self.tuner("새로운 소리에 놀랐다", listener, visibility)
        self.assertEqual("새로운 소리에 놀랐어요", tuned)

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
        tuned = self.tuner("어제 채점을 다 했다", listener, visibility)
        self.assertEqual("어제 채점을 다 했습니다", tuned)
        tuned = self.tuner("대강 훑어만 봤다", listener, visibility)
        self.assertEqual("대강 훑어만 봤습니다", tuned)
        tuned = self.tuner("그는 경주를 즐긴다", listener, visibility)
        self.assertEqual("그는 경주를 즐깁니다", tuned)
        tuned = self.tuner("물티슈가 말라 버렸다", listener, visibility)
        self.assertEqual("물티슈가 말라 버렸습니다", tuned)
        tuned = self.tuner("난 가끔 노래를 부른다", listener, visibility)
        self.assertEqual("전 가끔 노래를 부릅니다", tuned)
        tuned = self.tuner("아무도 모른다", listener, visibility)
        self.assertEqual("아무도 모릅니다", tuned)
        tuned = self.tuner("새로운 소리에 놀랐다", listener, visibility)
        self.assertEqual("새로운 소리에 놀랐습니다", tuned)

    def test_possessive(self):
        listener, visibility = self.jon
        tuned = self.tuner("난 내 가방을 들었다", listener, visibility)
        self.assertEqual("전 제 가방을 들었어요", tuned)
        listener, visibility = self.ban
        tuned = self.tuner("난 내 가방을 들었다", listener, visibility)
        self.assertEqual("난 내 가방을 들었어", tuned)







