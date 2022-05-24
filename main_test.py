import unittest
from unittest import TestCase
from politely import Styler


class TestStyler(TestCase):

    styler: Styler

    @classmethod
    def setUpClass(cls) -> None:
        cls.styler = Styler()

    def test_preprocess(self):
        sent = "이것은 예시 문장이다"
        self.styler.preprocess(sent)
        self.assertEqual("이것은 예시 문장이다.", self.styler.out)
        sent = "이것은 예시 문장이다."
        self.styler.preprocess(sent)
        self.assertEqual("이것은 예시 문장이다.", self.styler.out)

    def test_preprocess_trailing_spaces(self):
        sent = "이것은 예시 문장이다  "
        self.styler.preprocess(sent)
        self.assertEqual("이것은 예시 문장이다.", self.styler.out)
        sent = "이것은 예시 문장이다. "
        self.styler.preprocess(sent)
        self.assertEqual("이것은 예시 문장이다.", self.styler.out)

    def test_honorify_ra(self):
        """
        종결어미 -라
        """
        sent = "최선을 다하라."
        self.assertEqual("최선을 다하라.", self.styler(sent, 1))
        self.assertEqual("최선을 다하세요.", self.styler(sent, 2))
        self.assertEqual("최선을 다합시다.", self.styler(sent, 3))

    def test_honorify_ja(self):
        """
        종결어미 -자
        """
        sent = "자 이제 먹자."
        self.assertEqual("자 이제 먹자.", self.styler(sent, 1))  
        self.assertEqual("자 이제 먹어요.", self.styler(sent, 2))
        self.assertEqual("자 이제 먹읍시다.", self.styler(sent, 3))

    def test_honorify_nieun_dae(self):
        """
        종결어미 ㄴ대
        """
        sent = "밥먹고 누우면 안 된대."
        self.assertEqual("밥먹고 누우면 안 된대.", self.styler(sent, 1))
        self.assertEqual("밥먹고 누우면 안 된대요.", self.styler(sent, 2))
        self.assertEqual("밥먹고 누우면 안 된답니다.", self.styler(sent, 3))

    def test_honorify_nieun_dae_yo(self):
        """
        종결어미 ㄴ대요
        """
        sent = "밥먹고 누우면 안 된대요."
        self.assertEqual("밥먹고 누우면 안 된대.", self.styler(sent, 1))
        self.assertEqual("밥먹고 누우면 안 된대요.", self.styler(sent, 2))
        self.assertEqual("밥먹고 누우면 안 된답니다.", self.styler(sent, 3))

    def test_honorify_gae(self):
        sent = "회의를 시작할게."
        self.assertEqual("회의를 시작할게.", self.styler(sent, 1))  
        self.assertEqual("회의를 시작할게요.", self.styler(sent, 2))
        self.assertEqual("회의를 시작하겠습니다.", self.styler(sent, 3))

    def test_honorify_eo(self):
        """
        종결어미 -어
        """
        sent = "그 일은 내가 처리했어."
        self.assertEqual("그 일은 내가 처리했어.", self.styler(sent, 1))  
        self.assertEqual("그 일은 제가 처리했어요.", self.styler(sent, 2))
        self.assertEqual("그 일은 제가 처리했습니다.", self.styler(sent, 3))

    def test_honorify_yo(self):
        """
        종결어미 -요
        """
        sent = "제 패션을 함부로 비꼬지마요"
        self.assertEqual("내 패션을 함부로 비꼬지마.", self.styler(sent, 1))
        self.assertEqual("제 패션을 함부로 비꼬지마요.", self.styler(sent, 2))
        self.assertEqual("제 패션을 함부로 비꼬지마십시오.", self.styler(sent, 3))

    def test_honorify_ge_yo(self):
        """
        게 + 종결어미 -요
        """
        sent = "회의를 시작할게요."
        self.assertEqual("회의를 시작할게.", self.styler(sent, 1))
        self.assertEqual("회의를 시작할게요.", self.styler(sent, 2))
        self.assertEqual("회의를 시작하겠습니다.", self.styler(sent, 3))

    def test_honorify_yi_ya(self):
        """
        이+야
        """
        sent = "그 일은 내 담당이야."
        self.assertEqual("그 일은 내 담당이야.", self.styler(sent, 1))  
        self.assertEqual("그 일은 제 담당이에요.", self.styler(sent, 2))
        self.assertEqual("그 일은 제 담당입니다.", self.styler(sent, 3))

    def test_honorify_se_yo(self):
        """
        세+요
        """
        # 이미 규칙으로 존재하는 -세요 때문에 얘는 달라져야함
        sent = "최선을 다하세요."
        self.assertEqual("최선을 다해.", self.styler(sent, 1))
        self.assertEqual("최선을 다하세요.", self.styler(sent, 2))
        self.assertEqual("최선을 다하십시오.", self.styler(sent, 3))

    def test_honorify_yi_eyo(self):
        """
        이 + 에요
        """
        sent = "그 일은 제 담당이에요."
        self.assertEqual("그 일은 내 담당이야.", self.styler(sent, 1))
        self.assertEqual("그 일은 제 담당이에요.", self.styler(sent, 2))
        self.assertEqual("그 일은 제 담당입니다.", self.styler(sent, 3))

    def test_honorify_eu_yo_1(self):
        """
        종결어미 -어요 (1)
        """
        sent = "자 이제 먹어요."
        self.assertEqual("자 이제 먹어.", self.styler(sent, 1))
        self.assertEqual("자 이제 먹어요.", self.styler(sent, 2))
        self.assertEqual("자 이제 먹습니다.", self.styler(sent, 3))

    def test_honorify_eu_yo_2(self):
        """
        종결어미 -어요 (2)
        """
        sent = "그 일은 제가 처리했어요."
        self.assertEqual("그 일은 내가 처리했어.", self.styler(sent, 1))
        self.assertEqual("그 일은 제가 처리했어요.", self.styler(sent, 2))
        self.assertEqual("그 일은 제가 처리했습니다.", self.styler(sent, 3))

    def test_honorify_bo_ayo(self):
        """
        보 + 종결어미 -아요
        """
        sent = "좀만 더 버텨봐요"
        self.assertEqual("좀만 더 버텨봐.", self.styler(sent, 1))
        self.assertEqual("좀만 더 버텨봐요.", self.styler(sent, 2))
        self.assertEqual("좀만 더 버텨봅시다.", self.styler(sent, 3))

    def test_honorify_ma(self):
        sent = "내 패션을 함부로 비꼬지마"
        self.assertEqual("내 패션을 함부로 비꼬지마.", self.styler(sent, 1))  
        self.assertEqual("제 패션을 함부로 비꼬지마요.", self.styler(sent, 2))
        self.assertEqual("제 패션을 함부로 비꼬지마십시오.", self.styler(sent, 3))

    def test_honorify_bo_a(self):
        sent = "좀만 더 버텨봐"
        self.assertEqual("좀만 더 버텨봐.", self.styler(sent, 1))
        self.assertEqual("좀만 더 버텨봐요.", self.styler(sent, 2))
        self.assertEqual("좀만 더 버텨봅시다.", self.styler(sent, 3))

    def test_honorify_dae_q(self):
        sent = "걔 오늘 기분이 왜 이렇게 좋대?"
        self.assertEqual("걔 오늘 기분이 왜 이렇게 좋대?", self.styler(sent, 1))
        self.assertEqual("걔 오늘 기분이 왜 이렇게 좋대요?", self.styler(sent, 2))
        self.assertEqual("걔 오늘 기분이 왜 이렇게 좋습니까?", self.styler(sent, 3))

    def test_honorify_dae_yo_q(self):
        sent = "걔 오늘 기분이 왜 이렇게 좋대요?"
        self.assertEqual("걔 오늘 기분이 왜 이렇게 좋대?", self.styler(sent, 1))
        self.assertEqual("걔 오늘 기분이 왜 이렇게 좋대요?", self.styler(sent, 2))
        self.assertEqual("걔 오늘 기분이 왜 이렇게 좋습니까?", self.styler(sent, 3))

    def test_honorify_eo_q(self):
        """
        어?
        """
        # 했어?
        sent = "어제 공부는 마무리 했어?"
        self.assertEqual("어제 공부는 마무리 했어?", self.styler(sent, 1))  
        self.assertEqual("어제 공부는 마무리 했어요?", self.styler(sent, 2))
        self.assertEqual("어제 공부는 마무리 했습니까?", self.styler(sent, 3))

    def test_honorify_eo_yo_q_1(self):
        """
        의문형 종결어미 -어요? (1)
        """
        sent = "어제 공부는 마무리 했어요?"
        self.assertEqual("어제 공부는 마무리 했어?", self.styler(sent, 1))
        self.assertEqual("어제 공부는 마무리 했어요?", self.styler(sent, 2))
        self.assertEqual("어제 공부는 마무리 했습니까?", self.styler(sent, 3))

    def test_honorify_eo_yo_q_2(self):
        """
        의문형 종결어미 -어요 (2)
        """
        sent = "어디 가세요?"
        self.assertEqual("어디 가셔?", self.styler(sent, 1))
        self.assertEqual("어디 가세요?", self.styler(sent, 2))
        self.assertEqual("어디 가십니까?", self.styler(sent, 3))

    def test_honorify_si_eo_q(self):
        """
        시 + 의문형 종결어미 -어?
        """
        # 가셔? (가시어?)
        sent = "어디 가셔?"
        self.assertEqual("어디 가셔?", self.styler(sent, 1))
        self.assertEqual("어디 가셔요?", self.styler(sent, 2))
        self.assertEqual("어디 가십니까?", self.styler(sent, 3))

    def test_honorify_ddae_q(self):
        sent = "순서를 바꾸는건 어때?"
        self.assertEqual("순서를 바꾸는건 어때?", self.styler(sent, 1))  
        self.assertEqual("순서를 바꾸는건 어때요?", self.styler(sent, 2))
        self.assertEqual("순서를 바꾸는건 어떻습니까?", self.styler(sent, 3))
        sent = "순서를 바꾸는건 어때요?"
        self.assertEqual("순서를 바꾸는건 어때?", self.styler(sent, 1))  
        self.assertEqual("순서를 바꾸는건 어때요?", self.styler(sent, 2))
        self.assertEqual("순서를 바꾸는건 어떻습니까?", self.styler(sent, 3))

    # --- tests by irregular conjugations --- #
    def test_conjugate_ah_1(self):
        """
        동모음 탈락
        걸어가어요 (x)
        걸어가요 (o)
        """
        sent = "가까우니까 걸어가자."
        self.assertEqual("가까우니까 걸어가자.", self.styler(sent, 1))
        self.assertEqual("가까우니까 걸어가요.", self.styler(sent, 2))
        self.assertEqual("가까우니까 걸어갑시다.", self.styler(sent, 3))

    def test_conjugate_ah_2(self):
        """
        동모음 탈락
        떠나어요 (x)
        떠나요 (o)
        """
        sent = "자, 떠나자. 동해바다로."
        self.assertEqual("자, 떠나자. 동해바다로.", self.styler(sent, 1))
        self.assertEqual("자, 떠나요. 동해바다로.", self.styler(sent, 2))
        self.assertEqual("자, 떠납시다. 동해바다로.", self.styler(sent, 3))

    def test_conjugate_ah_3(self):
        """
        동모음 탈락 (3)
        """
        sent = "자, 떠나요. 동해바다로."
        self.assertEqual("자, 떠나. 동해바다로.", self.styler(sent, 1))
        self.assertEqual("자, 떠나요. 동해바다로.", self.styler(sent, 2))
        self.assertEqual("자, 떠납니다. 동해바다로.", self.styler(sent, 3))

    def test_conjugate_digud(self):
        """
        ㄷ 불규칙
        """
        sent = "나는 오늘 그 사실을 깨달았다."
        self.assertEqual("나는 오늘 그 사실을 깨달았다.", self.styler(sent, 1))  
        self.assertEqual("저는 오늘 그 사실을 깨달았어요.", self.styler(sent, 2))
        self.assertEqual("저는 오늘 그 사실을 깨달았습니다.", self.styler(sent, 3))
        sent = "저는 오늘 그 사실을 깨달았어요."
        self.assertEqual("나는 오늘 그 사실을 깨달았어.", self.styler(sent, 1))  
        self.assertEqual("저는 오늘 그 사실을 깨달았어요.", self.styler(sent, 2))
        self.assertEqual("저는 오늘 그 사실을 깨달았습니다.", self.styler(sent, 3))

    def test_conjugate_ru(self):
        """
        르 불규칙
        e.g. 들르 + 어 -> 들러
        e.g. 이르 + 어  -> 일러
        """
        sent = "나는 그 상점을 들렀다."
        self.assertEqual("나는 그 상점을 들렀다.", self.styler(sent, 1))  
        self.assertEqual("저는 그 상점을 들렀어요.", self.styler(sent, 2))
        self.assertEqual("저는 그 상점을 들렀습니다.", self.styler(sent, 3))
        sent = "저는 그 상점을 들렀어요."
        self.assertEqual("나는 그 상점을 들렀어.", self.styler(sent, 1))  
        self.assertEqual("저는 그 상점을 들렀어요.", self.styler(sent, 2))
        self.assertEqual("저는 그 상점을 들렀습니다.", self.styler(sent, 3))
        sent = "지금은 좀 일러."
        self.assertEqual("지금은 좀 일러.", self.styler(sent, 1))  
        self.assertEqual("지금은 좀 일러요.", self.styler(sent, 2))
        self.assertEqual("지금은 좀 이릅니다.", self.styler(sent, 3))

    def test_conjugate_bieup_1(self):
        """
        ㅂ 불규칙 (모음 조화 o)
        """
        sent = "모래가 참 고와."
        self.assertEqual("모래가 참 고와.", self.styler(sent, 1))  
        self.assertEqual("모래가 참 고와요.", self.styler(sent, 2))
        self.assertEqual("모래가 참 곱습니다.", self.styler(sent, 3))
        sent = "모래가 참 고와요."
        self.assertEqual("모래가 참 고와.", self.styler(sent, 1))  
        self.assertEqual("모래가 참 고와요.", self.styler(sent, 2))
        self.assertEqual("모래가 참 곱습니다.", self.styler(sent, 3))

    def test_conjugate_bieup_2(self):
        """
        ㅂ 불규칙 (모음 조화 x)
        """
        sent = "참 아름답다."
        self.assertEqual("참 아름답다.", self.styler(sent, 1))  
        self.assertEqual("참 아름다워요.", self.styler(sent, 2))
        self.assertEqual("참 아름답습니다.", self.styler(sent, 3))
        sent = "참 아름다워요."
        self.assertEqual("참 아름다워.", self.styler(sent, 1))  
        self.assertEqual("참 아름다워요.", self.styler(sent, 2))
        self.assertEqual("참 아름답습니다.", self.styler(sent, 3))

    def test_conjugate_bieup_3(self):
        """
        더워의 경우.
        """
        sent = "오늘이 어제보다 더워."
        self.assertEqual("오늘이 어제보다 더워.", self.styler(sent, 1))
        self.assertEqual("오늘이 어제보다 더워요.", self.styler(sent, 2))
        self.assertEqual("오늘이 어제보다 덥습니다.", self.styler(sent, 3))
        sent = "오늘이 어제보다 더워요."
        self.assertEqual("오늘이 어제보다 더워.", self.styler(sent, 1))
        self.assertEqual("오늘이 어제보다 더워요.", self.styler(sent, 2))
        self.assertEqual("오늘이 어제보다 덥습니다.", self.styler(sent, 3))

    def test_conjugate_bieup_4(self):
        """
        가려워의 경우.
        """
        sent = "너무 가려워."
        self.assertEqual("너무 가려워.", self.styler(sent, 1))
        self.assertEqual("너무 가려워요.", self.styler(sent, 2))
        self.assertEqual("너무 가렵습니다.", self.styler(sent, 3))
        sent = "너무 가려워요."
        self.assertEqual("너무 가려워.", self.styler(sent, 1))
        self.assertEqual("너무 가려워요.", self.styler(sent, 2))
        self.assertEqual("너무 가렵습니다.", self.styler(sent, 3))

    def test_conjugate_r_cho_is_bieup(self):
        """
        ㅂ니다
        """
        sent = "이름은 김유빈이야."
        self.assertEqual("이름은 김유빈입니다.", self.styler(sent, 3))
        sent = "이름은 김유빈이에요."
        self.assertEqual("이름은 김유빈입니다.", self.styler(sent, 3))

    def test_conjugate_siot(self):
        """
        ㅅ 불규칙
        """
        sent = "거기에 선을 그어."
        self.assertEqual("거기에 선을 그어.", self.styler(sent, 1))  
        self.assertEqual("거기에 선을 그어요.", self.styler(sent, 2))
        self.assertEqual("거기에 선을 긋습니다.", self.styler(sent, 3))
        sent = "거기에 선을 그어요."
        self.assertEqual("거기에 선을 그어.", self.styler(sent, 1))  
        self.assertEqual("거기에 선을 그어요.", self.styler(sent, 2))
        self.assertEqual("거기에 선을 긋습니다.", self.styler(sent, 3))

    def test_conjugate_siot_exception(self):
        """
        ㅅ 불규칙 (벗어는 예외)
        """
        sent = "한국의 목욕탕에서는 옷을 벗어."
        self.assertEqual("한국의 목욕탕에서는 옷을 벗어.", self.styler(sent, 1))  
        self.assertEqual("한국의 목욕탕에서는 옷을 벗어요.", self.styler(sent, 2))
        self.assertEqual("한국의 목욕탕에서는 옷을 벗습니다.", self.styler(sent, 3))
        sent = "한국의 목욕탕에서는 옷을 벗어요."
        self.assertEqual("한국의 목욕탕에서는 옷을 벗어.", self.styler(sent, 1))  
        self.assertEqual("한국의 목욕탕에서는 옷을 벗어요.", self.styler(sent, 2))
        self.assertEqual("한국의 목욕탕에서는 옷을 벗습니다.", self.styler(sent, 3))

    def test_conjugate_u(self):
        """
        우 불규칙
        """
        sent = "이 포스팅 퍼갈게."
        self.assertEqual("이 포스팅 퍼갈게.", self.styler(sent, 1))  
        self.assertEqual("이 포스팅 퍼갈게요.", self.styler(sent, 2))
        self.assertEqual("이 포스팅 퍼가겠습니다.", self.styler(sent, 3))
        sent = "이 포스팅 퍼갈게요."
        self.assertEqual("이 포스팅 퍼갈게.", self.styler(sent, 1))  
        self.assertEqual("이 포스팅 퍼갈게요.", self.styler(sent, 2))
        self.assertEqual("이 포스팅 퍼가겠습니다.", self.styler(sent, 3))

    def test_conjugate_u_jup(self):
        """
        우 불규칙 - 줍은 예외
        """
        sent = "쓰레기를 줍자."
        self.assertEqual("쓰레기를 줍자.", self.styler(sent, 1))
        self.assertEqual("쓰레기를 주워요.", self.styler(sent, 2))
        self.assertEqual("쓰레기를 주웁시다.", self.styler(sent, 3))
        sent = "쓰레기를 주워요."
        self.assertEqual("쓰레기를 주워.", self.styler(sent, 1))
        self.assertEqual("쓰레기를 주워요.", self.styler(sent, 2))
        self.assertEqual("쓰레기를 줍습니다.", self.styler(sent, 3))

    def test_conjugate_o(self):
        """
        오 불규칙
        """
        sent = "오늘 제주도로 여행왔어."
        self.assertEqual("오늘 제주도로 여행왔어.", self.styler(sent, 1))  
        self.assertEqual("오늘 제주도로 여행왔어요.", self.styler(sent, 2))
        self.assertEqual("오늘 제주도로 여행왔습니다.", self.styler(sent, 3))
        sent = "오늘 제주도로 여행왔어요."
        self.assertEqual("오늘 제주도로 여행왔어.", self.styler(sent, 1))  
        self.assertEqual("오늘 제주도로 여행왔어요.", self.styler(sent, 2))
        self.assertEqual("오늘 제주도로 여행왔습니다.", self.styler(sent, 3))

    def test_conjugate_drop_ue(self):
        """
        으 탈락 불규칙
        """
        sent = "전등을 껐다."
        self.assertEqual("전등을 껐다.", self.styler(sent, 1))  
        self.assertEqual("전등을 껐어요.", self.styler(sent, 2))
        self.assertEqual("전등을 껐습니다.", self.styler(sent, 3))
        sent = "전등을 껐어요."
        self.assertEqual("전등을 껐어.", self.styler(sent, 1))  
        self.assertEqual("전등을 껐어요.", self.styler(sent, 2))
        self.assertEqual("전등을 껐습니다.", self.styler(sent, 3))

    def test_conjugate_gara(self):
        """
        -가라 불규칙
        """
        sent = "저기로 가거라."
        self.assertEqual("저기로 가거라.", self.styler(sent, 1))  
        self.assertEqual("저기로 가세요.", self.styler(sent, 2))
        self.assertEqual("저기로 가십시오.", self.styler(sent, 3))
        sent = "저기로 가세요."
        self.assertEqual("저기로 가셔.", self.styler(sent, 1))  
        self.assertEqual("저기로 가세요.", self.styler(sent, 2))
        self.assertEqual("저기로 가십시오.", self.styler(sent, 3))

    def test_conjugate_neura(self):
        """
        -너라 불규칙
        """
        sent = "이리 오너라."
        self.assertEqual("이리 오너라.", self.styler(sent, 1))  
        self.assertEqual("이리 오세요.", self.styler(sent, 2))
        self.assertEqual("이리 오십시오.", self.styler(sent, 3))
        sent = "이리 오세요."
        self.assertEqual("이리 오셔.", self.styler(sent, 1))  
        self.assertEqual("이리 오세요.", self.styler(sent, 2))
        self.assertEqual("이리 오십시오.", self.styler(sent, 3))

    def test_conjugate_yue(self):
        """
        -여 불규칙
        """
        sent = "나는 그리하지 아니하였다."
        self.assertEqual("나는 그리하지 아니하였다.", self.styler(sent, 1))  
        self.assertEqual("저는 그리하지 아니했어요.", self.styler(sent, 2))
        self.assertEqual("저는 그리하지 아니했습니다.", self.styler(sent, 3))
        sent = "저는 그리하지 아니하였어요."
        self.assertEqual("나는 그리하지 아니했어.", self.styler(sent, 1))  
        self.assertEqual("저는 그리하지 아니하였어요.", self.styler(sent, 2))
        self.assertEqual("저는 그리하지 아니했습니다.", self.styler(sent, 3))

    def test_conjugate_drop_hiut(self):
        """
        ㅎ 탈락
        """
        sent = "하늘이 파랗다."
        self.assertEqual("하늘이 파랗다.", self.styler(sent, 1))  
        self.assertEqual("하늘이 파래요.", self.styler(sent, 2))
        self.assertEqual("하늘이 파랗습니다.", self.styler(sent, 3))
        sent = "하늘이 파래요."
        self.assertEqual("하늘이 파래.", self.styler(sent, 1))  
        self.assertEqual("하늘이 파래요.", self.styler(sent, 2))
        self.assertEqual("하늘이 파랗습니다.", self.styler(sent, 3))

    def test_conjugate_drop_yi(self):
        """
        ㅓ + 이.
        """
        sent = "이렇게 하는 거야?"
        self.assertEqual("이렇게 하는 거야?", self.styler(sent, 1))
        self.assertEqual("이렇게 하는 거죠?", self.styler(sent, 2))
        self.assertEqual("이렇게 하는 겁니까?", self.styler(sent, 3))
        sent = "이렇게 하는 거죠?"
        self.assertEqual("이렇게 하는 거야?", self.styler(sent, 1))
        self.assertEqual("이렇게 하는 거죠?", self.styler(sent, 2))
        self.assertEqual("이렇게 하는 겁니까?", self.styler(sent, 3))

    # --- known issues --- #
    @unittest.skip
    def test_more_1(self):
        """
        추가할만한 기능 (1)
        이것도 고려를 해야하나..? 잘 모르겠다.
        :return:
        """
        sent = "밥 먹어"
        self.assertEqual("밥 먹어.", self.styler(sent, 1))
        self.assertEqual("밥 먹어요", self.styler(sent, 2))
        self.assertEqual("진지 잡수세요", self.styler(sent, 3))

    @unittest.skip
    def test_more_2(self):
        """
        추가할만한 기능 (20
        존대를 할 때는 주어를 드랍하는 규칙이 있다. 하지만 현재 적용하진 상태.
        :return:
        """
        sent = "자네만 믿고 있겠네"
        # 만약.. 들어오는 입력이 반말이라면, 굳이 반말인 경우를 수정할 필요가 없다.
        self.assertEqual("자네만 믿고 있겠네.", self.styler(sent, 1))  
        self.assertEqual("믿고 있겠어요.", self.styler(sent, 2))
        self.assertEqual("믿고 있겠습니다.", self.styler(sent, 3))

    @unittest.skip
    def test_khaiii_error_1(self):
        """
        이건 khaiii에서의 문제다.
        "줍"만을 어간으로 추출해야하는데 알 수 없는 이유로 그렇게 되지 않는다.
        결과적으로,
        줍웠 + 어
        만을 고려하게된다. 그래서 ㅂ 블규칙이 적용되지 않음.
        """
        sent = "길가다가 동전을 주웠어."
        self.assertEqual("길가다가 동전을 주웠어.", self.styler(sent, 1))
        self.assertEqual("길가다가 동전을 주웠어요.", self.styler(sent, 2))
        self.assertEqual("길가다가 동전을 주웠습니다.", self.styler(sent, 3))
        sent = "길가다가 동전을 주웠어요."   # 아... 줍우... 줍이 아니라.. 줍우..
        self.assertEqual("길가다가 동전을 주웠어.", self.styler(sent, 1))
        self.assertEqual("길가다가 동전을 주웠어요.", self.styler(sent, 2))
        self.assertEqual("길가다가 동전을 주웠습니다.", self.styler(sent, 3))

    @unittest.skip
    def test_khaiii_error_2(self):
        """
        이것도 khaiii에서의 문제다.
        걷어를 맥락을 고려하지 않고 무조건적으로 걸어로 분석한다.
        """
        sent = "이참에 돈을 걷어가자."
        self.assertEqual("이참에 돈을 걷어가자.", self.styler(sent, 1))
        self.assertEqual("이참에 돈을 걷어가요.", self.styler(sent, 2))
        self.assertEqual("이참에 돈을 걷어갑시다.", self.styler(sent, 3))

    @unittest.skip
    def test_khaiii_error_3(self):
        sent = "가까우니까 걸어가요."
        self.assertEqual("가까우니까 걸어가자.", self.styler(sent, 1))
        self.assertEqual("가까우니까 걸어가요.", self.styler(sent, 2))
        self.assertEqual("가까우니까 걸어갑시다.", self.styler(sent, 3))

    @unittest.skip
    def test_contextual_1(self):
        # 이런 식으로 맥락이 필요한 경우도 대응이 어렵다. (존대 종결어미 선정에 맥락이 관여하는 경우)
        # 이제, 밥을 등, 단어 선택에 따라 formal의 형태가 달라지는데, 이것에 대응하는 것은 불가능하다.
        # 맥락이 필요하다. 오직 규칙만으로는 불가능하다.
        sent = "자 이제 먹어요."
        self.assertEqual("자 이제 먹읍시다", self.styler(sent, 3))
        sent = "전 밥을 먹어요."
        self.assertEqual("전 밥을 먹습니다", self.styler(sent, 3))

    @unittest.skip
    def test_contextual_2(self):
        """
        -르 불규칙 (conjugation 규칙에 맥락이 관여하는 경우)
        e.g. 이르 + 어 -> 이르러
        e.g.
        이건 -러 불규칙과 구분히 불가능하다. 나중에 맥락까지 고려할 수 있게된다면 그 때 해보자.
        여기 이슈참고: https://github.com/eubinecto/politely/issues/56#issue-1233231686
        """
        sent = "하지말라고 일렀다."
        self.assertEqual("하지말라고 일렀다.", self.styler(sent, 1))
        self.assertEqual("하지말라고 일렀어요.", self.styler(sent, 2))
        self.assertEqual("하지말라고 일렀습니다.", self.styler(sent, 3))
        sent = "드디어 정상에 이르렀다."
        self.assertEqual("드디어 정상에 이르렀다.", self.styler(sent, 1))  
        self.assertEqual("드디어 정상에 이르렀어요.", self.styler(sent, 2))
        self.assertEqual("드디어 정상에 이르렀습니다.", self.styler(sent, 3))
        
    @unittest.skip
    def test_contextual_3(self):
        """
        쓰레기를 주워요 -> 쓰레기를 주웁시다 / 쓰레기를 줍습니다 (존대 종결어미 선정에 맥락이 관여하는 경우)
        둘다 가능하다. 이 경우는 맥락이 필요하다. 규칙만으로는 불가능하다.
        # 자세한 설명: https://github.com/eubinecto/politely/issues/60#issuecomment-1126839221
        """
        sent = "저는 쓰레기를 주워요."
        self.assertEqual("나는 쓰레기를 주워.", self.styler(sent, 1))
        self.assertEqual("저는 쓰레기를 주워요.", self.styler(sent, 2))
        self.assertEqual("저는 쓰레기를 줍습니다.", self.styler(sent, 3))
        sent = "같이 쓰레기를 주워요."
        self.assertEqual("같이 쓰레기를 줍자.", self.styler(sent, 1))
        self.assertEqual("같이 쓰레기를 주워요.", self.styler(sent, 2))
        self.assertEqual("같이 쓰레기를 주웁시다.", self.styler(sent, 3))

    @unittest.skip
    def test_contextual_4(self):
        """
        이것도 마찬가지로 맥락이 필요하다.
        떠나요 -> 떠나 / 떠나자, 둘 중 무엇이 정답인지는 맥락을 보아야만 알 수 있다.
        떠나요 -> 떠납니다 / 떠납시다 -> 둘 중 무엇이 맞는지도... 마찬가지
        """
        sent = "자, 떠나요. 동해바다로."
        self.assertEqual("자, 떠나자. 동해바다로.", self.styler(sent, 1))
        self.assertEqual("자, 떠나요. 동해바다로.", self.styler(sent, 2))
        self.assertEqual("자, 떠납시다. 동해바다로.", self.styler(sent, 3))
