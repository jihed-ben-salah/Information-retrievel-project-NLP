import scrapy



            
class MySpider(scrapy.Spider):
    name = "myspider"

    def start_requests(self):
        urls = [
     
            #"http://www.femmes.gov.tn/fr/2023/03/28/a-loccasion-du-mois-du-ramadan/"
            #"http://www.femmes.gov.tn/fr/2023/03/16/la-ministre-de-la-famille-et-de-la-femme-sadresse-aux-participants-a-la-23eme-session-du-conseil-dadministration-du-centre-de-la-femme-frabe-pour-la-formation-et-la-recherche/"
            #"http://www.femmes.gov.tn/fr/2023/03/14/les-situations-des-enfants-issus-dun-mariage-tuniso-suedois-sont-au-centre-de-la-rencontre-du-ministre-de-la-famille-et-de-la-femme-avec-lambassadrice-de-suede-en-tunisie/"
            #"http://www.femmes.gov.tn/fr/2023/03/09/communique/"
            #"http://www.santetunisie.rns.tn/fr/toutes-les-actualites/1746-xviii-sommet-de-la-francophonie-2022"
            #"http://www.santetunisie.rns.tn/fr/presentations/roles-attributions"
            #"http://www.emploi.gov.tn/index.php/fr/669/deuxieme-conference-regionale-du-programme-pour-une-approche-globale-de-la-gouvernance-de-la"
             "http://www.emploi.gov.tn/index.php/fr/679/rencontre-avec-lambassadeur-de-palestine-en-tunisie"               ]
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
    # extract data from the page
        for paragraphs in response.css('div p'):
            try:
                yield{
                    'context': paragraphs.css('span::text').get(),
                    'context2': paragraphs.css('::text').get()
                   
                }
            except:
                yield{
                    'context':'not found',
                }
    # follow links to the next page
            next_page = response.css('a.next-page-link::attr(href)').get()
            if next_page is not None:
             yield response.follow(next_page, self.parse)
