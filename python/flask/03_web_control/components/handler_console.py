import json

def send(text):
    try:
        if isinstance(text, dict):
            for t in text:
                print('[handler_console]' + t + ':' + str(text[t]))
        else:
            print('[handler_console]:' + str(text))
    except Exception as e:
        print(e)
        return '[handler_console]:failed'
    return '[handler_console]:handled'
