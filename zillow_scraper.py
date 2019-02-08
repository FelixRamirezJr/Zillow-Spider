import scrapy
import re
from scrapy.http import FormRequest
import requests



# CONSTANTS
send_data_url = "https://frj-investments.herokuapp.com/api/potential_investments"
zillow_login_email = 'felix.ramirezjr.korea@gmail.com'
zillow_login_password = 'asdfasdf123123'
tes = 'https://www.zillow.com/browse/homes/tx/'
homes_url = 'https://www.zillow.com/browse/homes/'
zillow_captcha = 'https://www.zillow.com/captchaPerimeterX/?url=%2fuser%2facct%2flogin%2f&uuid=d3726630-2b62-11e9-9fb9-45f9f4604070&vid'



class ZillowScraper(scrapy.Spider):
    name = 'ZillerScraper'
    #start_urls = ['https://www.zillow.com/']
    start_urls = ['https://www.zillow.com/browse/homes/']
    allowed_domains = ['zillow.com']
    #login_url = 'https://www.zillow.com/user/acct/login/'

    def start_requests(self):
        yield scrapy.Request(homes_url, callback=self.parse, headers={"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3"})

    def parse(self, response):
        # we first want to get the list of houses in states
        for section in response.css('.zsg-content-component'):
            for state in section.css('li'):
                print state.css('a::attr(href)' ).extract_first()



    # def __init__(self):
    #     self.driver = webdriver.Firefox()
    #
    # def start_requests(self):
    #     # let's start by sending a first request to login page
    #     yield scrapy.Request(self.login_url, self.parse_login)
    #
    # def parse_login(self, response):
    #     # got the login page, let's fill the login form...
    #     data, url, method = fill_login_form(response.url, response.body,
    #                                         zillow_login_email, zillow_login_password)
    #
    #     # ... and send a request with our login data
    #     return scrapy.FormRequest(url, formdata=dict(data),
    #                        method=method, callback=self.start_crawl)

    # def start_crawl(self, response):
    #     self.driver.get(zillow_captcha)
    #     cap = self.driver.find_elements_by_class_name('recaptcha-checkbox-checkmark')
    #     for c in cap:
    #         c.click()
    #
    #     webDriver.Close()
    #
    #     yield scrapy.Request('https://www.zillow.com/', callback=self.parse)
    #
    # def parse(self, response):
    #     print "I should be able to go"
