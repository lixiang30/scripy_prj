# -*- coding: utf-8 -*-
import scrapy
from urllib import request
from PIL import Image
"""
formdata = {
    source: None
    redir: https://www.douban.com/
    form_email: 534551900@qq.com
    form_password: xxxxxx
    captcha-solution: because
    captcha-id: 5pzGRb6vHeS8g7ONfQ0k9zGy:en
    remember: on
    login: 登录
    }
"""

#  获取验证码图片链接，并打印出来
# class DoubanSpider(scrapy.Spider):
#     name = 'douban'
#     allowed_domains = ['douban.com']
#     start_urls = ['https://accounts.douban.com/login']
#
#     def parse(self, response):
#         formdata = {
#             'source':'None',
#             'redir':'https://www.douban.com/',
#             'form_email':'534551900@qq.com',
#             'form_password':'xxxxxx',
#             'remember':'on',
#             'login':'登录',
#         }
#         captcha_img = response.css('img#captcha_image::attr(src)').get()
#         print("="*30)
#         print(captcha_img)


# class DoubanSpider(scrapy.Spider):
#     name = 'douban'
#     allowed_domains = ['douban.com']
#     start_urls = ['https://accounts.douban.com/login']
#     login_url = 'https://accounts.douban.com/login'
#
#     def parse(self, response):
#         formdata = {
#             'source':'None',
#             'redir':'https://www.douban.com/',
#             'form_email':'534551900@qq.com',
#             'form_password':'xxxx',
#             'remember':'on',
#             'login':'登录',
#         }
#         captcha_url = response.css('img#captcha_image::attr(src)').get()
#         if captcha_url:
#             captcha = self.regonize_captcha(captcha_url)
#             formdata['captcha-solution'] = captcha
#             captcha_id = response.xpath("//input[@name='captcha-id']/@value").get()
#             formdata['captcha_id'] = captcha_id
#         yield scrapy.FormRequest(url=self.login_url,formdata=formdata,callback=self.parse_after_login)
#
#
#     def parse_after_login(self,response):
#         if response.url == 'https://www.douban.com/':
#             print("登陆成功了")
#         else:
#             print("登录失败了")
#
#
#
#     def regonize_captcha(self,image_url):
#         request.urlretrieve(image_url,'captcha.png')
#         image = Image.open('captcha.png')
#         image.show()
#         captcha = input("请输入验证码:")
#         return captcha

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://accounts.douban.com/login']
    login_url = 'https://accounts.douban.com/login'
    profile_url = 'https://www.douban.com/people/160520352/'
    editsignature_url = 'https://www.douban.com/people/160520352/edit_signature'

    def parse(self, response):
        formdata = {
            'source':'None',
            'redir':'https://www.douban.com/',
            'form_email':'534551900@qq.com',
            'form_password':'xxxx',
            'remember':'on',
            'login':'登录',
        }
        captcha_url = response.css('img#captcha_image::attr(src)').get()
        if captcha_url:
            captcha = self.regonize_captcha(captcha_url)
            formdata['captcha-solution'] = captcha
            captcha_id = response.xpath("//input[@name='captcha-id']/@value").get()
            formdata['captcha_id'] = captcha_id
        yield scrapy.FormRequest(url=self.login_url,formdata=formdata,callback=self.parse_after_login)


    def parse_after_login(self,response):
        # if response.url == 'https://www.douban.com/':
        #     print("登陆成功了")
        # else:
        #     print("登录失败了")
        account = response.xpath('//a[@class="bn-more"]/span/text()').extract_first()
        if account is None:
            print("登录失败")
        else:
            print("登录成功")
            yield scrapy.Request(self.profile_url)

    def parse_profile(self,response):
        print(response.url)
        if response.url == self.profile_url:
            print("进入到了个人中心")
            ck = response.xpath("//input[@name='ck']/@value").get()
            formdata = {
                'ck':ck,
                'signature':'测试签名．测试签名'
            }
            yield scrapy.FormRequest(self.editsignature_url,formdata=formdata)
        else:
            print("没有进入到个人中心")


    def regonize_captcha(self,image_url):
        request.urlretrieve(image_url,'captcha.png')
        image = Image.open('captcha.png')
        image.show()
        captcha = input("请输入验证码:")
        return captcha



