import unittest
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

    def test_apply_preprocess(self):
        sent = "이것은 예시 문장이다"
        self.tuner.sent = sent
        self.tuner.preprocess()
        self.assertEqual("이것은 예시 문장이다.", self.tuner.out)
        sent = "이것은 예시 문장이다."
        self.tuner.sent = sent
        self.tuner.preprocess()
        self.assertEqual("이것은 예시 문장이다.", self.tuner.out)

    def test_apply_honorifics_supnida(self):
        sent = "고운 손이 다 망가졌습니다"
        self.assertEqual("고운 손이 다 망가졌어", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("고운 손이 다 망가졌어요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("고운 손이 다 망가졌습니다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_ne(self):
        sent = "고운 손이 다 망가졌네"
        self.assertEqual("고운 손이 다 망가졌네", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("고운 손이 다 망가졌네요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("고운 손이 다 망가졌습니다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_neyo(self):
        sent = "고운 손이 다 망가졌네요"
        self.assertEqual("고운 손이 다 망가졌네", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("고운 손이 다 망가졌네요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("고운 손이 다 망가졌습니다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_ja(self):
        sent = "가까우니까 걸어가자"  # noqa
        self.assertEqual("가까우니까 걸어가자", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("가까우니까 걸어가요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("가까우니까 걸어갑시다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_gayo(self):
        sent = "가까우니까 걸어가요"
        self.assertEqual("가까우니까 걸어가자", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("가까우니까 걸어가요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("가까우니까 걸어갑시다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_gabsida(self):
        sent = "가까우니까 걸어갑시다"
        self.assertEqual("가까우니까 걸어가자", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("가까우니까 걸어가요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("가까우니까 걸어갑시다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_nde(self):
        sent = "밥먹고 바로 누우면 안된대"
        self.assertEqual("밥먹고 바로 누우면 안돼", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("밥먹고 바로 누우면 안돼요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("밥먹고 바로 누우면 안됩니다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_de(self):
        sent = "밥먹고 바로 누우면 안돼"
        self.assertEqual("밥먹고 바로 누우면 안돼", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("밥먹고 바로 누우면 안돼요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("밥먹고 바로 누우면 안됩니다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_ida(self):
        sent = "그는 전설이다"
        self.assertEqual("그는 전설이야", self.tuner(sent, self.ban[0], self.ban[1]))
        self.assertEqual("그는 전설이에요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("그는 전설입니다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_da(self):
        sent = "나는 어제 축구를 했다"
        self.assertEqual("나는 어제 축구를 했어", self.tuner(sent, self.ban[0], self.ban[1]))
        self.assertEqual("저는 어제 축구를 했어요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("저는 어제 축구를 했습니다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_irregulars_digud_drop(self):
        """
        ㄷ 탈락
        :return:
        """
        sent = "영희가 철수를 도왔어"
        self.assertEqual("영희가 철수를 도왔어", self.tuner(sent, self.ban[0], self.ban[1]))
        self.assertEqual("영희가 철수를 도왔어요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("영희가 철수를 도왔습니다", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "저 집은 매일 고기를 구워"
        self.assertEqual("저 집은 매일 고기를 구워", self.tuner(sent, self.ban[0], self.ban[1]))
        self.assertEqual("저 집은 매일 고기를 구워요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("저 집은 매일 고기를 굽습니다", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "미희는 옷을 잘 기워"
        self.assertEqual("미희는 옷을 잘 기워", self.tuner(sent, self.ban[0], self.ban[1]))
        self.assertEqual("미희는 옷을 잘 기워요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("미희는 옷을 잘 기웁니다", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "밥 먹고 바로 누우면 안 된대"
        self.assertEqual("밥 먹고 바로 누우면 안 돼", self.tuner(sent, self.ban[0], self.ban[1]))
        self.assertEqual("밥 먹고 바로 누우면 안 돼요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("밥 먹고 바로 누우면 안 됩니다", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "오다 주웠어"
        self.assertEqual("오다 주웠어", self.tuner(sent, self.ban[0], self.ban[1]))
        self.assertEqual("오다 주웠어요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("오다 주웠습니다", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "고운 손이 다 망가졌네"  # noqa
        self.assertEqual("고운 손이 다 망가졌네", self.tuner(sent, self.ban[0], self.ban[1]))
        self.assertEqual("고운 손이 다 망가졌네요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("고운 손이 다 망가졌습니다", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "오늘이 어제보다 더워"
        self.assertEqual("오늘이 어제보다 더워", self.tuner(sent, self.ban[0], self.ban[1]))
        self.assertEqual("오늘이 어제보다 더워요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("오늘이 어제보다 덥습니다", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "이 라면은 너무 매워"
        self.assertEqual("이 라면은 너무 매워", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("이 라면은 너무 매워요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("이 라면은 너무 맵습니다", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "이 라면은 너무 맵다"
        self.assertEqual("이 라면은 너무 매워", self.tuner(sent, self.ban[0], self.ban[1]))   # noqa
        self.assertEqual("이 라면은 너무 매워요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("이 라면은 너무 맵습니다", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "올해는 유난히 추워"
        self.assertEqual("올해는 유난히 추워", self.tuner(sent, self.ban[0], self.ban[1]))
        self.assertEqual("올해는 유난히 추워요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("올해는 유난히 춥습니다", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "오늘은 꿈자리가 사나웠어"
        self.assertEqual("오늘은 꿈자리가 사나웠어", self.tuner(sent, self.ban[0], self.ban[1]))
        self.assertEqual("오늘은 꿈자리가 사나웠어요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("오늘은 꿈자리가 사나웠습니다", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "난 뱀이 무서워"
        self.assertEqual("난 뱀이 무서워", self.tuner(sent, self.ban[0], self.ban[1]))
        self.assertEqual("전 뱀이 무서워요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("전 뱀이 무섭습니다", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "겨울산은 아름다워"
        self.assertEqual("겨울산은 아름다워", self.tuner(sent, self.ban[0], self.ban[1]))
        self.assertEqual("겨울산은 아름다워요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("겨울산은 아름답습니다", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "키가 큰 사람은 부러워"
        self.assertEqual("키가 큰 사람은 부러워", self.tuner(sent, self.ban[0], self.ban[1]))
        self.assertEqual("키가 큰 사람은 부러워요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("키가 큰 사람은 부럽습니다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_irregulars_bieub_drop(self):
        """
        ㅂ 탈락
        :return:
        """
        sent = "가까우니까 걸어가자"
        self.assertEqual("가까우니까 걸어가자", self.tuner(sent, self.ban[0], self.ban[1]))
        self.assertEqual("가까우니까 걸어가요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("가까우니까 걸어갑시다", self.tuner(sent, self.formal[0], self.formal[1]))  # or 걸어갑시다?
        sent = "난 걸어 갈게"
        self.assertEqual("난 걸어 가", self.tuner(sent, self.ban[0], self.ban[1]))
        self.assertEqual("전 걸어 가요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("전 걸어 갑니다", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "그걸 이제야 깨달았어"
        self.assertEqual("그걸 이제야 깨달았어", self.tuner(sent, self.ban[0], self.ban[1]))
        self.assertEqual("그걸 이제야 깨달았어요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("그걸 이제야 깨달았습니다", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "나는 그 문을 닫았어"
        self.assertEqual("나는 그 문을 닫았어", self.tuner(sent, self.ban[0], self.ban[1]))
        self.assertEqual("저는 그 문을 닫았어요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("저는 그 문을 닫았습니다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_postprocess(self):
        sent = "이것은 예시 문장이다"
        self.tuner.sent = sent
        self.tuner.out = sent + "."
        self.tuner.postprocess()
        self.assertEqual("이것은 예시 문장이다", self.tuner.out)
        sent = "이것은 예시 문장이다."
        self.tuner.sent = sent
        self.tuner.out = sent
        self.tuner.postprocess()
        self.assertEqual("이것은 예시 문장이다.", self.tuner.out)

    # --- known issues --- #
    @unittest.skip
    def test_apply_irregulars_eat(self):
        """
        이것도 고려를 해야하나..? 잘 모르겠다.
        :return:
        """
        sent = "밥 먹어"
        self.assertEqual("밥 먹어", self.tuner(sent, self.ban[0], self.ban[1]))
        self.assertEqual("밥 먹어요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("진지 잡수세요", self.tuner(sent, self.formal[0], self.formal[1]))

    @unittest.skip
    def test_apply_irregulars_collect(self):
        """
        맥락에 관게없이, 걷어 -> 걸어로 바꿔버려서... 사실 이 경우는 아직 어찌할수가 없다.
        재조립을 통한 높임법을 포기하면 가능하긴 한데... 그렇다면 재조립없이 하는 것은 어떻게 할 것인가.
        :return:
        """
        sent = "이참에 돈을 걷어가자"
        self.assertEqual("이참에 돈을 걷어가자", self.tuner(sent, self.ban[0], self.ban[1]))
        self.assertEqual("이참에 돈을 걷어가요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("이참에 돈을 걷어갑시다", self.tuner(sent, self.formal[0], self.formal[1]))
