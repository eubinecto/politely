import unittest
from unittest import TestCase
from politetune.processors import Styler


class TestTuner(TestCase):

    tuner: Styler

    @classmethod
    def setUpClass(cls) -> None:
        cls.tuner = Styler()
        cls.ban = ("adult family", "comfortable & informal")
        cls.jon = ("adult family", "formal")
        cls.formal = ("boss at work", "formal")

    def test_apply_preprocess(self):
        sent = "이것은 예시 문장이다"
        self.tuner.sent = sent
        self.tuner.preprocess()
        self.assertEqual("이것은 예시 문장이다.", self.tuner.out)
        sent = "이것은 예시 문장이다."
        self.tuner.sent = sent
        self.tuner.preprocess()
        self.assertEqual("이것은 예시 문장이다.", self.tuner.out)

    def test_apply_preprocess_trailing_spaces(self):
        sent = "이것은 예시 문장이다  "
        self.tuner.sent = sent
        self.tuner.preprocess()
        self.assertEqual("이것은 예시 문장이다.", self.tuner.out)
        sent = "이것은 예시 문장이다. "
        self.tuner.sent = sent
        self.tuner.preprocess()
        self.assertEqual("이것은 예시 문장이다.", self.tuner.out)

    # 평서문 어미 - this is used for making a statement
    def test_generic_EF_da(self):
        """
        ends with -다
        :return:
        """
        # 언제 , 언제 어를 써야하는가?
        # if it were to be used for learning, the results should be explainable.
        sent = "오늘 날씨가 정말 좋다"
        # 만약.. 들어오는 입력이 반말이라면, 굳이 반말인 경우를 수정할 필요가 없다.
        self.assertEqual("오늘 날씨가 정말 좋아", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("오늘 날씨가 정말 좋아요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("오늘 날씨가 정말 좋습니다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_generic_EF_nuenda(self):
        """
        ends with -는다
        :return:
        """
        sent = "한국 사람들은 설날에 떡국을 먹는다"
        # 만약.. 들어오는 입력이 반말이라면, 굳이 반말인 경우를 수정할 필요가 없다.
        # 
        self.assertEqual("한국 사람들은 설날에 떡국을 먹는다", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("한국 사람들은 설날에 떡국을 먹어요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("한국 사람들은 설날에 떡국을 먹습니다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_generic_EF_nieun_da(self):
        """
        ends with -ㄴ다
        :return:
        """
        sent = "난 오늘도 그녀애게 전화를 건다"
        # 만약.. 들어오는 입력이 반말이라면, 굳이 반말인 경우를 수정할 필요가 없다.
        self.assertEqual("난 오늘도 그녀애게 전화를 건다", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("전 오늘도 그녀애게 전화를 걸어요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("전 오늘도 그녀애게 전화를 겁니다", self.tuner(sent, self.formal[0], self.formal[1]))


    def test_generic_EF_guna(self):
        """
        ends with -구나
        :return:
        """

    def test_generic_EF_nuenguna(self):
        """
        ends with -는구나
        :return:
        """
        pass

    def test_generic_EF_gun(self):
        """
        ends with -군
        :return:
        """
        pass

    def test_generic_EF_nuengun(self):
        """
        ends with -는군
        :return:
        """
        pass

    def test_generic_EF_ne(self):
        """
        ends with -네
        :return:
        """
        pass

    def test_generic_EF_ma(self):
        """
        ends with -마
        :return:
        """
        pass

    def test_generic_EF_euema(self):
        """
        ends with -으마
        :return:
        """
        pass

    def test_generic_EF_euergul(self):
        """
        ends with -을걸
        :return:
        """
        pass

    def test_generic_EF_rieul_gul(self):
        """
        ends with - ㄹ걸
        :return:
        """
        pass

    def test_generic_EF_euelgae(self):
        """
        ends with -을게
        :return:
        """
        pass

    def test_generic_EF_rieul_gae(self):
        """
        ends with -ㄹ게
        :return:
        """
        pass

    def test_generic_EF_eulrae(self):
        """
        ends with -을래
        :return:
        """
        pass

    def test_generic_EF_rieul_rae(self):
        """
        ends with -ㄹ래
        :return:
        """

    # 의문문 어미

    # 명령문 어미

    # 후종결어미

    # 인용어미
    def test_apply_honorifics_bieup_nida_preceded_by_yi(self):
        sent = "그는 전설입니다"
        self.assertEqual("그는 전설이야", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("그는 전설이에요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("그는 전설입니다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_bieup_nida_preceded_by_ha(self):
        sent = "어제 생일선물을 받아서 행복합니다"
        self.assertEqual("어제 생일선물을 받아서 행복해", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("어제 생일선물을 받아서 행복해요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("어제 생일선물을 받아서 행복합니다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_thanks_intimate(self):
        sent = "도와줘서 고마워"
        self.assertEqual("도와줘서 고마워", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("도와줘서 고마워요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("도와줘서 고맙습니다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_thanks_polite(self):
        sent = "도와줘서 고마워요"
        self.assertEqual("도와줘서 고마워", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("도와줘서 고마워요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("도와줘서 고맙습니다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_thanks_2_polite(self):
        sent = "도와줘서 감사해요"
        self.assertEqual("도와줘서 고마워", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("도와줘서 감사해요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("도와줘서 감사합니다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_thanks_formal(self):
        sent = "도와줘서 고맙습니다"
        self.assertEqual("도와줘서 고마워", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("도와줘서 고마워요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("도와줘서 고맙습니다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_thanks_2_formal(self):
        sent = "도와줘서 감사합니다"
        self.assertEqual("도와줘서 고마워", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("도와줘서 감사해요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("도와줘서 감사합니다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_hi_formal(self):
        sent = "안녕하십니까"
        self.assertEqual("안녕", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("안녕하세요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("안녕하십니까", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_hi_polite(self):
        sent = "안녕하세요"
        self.assertEqual("안녕", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("안녕하세요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("안녕하십니까", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_hi_intimate(self):
        sent = "안녕"
        self.assertEqual("안녕", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("안녕하세요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("안녕하십니까", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_hagesupnida(self):
        sent = "이번 일은 내가 맡아서 하겠습니다"
        self.assertEqual("이번 일은 내가 맡아서 할게", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("이번 일은 제가 맡아서 할게요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("이번 일은 제가 맡아서 하겠습니다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_halgeyo(self):
        sent = "이번 일은 내가 맡아서 할게요"
        self.assertEqual("이번 일은 내가 맡아서 할게", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("이번 일은 제가 맡아서 할게요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("이번 일은 제가 맡아서 하겠습니다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_halge(self):
        sent = "이번 일은 내가 맡아서 할게"
        self.assertEqual("이번 일은 내가 맡아서 할게", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("이번 일은 제가 맡아서 할게요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("이번 일은 제가 맡아서 하겠습니다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_galge(self):
        sent = "난 걸어 갈게"
        self.assertEqual("난 걸어 갈게", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("전 걸어 갈게요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("전 걸어 가겠습니다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_gesupnida(self):
        sent = "새로운 레시피를 알려드리겠습니다"
        self.assertEqual("새로운 레시피를 알려줄게", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("새로운 레시피를 알려드릴게요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("새로운 레시피를 알려드리겠습니다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_julge(self):
        sent = "새로운 레시피를 알려줄게"
        self.assertEqual("새로운 레시피를 알려줄게", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("새로운 레시피를 알려드릴게요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("새로운 레시피를 알려드리겠습니다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_geyo(self):
        sent = "새로운 레시피를 알려드릴게요"
        self.assertEqual("새로운 레시피를 알려줄게", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("새로운 레시피를 알려드릴게요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("새로운 레시피를 알려드리겠습니다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_eoga(self):
        sent = "가까우니까 걸어가"
        self.assertEqual("가까우니까 걸어가", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("가까우니까 걸어가요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("가까우니까 걸어갑니다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_ana(self):
        sent = "시험의 난도가 만만치 않아"
        self.assertEqual("시험의 난도가 만만치 않아", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("시험의 난도가 만만치 않아요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("시험의 난도가 만만치 않습니다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_anayo(self):
        sent = "시험의 난도가 만만치 않아요"
        self.assertEqual("시험의 난도가 만만치 않아", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("시험의 난도가 만만치 않아요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("시험의 난도가 만만치 않습니다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_supnida(self):
        sent = "고운 손이 다 망가졌습니다"
        self.assertEqual("고운 손이 다 망가졌어", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("고운 손이 다 망가졌어요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("고운 손이 다 망가졌습니다", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_apply_honorifics_ne(self):
        sent = "고운 손이 다 망가졌네"  # noqa
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
        self.assertEqual("가까우니까 걸어가", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("가까우니까 걸어가요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("가까우니까 걸어갑니다", self.tuner(sent, self.formal[0], self.formal[1]))

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
        sent = "가까우니까 걸어가자"  # noqa
        self.assertEqual("가까우니까 걸어가자", self.tuner(sent, self.ban[0], self.ban[1]))
        self.assertEqual("가까우니까 걸어가요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("가까우니까 걸어갑시다", self.tuner(sent, self.formal[0], self.formal[1]))  # or 걸어갑시다?
        sent = "난 걸어 갈게"
        self.assertEqual("난 걸어 갈게", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("전 걸어 갈게요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("전 걸어 가겠습니다", self.tuner(sent, self.formal[0], self.formal[1]))
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
