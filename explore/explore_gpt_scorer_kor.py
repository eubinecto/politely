import torch
from transformers import  AutoTokenizer
from transformers import GPT2LMHeadModel


def sent_scoring(model, tokenizer, text, cuda):
    input_ids = torch.tensor(tokenizer.encode(text)).unsqueeze(0)  # Batch size 1
    if cuda:
        input_ids = input_ids.to('cuda')
    with torch.no_grad():
        outputs = model(input_ids, labels=input_ids)
    loss, logits = outputs[:2]
    # use negative-log likelihood
    sentence_prob = -loss.item()
    return sentence_prob


if __name__ == '__main__':
    # model, tokenizer = model_init('openai-gpt', False)
    model = GPT2LMHeadModel.from_pretrained('beomi/kykim-gpt3-kor-small_based_on_gpt2')
    tokenizer = AutoTokenizer.from_pretrained('beomi/kykim-gpt3-kor-small_based_on_gpt2')
    print(sent_scoring(model, tokenizer, "아버지가 진지를 드셔요", False))
    print(sent_scoring(model, tokenizer, "아버님께서 진지를 드셔요.", False))


"""
-6.792420864105225
-5.410952091217041
---
오케이... 나쁘지 않다...!
배치 처리가 되지 않는다면 ... 속도는 엄청 느릴 듯 ㅠㅠ
"""