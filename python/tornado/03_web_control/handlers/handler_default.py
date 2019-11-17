
def send(text):
    _name = 'handler_default'
    try:
        if isinstance(text, dict):
            for t in text:
                print('[' + _name + ']' + t + ':' + str(text[t]))
        else:
            print('[' + _name + ']:' + str(text))
    except Exception as e:
        print(e)
        return '[' + _name + ']:failed'
    return '[' + _name + ']:handled'
