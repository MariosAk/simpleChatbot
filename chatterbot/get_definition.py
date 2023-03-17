import requests

def get_definition(word):    
    definitionsURL = "https://api.dictionaryapi.dev/api/v2/entries/en/{}".format(word)
    return_dict = dict()
    response = requests.get(definitionsURL)
    responseDict = response.json()

    if response.status_code == 200:
        #try:
            word_definition = responseDict[0]['meanings'][0]['definitions'][0]['definition']            
            word_audio1 = responseDict[0]['phonetics'][0]['audio']                   
            word_audio2 = responseDict[0]['phonetics'][1]['audio'] if len(responseDict[0]['phonetics']) > 1 else ''
            word_origin = responseDict[0].get('origin')
            return_dict['word_definition']=word_definition
            return_dict['word_origin']=word_origin
            return_dict['word_audio1']=word_audio1
            return_dict['word_audio2']=word_audio2
            return_dict['error']=''            
    else:
        return_dict['error'] = '[!] HTTP {0} calling [{1}]'.format(response.status_code, definitionsURL)
    return return_dict