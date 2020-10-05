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
from selenium.webdriver.chrome.options import Options

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

category_dic={
    'Visas_kategorijas':'/html/body/div[3]/div[2]/form[2]/div[2]/div[4]/div/div/ul/li[1]/a/span[1]',
    'Transportlīdzekļi':'/html/body/div[3]/div[2]/form[2]/div[2]/div[4]/div/div/ul/li[2]/a/span[1]',
    'Cita_kustamā_manta':'/html/body/div[3]/div[2]/form[2]/div[2]/div[4]/div/div/ul/li[3]/a/span[1]',
    'Kuģi_un_peldošās_konstrukcijas_kas_reģistrētas_Kuģu_reģistrā':'/html/body/div[3]/div[2]/form[2]/div[2]/div[4]/div/div/ul/li[4]/a/span[1]',
    'Apbūves_tiesības':'/html/body/div[3]/div[2]/form[2]/div[2]/div[4]/div/div/ul/li[5]/a/span[1]',
    'Pamatkapitāla_daļas_akcijas_pajas_vērtspapīri':'/html/body/div[3]/div[2]/form[2]/div[2]/div[4]/div/div/ul/li[6]/a/span[1]',
    'Dārgmetāli_un_vērtslietas':'/html/body/div[3]/div[2]/form[2]/div[2]/div[4]/div/div/ul/li[7]/a/span[1]',
    'Dzīvnieki':'/html/body/div[3]/div[2]/form[2]/div[2]/div[4]/div/div/ul/li[8]/a/span[1]'
    }

path=config.path
HTML_text=[]
plain_text=[]

for key, value in category_dic.items():
    if key == "Transportlīdzekļi":
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://izsoles.ta.gov.lv/')
        time.sleep(2)
        action = ActionChains(driver)
        #Type selection
        firstLevelMenu = driver.find_element_by_xpath("/html/body/div[3]/div[2]/form[2]/div[2]/div[3]/div/button/span[2]")
        action.move_to_element(firstLevelMenu).perform()
        firstLevelMenu.click()
        secondLevelMenu = driver.find_element_by_xpath("/html/body/div[3]/div[2]/form[2]/div[2]/div[3]/div/div/ul/li[3]/a/span[1]")#Kustamā_manata
        action.move_to_element(secondLevelMenu).perform()
        secondLevelMenu.click()

        #Auction_state selection
        firstLevelMenu = driver.find_element_by_xpath("/html/body/div[3]/div[2]/form[2]/div[3]/div[3]/div/button/span[2]")
        action.move_to_element(firstLevelMenu).perform()
        firstLevelMenu.click()
        secondLevelMenu = driver.find_element_by_xpath("/html/body/div[3]/div[2]/form[2]/div[3]/div[3]/div/div/ul/li[1]/a/span[1]")
        action.move_to_element(secondLevelMenu).perform()
        secondLevelMenu.click()
        
        #Category selection
        firstLevelMenu = driver.find_element_by_xpath("/html/body/div[3]/div[2]/form[2]/div[2]/div[4]/div/button/span[2]")
        action.move_to_element(firstLevelMenu).perform()
        firstLevelMenu.click()
        secondLevelMenu = driver.find_element_by_xpath(value)
        action.move_to_element(secondLevelMenu).perform()
        secondLevelMenu.click()
        
        #Expand button
        expand=driver.find_element_by_xpath('/html/body/div[3]/div[2]/form[2]/div[3]/div[4]/div/a/span[1]')
        expand.click()
        sakumcenamin=driver.find_element_by_xpath('//*[@id="start-price-from"]')
        sakumcenamin.send_keys('1000')#Here you can set the starting price. If not needed comment out this line.
        sakumcenamax=driver.find_element_by_xpath('//*[@id="start-price-to"]')
        sakumcenamax.send_keys('8000')#Here you can set the max price. If not needed comment out this line.
        # novertejumsmin=driver.find_element_by_xpath('//*[@id="valuation-from"]')
        # novertejumsmin.send_keys('1000')
        # novertejumsmax=driver.find_element_by_xpath('//*[@id="valuation-to"]')
        # novertejumsmax.send_keys('10000')
        
        #Search button
        search=driver.find_element_by_xpath('/html/body/div[3]/div[2]/form[2]/div[5]/div[4]/div/button')
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
                    time.sleep(2)
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
                driver.quit()
            except NoSuchElementException:
                driver.quit()
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
                driver.quit()
            except NoSuchElementException:
                driver.quit()
                pass

HTML_text_file=open(path+"/unique_links_HTML_auto.txt", 'r').read().split('\n')
hdiff=[line for line in HTML_text if line not in HTML_text_file]#masīvs, kurā glabājas atrastās atšķirības
if len(hdiff) > 0:
    os.remove(path+"/unique_links_HTML_auto.txt")
    HTML_text_file=open(path+"/unique_links_HTML_auto.txt",'w')
    for elem in sorted(HTML_text):
        HTML_text_file.write(elem + '\n')
    HTML_text_file.close()
plain_text_file=open(path+"/unique_links_plain_auto.txt", 'r').read().split('\n')
diff=[line for line in plain_text if line not in plain_text_file]#masīvs, kurā glabājas atrastās atšķirības

if len(diff) > 0:
    os.remove(path+"/unique_links_plain_auto.txt")
    plain_text_file=open(path+"/unique_links_plain_auto.txt",'w')
    for elem in sorted(plain_text):
        plain_text_file.write(elem + '\n')
    plain_text_file.close()

while True:
    if len(hdiff)==0:
        break
    if len(hdiff)>0:
        sender_email = config.sender_email
        receiver_email = config.auto_receiver_email
        password = config.password
        message = MIMEMultipart("alternative")
        timestr = time.strftime("%d.%m.%Y-%H:%M:%S")
        message["Subject"] = "AUTO IZSOLES "+timestr 
        message["From"] = sender_email
        message["To"] = receiver_email
        epasta_saturs="\n".join([(str(i).replace('\n', '')) for i in diff])
        plain=f"""{epasta_saturs}"""
        html = f"""\
        <html>
        <body>
            <table border='1' style='border-collapse:collapse'>
                <tr>
                    <th>Sludinājuma virsraksts</th>
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