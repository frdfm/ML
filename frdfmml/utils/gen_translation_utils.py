import random

import torch


def generate_translation(model, tokenizer, src_str, max_seq_len, k1, k2):

    src_tokens = tokenizer(
        src_str,
        padding='max_length',
        truncation=True,
        max_length=max_seq_len - 1,
        return_tensors="pt",
        return_attention_mask=False
    )['input_ids']

    src_tokens = torch.cat([torch.tensor([[tokenizer.eos_token_id]]), src_tokens], dim=1)
    tgt = torch.tensor([[tokenizer.pad_token_id] * max_seq_len])
    tgt[0, 0] = tokenizer.eos_token_id  # tokenizer.convert_tokens_to_ids("!")

    device = model.device
    src_tokens = src_tokens.to(device)
    tgt = tgt.to(device)

    for i in range(max_seq_len - 1):
        logits = model(src_tokens, tgt)

        # next_token_id = torch.argmax(logits[:, i, :], dim=-1)
        next_token_id = torch.topk(logits[:, i, :], random.randint(k1, k2), dim=-1)[1][:, -1]

        tgt[0, i + 1] = next_token_id
        if next_token_id == tokenizer.eos_token_id:
            continue  # break

    return tokenizer.decode(tgt[0], skip_special_tokens=True)