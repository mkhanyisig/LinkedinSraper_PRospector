"""
Mkhanyisi Gamedze
Linkedin Webscraper Test

Prospector Portal Dev
16 July 2020
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common import exceptions
import time
import requests
import random
import sys
from bs4 import BeautifulSoup
import json
import os
import re
import csv
import unidecode

####### setup   ##########

###### get profiles #####

data=[]

with open('author_profiles_batch2.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

urls=[]

for profile in data:
    #print(profile)
    urls.append(profile[-1])

######## Global variables

urls.pop(0) # remove first element, header

#print("final list:\n",urls)


# Scraping Object variables
objects=[]
author_profiles=[]
past_companies=[]
past_job_titles=[]
past_job_details=[]
education_experience=[]


# external files
profiles="profiles.json"
authors_json="authors.json"
companies_json="companies.json"
author_jobhistory_json="authors_job_history.json"
authors_education_json="authors_education.json"


# Define Browser Options
print("Setting Up Driver")
chrome_options = Options()
chrome_options.add_argument("--headless")  # Hides the browser window

# Reference the local Chromedriver instance
chrome_path = '/usr/local/bin/chromedriver'

browser = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)

#browser = webdriver.Chrome('driver/chromedriver.exe')

#browser = webdriver.Chrome('driver/chromedriver.exe')
browser.get('https://www.linkedin.com/uas/login')

######### login  #########

file = open('config.txt')
lines = file.readlines()
username = lines[0]
password = lines[1]

print("username: ",username)
print("password: ",password)

elementID = browser.find_element_by_id('username')
elementID.send_keys(username)

elementID = browser.find_element_by_id('password')
elementID.send_keys(password)

#print("gets here")

#elementID = browser.find_element_by_class_name("login__form_action_container")

# <div class="login__form_action_container "><button class="btn__primary--large from__button--floating" data-litms-control-urn="login-submit" type="submit" aria-label="Sign in">Sign in</button></div>
# <button class="btn__primary--large from__button--floating" data-litms-control-urn="login-submit" type="submit" aria-label="Sign in">Sign in</button>

#elementID.click()

print("succesful login")

def scrape(url):

    print("###### link: ",url)

    browser.get(url)


    print("\n****\nsuccesfully gets link\n****\n")

    SCROLL_PAUSE_TIME = 5

    """ load whole page """

    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")

    print("scrolling")

    for i in range(4):
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    print("done scrolling")

    # expand summary if it's there
    try:
        expand_summary=browser.find_element_by_id("line-clamp-show-more-button")

        print("*** See more: \n",expand_summary)

        if(expand_summary!=None):
            print("**** Selection is not None")
            print(expand_summary)
            expand_summary.click()
    except:
        print("*** No About Section expand button")


    #browser.find_element_by_class_name("visually-hidden").click()

    # Dictionary objects
    author_attributes={}
    work_history={}
    job_title_history={}
    job_details={}
    edu_exp={}

    src = browser.page_source
    soup = BeautifulSoup(src, 'lxml')

    # personal info div
    print("getting info")

    name_div = soup.find('div', {'class': 'flex-1 mr5'})

    if(name_div is not None):
         name_loc = name_div.find_all('ul')
    else:
        name_loc=None

    if(name_loc is not None):
        name = name_loc[0].find('li').get_text().strip()

        loc = name_loc[1].find('li').get_text().strip()


    profile_title = name_div.find('h2').get_text().strip()

    connection = name_loc[1].find_all('li')
    connection = connection[1].get_text().strip()

    # <img title="Mkhanyisi Gamedze" src="https://media-exp1.licdn.com/dms/image/C4E35AQFRnMT7ztGljQ/profile-framedphoto-shrink_200_200/0?e=1595016000&amp;v=beta&amp;t=pADMDFJBWfKj7chpJQFyewAGSQ2ewj8EXdSnvHoor4w" loading="lazy" alt="Mkhanyisi Gamedze" id="ember714" class="pv-top-card__photo presence-entity__image EntityPhoto-circle-9 lazy-image ember-view">
    photo_link=soup.find('img', class_="pv-top-card__photo")

    print("photo link :",photo_link['src'])

    about=soup.find('p',class_="pv-about__summary-text mt4 t-14 ember-view")

    print("************\n*****About: ",about)

    if about!=None:
        about=about.find_all('span') #

    print("About :",about)

    if about is not None:
        #about=about.get_text()
        s=""
        for sp in about:
            s+=sp.get_text()
        print("about: ",s)
        s=s.replace("see more","")
        s=s.replace("...",".")
        s=s.replace("\n","<br>")
        about=s



    # <span class="lt-line-clamp__raw-line">Shini translates complex cutting-edge science into accessible and captivating watchable content. Her recent work includes projects for the BBC, PBS Digital, Sprint Business and Dyson. Previously, Shini hosted TechKnow for Al Jazeera America as well as working for networks such as Sky, Discovery and The Science Channel.<br><br>​Dr. Somara is an advocate for STEM education, encouraging women and girls in particular, to empower themselves by studying these subjects.<br><br>Check out her BRAND NEW podcast called Scilence.  https://itunes.apple.com/us/podcast/scilence/id1404424249?mt=2<br><br>Her other loves include her meditation, nature, and chocolate.</span>

    info = {}
    info.update({"link":link})
    info.update({"Name":name})
    info.update({"Title":profile_title})
    info.update({"About / Summary":about})
    if photo_link.has_attr("src"):
        info.update({"Profile Photo":photo_link['src']})
    else:
        info.update({"Profile Photo":"Item not found"})
    info.update({"location":loc})
    info.update({"Connections":connection})
    #info

    exp_section = soup.find('section',id="experience-section")

    #print("num exps: ",len(exp_section))


    # Work History

    if exp_section is not None:

        exp_section = exp_section.find('ul')
        li_tags = exp_section.find('div')
        a_tags = li_tags.find('a')

        try:
            job_title = a_tags.find('h3').get_text().strip()
        except ValueError:
            job_title=" N/A"

        try:
            company_name = a_tags.find_all('p')[1].get_text().strip()
        except IndexError:
            company_name=" N/A"
        try:
            joining_date = a_tags.find_all('h4')[0].find_all('span')[1].get_text().strip()
        except IndexError:
            joining_date=" N/A"

        try:
            exp = a_tags.find_all('h4')[1].find_all('span')[1].get_text().strip()
        except IndexError:
            exp=" N/A"

        info.update({"Company Name/ Current Position":company_name})
        info.update({"Job Title":job_title})
        info.update({"Joining Date":joining_date})
        info.update({"Experince / Tenure":exp})
    else:
        info.update({"Experience ":"Item not found"})

    # Updated method

    # Work History

    # only take first element
    curr_company=soup.find_all('div',class_="pv-entity__summary-info pv-entity__summary-info--background-section")

    job_titles=soup.find_all('h3',class_="t-16 t-black t-bold")

    company_history=soup.find_all('p',class_="pv-entity__secondary-title t-14 t-black t-normal")

    job_detail=soup.find_all('p',class_="pv-entity__description t-14 t-black t-normal")

    past_work_history=soup.find_all('p',class_="pv-entity__summary-info pv-entity__summary-info--background-section mb2")

    multiple_roles_company_div=soup.find_all('div',class_="pv-entity__company-summary-info")

    # Education
    edsect=soup.find('section',id="education-section")

    if edsect!=None:
        schools=edsect.find_all('div',class_="pv-entity__degree-info")
        dts=edsect.find_all('div',class_="pv-entity__summary-info pv-entity__summary-info--background-section")
    else:
        schools=soup.find_all('div',class_="pv-entity__degree-info")
        dts=soup.find_all('div',class_="pv-entity__summary-info pv-entity__summary-info--background-section")

    schools_list=[]
    k=0

    for school in schools:
        sname=school.find('h3',class_="pv-entity__school-name t-16 t-black t-bold")

        degname=school.find('span',class_="pv-entity__comma-item")

        dates=dts[k].find_all('time')
        k+=1

        if sname!=None:
            sname=sname.text
        fieldofstudy=""
        if degname!=None:
            if len(degname)!=0:

                for el in degname:
                    fieldofstudy+=unidecode.unidecode(el.string)+", "

        attendance=""
        #print("length of dates field: ",len(dates))
        j=0
        if len(dates)>0:
            attendance=dates[0].text
            j=1
            while j<len(dates):
                attendance+=" - "+dates[j].text
                j+=1



        schools_list.append([sname,fieldofstudy,attendance])

    print('\n*********************\n')

    print("companies worked for: ",len(curr_company))
    i=0
    for comp in curr_company:
        #print("\n*\n",comp,"\n*\n")
        i+=1

    print("\n ####### \n")

    print("\n####\n past work experiences: ",len(past_work_history))

    for comp in past_work_history:
        #print("\n*\n",comp,"\n*\n")
        i+=1

    print("\n ####### \n")

    print("one company multiple roles worked for: ",len(multiple_roles_company_div))

    for comp in multiple_roles_company_div:
        #print("\n*\n",comp,"\n*\n")
        i+=1

    pjtls=[]
    for jt in job_titles:
        pjtls.append(jt.text)

    p_companies=[]

    for pcomp in company_history:
        cmp=pcomp.text.strip()
        cmp=cmp.split("\n")
        p_companies.append(cmp[0])

    job_details_list=[]

    for jd in job_detail:
        job_details_list.append(jd.text)

    print("Past job titles:  ",pjtls)

    print("Past companies: ",p_companies)

    print("Past job details ",len(job_detail)," :",job_details_list)

    # Temporary fields => will refine later

    info.update({"Past job titles":pjtls})
    info.update({"Past companies":p_companies})
    info.update({"Past job details":job_details_list})


    print("Schools: ",len(schools))
    for s in schools:
        print(s,"\n*****\n")

    print(schools_list)


    info.update({"Education History":schools_list})
    print('\n*********************\n')

    edu_section = soup.find('section', id="education-section")

    #
    #print("edu section ",edu_section)

    if edu_section is not None:
        edu_section=edu_section.find('ul')

    if edu_section is not None:
        college_name = edu_section.find('h3').get_text().strip()

        degree_name = edu_section.find('p', {'class': 'pv-entity__secondary-title pv-entity__degree-name t-14 t-black t-normal'})

        if(degree_name!=None):
            degree_name=degree_name.find_all('span')[1].get_text().strip()

        stream = edu_section.find('p', {'class': 'pv-entity__secondary-title pv-entity__fos t-14 t-black t-normal'})

        if(stream!=None):
            stream=stream.find_all('span')[1].get_text().strip()

        dates_obj= edu_section.find('p', {'class': 'pv-entity__dates t-14 t-black--light t-normal'})

        if dates_obj!=None:
            dates_obj=dates_obj.find_all('span')
            dates_obj=dates_obj[-1].find_all('time')

        degree_year='NA'
        if(dates_obj!=None):
            if(len(dates_obj)>1):
                degree_year=dates_obj[0].text+" - "+dates_obj[-1].text
            else:
                degree_year="not given"

        info.update({"College Name":college_name})
        info.update({"Degree":degree_name})
        info.update({"Major":stream})
        info.update({"Grad Year":degree_year})
    else:
        info.update({"Education ":"Item not found"})


    # fix bug later
    skills_section = soup.find_all('div', class_="skill-categories-expanded")

    if len(skills_section)>=0:
        print("*******\n Skills:\n")
        for skill in skills_section:
            print(skill)

        print("skills ******")
    else:
        print("**** no skills *******")


    # populating other field objects

    # author profile table object
    aprof={}
    aprof.update({"Link":link})
    aprof.update({"Name":name})
    aprof.update({"Title":profile_title})
    aprof.update({"About/Summary":about})
    aprof.update({"Email":"Not given"})
    aprof.update({"Profile Photo":info['Profile Photo']})
    aprof.update({"Connections":connection})
    aprof.update({"Location":loc})

    # education history
    edu_history=[]
    for s in info["Education History"]:
        ed_obj={}
        ed_obj.update({"School":s[0]})
        ed_obj.update({"Degree":s[1]})
        ed_obj.update({"Attend Dates":s[2]})
        edu_history.append(ed_obj)



    # past companies
    companies=[]
    for c in info["Past companies"]:
        comp={}
        comp.update({"Company Name":c})
        companies.append(comp)

    # update fields
    author_profiles.append(aprof)
    past_companies.append({name:companies})
    past_job_titles.append({name:pjtls})
    past_job_details.append({name:job_details_list})
    education_experience.append({name:edu_history})

    print("***   Final  ****\n")

    for item in info:
        print(item," : ",info[item],"\n")
    print(info)
    objects.append(info)

    print("****")

# Open JSON file, read objects and update new products
def export(export_path, l):
	print("## => Exporting", len(l), " products to JSON file")
	# Export to file
	"""
	f = open(export_path, "a+")
	f.write(json.dumps(l))
	f.write(",")
	f.close()
	"""

	# Export to file => Reverted to my old method
	f = open(export_path, "r")
	data =[]
	if(os.stat(export_path).st_size == 0):
		print("*** empty file")
	else:
		data= json.loads(f.read())
		#print("***  data : ",data)
	f.close()

	f = open(export_path, "w")

	for le in l:
		data.append(le)

	f.write(json.dumps(data, indent=2))

	f.close()

# Open JSON file, read objects and update new products
def exportList(export_path, l):
	print("## => Exporting", len(l), " products to JSON file")
	# Export to file

	# Export to file => Reverted to my old method
	f = open(export_path, "r")
	data =[]
	if(os.stat(export_path).st_size == 0):
		print("*** empty file")
	else:
		data= json.loads(f.read())
		#print("***  data : ",data)
	f.close()


	f = open(export_path, "w")

	for le in l:
		data.append(le)

	f.write(json.dumps(data, indent=2))

	f.close()

def exportDict(export_path, l):
	print("## => Exporting", len(l), " products to JSON file")
	# Export to file

	# Export to file => Reverted to my old method
	f = open(export_path, "r")
	data =[]
	if(os.stat(export_path).st_size == 0):
		print("*** empty file")
	else:
		data= json.loads(f.read())
		#print("***  data : ",data)
	f.close()


	f = open(export_path, "w")

	for le in l:
		data.append(le)

	f.write(json.dumps(data, indent=2))

	f.close()

#def exportDF(jsfile):

########### Test   ############

for link in urls:
    scrape(link)

#print(objects)

export(profiles,objects)
export(authors_json,author_profiles)
exportDict(companies_json,past_companies)
exportDict(author_jobhistory_json,past_job_details)
exportDict(authors_education_json,education_experience)

# close chrome tab
browser.close()
