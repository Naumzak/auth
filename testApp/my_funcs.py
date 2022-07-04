def list_to_dict(data_list):
    ready_list = []
    for line in data_list:
        key_word = line[:line.find(':')]
        value_word = line[line.find(':') + 1:]
        if key_word != 'ASIN' and key_word != 'Itemmodelnumber':
            ready_list.append(value_word)
    return ready_list


def upadate_minidescription(text):
    text = str(text)
    if text.find('default') > 0:
        ready_text = text[text.find('default') + 8:]
    else:
        ready_text = text
    return ready_text
