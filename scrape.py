import aiohttp
from selectorlib import Extractor
from data_process import data_process
#import logging

async def scrape(sr,url):
    headers = {
        'authority': 'www.blackcoffer.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    async with aiohttp.ClientSession() as session:
        #print(url)
        async with session.get(url=url,headers=headers) as response:
            if response.status == 200:
                e = Extractor.from_yaml_file('selector.yml')
                data = e.extract(await response.text())
                
                if data["Text"]["text"] == "" or data["Text"]["text"] is None:
                    print(f"{sr} 200 ok string is empty {url}")

            elif response.status == 404:
                #print(f"{sr} 404 error {url}")
                pass
            
            else:
                print(f"{sr} undefined error {url}")
                print(f"{response.status}\n")
                data = None
    try:
        if data is not None and data['Text']['para'] is not None:
            res = [None]*15
            res[0] =sr
            pro_obj = data_process(data)
            
            pro_obj.remove_stopword()
            
            res[1] = url
            res[2] = pro_obj.get_posscore()
            res[3] = pro_obj.get_negscore()
            res[4] = pro_obj.get_polarityscore()
            res[5] = pro_obj.get_subjectivityscore()
            res[6] = pro_obj.get_avgsentencelenght()

            res[10] = pro_obj.get_numcomplexwords()
            res[11] = pro_obj.get_wordcount()

            res[7] = pro_obj.get_percomplexword()
            res[8] = 0.4*(res[7]+res[6])

            res[9] = res[6]

            res[12] = pro_obj.get_avgsyllperword()
            res[13] = pro_obj.get_numperpro()
            res[14] = pro_obj.get_avgwordlen()

            #print(res)
            #print("succes ", url)


            return res
        
    except:
        #print(e)
        #print("unsuccessfull    ", url)
        return None

