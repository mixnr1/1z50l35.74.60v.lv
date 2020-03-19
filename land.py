import os
import re
import time
import smtplib, ssl
import config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
start = time.time()
start_tuple=time.localtime()
start_time = time.strftime("%Y-%m-%d %H:%M:%S", start_tuple)
def navigation_pages():
    try:
        navigator=driver.find_element_by_class_name('pagination')
        pages=navigator.find_elements_by_tag_name('a')
        not_sorted_links=[]
        for page in pages:
            link=page.get_attribute("href")
            pattern = re.compile("http[s]?://izsoles.ta.gov.lv/(?:[0-9]+)")
            if pattern.match(str(link)):
                not_sorted_links.append(link)
        return sorted(set(not_sorted_links))
    except NoSuchElementException:
        return []
#Using 'region_nr' you can specify the region which interest you. The ones that doesn't interest you can be simply comment out
regionu_nr=['7'#Rīga!!!!!!!!!!
            # '1',#Daugavpils
            # '2',#Jēkabpils
            # '3',#Jelgava
            # '4',#Jūrmala
            # '5',#Liepāja
            # '6',#Rēzekne
            # '8',#Valmiera!!!!!!!!!
            # '9',#Ventspils
            # '10',#Ādažu novads!!!!!!!!!!
            # '11',#Aglonas novads
            # '12',#Aizkraukles novads
            # '13',#Aizputes novads
            # '14',#Aknīstes novads
            # '15',#Alojas novads
            # '16',#Alsungas novads
            # '17',#Alūksnes novads
            # '18',#Amatas novads
            # '19',#Apes novads
            # '20',#Auces novads
            # '21',#Babītes novads
            # '22',#Baldones novads
            # '23',#Baltinavas novads
            # '24',#Balvu novads
            # '25',#Bauskas novads
            # '26',#Beverīnas novads
            # '27',#Brocēnu novads
            # '28',#Burtnieku novads
            # '29',#Carnikavas novads!!!!!!!!!!!!
            # '30',#Cēsu novads
            # '31',#Cesvaines novads
            # '32',#Ciblas novads
            # '33',#Dagdas novads
            # '34',#Daugavpils novads
            # '35',#Dobeles novads
            # '36',#Dundagas novads
            # '37',#Durbes novads
            # '38',#Engures novads
            # '39',#Ērgļu novads
            # '40',#Garkalnes novads!!!!!!!!!!!
            # '41',#Grobiņas novads
            # '42',#Gulbenes novads
            # '43',#Iecavas novads
            # '44'#Ikšķiles novads!!!!!!!!!!!
            # '45',#Ilūkstes novads
            # '46',#Inčukalna novads
            # '47',#Jaunjelgavas novads
            # '48',#Jaunpiebalgas novads
            # '49',#Jaunpils novads
            # '50',#Jēkabpils novads
            # '51',#Jelgavas novads
            # '52',#Kandavas novads
            # '53',#Kārsavas novads
            # '54',#Ķeguma novads
            # '55',#Ķekavas novads
            # '56',#Kocēnu novads
            # '57',#Kokneses novads
            # '58',#Krāslavas novads
            # '59',#Krimuldas novads
            # '60',#Krustpils novads
            # '61',#Kuldīgas novads
            # '62',#Lielvārdes novads
            # '63',#Līgatnes novads
            # '64',#Limbažu novads
            # '65',#Līvānu novads
            # '66',#Lubānas novads
            # '67',#Ludzas novads
            # '68',#Madonas novads
            # '69',#Mālpils novads
            # '70',#Mārupes novads
            # '71',#Mazsalacas novads
            # '72',#Mērsraga novads
            # '73',#Naukšēnu novads
            # '74',#Neretas novads
            # '75',#Nīcas novads
            # '76',#Ogres novads
            # '77',#Olaines novads
            # '78',#Ozolnieku novads
            # '79',#Pārgaujas novads
            # '80',#Pāvilostas novads
            # '81',#Pļaviņu novads
            # '82',#Preiļu novads
            # '83',#Priekules novads
            # '84',#Priekuļu novads
            # '85',#Raunas novads
            # '86',#Rēzeknes novads
            # '87',#Riebiņu novads
            # '88',#Rojas novads
            # '89',#Ropažu novads
            # '90',#Rucavas novads
            # '91',#Rugāju novads
            # '92',#Rūjienas novads
            # '93',#Rundāles novads
            # '94',#Salacgrīvas novads
            # '95',#Salas novads
            # '97',#Saldus novads
            # '98',#Saulkrastu novads
            # '99',#Sējas novads
            # '100',#Siguldas novads
            # '101',#Skrīveru novads
            # '102',#Skrundas novads
            # '103',#Smiltenes novads
            # '104',#Stopiņu novads
            # '105',#Strenču novads
            # '106',#Talsu novads
            # '107',#Tērvetes novads
            # '108',#Tukuma novads
            # '109',#Vaiņodes novads
            # '110',#Valkas novads
            # '111',#Varakļānu novads
            # '112',#Vārkavas novads
            # '113',#Vecpiebalgas novads
            # '114',#Vecumnieku novads
            # '115',#Ventspils novads
            # '116',#Viesītes novads
            # '117',#Viļakas novads
            # '118',#Viļānu novads
            # '119',#Zilupes novads
            # '120',#Ārzemes
            # '96'] #Salaspils!!!!!!!!!!!!
]

category_nr=['1',#Zeme / mežs
            # '2',#Ēkas
			# '3',#Dzīvokļi
			# '4',#Dažādi
            # '8',#Funkcionāli saistīti īpašumi
			# '17',#Telpas
			'18',#Ēkas un zeme
			# '20',#Dzīvojamās telpas
			# '21',#Reklāmas laukumi/brandmūri
            '19']#Zeme
path=config.path
HTML_text=[]
plain_text=[]
for reg in regionu_nr:
    driver=webdriver.Chrome()
    # driver.set_window_size(1920, 1080)
    driver.get('https://izsoles.ta.gov.lv/')
    time.sleep(2)  
    action = ActionChains(driver)
    firstLevelMenu = driver.find_element_by_xpath("/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/button/span[2]")
    action.move_to_element(firstLevelMenu).perform()
    firstLevelMenu.click()
    secondLevelMenu = driver.find_element_by_xpath("/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[8]/a/span[1]")
    action.move_to_element(secondLevelMenu).perform()
    secondLevelMenu.click()
    # driver.execute_script('document.getElementById("region").selectedIndex = '+ reg +';')
    #Next line returns selected value from dropdown menu
    print("Region:", Select(driver.find_element_by_id("region")).first_selected_option.get_attribute("value"))
    
    firstLevelMenu = driver.find_element_by_xpath("/html/body/div[3]/div[1]/form[2]/div[2]/div[2]/div/button/span[2]")
    action.move_to_element(firstLevelMenu).perform()
    firstLevelMenu.click()
    secondLevelMenu = driver.find_element_by_xpath("/html/body/div[3]/div[1]/form[2]/div[2]/div[2]/div/div/ul/li[2]/a/span[1]")
    action.move_to_element(secondLevelMenu).perform()
    secondLevelMenu.click()
    # driver.execute_script('document.getElementById("type").selectedIndex = 1;')#Nekustamie īpašumi
    #Next line returns selected value from dropdown menu
    print("Type:", Select(driver.find_element_by_id("type")).first_selected_option.get_attribute("value"))
    firstLevelMenu = driver.find_element_by_xpath("/html/body/div[3]/div[1]/form[2]/div[2]/div[3]/div/button/span[2]")
    action.move_to_element(firstLevelMenu).perform()
    firstLevelMenu.click()
    secondLevelMenu = driver.find_element_by_xpath("/html/body/div[3]/div[1]/form[2]/div[2]/div[3]/div/div/ul/li[2]/a/span[1]")
    action.move_to_element(secondLevelMenu).perform()
    secondLevelMenu.click()
    # driver.execute_script('document.getElementById("category").selectedIndex = 1;')
    #Next line returns selected value from dropdown menu
    print("Category:", Select(driver.find_element_by_id("category")).first_selected_option.get_attribute("value"))
    firstLevelMenu = driver.find_element_by_xpath("/html/body/div[3]/div[1]/form[2]/div[3]/div[3]/div/button/span[2]")
    action.move_to_element(firstLevelMenu).perform()
    firstLevelMenu.click()
    secondLevelMenu = driver.find_element_by_xpath("/html/body/div[3]/div[1]/form[2]/div[3]/div[3]/div/div/ul/li[1]/a/span[1]")
    action.move_to_element(secondLevelMenu).perform()
    secondLevelMenu.click()
    # driver.execute_script('document.getElementById("auction_state").value = "can_register";')#Var pieteikties
    #Next line returns selected value from dropdown menu
    print("Auction_state:", Select(driver.find_element_by_id("auction_state")).first_selected_option.get_attribute("value"))
    expand=driver.find_element_by_xpath('/html/body/div[3]/div[1]/form[2]/div[3]/div[4]/div/a/span[1]')
    expand.click()
    # platibamin=driver.find_element_by_xpath('//*[@id="area_from"]')
    # platibamin.send_keys('20')#Here you can set min area in square meters. If not needed comment out this line.
    # platibamax=driver.find_element_by_xpath('//*[@id="area_to"]')
    # platibamax.send_keys('98')#Here you can set max area in square meters. If not needed comment out this line.
    sakumcenamin=driver.find_element_by_xpath('//*[@id="start-price-from"]')
    sakumcenamin.send_keys('1000')#Here you can set the starting price. If not needed comment out this line.
    sakumcenamax=driver.find_element_by_xpath('//*[@id="start-price-to"]')
    sakumcenamax.send_keys('30000')#Here you can set the max price. If not needed comment out this line.
    novertejumsmin=driver.find_element_by_xpath('//*[@id="valuation-from"]')
    novertejumsmin.send_keys('1000')
    novertejumsmax=driver.find_element_by_xpath('//*[@id="valuation-to"]')
    novertejumsmax.send_keys('30000')
    search=driver.find_element_by_xpath('/html/body/div[3]/div[1]/form[2]/div[5]/div[2]/div/button')
    search.click()
    time.sleep(5)

    sorted_links=navigation_pages()
    if len(sorted_links)>0:
        try:
            parentElement=driver.find_element_by_xpath('/html/body/div[3]/table/tbody')
            count=0
            visi_linki=parentElement.find_elements_by_tag_name('a')
            for elem in visi_linki:
                count+=1
                e=elem.get_attribute("href")
                b=elem.get_attribute("text")
                sakumcena=parentElement.find_element_by_xpath(f'/html/body/div[3]/table/tbody/tr[{count}]/td[4]').text
                novertejums=parentElement.find_element_by_xpath(f'/html/body/div[3]/table/tbody/tr[{count}]/td[3]').text
                HTML_text.append(str('<tr><td><a href="'+e+'">'+b.replace("\t", "").replace("\n", "")+'</a></td><td>'+sakumcena+'</td><td>'+novertejums+'</td></tr>'))
                plain_text.append(str(e+" - "+b.replace('\t', '').replace('\n', '')))
            for next_page in sorted_links:
                driver.get(next_page)
                time.sleep(3)
                parentElement=driver.find_element_by_xpath('/html/body/div[3]/table/tbody')
                count=0
                visi_linki=parentElement.find_elements_by_tag_name('a')
                for elem in visi_linki:
                    count+=1
                    e=elem.get_attribute("href")
                    b=elem.get_attribute("text")
                    sakumcena=parentElement.find_element_by_xpath(f'/html/body/div[3]/table/tbody/tr[{count}]/td[4]').text
                    novertejums=parentElement.find_element_by_xpath(f'/html/body/div[3]/table/tbody/tr[{count}]/td[3]').text
                    HTML_text.append(str('<tr><td><a href="'+e+'">'+b.replace("\t", "").replace("\n", "")+'</a></td><td>'+sakumcena+'</td><td>'+novertejums+'</td></tr>'))
                    plain_text.append(str(e+" - "+b.replace('\t', '').replace('\n', '')))
            driver.close()
        except NoSuchElementException:
            driver.close()
            pass
    else:
        try:
            parentElement=driver.find_element_by_xpath('/html/body/div[3]/table/tbody')
            count=0
            visi_linki=parentElement.find_elements_by_tag_name('a')
            for elem in visi_linki:
                count+=1
                e=elem.get_attribute("href")
                b=elem.get_attribute("text")
                sakumcena=parentElement.find_element_by_xpath(f'/html/body/div[3]/table/tbody/tr[{count}]/td[4]').text
                novertejums=parentElement.find_element_by_xpath(f'/html/body/div[3]/table/tbody/tr[{count}]/td[3]').text
                HTML_text.append(str('<tr><td><a href="'+e+'">'+b.replace("\t", "").replace("\n", "")+'</a></td><td>'+sakumcena+'</td><td>'+novertejums+'</td></tr>'))
                plain_text.append(str(e+" - "+b.replace('\t', '').replace('\n', '')))
            driver.close()
        except NoSuchElementException:
            driver.close()
            pass
HTML_text_file=open(path+"/unique_links_HTML_land.txt", 'r').read().split('\n')
hdiff=[line for line in HTML_text if line not in HTML_text_file]#masīvs, kurā glabājas atrastās atšķirības
if len(hdiff) > 0:
    os.remove(path+"/unique_links_HTML_land.txt")
    HTML_text_file=open(path+"/unique_links_HTML_land.txt",'w')
    for elem in sorted(HTML_text):
        HTML_text_file.write(elem + '\n')
    HTML_text_file.close()
plain_text_file=open(path+"/unique_links_plain_land.txt", 'r').read().split('\n')
diff=[line for line in plain_text if line not in plain_text_file]#masīvs, kurā glabājas atrastās atšķirības
if len(diff) > 0:
    os.remove(path+"/unique_links_plain_land.txt")
    plain_text_file=open(path+"/unique_links_plain_land.txt",'w')
    for elem in sorted(plain_text):
        plain_text_file.write(elem + '\n')
    plain_text_file.close()

while True:
    if len(hdiff)==0:
        break
    if len(hdiff)>0:
        sender_email = config.sender_email
        receiver_email = config.receiver_email
        password = config.password
        message = MIMEMultipart("alternative")
        timestr = time.strftime("%d.%m.%Y-%H:%M:%S")
        message["Subject"] = "Izsoles jaunumi (zeme) "+timestr 
        message["From"] = sender_email
        message["To"] = receiver_email
        epasta_saturs="\n".join([(str(i).replace('\n', '')) for i in diff])
        plain=f"""{epasta_saturs}"""
        html = f"""\
        <html>
        <body>
            <table border='1' style='border-collapse:collapse'>
                <tr>
                    <th>Adrese</th>
                    <th>Sākumcena</th>
                    <th>Novērtējums</th>
                </tr>
                {" ".join(str(x) for x in hdiff)}
            </table>
        </body>
        </html>
        """
        part1 = MIMEText(plain, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
        break
end = time.time()
end_tuple = time.localtime()
end_time = time.strftime("%Y-%m-%d %H:%M:%S", end_tuple)
print("Script ended: "+end_time)
print("Script running time: "+time.strftime('%H:%M:%S', time.gmtime(end - start)))