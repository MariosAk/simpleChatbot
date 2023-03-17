import requests
import pycountry
import spacy

api_key=""
url="https://newsapi.org/v2/"
def get_news(query, bot_response):
    nlp = spacy.load("en_core_web_lg")
    return_dict = dict()
    return_list = []
    gpe_name=''
    country_search = []

    if 'from' in query:
        nlped_input = nlp(query)
        for ent in nlped_input.ents:                       
            if ent.label_ == 'GPE':
                gpe_name = ent.text
                break
        if gpe_name:
            country_search = pycountry.countries.search_fuzzy(gpe_name)
        else:
            return_list.append({'error': 'Enter a valid country'})            
            return return_list
        if len(country_search) > 0:
            country_alpha = country_search[0].alpha_2
            country_name = country_search[0].name
        else:
            return_list.append({'error': 'Could not find country.'})
            return return_list
        fromUrl=url+"top-headlines?country={}&apiKey={}".format(country_alpha,api_key)
        response = requests.get(fromUrl)
        return populate_and_return_list(country_name, response, fromUrl)        
    
    elif 'about' in query:        
        i=0
        newsWordIndex=0
        ymlMatch_array = bot_response.split(' ')
        query_array = query.split(' ')                
        for ymlMatch in ymlMatch_array:                    
            if ymlMatch != '$':
                i=i+1                        
            else:
                newsWordIndex=i
                break
        word = query_array[newsWordIndex] 
        aboutUrl = url+"top-headlines?q={}&apiKey={}".format(word, api_key)       
        response = requests.get(aboutUrl)
        return populate_and_return_list(word, response, aboutUrl)
            
    else:
        lang='en'
        langUrl = url+"top-headlines?language={}&apiKey={}".format(lang, api_key)
        response = requests.get(langUrl)
        return populate_and_return_list('', response, langUrl)
        
def populate_and_return_list(var, response, url):
    return_list=[]
    if response.status_code == 200:
        responseDict = response.json()
        if responseDict['totalResults'] == 0:
            error = 'No news for {} found'.format(var) if var else 'No news found'
            return_list.append({'error': error})
            return return_list
        else:
            for news in responseDict['articles']:
                return_list.append({'title': news['title'], 'url': news['url'], 'publishedAt': news['publishedAt'], 'error': ''})
            return return_list
    else:
        return_list.append({'error':'[!] HTTP {0} calling [{1}]'.format(response.status_code, url)})
        return return_list