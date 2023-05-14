"""
courtesy of: https://gist.github.com/yuchenlin/eb63e2d0513f70cfc9bb85fa5a78953b
"""
from transformers import OpenAIGPTTokenizer, OpenAIGPTLMHeadModel
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch


def model_init(model_string, cuda):
    if model_string.startswith("gpt2"):
        tokenizer = GPT2Tokenizer.from_pretrained(model_string)
        model = GPT2LMHeadModel.from_pretrained(model_string)
    else:
        tokenizer = OpenAIGPTTokenizer.from_pretrained(model_string)
        model = OpenAIGPTLMHeadModel.from_pretrained(model_string)
    model.eval()
    if cuda:
        model.to('cuda')
    print("Model init")
    return model, tokenizer


def sent_scoring(model_tokenizer, text, cuda):
    model = model_tokenizer[0]
    tokenizer = model_tokenizer[1]
    assert model is not None
    assert tokenizer is not None
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
    model, tokenizer = model_init('gpt2', False)
    print(sent_scoring((model, tokenizer), "I love my cute dog.", False))
    print(sent_scoring((model, tokenizer), "I love your stupid dog.", False))