import scrapy


class PartnerSpider(scrapy.Spider):
    name = "github"

    def start_requests(self):
        urls = [
            #give a github link to linkedin, this can be extended by adding ?page=2/3/4 for additional requests
            'https://github.com/linkedin',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse) #can we generate a request for a contribs page with callback=self.scrapeContributor? 

    def parse(self, response):
            projectList = response.css('div.org-repos').css('h3').css('a::text').extract() #gives the project names, from which we can make the github/projectname/contributors link
            
            #for each project, yield a request to scrape it's contributor page
            for proj in projectList:
                yield scrapy.Request(url='https://github.com/linkedin/' + proj.Split() + '/graphs/contributors', callback=self.parseProfile)
            
            #need to get the contributors
            
            #need to acces the contrib. page and get their company
            
            self.log('Crawled a Github page')
        
        #Get links for the partner pages
        #next_page = response.css('li.linkedin-list-item').css('div.parbase').css('a::attr(href)').extract_first()
        #if next_page is not None:
            #next_page = response.urljoin(next_page)
            #yield scrapy.Request(next_page, callback=self.parse)
        
        #self.log('Saved file %s' % filename)
        
    
    def parseProfile(self, response):
        
        self.log('The profile spider was called')
        
        #li.linkedin-list-item:nth-child(1) > div:nth-child(1) > article:nth-child(1) > div:nth-child(3) > p:nth-child(1) > a:nth-child(2)).re(r'Go to (\w+)')
        #response.css('a.image-link::text').re(r'to (\w
        #response.css('a.image-link').css('img.image-tag').xpath('@alt')