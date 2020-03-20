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

regionu_dic={
    'Daugavpils':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[2]/a/span[1]',
    'Jēkabpils':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[3]/a/span[1]',
    'Jelgava':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[4]/a/span[1]',
    'Jūrmala':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[5]/a/span[1]',
    'Liepāja':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[6]/a/span[1]',
    'Rēzekne':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[7]/a/span[1]',
    'Rīga':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[8]/a/span[1]',
    'Valmiera':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[9]/a/span[1]',
    'Ventspils':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[10]/a/span[1]',
    'Ādažu_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[11]/a/span[1]',
    'Aglonas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[12]/a/span[1]',
    'Aizkraukles_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[13]/a/span[1]',
    'Aizputes_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[14]/a/span[1]',
    'Aknīstes_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[15]/a/span[1]',
    'Alojas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[16]/a/span[1]',
    'Alsungas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[17]/a/span[1]',
    'Alūksnes_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[18]/a/span[1]',
    'Amatas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[19]/a/span[1]',
    'Apes_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[20]/a/span[1]',
    'Auces_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[21]/a/span[1]',
    'Babītes_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[22]/a/span[1]',
    'Baldones_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[23]/a/span[1]',
    'Baltinavas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[24]/a/span[1]',
    'Balvu_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[25]/a/span[1]',
    'Bauskas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[26]/a/span[1]',
    'Beverīnas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[27]/a/span[1]',
    'Brocēnu_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[28]/a/span[1]',
    'Burtnieku_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[29]/a/span[1]',
    'Carnikavas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[30]/a/span[1]',
    'Cēsu_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[31]/a/span[1]',
    'Cesvaines_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[32]/a/span[1]',
    'Ciblas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[33]/a/span[1]',
    'Dagdas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[34]/a/span[1]',
    'Daugavpils_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[35]/a/span[1]',
    'Dobeles_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[36]/a/span[1]',
    'Dundagas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[37]/a/span[1]',
    'Durbes_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[38]/a/span[1]',
    'Engures_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[39]/a/span[1]',
    'Ērgļu_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[40]/a/span[1]',
    'Garkalnes_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[41]/a/span[1]',
    'Grobiņas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[42]/a/span[1]',
    'Gulbenes_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[43]/a/span[1]',
    'Iecavas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[44]/a/span[1]',
    'Ikšķiles_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[45]/a/span[1]',
    'Ilūkstes_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[46]/a/span[1]',
    'Inčukalna_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[47]/a/span[1]',
    'Jaunjelgavas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[48]/a/span[1]',
    'Jaunpiebalgas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[49]/a/span[1]',
    'Jaunpils_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[50]/a/span[1]',
    'Jēkabpils_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[51]/a/span[1]',
    'Jelgavas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[52]/a/span[1]',
    'Kandavas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[53]/a/span[1]',
    'Kārsavas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[54]/a/span[1]',
    'Ķeguma_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[55]/a/span[1]',
    'Ķekavas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[56]/a/span[1]',
    'Kocēnu_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[57]/a/span[1]',
    'Kokneses_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[58]/a/span[1]',
    'Krāslavas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[59]/a/span[1]',
    'Krimuldas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[60]/a/span[1]',
    'Krustpils_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[61]/a/span[1]',
    'Kuldīgas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[62]/a/span[1]',
    'Lielvārdes_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[63]/a/span[1]',
    'Līgatnes_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[64]/a/span[1]',
    'Limbažu_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[65]/a/span[1]',
    'Līvānu_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[66]/a/span[1]',
    'Lubānas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[67]/a/span[1]',
    'Ludzas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[68]/a/span[1]',
    'Madonas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[69]/a/span[1]',
    'Mālpils_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[70]/a/span[1]',
    'Mārupes_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[71]/a/span[1]',
    'Mazsalacas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[72]/a/span[1]',
    'Mērsraga_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[73]/a/span[1]',
    'Naukšēnu_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[74]/a/span[1]',
    'Neretas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[75]/a/span[1]',
    'Nīcas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[76]/a/span[1]',
    'Ogres_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[77]/a/span[1]',
    'Olaines_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[78]/a/span[1]',
    'Ozolnieku_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[79]/a/span[1]',
    'Pārgaujas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[80]/a/span[1]',
    'Pāvilostas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[81]/a/span[1]',
    'Pļaviņu_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[82]/a/span[1]',
    'Preiļu_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[83]/a/span[1]',
    'Priekules_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[84]/a/span[1]',
    'Priekuļu_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[85]/a/span[1]',
    'Raunas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[86]/a/span[1]',
    'Rēzeknes_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[87]/a/span[1]',
    'Riebiņu_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[88]/a/span[1]',
    'Rojas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[89]/a/span[1]',
    'Ropažu_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[90]/a/span[1]',
    'Rucavas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[91]/a/span[1]',
    'Rugāju_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[92]/a/span[1]',
    'Rūjienas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[93]/a/span[1]',
    'Rundāles_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[94]/a/span[1]',
    'Salacgrīvas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[95]/a/span[1]',
    'Salas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[96]/a/span[1]',
    'Salaspils_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[97]/a/span[1]',
    'Saldus_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[98]/a/span[1]',
    'Saulkrastu_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[99]/a/span[1]',
    'Sējas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[100]/a/span[1]',
    'Siguldas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[101]/a/span[1]',
    'Skrīveru_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[102]/a/span[1]',
    'Skrundas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[103]/a/span[1]',
    'Smiltenes_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[104]/a/span[1]',
    'Stopiņu_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[105]/a/span[1]',
    'Strenču_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[106]/a/span[1]',
    'Talsu_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[107]/a/span[1]',
    'Tērvetes_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[108]/a/span[1]',
    'Tukuma_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[109]/a/span[1]',
    'Vaiņodes_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[110]/a/span[1]',
    'Valkas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[111]/a/span[1]',
    'Varakļānu_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[112]/a/span[1]',
    'Vārkavas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[113]/a/span[1]',
    'Vecpiebalgas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[114]/a/span[1]',
    'Vecumnieku_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[115]/a/span[1]',
    'Ventspils_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[116]/a/span[1]',
    'Viesītes_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[117]/a/span[1]',
    'Viļakas_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[118]/a/span[1]',
    'Viļānu_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[119]/a/span[1]',
    'Zilupes_novads':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[120]/a/span[1]',
    'Ārzemes':'/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/div/ul/li[121]/a/span[1]'
}
category_dic={
    'Zeme/mežs':'/html/body/div[3]/div[1]/form[2]/div[2]/div[3]/div/div/ul/li[2]/a/span[1]', #Zeme / mežs
    'Ēkas':'/html/body/div[3]/div[1]/form[2]/div[2]/div[3]/div/div/ul/li[3]/a/span[1]', #Ēkas
	'Dzīvokļi':'/html/body/div[3]/div[1]/form[2]/div[2]/div[3]/div/div/ul/li[4]/a/span[1]',#Dzīvokļi
	'Dažādi':'/html/body/div[3]/div[1]/form[2]/div[2]/div[3]/div/div/ul/li[5]/a/span[1]',#Dažādi
    'Funkcionāli_saistīti_īpašumi':'/html/body/div[3]/div[1]/form[2]/div[2]/div[3]/div/div/ul/li[6]/a/span[1]',#Funkcionāli saistīti īpašumi
	'Telpas':'/html/body/div[3]/div[1]/form[2]/div[2]/div[3]/div/div/ul/li[7]/a/span[1]',#Telpas
	'Ēkas_un_zeme':'/html/body/div[3]/div[1]/form[2]/div[2]/div[3]/div/div/ul/li[8]/a/span[1]',#Ēkas un zeme
	'Dzīvojamās_telpas':'/html/body/div[3]/div[1]/form[2]/div[2]/div[3]/div/div/ul/li[10]/a/span[1]',#Dzīvojamās telpas
	'Reklāmas_laukumi/brandmūri':'/html/body/div[3]/div[1]/form[2]/div[2]/div[3]/div/div/ul/li[11]/a/span[1]',#Reklāmas laukumi/brandmūri
    'Zeme':'/html/body/div[3]/div[1]/form[2]/div[2]/div[3]/div/div/ul/li[9]/a/span[1]'}#Zeme

path=config.path
HTML_text=[]
plain_text=[]
for xkey, xvalue in regionu_dic.items():
    if xkey == "Rīga" or xkey == "Ikšķiles_novads":
        for key, value in category_dic.items():
            if key == "Zeme/mežs" or key == "Dzīvokļi":
                driver=webdriver.Chrome()
                driver.get('https://izsoles.ta.gov.lv/')
                time.sleep(2)
                action = ActionChains(driver)
                #Region selection
                firstLevelMenu = driver.find_element_by_xpath("/html/body/div[3]/div[1]/form[2]/div[2]/div[1]/div/button/span[2]")
                action.move_to_element(firstLevelMenu).perform()
                firstLevelMenu.click()
                secondLevelMenu = driver.find_element_by_xpath(xvalue)
                action.move_to_element(secondLevelMenu).perform()
                secondLevelMenu.click()
            
                #Type selection
                firstLevelMenu = driver.find_element_by_xpath("/html/body/div[3]/div[1]/form[2]/div[2]/div[2]/div/button/span[2]")
                action.move_to_element(firstLevelMenu).perform()
                firstLevelMenu.click()
                secondLevelMenu = driver.find_element_by_xpath("/html/body/div[3]/div[1]/form[2]/div[2]/div[2]/div/div/ul/li[2]/a/span[1]")
                action.move_to_element(secondLevelMenu).perform()
                secondLevelMenu.click()

                #Auction_state selection
                firstLevelMenu = driver.find_element_by_xpath("/html/body/div[3]/div[1]/form[2]/div[3]/div[3]/div/button/span[2]")
                action.move_to_element(firstLevelMenu).perform()
                firstLevelMenu.click()
                secondLevelMenu = driver.find_element_by_xpath("/html/body/div[3]/div[1]/form[2]/div[3]/div[3]/div/div/ul/li[1]/a/span[1]")
                action.move_to_element(secondLevelMenu).perform()
                secondLevelMenu.click()
                
                #Category selection
                firstLevelMenu = driver.find_element_by_xpath("/html/body/div[3]/div[1]/form[2]/div[2]/div[3]/div/button/span[2]")
                action.move_to_element(firstLevelMenu).perform()
                firstLevelMenu.click()
                secondLevelMenu = driver.find_element_by_xpath(value)
                action.move_to_element(secondLevelMenu).perform()
                secondLevelMenu.click()
                
                #Expand button
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
                
                #Search button
                search=driver.find_element_by_xpath('/html/body/div[3]/div[1]/form[2]/div[5]/div[2]/div/button')
                search.click()
                time.sleep(2)
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
        message["Subject"] = "Izsoles jaunumi "+timestr 
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