import scrapy

from cian.local_settings import proxy


class CianSpider(scrapy.Spider):
    name = "cian"
    iteration_repeat_request = 5

    def build_url(self, page_number=1, region='4581', offer_type='flat', type_object='sale'):
        """
        Формирование ссылки для запроса
        !!!Требуеться дороботка, собирает с 1 по 55 страницу, далее сайт выкидываеть 301 с редиректом на первую
        Надо разбить на интервалы цене или по количеству комнат
        """
        url = "https://www.cian.ru/cat.php?deal_type=sale&engine_version=2" \
              "&p={page_number}" \
              "&region={region}" \
              "&offer_type={offer_type}" \
              "&type={type_object}"
        return url.format(page_number=page_number, region=region, offer_type=offer_type, type_object=type_object)

    def start_requests(self):
        for page_number in range(1, 2):
            url = self.build_url(page_number=page_number)
            cian_request = scrapy.Request(url=url, callback=self.parse, meta={'proxy': proxy})
            yield cian_request

    def parse(self, response):
        ads = response.css('[data-name="CardComponent"]')
        self.log(len(ads))
        if len(ads) == 0 and response.status == 200 and self.iteration_repeat_request > 0:
            self.log('Некоректная страница запрашиваем еще раз')
            self.iteration_repeat_request -= 1
            yield response.follow(response.url, callback=self.parse, dont_filter=True)
        else:
            for estate_object in ads:
                address_list = estate_object.css('[data-name="GeoLabel"]::text').getall()
                address = ', '.join(address_list)
                yield {
                    'title': estate_object.css('[data-mark="OfferTitle"]>span::text').get(),
                    'address': address,
                    'price': estate_object.css('[data-mark="MainPrice"]>span::text').get()[:-2],
                    'price_square': estate_object.css('[data-mark="PriceInfo"]::text').get()[:-5],
                    'owner': estate_object.css('._93444fe79c--name-container--enElO>span::text').get(),
                    'link': estate_object.css('[data-name="LinkArea"]>a').attrib['href'],
                }
        self.log(response.request.headers.get("User-Agent"))
