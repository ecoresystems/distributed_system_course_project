from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.index import open_dir
import subprocess
import mysql.connector
import time
import os
from whoosh.filedb.filestore import FileStorage



class searcher(object):
    def __init__(self):
        pass

    def search_documents(self, fields, query_str, item_count, weighting_alg, data_source):
        print(
            "Receiving Request Paras: %s | %s | %s | %s | %s" % (
                fields, query_str, item_count, weighting_alg, data_source))
        results_list = []
        w = scoring.Frequency
        if weighting_alg == 'TF-IDF':
            w = scoring.TF_IDF
        if weighting_alg == 'Frequency':
            w = scoring.Frequency
        if weighting_alg == 'BM25F':
            w = scoring.BM25F()
        if data_source == 'US Financial News':
            storage = FileStorage("/var/www/distApp/distApp/en_index")
            ix = storage.open_index()
            with ix.searcher(weighting=w) as searcher:
                query = QueryParser(fields.lower(), ix.schema).parse(query_str)
                results = searcher.search(query, limit=item_count)
                for i in range(results.scored_length()):
                    print(results[i]['title'], str(results[i].score), results[i]['url'])
                    results_list.append(
                        {"title": results[i]['title'], "score": results[i].score, "content": results[i]['content'],
                         "url": results[i]['url'], "uuid": results[i]['uuid']})
        elif data_source == 'Japanese Wiki':
            ix = open_dir("/var/www/distApp/distApp/jp_index")
            with ix.searcher(weighting=w) as searcher:
                query = QueryParser('content', ix.schema).parse(query_str)
                results = searcher.search(query, limit=item_count)
                for i in range(results.scored_length()):
                    print(results[i].score, results[i]['content'])
                    title = str(results[i]['content']).split('は')[0]
                    title = title.split('と')[0]
                    results_list.append(
                        {"score": results[i].score, "title": title, "content": results[i]['content'],
                         "uuid": results[i]['uuid']})
        return results_list, results.runtime, results.scored_length()

    #
    # search_documents("title", "technology", 10, 'BM25F')
    def geta_search(self, fields, query_str, item_count, data_source):
        print("%s | %s | %s | %s on GETA" % (fields.lower(), query_str, item_count, data_source))
        if data_source == 'US Financial News':
            print("This gets executed")
            if fields == 'Content':
                fields = 'text'
            start_time = time.time()
            cnx = mysql.connector.connect(user='dist-admin', password='dist-admin',
                                          host='localhost',
                                          database='distributed_system_2019')
            cursor = cnx.cursor(buffered=True)
            os.chdir('/var/www/distApp/distApp')
            print("The current work directory is: %s" % os.getcwd())
            process = subprocess.Popen(
                "perl search.pl -q %s -n %s -d us_financial_%s" % (query_str, item_count, fields.lower()),
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE, shell=True)
            print(fields)
            process1 = subprocess.Popen(
                "perl searchWord.pl -q %s -n %s -d us_financial_%s" % (query_str, item_count, fields.lower()),
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE, shell=True)
            out, err = process.communicate()
            out1, err1 = process1.communicate()
            search_res = out.decode('utf-8')
            searchWord_res = out1.decode('utf-8')
            uuid_list = []
            weight_list = []
            score_list = []
            word_list = []
            for row in search_res.split('\n'):
                if row != '':
                    uuid_list.append(row)
            for row in searchWord_res.split('\n'):
                if row != '':
                    weight_list.append(row.split(' ')[0])
                    score_list.append(row.split(' ')[1])
                    word_list.append(row.split(' ')[2])
            res = []
            result_list = []
            for uuid in uuid_list:
                query = 'SELECT * FROM us_financial WHERE UUID=\'%s\'' % uuid
                cursor.execute(query)
                res.append(cursor.fetchone())
            print(res)
            for index, row in enumerate(res):
                result_list.append({"score": score_list[index], "url": row[1], "title": row[2], "content": row[3],
                                    "uuid": row[0]})
            return result_list, time.time() - start_time, len(result_list)
