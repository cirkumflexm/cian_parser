import scrapy


class CianSpider(scrapy.Spider):
    name = "cian"

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
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for estate_object in response.css('[data-name="CardComponent"]'):
            address_list = estate_object.css('[data-name="GeoLabel"]::text').getall()
            address = ', '.join(address_list)
            yield {
                'title': estate_object.css('[data-mark="OfferTitle"]>span::text').get(),
                'address': address,
                'price': estate_object.css('[data-mark="MainPrice"]>span::text').get(),
                'price_square': estate_object.css('[data-mark="PriceInfo"]::text').get(),
            }
        self.log(response.request.headers.get("User-Agent"))
