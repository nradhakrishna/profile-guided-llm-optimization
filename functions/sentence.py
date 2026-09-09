def create_sentence(words):
    sentence = ""

    for word in words:
        sentence += word + " "

    return sentence.strip()