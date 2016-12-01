import scrapy


class PartnerSpider(scrapy.Spider):
    name = "partners"

    def start_requests(self):
        urls = [
            'https://business.linkedin.com/marketing-solutions/certified-marketing-partners/content-partners',
            'https://business.linkedin.com/marketing-solutions/certified-marketing-partners/company-page-partners/',
            'https://business.linkedin.com/marketing-solutions/certified-marketing-partners/ads-partners',
            'https://business.linkedin.com/marketing-solutions/certified-marketing-partners/custom-apps-partners',
            'https://business.linkedin.com/marketing-solutions/certified-marketing-partners/compliance-partners',
        ]
        nlurls = [
            'https://developer.linkedin.com/partner-programs/talent#partners',
            'https://developer.linkedin.com/partner-programs/consumer',
            'https://developer.linkedin.com/partner-programs/sales',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        yield scrapy.Request(url='https://business.linkedin.com/talent-solutions/partners', callback=self.talentParse)

    def parse(self, response):
        #page = response.url.split("/")[-1]
        #filename = 'quotes-%s.html' % page
        #filename = 'marketing-%s.csv' % page
        filename = 'partnertable.csv'
        with open(filename, 'a') as f:
            #Setting up lists and dics to store stuff in
            CompanyData = {}
            CompanyLogos = {}
            
            #Get the type of partnership
            PartnerTypeOutput = response.css('h2.component-section-headline::text').extract()
            PartnerType = PartnerTypeOutput[0].replace("Explore our Certified ", "")
        
            #Get the company names
            CompanyNamesList = response.css('a.image-link::text').re(r'to (\w+)')
            
            #Get the company descriptions
            CompanyDescriptionList = response.css('p.description.component-subheadline::text').extract()
            dicIndex = 0;
            for CompanyDescription in CompanyDescriptionList:
                CompanyData[CompanyNamesList[dicIndex]] = CompanyDescription
                dicIndex += 1
                              
            #Get the images associated with a company
            ImageLinks = response.css('a.image-link').css('img.image-tag').xpath('@src').extract()
            dicIndex2 = 0
            for link in ImageLinks:
                CompanyLogos[CompanyNamesList[dicIndex2]] = link
                dicIndex2 += 1
                
            #write the dics to the output file
            for key in CompanyData.keys():
                f.write((key + ',"' + CompanyData[key] + '",' + PartnerType + ',' + CompanyLogos[key] + "\n").encode("utf-8"))
            
        self.log('Saved file %s' % filename)
        
    def talentParse(self, response):
        filename = 'partnertable.csv'
        with open(filename, 'a') as f:
            #Setting up lists and dics to store stuff in
            CompanyData = {}
            CompanyLogos = {}
            
            #Get the company names
            CompanyNamesList = response.css('a.image-link::text').re(r'to (\w+)')
            
            #Get the company descriptions
            CompanyDescriptionList = response.css('p.description.component-subheadline::text').extract()
            dicIndex = 0;
            for CompanyDescription in CompanyDescriptionList:
                CompanyData[CompanyNamesList[dicIndex]] = CompanyDescription
                dicIndex += 1
                              
            #Get the images associated with a company
            ImageLinks = response.css('a.image-link').css('img.image-tag').xpath('@src').extract()
            dicIndex2 = 0
            for link in ImageLinks:
                CompanyLogos[CompanyNamesList[dicIndex2]] = link
                dicIndex2 += 1
                
            #Get the additional companies that are not part of the list
            nlCompanyNames = response.css('li.logo-item').css('a').xpath('@title').extract()
            nlCompanyIcons = response.css('li.logo-item').css('img').xpath('@src').extract()
            
            nli = 0
            while nli < len(nlCompanyNames):
                f.write(nlCompanyNames[nli] + ',None given, Talent Solutions Partner,' + nlCompanyIcons[nli] + "\n")
                nli += 1
                
            #write the dics to the output file (Name, description, partnership type, logo link)
            for key in CompanyData.keys():
                f.write((key + ',"' + CompanyData[key] + '",Talent Solutions Partner,' + CompanyLogos[key] + "\n").encode("utf-8"))
        self.log('I crawled the talent solutions page!')
        
    def nonListParse(self, response):
        i = 5