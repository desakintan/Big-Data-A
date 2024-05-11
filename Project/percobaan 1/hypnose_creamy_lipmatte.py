from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import pandas as pd
from time import sleep

driver = webdriver.Chrome()

def loaded_page(self, element):
    global myElem
    delay = 5
    try:
        myElem = WebDriverWait(self, delay).until(EC.presence_of_element_located((By.XPATH, element)))
    except TimeoutException:
        print('Loading too much time')

    return myElem


def get_ulasan():
    ulasan_list = []  # Inisialisasi daftar untuk menyimpan data ulasan

    i = 1
    review_count = 0
    count = loaded_page(driver, f'//*[@id="zeus-root"]/div/main/div[2]/div[1]/div[2]/section/div[2]/div/p').text   
    count = int(count.split(" ")[-2])
    print(count)
    while i <= 50:
        try:
            nama_akun = loaded_page(driver, f'//*[@id="review-feed"]/article[{i}]/div/div[2]/span').text
            ulasan_produk_element = driver.find_element(By.XPATH,f'//*[@id="review-feed"]/article[{i}]/div/p[2]/button')
            ulasan_produk_element.click()
            ulasan_produk = loaded_page(driver, f'//*[@id="review-feed"]/article[{i}]/div/p/span').text
        except NoSuchElementException:
            ulasan_produk = loaded_page(driver, f'//*[@id="review-feed"]/article[{i}]/div/p/span').text

        review_count += 1
        print(f'Review {review_count}: {nama_akun}, {ulasan_produk}')
        
        # Menambahkan data ulasan ke dalam daftar
        ulasan_list.append({"Nama Akun": nama_akun, "Ulasan": ulasan_produk})
        
        if review_count == count:
            print('Scrapping selesai')
            break

        i += 1
        
        if i > 50:
            button_next = loaded_page(driver, f'//*[@id="zeus-root"]/div/main/div[2]/div[1]/div[2]/section/div[3]/nav/ul/li[11]/button')
            button_next.click()
            sleep(3)
            i = 1

    # Mengonversi daftar ulasan ke dalam DataFrame menggunakan pandas
    df = pd.DataFrame(ulasan_list)
    
    # Menyimpan DataFrame ke dalam file CSV
    file_path = "hypnose_creamy_lipmatte.csv"
    df.to_csv(file_path, index=False)

    print(f"Ulasan produk berhasil disimpan ke dalam file: {file_path}")


def load_ulasan():
    batas = loaded_page(driver, '//*[@id="pdp_comp-product_detail_media"]')
    driver.execute_script("arguments[0].scrollIntoView();", batas)
    sleep(3)

    loadmore = loaded_page(driver,'//*[@id="pdp_comp-review"]/div/div/section/div[3]/a')
    loadmore.click()
    sleep(3)

    get_ulasan()

def main():
    driver.get(f'https://www.tokopedia.com/officialmakeover/make-over-color-hypnose-creamy-lipmatte-4-3-g-lipstick-07-temptation?extParam=ivf%3Dtrue%26src%3Dsearch')
    sleep(5)
    
    nama_product = loaded_page(driver, '//*[@id="pdp_comp-product_content"]/div/h1').text
    print(nama_product)
    sleep(5)

    load_ulasan()

if __name__ == "__main__":
    main()