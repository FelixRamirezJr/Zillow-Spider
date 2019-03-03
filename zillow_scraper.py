import scrapy
import re
import requests
from random_user_agent.user_agent import UserAgent
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
                print('Sleeping...Zzzz')
                time.sleep(1)
                print('Crawling: ' + url)
                yield scrapy.Request(url,
                    callback=self.parse,
                    meta={'city': city, 'state': state, 'location': city + ' ' + state, 'page': 1},
                    headers={"User-Agent": agent})
        # yield scrapy.Request('https://www.zillow.com/homes/for_sale/Aguada,-PR_rb/',
        #     callback=self.parse,
        #     meta={'city': 'city', 'state': 'state', 'location': 'test' + ' ' + 'test', 'page': 1},
        #     headers={"User-Agent": agent})

    def parse_house(self, response):
        print("parsing house")
        print(response.meta['location'])

        # Let's get the price
        price = response.xpath('//div[@class="price"]/span/text()').extract_first()
        if price == None:
            print("Couldn't find price with .price class attempting to find with ds-value")
            price = response.xpath('//span[@class="ds-value"]/text()').extract_first()

        price = price.replace('$', '').replace(',', '').strip()

        print("===== FINAL PRICE ======")
        print(price)

        # Now let's get the details
        beds = ''
        bathrooms = ''
        for text in response.xpath('//span/text()').extract():
            if "beds" in text or text.isdigit():
                print("Found beds")
                beds = text.replace('beds', '').strip()
            if "baths" in text or text.isdigit():
                print("Found baths")
                bathrooms = text.replace('baths', '').strip()
            if len(beds) > 0 and len(bathrooms) > 0:
                break

        if len(price) > 0 and len(beds) > 0 and len(bathrooms) > 0:
            print("==== Found some good data ====")
            data = {'rooms': beds, 'description': '' ,'bathrooms': bathrooms, 'price': price, 'url': response.url, 'location': response.meta['location']}
            print(data)
            r = requests.post(url = send_data_url, data = data)
            print(r.text)



    def parse(self, response):
        print('in the parse')
        print(response.meta['location'])
        index = 0
        all_data = []
        print("Sleeping when in the parse...")
        time.sleep(10)

        # Get the url first
        for link_dom in response.css('.zsg-photo-card-overlay-link'):
            url = link_dom.css('a::attr(href)').extract_first()
            # data = {'rooms': '', 'description': '' ,'bathrooms': '', 'price': '', 'url': '', 'location': ''}
            # data['location'] = response.meta['location']
            # data['url'] = "https://www.zillow.com" + url
            print('sleeping before trying to scrape' + url)
            time.sleep(1)
            yield scrapy.Request(zillow_url + url,
                callback=self.parse_house,
                meta=response.meta,
                headers={"User-Agent": user_agent_rotator.get_random_user_agent()})

            #all_data.append(data)

        # description = ""
        # for house in response.css('.zsg-photo-card-caption'):
        #     print("This is index at the start:")
        #     print(index)
        #     data = all_data[index]
        #     data["description"] = house.xpath('//span[@class="zsg-photo-card-status"]/text()').extract()[index]
        #     #description += status
        #     data["price"] = house.xpath('//p[@class="zsg-photo-card-spec"]/span[@class="zsg-photo-card-price"]/text()').extract()[index]
        #     data['price'] = data['price'].replace('$', '').replace(',','').strip()
        #
        #     room_data = house.xpath('//p[@class="zsg-photo-card-spec"]/span[@class="zsg-photo-card-info"]/text()').extract()[index]
        #
        #     data["rooms"] = room_data[0]
        #     data["rooms"] = data["rooms"].replace('bds', '').strip()
        #
        #     data["bathrooms"] = room_data[1]
        #     data["bathrooms"] = data["bathrooms"].replace('ba', '').strip()
        #
        #     data['description'] = data["description"] + " URL: " + response.url + " page: " + str(response.meta['page'])
        #     #print house.xpath('//p[@class="zsg-photo-card-spec"]/text()')
        #     print("========== DATA ==========")
        #     print(data)
        #     index = index + 1
        #     #r = requests.post(url = send_data_url, data = data)
        #     #print(r.text)
        #
        # print("About to try and get the next page")
        # for next in response.css('.zsg-pagination-next'):
        #     print("About to try css get for zsg pagination")
        #     next_page = zillow_url + next.xpath('a/@href').extract_first()
        #     if next_page != None:
        #         response.meta['page'] = response.meta['page'] + 1
        #         print("Sleeping and going to the next page")
        #         print(response.meta['page'])
        #         print(next_page)
        #         time.sleep(5)
        #
        #         yield scrapy.Request(next_page,
        #             callback=self.parse,
        #             meta=response.meta,
        #             headers={"User-Agent": user_agent_rotator.get_random_user_agent()})
