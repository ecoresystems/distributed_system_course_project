from flask import Flask
from flask import request, render_template
from flask import jsonify
from .search import searcher
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/doc_search', methods=['GET'])
def search_documents():
    data_source = request.args.get('data_source')
    engine = request.args.get('search_engine')
    key_word_string = request.args.get('key_words')
    limits = request.args.get('limit')
    search_alg = request.args.get('search_algorithm')
    fields = request.args.get('fields')
    search_engine = searcher()
    if data_source == "Japanese Wiki":
        engine = 'Python'
    # print("Receiving request with parameters: %s | %s | %s | %s | %s | %s" % (
    #     data_source, engine, key_word_string, limits, search_alg, fields))
    if engine == 'Python':
        results, runtime, hits = search_engine.search_documents(fields, key_word_string, int(limits), search_alg,
                                                                data_source)
        return_value = jsonify(search_results=results, runtime=runtime, hits=hits)
        print(return_value)
        return jsonify(search_results=results, runtime=runtime, hits=hits)
    if engine == 'GETA':
        results, runtime, hits = search_engine.geta_search(fields, key_word_string, limits, data_source)
        return_value = jsonify(search_results=results, runtime=runtime, hits=hits)
        print(return_value)
        return return_value


if __name__ == '__main__':
    app.run(debug=True)
