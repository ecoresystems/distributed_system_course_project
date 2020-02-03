import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
import mysql.connector


def create_en_index(cursor):
    counter = 0
    schema = Schema(uuid=ID(stored=True), title=TEXT(stored=True), content=TEXT(stored=True),
                    url=TEXT(stored=True), published=TEXT(stored=True))
    if not os.path.exists("en_index"):
        os.mkdir("en_index")
    # Creating a index writer to add document as per schema
    ix = create_in("en_index", schema)
    writer = ix.writer()
    cursor.execute("SELECT * FROM us_financial")
    result = cursor.fetchall()
    for row in result:
        counter += 1
        if counter % 100 == 0:
            print("Processing data in row %d" % counter)
        writer.add_document(uuid=row[0], url=row[1], title=row[2], content=row[3], published=row[4])
    writer.commit()


if __name__ == '__main__':
    cnx = mysql.connector.connect(user='dist-admin', password='dist-admin',
                                  host='13.231.178.152',
                                  database='distributed_system_2019')
    cursor = cnx.cursor()
    create_en_index(cursor)
