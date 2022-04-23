import unittest
from unittest import TestCase
from politely.processors import KPS


class TestKPS(TestCase):

    tuner: KPS

    @classmethod
    def setUpClass(cls) -> None:
        cls.tuner = KPS()
        cls.ban = ("adult family 👨‍👩‍👧‍👦", "comfortable & informal")
        cls.jon = ("adult family 👨‍👩‍👧‍👦", "formal")
        cls.formal = ("boss at work 💼", "formal")

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

    # --- casual --- #
    def test_EF_ja(self):
        sent = "자 이제 먹자."
        self.assertEqual("자 이제 먹자.", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("자 이제 먹어요.", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("자 이제 먹읍시다.", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "자 이제 먹어요."
        self.assertEqual("자 이제 먹어.", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("자 이제 먹어요.", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("자 이제 먹습니다.", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "자 이제 먹습니다."
        self.assertEqual("자 이제 먹어.", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("자 이제 먹어요.", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("자 이제 먹습니다.", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_EF_gae(self):
        sent = "회의를 시작할게."
        self.assertEqual("회의를 시작할게.", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("회의를 시작할게요.", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("회의를 시작하겠습니다.", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "회의를 시작할게요."
        self.assertEqual("회의를 시작할게.", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("회의를 시작할게요.", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("회의를 시작하겠습니다.", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "회의를 시작하겠습니다."
        self.assertEqual("회의를 시작하겠어.", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("회의를 시작하겠어요.", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("회의를 시작하겠습니다.", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_EF_eo(self):
        """
        어
        """
        sent = "그 일은 내가 처리했어."
        self.assertEqual("그 일은 내가 처리했어.", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("그 일은 제가 처리했어요.", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("그 일은 제가 처리했습니다.", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "그 일은 제가 처리했어요."
        self.assertEqual("그 일은 내가 처리했어.", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("그 일은 제가 처리했어요.", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("그 일은 제가 처리했습니다.", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "그 일은 제가 처리했습니다."
        self.assertEqual("그 일은 내가 처리했어.", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("그 일은 제가 처리했어요.", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("그 일은 제가 처리했습니다.", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_EF_yi_ya(self):
        """
        이+야
        """
        sent = "그 일은 내 담당이야."
        self.assertEqual("그 일은 내 담당이야.", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("그 일은 제 담당이에요.", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("그 일은 제 담당입니다.", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "그 일은 제 담당이에요."
        self.assertEqual("그 일은 내 담당이야.", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("그 일은 제 담당이에요.", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("그 일은 제 담당입니다.", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "그 일은 제 담당입니다."
        self.assertEqual("그 일은 내 담당이야.", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("그 일은 제 담당이에요.", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("그 일은 제 담당입니다.", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_EF_ma(self):
        sent = "내 패션을 함부로 비꼬지마"
        self.assertEqual("내 패션을 함부로 비꼬지마.", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("제 패션을 함부로 비꼬지마요.", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("제 패션을 함부로 비꼬지마십시오.", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "제 패션을 함부로 비꼬지마요"
        self.assertEqual("내 패션을 함부로 비꼬지마.", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("제 패션을 함부로 비꼬지마요.", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("제 패션을 함부로 비꼬지마십시오.", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "제 패션을 함부로 비꼬지마십시오"
        self.assertEqual("내 패션을 함부로 비꼬지마셔.", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("제 패션을 함부로 비꼬지마셔요.", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("제 패션을 함부로 비꼬지마십시오.", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_EF_eo_q(self):
        """
        어?
        """
        # 했어?
        sent = "어제 공부는 마무리 했어?"
        self.assertEqual("어제 공부는 마무리 했어?", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("어제 공부는 마무리 했어요?", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("어제 공부는 마무리 했습니까?", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "어제 공부는 마무리 했어요?"
        self.assertEqual("어제 공부는 마무리 했어?", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("어제 공부는 마무리 했어요?", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("어제 공부는 마무리 했습니까?", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "어제 공부는 마무리 했습니까?"
        self.assertEqual("어제 공부는 마무리 했어?", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("어제 공부는 마무리 했어요?", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("어제 공부는 마무리 했습니까?", self.tuner(sent, self.formal[0], self.formal[1]))
        # 가셔? (가시어?)
        sent = "어디 가셔?"
        self.assertEqual("어디 가셔?", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("어디 가셔요?", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("어디 가십니까?", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "어디 가셔요?"
        self.assertEqual("어디 가셔?", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("어디 가셔요?", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("어디 가십니까?", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "어디 가십니까?"
        self.assertEqual("어디 가셔?", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("어디 가셔요?", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("어디 가십니까?", self.tuner(sent, self.formal[0], self.formal[1]))

    def test_EF_ddae_q(self):
        sent = "순서를 바꾸는건 어때?"
        self.assertEqual("순서를 바꾸는건 어때?", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("순서를 바꾸는건 어때요?", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("순서를 바꾸는건 어떻습니까?", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "순서를 바꾸는건 어때요?"
        self.assertEqual("순서를 바꾸는건 어때?", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("순서를 바꾸는건 어때요?", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("순서를 바꾸는건 어떻습니까?", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "순서를 바꾸는건 어떻습니까?"
        self.assertEqual("순서를 바꾸는건 어때?", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("순서를 바꾸는건 어때요?", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("순서를 바꾸는건 어떻습니까?", self.tuner(sent, self.formal[0], self.formal[1]))

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

    @unittest.skip
    def test_drop_subject_when_honorified(self):
        """
        존대를 할 때는 주어를 드랍하는 규칙이 있다. 하지만 현재 적용하진 상태.
        :return:
        """
        sent = "자네만 믿고 있겠네"
        # 만약.. 들어오는 입력이 반말이라면, 굳이 반말인 경우를 수정할 필요가 없다.
        self.assertEqual("자네만 믿고 있겠네", self.tuner(sent, self.ban[0], self.ban[1]))  # noqa
        self.assertEqual("믿고 있겠어요", self.tuner(sent, self.jon[0], self.jon[1]))
        self.assertEqual("믿고 있겠습니다", self.tuner(sent, self.formal[0], self.formal[1]))

    @unittest.skip
    def test_contextual(self):
        # 이런 식으로 맥락이 필요한 경우도 대응이 어렵다.
        # 이제, 밥을 등, 단어 선택에 따라 formal의 형태가 달라지는데, 이것에 대응하는 것은 불가능하다.
        sent = "자 이제 먹어요"
        self.assertEqual("자 이제 먹읍시다", self.tuner(sent, self.formal[0], self.formal[1]))
        sent = "전 밥을 먹어요"
        self.assertEqual("전 밥을 먹습니다", self.tuner(sent, self.formal[0], self.formal[1]))