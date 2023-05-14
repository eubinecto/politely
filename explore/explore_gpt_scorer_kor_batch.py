"""
loss by sequence
# https://github.com/huggingface/transformers/issues/16411
"""
from pprint import pprint

import torch
from torch.nn import CrossEntropyLoss
from transformers import BertTokenizerFast
from transformers import GPT2LMHeadModel


texts = [
    "저는 쓰레기를 줍습니다.",
    "저는 쓰레기를 주웁시다.",
]

if __name__ == '__main__':
    # ---- as a batch --- #
    # model, tokenizer = model_init('openai-gpt', False)
    model = GPT2LMHeadModel.from_pretrained('beomi/kykim-gpt3-kor-small_based_on_gpt2')
    tokenizer = BertTokenizerFast.from_pretrained('beomi/kykim-gpt3-kor-small_based_on_gpt2')
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)  # (N, L)
    pprint(inputs.input_ids)
    with torch.no_grad():
        # output the loss of each instance
        outputs = model(**inputs)
    logits = outputs['logits']   # (N, L, |V|)
    labels = inputs.input_ids
    # --- shift them --- #
    shift_logits = logits[:, :-1, :].contiguous()
    shift_labels = labels[:, 1:].contiguous()
    # Flatten the tokens
    loss_fct = CrossEntropyLoss(reduction='none', ignore_index=tokenizer.pad_token_id)
    loss = loss_fct(shift_logits.view(-1, shift_logits.size(-1)), shift_labels.view(-1))
    loss_by_sequence = loss.view(logits.size(0), -1).mean(dim=1)
    # negative log likelihood
    loss_by_sequence = - loss_by_sequence
    print(loss_by_sequence)
    # --- independantly --- #
    for text in texts:
        input_ids = tokenizer(text, return_tensors="pt").input_ids
        with torch.no_grad():
            outputs = model(input_ids, labels=input_ids)
        loss = outputs['loss']   # (N, L, |V|)
        print(-loss.item())



"""
tensor([[    2, 18361, 15033, 22647,  8273, 24254,  8055,     3],
        [    2, 20860, 18126, 19150,     3,     0,     0,     0]])
tensor([ -6.1531, -11.0299])
"""