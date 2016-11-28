import scrapy


class PartnerSpider(scrapy.Spider):
    name = "partners"

    def start_requests(self):
        urls = [

        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
            response.css('div.org-repos').css('h3').css('a::text').extract() #gives the project names
            
        
        #Get links for the partner pages
        #next_page = response.css('li.linkedin-list-item').css('div.parbase').css('a::attr(href)').extract_first()
        #if next_page is not None:
            #next_page = response.urljoin(next_page)
            #yield scrapy.Request(next_page, callback=self.parse)
        
        self.log('Saved file %s' % filename)
        
        #li.linkedin-list-item:nth-child(1) > div:nth-child(1) > article:nth-child(1) > div:nth-child(3) > p:nth-child(1) > a:nth-child(2)).re(r'Go to (\w+)')
        #response.css('a.image-link::text').re(r'to (\w
        #response.css('a.image-link').css('img.image-tag').xpath('@alt')