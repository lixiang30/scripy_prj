
from scrapy import cmdline
# cmdline.execute("scrapy crawl qsbk_spider".split()) # 等价于下面这种写法
cmdline.execute(["scrapy","crawl","qsbk_spider"])