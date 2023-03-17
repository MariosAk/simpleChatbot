from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from chatterbot.conversation import Statement
from chatterbot.response_selection import get_random_response
from IPython.display import Audio
import chatterbot
import requests
import spacy
import logging
import get_weather
import get_definition
import get_news

logging.basicConfig(level=logging.INFO)
nlp = spacy.load("en_core_web_lg")
bot = ChatBot('MariosBot', response_selection_method=get_random_response,
              logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',            
            'maximum_similarity_threshold': 0.6,            
        },
])

trainer = ChatterBotCorpusTrainer(bot)
trainer.train('./train_weather.yml', './train_conv.yml', './train_definitions.yml',
              './train_news.yml', "chatterbot.corpus.english")

bot.read_only = True

exit_conditions = (":q", "quit", "exit")

while True:
    query = input("> ")    
    if query in exit_conditions:
        break
    else:
        try:
            city_name = ''
            bot_response = bot.get_response(query)                                    
            try:
                response_tags = list(bot_response.tags)                                    
            except AttributeError:
                response_tags = list(bot_response['response'].tags)

            ## user input is about the weather, getting the city name from ent.label_                        
            if response_tags[0] == 'weather_info':
                nlped_input = nlp(query)
                for ent in nlped_input.ents:                       
                    if ent.label_ == 'GPE':
                        city_name = ent.text
                        break
                weather_description = get_weather.get_weather(city_name)                
                print(bot_response.text.format(city_name, weather_description))

            ## user is asking the definition of a word
            elif response_tags[0] == 'definition_info':
                definitionWordIndex=0                
                i=0
                ymlMatch_array = bot_response['ymlMatch'].split(' ')
                query_array = query.split(' ')                
                for ymlMatch in ymlMatch_array:                    
                    if ymlMatch != '$':
                        i=i+1                        
                    else:
                        definitionWordIndex=i
                        break
                to_define = query_array[definitionWordIndex]
                definition_dict=get_definition.get_definition(to_define)
                if definition_dict['error']:
                    print('This error occured: {}'.format(definition_dict['error']))
                else:
                    if definition_dict['word_origin'] == None:
                        definition_dict['word_origin']="No origin found" 
                    if not definition_dict['word_audio1'] :
                        definition_dict['word_audio1'] == 'Audio1 not found'
                    else:
                        content = requests.get(definition_dict['word_audio1']).content
                    if not definition_dict['word_audio2']:
                        definition_dict['word_audio2'] == 'Audio2 not found'
                    else:
                        content = requests.get(definition_dict['word_audio2']).content
                    print("Definition: {}".format(definition_dict['word_definition']))
                    print("Origin: {}".format(definition_dict['word_origin']))
                    print("Audio1: {}".format(definition_dict['word_audio1']))
                    print("Audio2: {}".format(definition_dict['word_audio2']))

            ## user asked about news
            elif response_tags[0] == 'news_info':
                news_list=get_news.get_news(query, bot_response['ymlMatch'])                
                if news_list[0]['error']:
                    print(news_list[0]['error'])
                else:
                    for news in news_list:
                        print("Title: {}".format(news['title']))
                        print("Url: {}".format(news['url']))
                        print("Date published: {}".format(news['publishedAt']))
                        print('-----------')                
            else:
                print(bot_response)
        ## If something not in .yml files is given this exception handles it
        except IndexError:
            print('I am sorry, but I do not understand.') 