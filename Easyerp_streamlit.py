from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep
from bs4 import BeautifulSoup
import streamlit as st 


def get_attendence_page_html(
        admission_id: int, 
        password: str | float,
        login_information_waiting_time: float | int = 0.5
    ) -> str :
    """
    Returns the HTML content of Attendence page.

    Args:
        admission_id (int): Admission number provide by University/College (i.e. 212413**)
        password (str | float): Your ERP(iimt.icloudems.com) password
    """
    
    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage") 

    # Create the WebDriver instance
    driver = webdriver.Chrome(
        options=chrome_options,
        service=Service(ChromeDriverManager().install())
    )

    # URLs
    login_url = "https://iimt.icloudems.com/corecampus/index.php"

    # Step 1: Open the login page
    driver.get(login_url)

    # Step 2: Find login elements and enter credentials
    admission_input = driver.find_element(By.NAME, "userid")  # Adjust selector if needed
    password_input = driver.find_element(By.NAME, "pass_word")  # Adjust selector if needed

    # Replace with actual credentials
    admission_input.send_keys(admission_id)
    password_input.send_keys(password)

    sleep(login_information_waiting_time)

    # Submit the form
    password_input.send_keys(Keys.RETURN)

    # clicking on 'Attendence Link'
    driver.find_element(By.XPATH, "//a[contains(@href, 'attendance/subwise_attendace_new.php')]").click()

    page_source = driver.page_source

    driver.close()

    return page_source



def display_attendence():
    page_source = get_attendence_page_html(admission_id, password)
    
    # creating an object of Beautiful Soup class 
    soup = BeautifulSoup(page_source, 'html.parser')

    # Extracting Total attendence percentage form attendence page's soure
    total_attendence = soup.find_all('tr')[-1].find_all('td')[-1].text 
    
    data = {
        'admission_id': admission_id,
        'total_attendence': total_attendence
    }

    st.write(data)


def main():
    global admission_id, password

    st.title("Easy ERP")
    admission_id = st.number_input(
        "Admission number",
        placeholder="example: 2123XXXX",
        value=21231320
    )

    password = st.text_input(
        "ERP password",
        placeholder="password ",
        value="#Iimt23@Bxyz"
    )

    st.button(
        "Get my attendence",
        on_click = display_attendence
    )
    

if __name__ == "__main__":
    main()



