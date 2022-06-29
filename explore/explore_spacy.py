import spacy


def main():
    # Load English tokenizer, tagger, parser and NER
    nlp = spacy.load("en_core_web_sm")

    # Process whole documents
    text = (
        "When Sebastian Thrun started working on self-driving cars at "
        "Google in 2007, few people outside of the company took him "
        "seriously. “I can tell you very senior CEOs of major American "
        "car companies would shake my hand and turn away because I wasn’t "
        "worth talking to,” said Thrun, in an interview with Recode earlier "
        "this week."
    )
    doc = nlp(text)

    # 사실..  영어는 굴절어라.. 토큰화는 말그대로 토큰화만 하면된다.
    print(" ".join([token.text for token in doc]))
    # 하지만 교착어인 한국어는 토큰화만으로는 부족하다. 토큰으로 분리하고, 각 토큰이 어떤 형태소가 결합되어 만들어졌는지도 분석해야하기 때문이다.


if __name__ == "__main__":
    main()
