from train import textbot, imgbot

'''
1. load model # model = load_model('chatbotmodel.h5')
2. def get_response(input):
    if input word:
        1. textbot.toknizer
        2. model predict
        3. result
    if input img:
        1. img.toknizer 
        2. model predict
        3. result
'''
class chatbot:
    def get_response(userinput):
        if userinput[:7].lower() == 'picture':
            return imgbot.test()
        else:
            return textbot.test()

        
        