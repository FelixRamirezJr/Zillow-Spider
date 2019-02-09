import scrapy
import re
from scrapy.http import FormRequest
import requests
from random_user_agent.user_agent import UserAgent
from scrapy_splash import SplashRequest
import time


# CONSTANTS
send_data_url = "https://frj-investments.herokuapp.com/api/potential_investments"
homes_url = 'https://www.zillow.com/browse/homes/'
zillow_url = 'https://www.zillow.com'
my_user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3"
 # In order to prevent Zillow from knowing we are robots,
 # ensure that we are always using a random user agent
user_agent_rotator = UserAgent()
zillow_homes_for_sale = 'https://www.zillow.com/homes/for_sale/*city*,-*SS*_rb/'


class ZillowScraper(scrapy.Spider):
    name = 'ZillerScraper'
    #start_urls = ['https://www.zillow.com/']
    start_urls = ['https://www.zillow.com/browse/homes/']
    allowed_domains = ['zillow.com']
    handle_httpstatus_list = [500, 503, 504, 400, 408, 307, 403]
    #login_url = 'https://www.zillow.com/user/acct/login/'

    def start_requests(self):
        urls_to_scrape = []
        agent = user_agent_rotator.get_random_user_agent()

        file = open ("us_cities_states_counties.txt", "r")
        for line in file:
            splitted = line.strip().split('|')
            city = splitted[0].replace(' ', '-')
            state = splitted[1]
            url = zillow_homes_for_sale.replace('*city*', city).replace('*SS*', state)
            # Now sleeping and yielding
            if url not in urls_to_scrape:
                urls_to_scrape.append(url)
                print 'Sleeping...Zzzz'
                time.sleep(5)
                print 'Crawling: ' + url
                yield scrapy.Request(url,
                    callback=self.parse,
                    meta={'city': city, 'state': state, 'location': city + ' ' + state },
                    headers={"User-Agent": agent})


    def parse(self, response):
        print 'in the parse'
        print response.meta['location']


        #yield scrapy.Request(homes_url, callback=self.parse, headers={"User-Agent": agent})

    # def parse(self, response):
    #     # we first want to get the list of houses in states
    #     for section in response.css('.zsg-content-component'):
    #         for state in section.css('li'):
    #             path_to_state = state.css('a::attr(href)').extract_first()
    #             location_name = path_to_state.replace('/browse/homes/', '')
    #             agent = user_agent_rotator.get_random_user_agent()
    #             print 'sleep five seconds??'
    #             time.sleep(5)
    #             yield scrapy.Request(zillow_url + path_to_state,
    #                 callback=self.parse_state,
    #                 headers={"User-Agent": agent},
    #                 meta={'location': location_name})
    #
    #
    # def parse_state(self, response):
    #     print 'Hello I am here in the preview!'
    #     for county in response.css('li'):
    #         print 'county??'
    #         print county.css('a::attr(href)').extract_first()





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
