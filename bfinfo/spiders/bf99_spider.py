import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'bf99'

    start_urls = ['https://www.bf99.com/User/List.htm']

    def parse(self, response):
        # follow links to author pages
        for href in response.css('a.lnk_01::attr(href)'):
            yield response.follow(href, self.parse_author)

        # follow pagination links
        for href in response.xpath('//div[@class="viciao"]/a[last()-1]'):
            yield response.follow(href, self.parse)

    def parse_author(self, response):
        def extract_with_xpath(query):
            return response.xpath(query).extract_first().strip()

        yield {
            'home': extract_with_xpath('//tr[8]/td[@class="nav2-25 friend_view_typecontent"]/text()'),
            'age': extract_with_xpath('//tr[5]/td[@class="nav2-25 friend_view_typecontent"]/font[1]/text()')
        }