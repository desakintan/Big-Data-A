import csv
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.alert import Alert
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
    reviews = []
    i = 1
    review_count = 0
    count = 500
    print(count)
    while i <= 50:
        try:
            nama_akun = loaded_page(driver, f'//*[@id="review-feed"]/article[{i}]/div/div[2]/span').text
            elemen_div = driver.find_element(By.XPATH, '//*[@id="review-feed"]/article[1]/div/div[1]/div/div')

            # Dapatkan nilai dari atribut aria-label
            rating_user_element = driver.find_element(By.XPATH, f'//*[@id="review-feed"]/article[{i}]/div/div[1]/div/div')
            rating_user = rating_user_element.get_attribute('aria-label')

            ulasan_produk_element = driver.find_element(By.XPATH,f'//*[@id="review-feed"]/article[{i}]/div/p[2]/button')

            ulasan_produk_element.click()
            ulasan_produk = loaded_page(driver, f'//*[@id="review-feed"]/article[{i}]/div/p/span').text
        except NoSuchElementException:
            ulasan_produk = loaded_page(driver, f'//*[@id="review-feed"]/article[{i}]/div/p/span').text

        review_count += 1
        print(f'Review {review_count}: {nama_akun}, {rating_user}, {ulasan_produk}')
        
        # Append review to list
        reviews.append({
            'Nama Akun': nama_akun,
            'Rating Pengguna': rating_user,
            'Ulasan Produk': ulasan_produk
        })
        
        if review_count == count:
            break

        i += 1
        
        if i > 50:
            button_next = loaded_page(driver, f'//*[@id="zeus-root"]/div/main/div[2]/div[1]/div[2]/section/div[3]/nav/ul/li[11]/button')
            button_next.click()
            sleep(3)
            i = 1

    return reviews

def load_ulasan():
    batas = loaded_page(driver, '//*[@id="pdp_comp-product_detail_media"]')
    driver.execute_script("arguments[0].scrollIntoView();", batas)
    sleep(5)

    loadmore = loaded_page(driver,'//*[@id="pdp_comp-review"]/div/div/section/div[3]/a')
    loadmore.click()
    sleep(5)

    reviews = get_ulasan()

    sleep(5)
    print('Scrapping selesai')

    return reviews

def get_produkinfo(url_name):
    driver.get(url_name)

    nama_produk = loaded_page(driver, '//*[@id="pdp_comp-product_content"]/div/h1').text

    jumlah_produk = loaded_page(driver, '//*[@id="pdp_comp-product_content"]/div/div[1]/div/p[1]').text

    try:
        harrgajual_produk_element = driver.find_element(By.XPATH,'//*[@id="pdp_comp-product_content"]/div/div[2]/div[2]')
        hargajual_produk = loaded_page(driver, '//*[@id="pdp_comp-product_content"]/div/div[2]/div[1]').text
    except NoSuchElementException:
        hargajual_produk = loaded_page(driver, '//*[@id="pdp_comp-product_content"]/div/div[2]/div').text

    try:
        rating_produk_element = driver.find_element(By.XPATH,'//*[@id="pdp_comp-product_content"]/div/div[1]/div/p[1]')
        rating_produk = loaded_page(driver, '//*[@id="pdp_comp-product_content"]/div/div[1]/div/p[2]/span[1]/span[2]').text
    except NoSuchElementException:
        rating_produk = 0

    print(f'Nama Produk: {nama_produk}, Jumlah Produk: {jumlah_produk}, Harga Jual: {hargajual_produk}, Rating Produk: {rating_produk}')
    
    product_info = {
        'Nama Produk': nama_produk,
        'Jumlah Produk': jumlah_produk,
        'Harga Jual': hargajual_produk,
        'Rating Produk': rating_produk
    }

    reviews = load_ulasan()

    return product_info, reviews

def main():
    urls = [
        "https://www.tokopedia.com/officialmakeover/make-over-powerstay-24h-matte-powder-foundation-w22-warm-ivory",
        "https://www.tokopedia.com/officialmakeover/make-over-color-stick-matte-crayon-2-6-g-lip-crayon-105-skye",
        "https://www.tokopedia.com/officialmakeover/make-over-hydrastay-smooth-lip-whip-6-5-g-lip-cream-c11-suave",
        "https://www.tokopedia.com/officialmakeover/make-over-powerstay-24h-weightless-liquid-foundation-40ml-foundation-w22-warm-ivory",
        "https://www.tokopedia.com/officialmakeover/make-over-powerstay-transferproof-matte-lip-cream-7-g-lip-cream-b03-hype",
        "https://www.tokopedia.com/officialmakeover/make-over-powerstay-glazed-lock-lip-pigment-d11-pompous-2-0",
        "https://www.tokopedia.com/officialmakeover/make-over-silky-smooth-translucent-powder-35-g-bedak-tabur-01-porcelain",
        "https://www.tokopedia.com/officialmakeover/make-over-color-hypnose-creamy-lipmatte-4-3-g-lipstick-07-temptation",
        "https://www.tokopedia.com/officialmakeover/make-over-hydrastay-lite-glow-cushion-15-g-cushion-for-dry-skin-c11-pink-marble-34114",
        "https://www.tokopedia.com/officialmakeover/make-over-powerstay-fix-matte-makeup-setting-spray-50-ml", 
        "https://www.tokopedia.com/officialmakeover/make-over-powerstay-total-cover-liquid-concealer-6-5-ml-02-light-to-med", 
        "https://www.tokopedia.com/officialmakeover/make-over-cliquematte-lip-stylo-2-g-lipstick-matte-205-jetsetter", 
        "https://www.tokopedia.com/officialmakeover/make-over-trivia-eye-shadow-6-g-eye-shadow-palette-dolly-crush", 
        "https://www.tokopedia.com/officialmakeover/make-over-hydrastay-radiant-finishing-powder-8-g-bedak-tabur", 
        "https://www.tokopedia.com/officialmakeover/make-over-trivia-eye-shadow-6-g-eye-shadow-palette-skycrapping-blu", 
        "https://www.tokopedia.com/officialmakeover/make-over-blush-on-single-6-g-blush-on-03-prom-peach",
        "https://www.tokopedia.com/officialmakeover/make-over-multifix-matte-blusher-9-g-blush-on-stick-02-quickpinker", 
        "https://www.tokopedia.com/officialmakeover/make-over-velvet-mattifying-primer-20-ml-makeup-primer",
        "https://www.tokopedia.com/officialmakeover/make-over-powerstay-demi-matte-cover-cushion-15-g-c11-pink-marble-b04a0",
        "https://www.tokopedia.com/officialmakeover/make-over-perfect-cover-refill-twc-12-g-bedak-padat-03-maple",
        "https://www.tokopedia.com/officialmakeover/make-over-eye-liner-pencil-1-2-g-eye-liner-black-jack",
        "https://www.tokopedia.com/officialmakeover/make-over-eyebrow-pencil-1-14-g-eye-brow-pencil-black-lines"
    ]

    for url in urls:
        product_info, reviews = get_produkinfo(url)  
        write_to_csv(product_info, reviews)

def write_to_csv(product_info, reviews):
    with open(f'{product_info['Nama Produk']}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Nama Produk', 'Jumlah Produk', 'Harga Jual', 'Rating Produk', 'Nama Akun', 'Rating Pengguna', 'Ulasan Produk']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()

        for review in reviews:
            row = {
                'Nama Produk': product_info['Nama Produk'],
                'Jumlah Produk': product_info['Jumlah Produk'],
                'Harga Jual': product_info['Harga Jual'],
                'Rating Produk': product_info['Rating Produk'],
                'Nama Akun': review['Nama Akun'],
                'Rating Pengguna': review['Rating Pengguna'],
                'Ulasan Produk': review['Ulasan Produk']
            }
            writer.writerow(row)

if __name__ == "__main__":
    main()