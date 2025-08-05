import csv
import heapq


with open('file.txt','r',encoding='utf-8') as cfile:
    csvReader=csv.DictReader(cfile)
    heads=csvReader.fieldnames
    rows=list(csvReader)

#arrays we will use for each question where necessary
country_nameS=[]

HighestCityPop=[]

all_langs=[]

HighestCountryPop=[]

independece=[]

LargestLandMass=[]

IYCounter=[] #independent year counter to keep track of which countries we have already seen

lifeExp=[]

jist={}

Top5Lang=[]

#arrays we will use for each question where necessary

#counters
indepYearCounter=0
country_counter=0
#counters

#functions for the top 5 related questions
#Example: finding the 5 highest city population using min heap
#(if the city we find in THIS row is greater than the lowest/minimum city in the heap
# we replace the minimum value, as it is already not in the top 5 from what we have found.
# Then the array will not yet sort but bring the lowest value of the array into the first positon ie HighestCityPop[0])
def update_top_5(heap, item):
    if len(heap) < 5:
        heapq.heappush(heap, item)
    elif item[0] > heap[0][0] and item not in heap:
        heapq.heapreplace(heap, item)
#functions for the top 5 related questions

for row in rows:
    #All the information  we will need
    city_name=row.get('CityName')

    city_pop=row.get('CityPopulation')

    country_name = row.get('CountryName')

    country_pop = row.get('CountryPopulation')

    country_lang = row.get('Language')

    percentage = row.get('Percentage')

    country = (int(country_pop), country_name)

    landMass=row.get('LandMass')
    country_lifeEXP=row.get('LifeExpectancy')

    country_landMass = (float(landMass), country_name)

    city = (int(city_pop), city_name)

    indepYear=row.get('IndepYear')

    continent=row.get('Continent')
    #All the information we will need

    #answers both Questions (a) and (h)
    if country_name in country_nameS:
        pass
    elif country_name not in country_nameS and country_name.endswith("a"):
        country_nameS.append(country_name)
        country_counter+=1
    #Question b
    update_top_5(HighestCityPop, city)

    #repeat what we did for highest city populations and transcribe it to land mass
    #Question c
    update_top_5(LargestLandMass, country_landMass)

    # # repeat what we did for highest city populations and transcribe it to country pop
    # update_top_5(HighestCountryPop, country)

    if indepYear == 'NULL' or indepYear is None:
        pass
    elif int(indepYear)>=1830 and int(indepYear)<=1850 and country_name not in independece:
        independece.append(country_name)
    elif int(indepYear)>=1960 and int(indepYear)<=1980 and country_name not in IYCounter:
        indepYearCounter=indepYearCounter+1
        IYCounter.append(country_name)

    spoken={'Population':int(country_pop),
            'Language':country_lang,
            'Percentage':percentage,
            'Country':country_name
            }
    if spoken not in all_langs:
        all_langs.append(spoken)
    if country_lifeEXP=="NULL" or None:
        pass
    else:
        country_Life=(float(country_lifeEXP), country_name)
    if continent=="NULL" or continent is None:
        pass
    else :
        if continent == "Africa":
            update_top_5(lifeExp, country_Life)

#question g:
#Here we used a bit of logic to find the exact amount of speakers of each language
#As each language can be found on multiple countries
for spoken in all_langs:
    lang=spoken['Language']
    percentage=float(spoken['Percentage'])/100
    population=float(spoken['Population'])
    country_name=spoken['Country']
    pair=lang +'-'+country_name
    #Key is stored in jist, if the language and country pair are already in jist,then
    #it is ignored
    if spoken['Language'] in jist and pair not in jist:
        jist[spoken['Language']]+=percentage*population
        jist[pair]=True
        continue
    elif spoken['Language'] not in jist:
        jist[spoken['Language']]=percentage*population
        jist[pair]=True

for lang,total in jist.items():
    update_top_5(Top5Lang,(total,lang))
with open('file2.txt','w',newline='', encoding='utf-8') as file2:
    csvWriter=csv.writer(file2)

    csvWriter.writerow(["Question a:"])
    csvWriter.writerow([str(country_counter)])

    csvWriter.writerow(["Question b:"])
    csvWriter.writerow([", ".join(f"{city} ({pop})" for pop, city in sorted(HighestCityPop)[::-1])])

    csvWriter.writerow(["Question c:"])
    csvWriter.writerow([", ".join(f"{country} ({landmass})\n" for landmass, country in sorted(LargestLandMass)[::-1])])

    csvWriter.writerow(["Question d:"])
    csvWriter.writerow([", ".join(IYCounter)])

    csvWriter.writerow(["Question e:"])
    csvWriter.writerow([", ".join(independece)])

    csvWriter.writerow(["Question f:"])
    csvWriter.writerow([", ".join(f"{country} ({pop})" for pop, country in lifeExp)])

    csvWriter.writerow(["Question g:"])
    csvWriter.writerow([", ".join(f"{lang} ({int(pop)})" for pop, lang in sorted(Top5Lang)[::-1])])

    csvWriter.writerow(["Question h:"])
    csvWriter.writerow([", ".join(country_nameS)])
