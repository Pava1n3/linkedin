import scrapy


class PartnerSpider(scrapy.Spider):
    name = "partners"

    def start_requests(self):
        urls = [
            'https://business.linkedin.com/marketing-solutions/certified-marketing-partners/content-partners',
            'https://business.linkedin.com/marketing-solutions/certified-marketing-partners/company-page-partners/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #page = response.url.split("/")[-1]
        #filename = 'quotes-%s.html' % page
        #filename = 'marketing-%s.csv' % page
        filename = 'partnertable.csv'
        with open(filename, 'a') as f:
            #Setting up lists and dics to store stuff in
            CompanyData = {}
            CompanyLogos = {}
        
            #Get the company names
            CompanyNamesList = response.css('a.image-link::text').re(r'to (\w+)')
            #for CompanyName in CompanyNamesList:
                #f.write(CompanyName)
            
            #Get the company descriptions
            CompanyDescriptionList = response.css('p.description.component-subheadline::text').extract()
            dicIndex = 0;
            for CompanyDescription in CompanyDescriptionList:
                CompanyData[CompanyNamesList[dicIndex]] = CompanyDescription
                dicIndex += 1
                #f.write(CompanyDescription)
                              
            #Get the images associated with a company
            ImageLinks = response.css('a.image-link').css('img.image-tag').xpath('@src').extract()
            dicIndex2 = 0
            for link in ImageLinks:
                CompanyLogos[CompanyNamesList[dicIndex2]] = link
                dicIndex2 += 1
                
            #write the dics to the output file
            for key in CompanyData.keys():
                f.write((key + ',' + CompanyData[key] + ',' + CompanyLogos[key] + "\n").encode("utf-8"))
            
            #f.write(response.body)
        
        #Get links for the partner pages
        #next_page = response.css('li.linkedin-list-item').css('div.parbase').css('a::attr(href)').extract_first()
        #if next_page is not None:
            #next_page = response.urljoin(next_page)
            #yield scrapy.Request(next_page, callback=self.parse)
        
        self.log('Saved file %s' % filename)
        
        #li.linkedin-list-item:nth-child(1) > div:nth-child(1) > article:nth-child(1) > div:nth-child(3) > p:nth-child(1) > a:nth-child(2)).re(r'Go to (\w+)')
        #response.css('a.image-link::text').re(r'to (\w
        #response.css('a.image-link').css('img.image-tag').xpath('@alt')