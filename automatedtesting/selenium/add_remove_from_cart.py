
from login import login
from login import print_with_timestamp
from login import By
from selenium.common.exceptions import NoSuchElementException
import syslog

def add_cart(driver, n_items):
    for i in range(n_items):
        element = "a[id='item_" + str(i) + "_title_link']"  
        driver.find_element(By.CSS_SELECTOR, element).click()  
        driver.find_element(By.CSS_SELECTOR,"button.btn_primary.btn_inventory").click()  
        product = driver.find_element(By.CSS_SELECTOR,"div[class='inventory_details_name large_size']").text  
        print_with_timestamp(product + "is being added to the shopping cart")
        driver.find_element(By.CSS_SELECTOR,"button.inventory_details_back_button").click()

    syslog.syslog('{:d} items are all added to the shopping cart successfully.'.format(n_items))

def delete_cart(driver, n_items):
    for i in range(n_items):
        element = "a[id='item_" + str(i) + "_title_link']"
        driver.find_element(By.CSS_SELECTOR,element).click()
        driver.find_element(By.CSS_SELECTOR,"button.btn_secondary.btn_inventory").click()
        product = driver.find_element(By.CSS_SELECTOR,"div[class='inventory_details_name large_size']").text
        print_with_timestamp(product + " is deleted from the shopping cart.")
        driver.find_element(By.CSS_SELECTOR,"button.inventory_details_back_button").click()
    syslog.syslog('{:d} items are deleted from the shopping cart successfully.'.format(n_items))

if __name__ == "__main__":
    N_ITEMS = 6
    TEST_USERNAME = 'standard_user'
    TEST_PASSWORD = 'secret_sauce'
    driver = login(TEST_USERNAME, TEST_PASSWORD)
    add_cart(driver, N_ITEMS)
    syslog.syslog('Add done')

    delete_cart(driver, N_ITEMS)
    syslog.syslog('Delete done')

    driver.stop_client()
    driver.close()
    driver.quit()
    syslog.syslog('Clean the client done!')