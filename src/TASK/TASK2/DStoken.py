from transformers import AutoTokenizer, LlamaTokenizer

def calc_token(msg:str, model: str = "DeepSeek-R1"):
    if model == "DeepSeek-R1":
        tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-r1")
        text = msg
        tokens = tokenizer.tokenize(text)
        print(tokens)
        print("Total tokens:", len(tokens))
    elif model == "Llama-7b":
        tokenizer = LlamaTokenizer.from_pretrained("huggyllama/llama-7b")
        text = msg
        tokens = tokenizer.tokenize(text)
        print(tokens)
        print("Total tokens:", len(tokens))
    return tokens

if __name__ == '__main__':
    msg = "To be or not to be, that is the question."
    calc_token(msg, "Llama-7b")
    