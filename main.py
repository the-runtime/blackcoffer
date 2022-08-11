import asyncio
from types import NoneType
import pandas as pd
import csv

import scrape


async def main():

	inp_file_add = "input/Input.xlsx"
	input_data = pd.read_excel(inp_file_add)
	
	# A list to be populated with async tasks
	tasks = []

	i = 0
	final_i = input_data.shape[0]
	while i<final_i:
		sr = input_data["URL_ID"][i]
		url = input_data["URL"][i]
		tasks.append(asyncio.ensure_future(scrape.scrape(sr,url)))
		i+=1

	
	data_list = await asyncio.gather(*tasks)

	#final_data =[None]*len(data_list)

	final_list =[]

	for r in data_list:
		if r is not None:
			final_list.append(r)
			#final_data[r[0] = r
	
	#print(final_list)


	csv_header = ["URL_ID", "URL", "POSITIVE SCORE", "NEGATIVE SCORE", "POLARITY SCORE", "SUBJECTIVITY SCORE", "AVG SENTENCE LENGTH", "PERCENTAGE OF COMPLEX WORDS", "FOG INDEX", "AVG NUMBER OF WORDS PER SENTENCE", "COMPLEX WORD COUNT", "WORD COUNT", "SYLLABLE PER WORD", "PERSONAL PRONOUNS", "AVG WORD LENGTH"]

	with open("output.csv",'w',newline='')	as f:

		writer = csv.writer(f)
		writer.writerow(csv_header)

		writer.writerows(final_list)

		f.close()
	


if __name__=="__main__":
	asyncio.run(main())