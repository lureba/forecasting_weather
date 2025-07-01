from google import genai
from google.genai import types
from functionss.webscraping import find_urls,writing,compare_urls,return_info
from datetime import date
import logging
import psycopg2 as pg
import sys
import os
logger = logging.getLogger(__name__)
logging.basicConfig(filename='scrapping.log',level=logging.INFO)
from pathlib import Path


def response_weather(texto):
    api_key = os.getenv("API_GEMINI")
    clientai = genai.Client(api_key=api_key)
    response = clientai.models.generate_content(
        model="gemini-2.0-flash",contents="" \
        f"Você é um meteorologista experiente. Analise cuidadosamente o texto:{texto}.com base na intensidade das informações e na sua relevância para mudanças climáticas, " \
        "classifique-o em uma das seis categorias de decisão do tempo, considerando que o que está sendo medido é a temperatura:" \
        "+++ (Vai aumentar muito)" \
        "++ (Vai aumentar)" \
        "+ (Vai aumentar pouco)" \
        "- (Vai diminuir pouco)" \
        "-- (Vai diminuir)" \
        "--- (Vai diminuir muito)" \
        "Considere elementos como termos que indicam elevação ou queda brusca da temperatura, contexto climático, projeções meteorológicas, intensidade dos fenômenos" \
        " e outras pistas relevantes. Retorne apenas a classificação final, sem explicações ou comentários adicionais.",config=types.GenerateContentConfig(max_output_tokens=100,temperature=0.1)
    )
    return response.text

new_urls = find_urls("https://www.012news.com.br/?s=tempo")
writing(new_urls)
final_urls = compare_urls(new_urls)
print(final_urls)

if final_urls:
    info = return_info(final_urls)
else:
    logger.info("Not info today")
    sys.exit()

dbname = os.getenv("DBNAME")
user = os.getenv("USER_POSTGRES")
password = os.getenv("PASSWORD")
conn = pg.connect("user={} password={} dbname={}",user,password,dbname)
curs = conn.cursor()
for i,j in zip (info,final_urls):
    date_scrap = date.today()
    text = i
    urls = j
    answer = response_weather(i)
    curs.execute('''INSERT INTO scrapping VALUES(%s,%s,%s,%s)''',(answer,i,date_scrap,j))
    conn.commit()

