import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from helpers.colors import colors
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidSelectorException
load_dotenv()


class contest:
    def __init__(self,url,contests,id):
        self.url = url
        self.contests = contests
        self.id = id


class problem:
    def __init__(self,Name,id):
        self.name=Name
        self.id=id

curr_contests = []
contests_vis = {}
contests_prob = {}
# Create chrome driver
def createDriver():
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=chrome_options, service=chrome_service)
    return driver


# make timeout 30 seconds for command find element
def find_element(driver, by, value, timeout=40):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, value)), f'{colors.red}Timeout while trying to reach an element ❌{colors.reset}')

def check_valid_int(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

def check_exists_by_xpath(xpath,driver):
    try:
        driver.find_element("xpath",xpath)
    except NoSuchElementException:
        return False
    except InvalidSelectorException:
        return False
    return True


def check_valid_code(driver,code):
    driver.get("https://codeforces.com/contests/"+code)

    if check_exists_by_xpath('//*[@id="pageContent"]/div[1]/div[1]/div/div[5]',driver):
        return True
    else:
        return False
    

def add_contest(driver,links_file):
    print("Enter the code of contests you want to add: ")
    code=""
    while True:
        code = input()
        if check_valid_int(code) and check_valid_code(driver,code):
            # links_file.write(code + "\n")
            print("Contest added successfully ✅")
            break
        else:
            print("Invalid code ❌\n try again : ")
    contests_vis[code] = True
    contests_prob[code] = []
    print(find_element(driver,By.XPATH,'//*[@id="pageContent"]/div[1]/div[1]/div/div[5]').text + "\n")
    find_element(driver,By.XPATH,'//*[@id="pageContent"]/div[1]/div[1]/div/div[6]/table/tbody/tr[2]/td[1]/a').click()
    element = find_element(driver,By.XPATH,'//*[@id="pageContent"]/div[2]/div[6]/table')
    # //*[@id="pageContent"]/div[2]/div[6]/table/tbody/tr[3]/td[1]   //*[@id="pageContent"]/div[2]/div[6]/table/tbody/tr[2]/td[1]
    tr=2
    td=1
    problems = []
    while check_exists_by_xpath(f'//*[@id="pageContent"]/div[2]/div[6]/table/tbody/tr[{tr}]',driver) :
        problem_name = find_element(driver,By.XPATH,f'//*[@id="pageContent"]/div[2]/div[6]/table/tbody/tr[{tr}]/td[2]/div/div[1]/a').text
        problem_id = find_element(driver,By.XPATH,f'//*[@id="pageContent"]/div[2]/div[6]/table/tbody/tr[{tr}]/td[1]/a').text
        new_proplem = problem(problem_name,problem_id)
        problems.append(new_proplem)
        tr+=1
    
    for prob in problems:
        print(prob.id + " " + prob.name)
    
    print("Enter the id of problems you want to add after you finish type -1: ")
    while True:
        id = input()
        if id == "-1":
            break
        flag = 1
        for prob in problems:
            if prob.id == id :
                if prob.id in contests_prob[code]:
                    print("Problem already added ❌ try again :")
                    break
                contests_prob[code].append(id)
                print("Problem added successfully ✅")
                flag = 0
                break
        if flag == 1:
            print("Invalid id ❌\n try again : ")
    
    # for prob in contests_prob[code]:
    #     print(prob)

    


def write_links(links_file):
    for contest in curr_contests:
        links_file.write(contest.id + " {\n")
        for [contest,problems] in contests_prob.items():
            links_file.write(contest + " :")
            for problem in problems:
                links_file.write(problem + " ")
            links_file.write("\n")
        links_file.write("}\n")



def read_links(links_file):
    
    

def startup(driver,links_file):
    Handle = os.getenv('CF_HANDEL')
    Password = os.getenv('CF_PASS')
    driver.get('https://codeforces.com/enter?back=%2F%3Ff0a28%3D1')
    find_element(driver,By.XPATH,'//*[@id="handleOrEmail"]').send_keys(Handle)
    find_element(driver,By.XPATH,'//*[@id="password"]').send_keys(Password)
    find_element(driver,By.XPATH,' //*[@id="enterForm"]/table/tbody/tr[4]/td/div[1]/input').click()
    time.sleep(1)
    read_links(links_file)


def shutdown(driver,links_file):
    driver.quit()
    write_links(links_file)
    read_links(links_file)


def main() :
    
    links_file = open("links.txt", "a+") 
    driver = createDriver()
    startup(driver)
    print("Welcome to contest maker 🎉")

    while True:
        print("choose one of the following options: ")
        print("1- Add contest")
        print("2- Remove contest")
        print("3- Exit")
        choice = input()
        if choice == "1":
            add_contest(driver,links_file)
        if choice == "3":
            break
        

    shutdown(driver,links_file)

    
    
    

if __name__ == "__main__":
    main()