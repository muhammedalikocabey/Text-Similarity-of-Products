# -*- coding: utf-8 -*-
"""
@author: Muhammed Ali Kocabey
"""
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import locale
import time 


import re

import pandas as pd

locale.setlocale(locale.LC_ALL, "Turkish")

######################################################################################################## 


class Scraper():
    def __init__(self, driver_path="chrome_driver/chromedriver.exe", headless=True):
        self.driver_path = driver_path
        self.headless = headless
        


    def createBrowser(self, disableBrowserNotification=False):
        
    
        options = webdriver.ChromeOptions()
        #options.add_experimental_option('prefs', {'intl.accept_languages': 'tr'})
        options.add_argument('--lang=tr')
        options.add_argument('--dns-prefetch-disable')
        if self.headless:
            options.add_argument("--headless") 
        options.add_experimental_option("excludeSwitches", ["enable_automation"])
        options.add_experimental_option("useAutomationExtension", False)
    
    
        if disableBrowserNotification:
            prefs = {"profile.default_content_setting_values.notifications" : 2}
            options.add_experimental_option("prefs",prefs)
            
        browser = webdriver.Chrome(executable_path=self.driver_path, options = options)
        browser.maximize_window()
    
        return browser
    
    def create_ActionChains(self, browser):
        action = ActionChains(browser)
        return action
    
    
    
    
    
    def cleanHTML_and_raw(self, raw_html): 
      cleanr    = re.compile('<.*?>')
      cleantext = re.sub(cleanr, '', raw_html)
      cleantext = re.sub("[\(\[].*?[\)\]]", "", cleantext)
      return cleantext
    
    
    
    
    
    def replace_specialCharacter_folder(self, string):
        special_character_list = [':', '/', '/', '*', '?', '<', '>', '|']
        for i in range(len(string)):
            if string[i] in special_character_list:
                string.replace(string[i], "")
            
        string.strip()
        
        return string
        
        
    
    
    
    
    ########################################################################################################################################################################
    
    
        
    def close_n11_notifications(self, browser):
        
        try:
            kvkk_notification = browser.find_element_by_xpath("//div/div/span[@class='btn btnBlack']")
            kvkk_notification.click()
        except:
            pass
        
        try:
            cookie_notification = browser.find_element_by_xpath("//div[@id='cookieUsagePopIn']/span")
            cookie_notification.click()
        except:
            pass
        
    
    
    def n11(self, browser, category):
        browser.get("https://www.n11.com/elektronik")
        
        category_link = browser.find_element_by_xpath("//div/div[@class='subCatMenu l6']/ul/li/ul/li/a[text()='"+category+"']")
        category_link = category_link.get_attribute("href")
           
        
        browser.get(str(category_link))
        
        time.sleep(1)
        
        en_cok_satan_sirala = browser.find_element_by_xpath("//div/div/div/select/option[@value='SALES_VOLUME']")
        en_cok_satan_sirala.click()
            
        browser.execute_script("window.scrollTo(0, 300)")
        
        time.sleep(1)
        
        self.close_n11_notifications(browser) 
        
        ürün_isimleri = browser.find_elements_by_xpath("//div[@id='view']/ul/li/div/div[@class='pro']/a/h3")
            
        ürün_fiyatları = browser.find_elements_by_xpath("//div[@id='view']/ul/li/div/div[@class='proDetail']/a/ins")
        
        ürün_resimleri = browser.find_elements_by_xpath("//div[@id='view']/ul/li/div/div[@class='pro']/a/img")
        
        ürün_linkleri = browser.find_elements_by_xpath("//div[@id='view']/ul/li/div/div[@class='pro']/a")
        
        ürün_isimleri_list = list()
        ürün_fiyatları_list = list()
        ürün_resimleri_list = list()
        ürün_linkleri_list = list()
        
        
        for inn in range(min(len(ürün_isimleri), len(ürün_fiyatları), len(ürün_resimleri), len(ürün_linkleri))):
            ürün_isimleri_list.append(self.cleanHTML_and_raw(ürün_isimleri[inn].get_attribute("innerHTML")).strip())
            ürün_fiyatları_list.append(self.cleanHTML_and_raw(ürün_fiyatları[inn].get_attribute("innerHTML")).split()[0].strip())
            ürün_resimleri_list.append(self.cleanHTML_and_raw(ürün_resimleri[inn].get_attribute("data-original")).strip())
            ürün_linkleri_list.append(self.cleanHTML_and_raw(ürün_linkleri[inn].get_attribute("href")).strip())
            
        ürün_detaylari = list()
        
        count = 0
        for i, f, r, l in zip(ürün_isimleri_list, ürün_fiyatları_list, ürün_resimleri_list, ürün_linkleri_list):
            if count == 15:
                break
    
            ürün = {'ürün_sırası': count+1, 'ürün_ismi': i, 'ürün_fiyatı': f, "ürün_linki": l, "ürün_resmi": r, "ürün_sitesi": "N11"}
            ürün_detaylari.append(ürün)
            count = count+1
            
        ürün_detaylari = pd.DataFrame(ürün_detaylari)
        return ürün_detaylari
        
        
    ########################################################################################################################################################################   
            
       
    def close_hepsiBurada_notifications(self, browser, category):
        try:
            cookie_notification = browser.find_element_by_xpath("//div[@class='cookie-info']/img")
            cookie_notification.click()
        except:
            pass
        
        if category == 'Tablet':
            try:
                tablet_notification = browser.find_element_by_xpath("//div/div/div/button[@class='_hj-OO1S1__styles__openStateToggle']")
                tablet_notification.click()
            except:
                pass
    

           
    def hepsiBurada(self, browser, category):    
        if category == 'Cep Telefonu':
            browser.get("https://www.hepsiburada.com/cep-telefonlari-c-371965")
        
        elif category == 'Dizüstü Bilgisayar':
            browser.get("https://www.hepsiburada.com/laptop-notebook-dizustu-bilgisayarlar-c-98")
            
        elif category == 'Tablet':
            browser.get("https://www.hepsiburada.com/tablet-c-3008012")
        
        else:
            browser.close()
            return -1
        
        en_cok_satan_sirala = browser.find_element_by_xpath("//div/div/a[@class='button sorting-label' and @hbustag='CokSatan']")
        en_cok_satan_sirala.click()
        
        browser.execute_script("window.scrollTo(0, 300)")
        
        time.sleep(1)
        
        self.close_hepsiBurada_notifications(browser, category)
        
        
        ürün_isimleri = browser.find_elements_by_xpath("//div[@class='product-detail']/h3/div/p/span")
        
        ürün_linkleri = browser.find_elements_by_xpath("//li[@class='search-item col lg-1 md-1 sm-1  custom-hover not-fashion-flex']/div/a")
        
        
        ürün_isimleri_list = list()
        ürün_linkleri_list = list()
        
        
        for inn in range(min(len(ürün_isimleri), len(ürün_linkleri))):
            ürün_isimleri_list.append(self.cleanHTML_and_raw(ürün_isimleri[inn].get_attribute("innerHTML")).strip())
            ürün_linkleri_list.append(self.cleanHTML_and_raw(ürün_linkleri[inn].get_attribute("href")).strip())
            
        ürün_detaylari = list()
        
        count = 0
        for i, l in zip(ürün_isimleri_list, ürün_linkleri_list):
            if count == 15:
                break
    
            ürün = {'ürün_sırası': count+1, 'ürün_ismi': i, 'ürün_fiyatı': None, "ürün_linki": l, "ürün_resmi": None, "ürün_sitesi": "HepsiBurada"}
            ürün_detaylari.append(ürün)
            count = count+1
            
        ürün_detaylari = pd.DataFrame(ürün_detaylari)
        return ürün_detaylari
        
        
    ######################################################################################################################################################################## 
        
        
    def close_trendyol_notifications(self, browser):
        time.sleep(1)
        
        try:
            cinsiyet_notification = browser.find_element_by_xpath("//div[@class='fancybox-skin']/a[@class='fancybox-item fancybox-close']")
            cinsiyet_notification.click()
        except:
            pass
        
        time.sleep(0.5)
        
        try:
            cookie_notification = browser.find_element_by_xpath("//div[@class='vnotify-container vn-bottom-left']/div[@class='vnotify-item vnotify-notify']/span")
            cookie_notification.click()
        except:
            pass
            
    
    
    def trendyol(browser, category = "Cep Telefonu"):
        if category == 'Cep Telefonu':
            browser.get("https://www.trendyol.com/cep-telefonu")
        
        elif category == 'Dizüstü Bilgisayar':
            browser.get("https://www.trendyol.com/laptop")
            
        elif category == 'Tablet':
            browser.get("https://www.trendyol.com/tablet")
            
        else:
            browser.close()
            return -1
        
        
        self.close_trendyol_notifications(browser)
        
        
        en_cok_satan_sirala = browser.find_element_by_xpath("//div[@class='sort-fltr-cntnr']/select/option[text()='En çok satanlar']")
        en_cok_satan_sirala.click()
    
    
        time.sleep(1)
    
        ürün_isimleri = browser.find_elements_by_xpath("//div/div/span[@class='prdct-desc-cntnr-name hasRatings']")
        #   //div[@class='p-card-wrppr']/div/a/div[@class='prdct-desc-cntnr-wrppr']/div/div/span[@class='prdct-desc-cntnr-name hasRatings']
        #   //div/div/span[@class='prdct-desc-cntnr-name hasRatings']
        #   innerHTML
        
        ürün_fiyatları = browser.find_elements_by_xpath("//div[@class='price-promotion-container']/div[@class='prmtn-cntnr']/div[@class='prmtn']/div[@class='prc-box-dscntd']")
        
        #   innerHTML
        
        ürün_resimleri = browser.find_elements_by_xpath("//div[@class='p-card-img-wr']/img[@class='p-card-img']")
        
        #   src
        
        ürün_linkleri = browser.find_elements_by_xpath("//div[@class='prdct-cntnr-wrppr']/div/div/a")
    
        #   href
    
    
        ürün_isimleri_list = list()
        ürün_fiyatları_list = list()
        ürün_resimleri_list = list()
        ürün_linkleri_list = list()
        
        
        for inn in range(min(len(ürün_isimleri), len(ürün_fiyatları), len(ürün_resimleri), len(ürün_linkleri))):
            ürün_isimleri_list.append(self.cleanHTML_and_raw(ürün_isimleri[inn].get_attribute("title")).strip())
            ürün_fiyatları_list.append(self.cleanHTML_and_raw(ürün_fiyatları[inn].get_attribute("innerHTML")).strip())
            ürün_resimleri_list.append(self.cleanHTML_and_raw(ürün_resimleri[inn].get_attribute("src")).strip())
            ürün_linkleri_list.append(self.cleanHTML_and_raw(ürün_linkleri[inn].get_attribute("href")).strip())
            
        ürün_detaylari = list()
        
        count = 0
        for i, f, r, l in zip(ürün_isimleri_list, ürün_fiyatları_list, ürün_resimleri_list, ürün_linkleri_list):
            if count == 15:
                break
    
            ürün = {'ürün_sırası': count+1, 'ürün_ismi': i, 'ürün_fiyatı': f, "ürün_linki": l, "ürün_resmi": r, "ürün_sitesi": "Trendyol"}
            ürün_detaylari.append(ürün)
            count = count+1
            
        ürün_detaylari = pd.DataFrame(ürün_detaylari)        
        return ürün_detaylari
    
    
    ########################################################################################################################################################################
    
    
    def close_amazon_notifications(self, browser):
        try:
            cookie_notification = browser.find_element_by_xpath("//span[@class='a-button-inner']/input[@id='sp-cc-accept']")
            cookie_notification.click()
        except:
            pass
    
    
    
    def amazon(self, browser, category = "Cep Telefonu"):    
        if category == 'Cep Telefonu':
            browser.get("https://www.amazon.com.tr/gp/bestsellers/electronics/13709907031?ref_=Oct_s9_apbd_obs_hd_bw_bExpN6l_S&pf_rd_r=5KQ7FHT56096DWE5NBRW&pf_rd_p=08b129b6-9e3b-500f-8217-5da1a58501ba&pf_rd_s=merchandised-search-11&pf_rd_t=BROWSE&pf_rd_i=13709907031")
        
        elif category == 'Dizüstü Bilgisayar':
            browser.get("https://www.amazon.com.tr/gp/bestsellers/computers/12601898031?ref_=Oct_s9_apbd_obs_hd_bw_bDkqHLr_S&pf_rd_r=18KZFE1HKWWFHDHHHP52&pf_rd_p=8213719a-cf26-59aa-a1c8-a6a8c092b725&pf_rd_s=merchandised-search-11&pf_rd_t=BROWSE&pf_rd_i=12601898031")
            
        elif category == 'Tablet':
            browser.get("https://www.amazon.com.tr/s?n=12601907031&p_72=4-&ref_=Oct_s9_apbd_otopr_hd_bw_bDkqJh1_S&pf_rd_r=W23MCRTWWZD79DX6S9DB&pf_rd_p=2004f426-8676-5c0f-8c80-4aae9d1aed98&pf_rd_s=merchandised-search-11&pf_rd_t=BROWSE&pf_rd_i=12601907031")
            
        else:
            browser.close()
            return -1
        
        
        time.sleep(1)
        
        self.close_amazon_notifications(browser)
        
        
        ürün_isimleri = list()
        
        if category == "Tablet":
            ürün_isimleri = browser.find_elements_by_xpath("//h2/a/span[@class='a-size-base-plus a-color-base a-text-normal']")
        else:
            ürün_isimleri = browser.find_elements_by_xpath("//div[@class='p13n-sc-truncate-mobile-type p13n-sc-truncated']")
            if len(ürün_isimleri) == 0:
                ürün_isimleri = browser.find_elements_by_xpath("//div[@class='p13n-sc-truncated']")
            
        #   Dizüstü Bilgisayar = //div[@class='p13n-sc-truncated']
        #   Cep Telefonu = //div[@class='p13n-sc-truncate-mobile-type p13n-sc-truncated']
        #   innerHTML
            
        if category == "Tablet":
            ürün_fiyatları = browser.find_elements_by_xpath("//span[@class='a-price-whole']")
        else:
            ürün_fiyatları = browser.find_elements_by_xpath("//span/span[@class='p13n-sc-price']")
        #   innerHTML
        
        if category == "Tablet":
            ürün_resimleri = browser.find_elements_by_xpath("//a/div[@class='a-section aok-relative s-image-square-aspect']/img")
        else:
            ürün_resimleri = browser.find_elements_by_xpath("//span/div[@class='a-section a-spacing-small']/img")
        #   src
        
        if category == "Tablet":
            ürün_linkleri = browser.find_elements_by_xpath("//div[@class='a-section a-spacing-medium']/span/a")
        else:        
            ürün_linkleri = browser.find_elements_by_xpath("//span[@class='aok-inline-block zg-item']/a")
        #   href
            
        
        ürün_isimleri_list = list()
        ürün_fiyatları_list = list()
        ürün_resimleri_list = list()
        ürün_linkleri_list = list()
        
        
        for inn in range(min(len(ürün_isimleri), len(ürün_fiyatları), len(ürün_resimleri), len(ürün_linkleri))):
            ürün_isimleri_list.append(self.cleanHTML_and_raw(ürün_isimleri[inn].get_attribute("innerHTML")).strip())
            ürün_fiyatları_list.append(self.cleanHTML_and_raw(ürün_fiyatları[inn].get_attribute("innerHTML")).replace("₺","").strip())
            ürün_resimleri_list.append(self.cleanHTML_and_raw(ürün_resimleri[inn].get_attribute("src")).strip())
            ürün_linkleri_list.append(self.cleanHTML_and_raw(ürün_linkleri[inn].get_attribute("href")).strip())
            
        ürün_detaylari = list()
        
        count = 0
        for i, f, r, l in zip(ürün_isimleri_list, ürün_fiyatları_list, ürün_resimleri_list, ürün_linkleri_list):
            if count == 15:
                break
            if category == "Dizüstü Bilgisayar" or category == "Tablet":
                ürün = {'ürün_sırası': count+1, 'ürün_ismi': i, 'ürün_fiyatı': None, "ürün_linki": l, "ürün_resmi": r, "ürün_sitesi": "Amazon"}
            else:
                ürün = {'ürün_sırası': count+1, 'ürün_ismi': i, 'ürün_fiyatı': f, "ürün_linki": l, "ürün_resmi": r, "ürün_sitesi": "Amazon"}
            ürün_detaylari.append(ürün)
            count = count+1
            
        ürün_detaylari = pd.DataFrame(ürün_detaylari)
        return ürün_detaylari
            
            
            
    ########################################################################################################################################################################       
            
    
    def close_vatanBilgisayar_notifications(self, browser):
        try:
            kvkk_notification = browser.find_element_by_xpath("//div[@class='cookie-privacy']/a[@class='close-privacy-btn']")        
            kvkk_notification.click()
        except:
            pass
            
        
        
    def vatanBilgisayar(self, browser, category = "Cep Telefonu"):
        if category == 'Cep Telefonu':
            browser.get("https://www.vatanbilgisayar.com/cep-telefonu-modelleri/")
        
        elif category == 'Dizüstü Bilgisayar':
            browser.get("https://www.vatanbilgisayar.com/notebook/")
            
        elif category == 'Tablet':
            browser.get("https://www.vatanbilgisayar.com/tabletler/")
        
        else:
            browser.close()
            return -1
        
        
        time.sleep(1)
        
        self.close_vatanBilgisayar_notifications(browser)
        
        en_cok_satan_sirala = browser.find_element_by_xpath("//div[@class='desktop-sort-select']/select/option[@value='ES']")
        en_cok_satan_sirala.click()
            
        browser.execute_script("window.scrollTo(0, 300)")
        
        time.sleep(1)
        
        
        ürün_isimleri = browser.find_elements_by_xpath("//a/div[@class='product-list__product-name']")
        #   //div[@class='product-list product-list--list-page']/div[@class='product-list__content']/a/div[@class='product-list__product-name']
        #   innerHTML
        
        ürün_fiyatları = browser.find_elements_by_xpath("//div[@class='wrapper-product-main']/div[@class='wrapper-product wrapper-product--list-page clearfix']/div/div[@class='product-list__content']/div[@class='product-list__cost']/span[@class='product-list__price']")
        #   innerHTML
        
        ürün_linkleri = browser.find_elements_by_xpath("//div[@class='wrapper-product wrapper-product--list-page clearfix']/div[@class='product-list product-list--list-page']/div[@class='product-list__content']/a")
        #   href
        
        ürün_isimleri_list = list()
        ürün_fiyatları_list = list()
        ürün_linkleri_list = list()
        
        
        for inn in range(min(len(ürün_isimleri), len(ürün_fiyatları), len(ürün_linkleri))):
            ürün_isimleri_list.append(self.cleanHTML_and_raw(ürün_isimleri[inn].get_attribute("innerHTML")).strip())
            ürün_fiyatları_list.append(self.cleanHTML_and_raw(ürün_fiyatları[inn].get_attribute("innerHTML")).strip())
            ürün_linkleri_list.append(self.cleanHTML_and_raw(ürün_linkleri[inn].get_attribute("href")).strip())
            
        ürün_detaylari = list()
        
        count = 0
        for i, f, l in zip(ürün_isimleri_list, ürün_fiyatları_list, ürün_linkleri_list):
            if count == 15:
                break
    
            ürün = {'ürün_sırası': count+1, 'ürün_ismi': i, 'ürün_fiyatı': f, "ürün_linki": l, "ürün_resmi": None, "ürün_sitesi":"Vatan Bilgisayar"}
            ürün_detaylari.append(ürün)
            count = count+1
            
        ürün_detaylari = pd.DataFrame(ürün_detaylari)
        return ürün_detaylari
    
    
    ########################################################################################################################################################################
    
    
    def close_gittiGidiyor_notifications(self, browser):
        try:
            cookie_notification = browser.find_element_by_xpath("//section[@class='styles__AlertTextContainer-tyj39b-1 cinJAZ']/a[@class='styles__AlertClose-tyj39b-3 bcfLkR']")
            cookie_notification.click()
        except:
            pass
        
        try:
            cookie_notification = browser.find_element_by_xpath("//a[@class='policy-alert-close btn-alert-close']")
            cookie_notification.click()
        except:
            pass
    
    
    
    def gittiGidiyor(self, browser, category = "Cep Telefonu"):
        if category == 'Cep Telefonu':
            browser.get("https://www.gittigidiyor.com/cep-telefonu")
        
        elif category == 'Dizüstü Bilgisayar':
            browser.get("https://www.gittigidiyor.com/dizustu-laptop-notebook-bilgisayar")
            
        elif category == 'Tablet':
            browser.get("https://www.gittigidiyor.com/tablet")
            
        else:
            browser.close()
            return -1
        
        
        if category != "Tablet":
            en_cok_satan_sirala = browser.find_element_by_xpath("//div/select[@id='order_selectbox']/option[text()='En Çok Satanlar']")
            en_cok_satan_sirala.click()
        
        time.sleep(1)
    
        self.close_gittiGidiyor_notifications(browser)
        
        ürün_isimleri = list()
        ürün_fiyatları = list()
        ürün_resimleri = list()
        ürün_linkleri = list()
        if category == "Tablet":
            ürün_isimleri = browser.find_elements_by_xpath("//ul[@class='catalog-view clearfix products-container']/li/a")
            
            ürün_fiyatları = browser.find_elements_by_xpath("//p[@class='fiyat price-txt robotobold price']")
                   
            ürün_resimleri = browser.find_elements_by_xpath("//ul/li/a/div/p/img")
                    
            ürün_linkleri = browser.find_elements_by_xpath("//ul[@class='catalog-view clearfix products-container']/li/a")
                    
            
            
            
        else:
            ürün_isimleri = browser.find_elements_by_xpath("//ul/li/div/a/h3")
            
            ürün_fiyatları = browser.find_elements_by_xpath("//ul/li/div/a/div/div/span/span/span")
        
            ürün_resimleri = browser.find_elements_by_xpath("//ul/li/div/a/div/img")
            
            ürün_linkleri = browser.find_elements_by_xpath("//ul/li/div/a")
        
        
        
        
        ürün_isimleri_list = list()
        ürün_fiyatları_list = list()
        ürün_resimleri_list = list()
        ürün_linkleri_list = list()
        
        
        for inn in range(min(len(ürün_isimleri), len(ürün_fiyatları), len(ürün_resimleri), len(ürün_linkleri))):
            if category == "Tablet":
                ürün_isimleri_list.append(self.cleanHTML_and_raw(ürün_isimleri[inn].get_attribute("title")).strip())
                ürün_fiyatları_list.append(self.cleanHTML_and_raw(ürün_fiyatları[inn].get_attribute("innerHTML")).split()[0].strip())
                ürün_resimleri_list.append(self.cleanHTML_and_raw(ürün_resimleri[inn].get_attribute("data-original")).strip())
                ürün_linkleri_list.append(self.cleanHTML_and_raw(ürün_linkleri[inn].get_attribute("href")).strip())
            else:
                ürün_isimleri_list.append(self.cleanHTML_and_raw(ürün_isimleri[inn].get_attribute("innerHTML")).strip())
                ürün_fiyatları_list.append(self.cleanHTML_and_raw(ürün_fiyatları[inn].get_attribute("innerHTML")).split()[0].strip())
                ürün_resimleri_list.append(self.cleanHTML_and_raw(ürün_resimleri[inn].get_attribute("data-original")).strip())
                ürün_linkleri_list.append(self.cleanHTML_and_raw(ürün_linkleri[inn].get_attribute("href")).strip())
         
        ürün_detaylari = list()
        
        count = 0
        for i, f, r, l in zip(ürün_isimleri_list, ürün_fiyatları_list, ürün_resimleri_list, ürün_linkleri_list):
            if count == 15:
                break
            
            if category == "Tablet":
                ürün = {'ürün_sırası': count+1, 'ürün_ismi': i, 'ürün_fiyatı': None, "ürün_linki": l, "ürün_resmi": r, "ürün_sitesi": "Gittigidiyor"}
            else:
                ürün = {'ürün_sırası': count+1, 'ürün_ismi': i, 'ürün_fiyatı': f, "ürün_linki": l, "ürün_resmi": r, "ürün_sitesi": "Gittigidiyor"}
            ürün_detaylari.append(ürün)
            count = count+1
         
            
        ürün_detaylari = pd.DataFrame(ürün_detaylari)
        return ürün_detaylari
    
    
    def scrap_websites(self, category = "Cep Telefonu"):
        browser = self.createBrowser(disableBrowserNotification=True)
        
        df_list = list()
        
        df_list.append(self.n11(browser, category))
        time.sleep(1)
        df_list.append(self.hepsiBurada(browser, category))
        time.sleep(1)
        df_list.append(self.amazon(browser, category))
        time.sleep(1)
        df_list.append(self.vatanBilgisayar(browser, category))
        time.sleep(1)
        df_list.append(self.gittiGidiyor(browser, category))
        
        browser.close()
        
        return df_list
    
    def getAll(self, category = "Cep Telefonu", saveCSV=False):
        result = self.scrap_websites(category)
        

        result_concat = pd.concat(result, ignore_index=True,)
        
        if saveCSV:
            result_concat.to_csv("Tüm_Ürünler.csv", index=False)
        # result.drop("index", axis=1, ignore_index=True, inplace=True)
        # result.reset_index(inplace=True)
        return [result, result_concat]
            
#%%

# a = n11(category = "Dizüstü Bilgisayar")

# a = hepsiBurada(category = "Dizüstü Bilgisayar")

# a = amazon(category = "Dizüstü Bilgisayar")

# a = vatanBilgisayar(category = "Tablet")

# a = gittiGidiyor(category = "Tablet")

# a = getAll(category = "Cep Telefonu", concat_all=False)







