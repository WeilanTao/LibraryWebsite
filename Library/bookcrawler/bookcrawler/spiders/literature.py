import time
import scrapy 

import json
from bookcrawler.items import AuthorItem, BookItem, ChapterItem

class LiteratureSpider(scrapy.Spider):
    name = 'literature'
    start_urls = [
        'https://www.literature.org/authors/contents.json']

    url = 'https://www.literature.org/authors/%scontents.json'

    def __init__(self, name=None, **kwargs):
        self.start_time = time.time()

    def parse(self, response):
        # extract all the authors
        author_list = json.loads(response.text)['authors']

        for author in author_list:
            # book_page_url:
            authoritem = AuthorItem()
            bookitem = BookItem()
            chapteritem = ChapterItem()

            authoritem['author_name'] = author['name'].title().lstrip().rstrip()
            authoritem['author_tag'] = author['href'].strip()

            book_page_url = format(self.url % (author['href']+'/'))
            # Parse the author page
            yield scrapy.Request(url=book_page_url, callback=self.parse_book_page,
             meta={'authoritem': authoritem.copy(), 'bookitem' : bookitem.copy(),'chapteritem' :chapteritem.copy()})

    def parse_book_page(self, response):
        authoritem = response.meta['authoritem']
        bookitem=response.meta['bookitem']
        chapteritem = response.meta['chapteritem']

        author_name = authoritem['author_name']
        author_tag = authoritem['author_tag']

        # get the book list of an author:
        book_list_json = json.loads(response.text)
        book_list = []

        try:
            if 'books' in book_list_json:
                book_list = book_list_json['books']
            elif 'chapters' in book_list_json:
                book_list = book_list_json['chapters']
        except KeyError as err:
            print("Key Error for author: ", author_name, err)

        # for each book of an other, Parse the book page
        for book in book_list:
            book_tag = book['href'].strip()

            bookitem['book_name'] = book['title'].title().lstrip().rstrip()
            bookitem['book_tag'] = book_tag
            bookitem['author_tag']=author_tag

            book_content_url = format(
                self.url % (author_tag+'/'+book_tag+'/'))

            yield scrapy.Request(url=book_content_url, callback=self.parse_book_content, meta={'authoritem': authoritem.copy(),'bookitem':bookitem.copy(),'chapteritem':chapteritem.copy()})

    def parse_book_content(self, response):
        authoritem = response.meta['authoritem']
        bookitem=response.meta['bookitem']
        chapteritem = response.meta['chapteritem']


        author_tag = authoritem['author_tag']
        book_tag = bookitem['book_tag']

        # print(item['book_name'])

        chapter_json = json.loads(response.text)
        chapters = chapter_json['chapters']

        # parse book content
        for chapter in chapters:
            chapter_href = chapter['href']
            chapter_name = chapter['title'].title(
            ).lstrip().rstrip().replace('-', '')

            chapter_url = 'https://www.literature.org/authors/' + \
                author_tag+'/'+book_tag+'/'+chapter_href
            
            chapteritem['chapter_index'] = chapter_href
            chapteritem['chapter_name'] = chapter_name
            chapteritem['book_tag']= book_tag
            yield scrapy.Request(url=chapter_url, callback=self.parse_chapter,  
            meta={'authoritem': authoritem.copy(),'bookitem':bookitem.copy(),'chapteritem':chapteritem.copy()})

    def parse_chapter(self, response):
        authoritem = response.meta['authoritem']
        bookitem=response.meta['bookitem']
        chapteritem = response.meta['chapteritem']

        # parse chapter content
        chapter_content = ''.join(response.xpath('//article//text()').getall())

        # print(item['chapter_name'])
        chapteritem['chapter_content'] = chapter_content.lstrip().rstrip()
        

        transitem ={}
        transitem['authoritem'] = authoritem
        transitem['bookitem']=bookitem
        transitem['chapteritem']=chapteritem

        # pass item to the pipline
        yield transitem

    def closed(self, spider):
        print(time.time() - self.start_time)

