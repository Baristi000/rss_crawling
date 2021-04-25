class Setting():
    urls:dict = {
        "https://tools.cdc.gov/api/v2/resources/media/404952.rss":"covid",
#        "https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q=CORONA+OR+COVID19":"google_rss_feed"
    }
    elastic_host:str = "tstsv.ddns.net"
    elastic_port:int = 9200

setting = Setting()