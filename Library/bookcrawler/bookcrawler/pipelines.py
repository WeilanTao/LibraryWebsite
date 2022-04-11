# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
from dataclasses import dataclass

class BookcrawlerPipeline:
    def __init__(self) -> None:
        # connect to mysqk db
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='toor',
            database='Library'
        )
        self.curr = self.conn.cursor()

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute("""SET FOREIGN_KEY_CHECKS = 0;""")
        authoritem = item['authoritem']
        bookitem = item['bookitem']
        chapteritem = item['chapteritem']
        self.store_author(authoritem)
        self.store_book(bookitem)
        self.store_chapter(chapteritem)

    def store_author(self, item):
        # check if the author is in the database
        self.curr.execute(
            """SELECT author_tag FROM Library.books_author WHERE author_tag = %s""",
            (item['author_tag'],))
        myresult = self.curr.fetchall()

        # if author not on the database, insert it
        if not myresult:
            self.curr.execute(""" INSERT INTO Library.books_author VALUES (%s, %s)""",
                              (
                                  item['author_tag'],
                                  item['author_name']
                              ))
            self.conn.commit()

    def store_book(self, item):
        # # check if the book is in the database
        self.curr.execute(
            """SELECT book_tag FROM Library.books_book WHERE book_tag = %s""",
            (item['book_tag'],))
        myresult = self.curr.fetchall()

        # if book not on the database, insert it
        if not myresult:
            self.curr.execute(""" INSERT INTO Library.books_book (book_tag, book_name, author_tag) VALUES (%s, %s, %s)""",
                              (
                                  item['book_tag'],
                                  item['book_name'],
                                  item['author_tag']
                              ))
            self.conn.commit()

    def store_chapter(self, item):
        # check if the chapter is in the database
        self.curr.execute(
            """SELECT chapter_name FROM Library.books_chapter WHERE chapter_index = %s AND book_tag = %s""",
            (item['chapter_index'], item['book_tag']))
        myresult = self.curr.fetchall()

        # # if chapter not on the database, insert it
        if not myresult:
            self.curr.execute(""" INSERT INTO Library.books_chapter (chapter_index, chapter_name,book_tag, chapter_content) VALUES (%s ,%s, %s, %s)""",
                              (
                                  item['chapter_index'],
                                  item['chapter_name'],
                                  item['book_tag'],
                                  item['chapter_content']
                              ))
            self.conn.commit()