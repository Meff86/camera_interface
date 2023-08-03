from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def parse_wildberries_price(url):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        # Ожидаем, пока элемент с классом "price-block__final-price" появится на странице
        price_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ins.price-block__final-price"))
        )
        price_text = price_element.text
        price = int(''.join(filter(str.isdigit, price_text)))
        return price
    except Exception as e:
        print(f"Ошибка при парсинге: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    product_url = "https://www.wildberries.ru/catalog/169857826/detail.aspx"
    product_price = parse_wildberries_price(product_url)
    if product_price:
        print(f"Цена товара: {product_price} ₽")
