import tinysegmenter
from whooshjp.TinySegmenterTokenizer import TinySegmenterTokenizer
import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
import mysql.connector


def create_en_index(cursor):
    counter = 0
    tk = TinySegmenterTokenizer(tinysegmenter.TinySegmenter())
    schema = Schema(uuid=ID(stored=True), content=TEXT(analyzer=tk, stored=True))
    if not os.path.exists("jp_index"):
        os.mkdir("jp_index")
    # Creating a index writer to add document as per schema
    ix = create_in("jp_index", schema)
    writer = ix.writer()
    cursor.execute("SELECT * FROM jp_wiki")
    result = cursor.fetchall()
    for row in result:
        counter += 1
        if counter % 100 == 0:
            print("Processing data in row %d" % counter)
        writer.add_document(uuid=row[0], content=row[1])
    writer.commit()


if __name__ == '__main__':
    cnx = mysql.connector.connect(user='dist-admin', password='dist-admin',
                                  host='13.231.178.152',
                                  database='distributed_system_2019')
    cursor = cnx.cursor()
    create_en_index(cursor)
