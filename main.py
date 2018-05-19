from flask import Flask, render_template, request, session, redirect, url_for
from models import db, TopicClass, Reviews
from forms import TopicSearchForm, reviewPredForm
from sqlalchemy import or_

import numpy as np
import TextClean as tc
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

# from keras.preprocessing import text, sequence
# from keras.models import Model
# from keras.layers import Input, Dense, Embedding, SpatialDropout1D, concatenate, Dropout
# from keras.layers import GRU, Bidirectional, GlobalAveragePooling1D, GlobalMaxPooling1D
# from keras.preprocessing import text, sequence
# from keras.callbacks import Callback, EarlyStopping, ModelCheckpoint


def model_rnn(dropout_rate, GRU_unit, dense_unit):
    
    inp = Input(shape=(maxlen, ))
    x = Embedding(max_features, embed_size, weights=[embedding_matrix], trainable=True)(inp)
    x = SpatialDropout1D(dropout_rate)(x)
    avg_pool0 = GlobalAveragePooling1D()(x)
    max_pool0 = GlobalMaxPooling1D()(x)
    
    x = Bidirectional(GRU(GRU_unit, dropout=dropout_rate, recurrent_dropout=dropout_rate, return_sequences=True))(x)
    x = SpatialDropout1D(dropout_rate)(x)
    avg_pool1 = GlobalAveragePooling1D()(x)
    max_pool1 = GlobalMaxPooling1D()(x)
    
    
    x = Bidirectional(GRU(GRU_unit, dropout=dropout_rate, recurrent_dropout=dropout_rate, return_sequences=True))(x)
    x = SpatialDropout1D(dropout_rate)(x)
    avg_pool2 = GlobalAveragePooling1D()(x)
    max_pool2 = GlobalMaxPooling1D()(x)


    conc = concatenate([avg_pool0, avg_pool1, avg_pool2, max_pool0, max_pool1, max_pool2])
    
    
    outp = Dense(5, activation="softmax")(conc)
    
    model = Model(inputs=inp, outputs=outp)
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    return model

batch_size = 128
epochs = 3
cvscores = []
num_fold = 5
dropout_rate = 0.3
GRU_unit = 64
dense_unit = 128

model = model_rnn(dropout_rate, GRU_unit, dense_unit)
model.load_weights = ('GRU_model-02-0.68.hdf5')


app = Flask(__name__)


POSTGRES = {
    'user': 'postgres',
    'pw': 'Dyn_19900814',
    'db': 'Reviews',
    'host': 'localhost',
    'port': '5432',
}

## setup encoding before each run
# set client_encoding 'utf8'
## sql for getting column types
# where table_name = 'db_reviews';
# select column_name, data_type from information_schema.columns  
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

db.init_app(app)

app.secret_key = "development-key"


# sklearn models loading
clf = joblib.load('My_logisticRegression.pkl') 
tfidf = joblib.load('My_tfidf.pkl') 


@app.route('/', methods=['GET', 'POST'])
def index():
    rf = request.form
    if rf.get('text_input') == None:
        search = TopicSearchForm(rf)
        if request.method == 'POST':
            return search_results(search)
    else:
        text_input = reviewPredForm(rf)
        if request.method == 'POST':
            return predict_star(text_input)
    return render_template('index.html', form1=search, form2=reviewPredForm())

@app.route('/search_results')
def search_results(search):
    search_topic = search.data['select']
    search_name = search.data['search']
    search_star = search.data['star']
    search_begin = search.data['begin_date']
    search_end = search.data['end_date']

    content = Reviews.query.with_entities(Reviews.stars,
     Reviews.topics, Reviews.date, Reviews.name, Reviews.text)

    content = content.filter(Reviews.topics==search_topic, 
     Reviews.name == search_name, Reviews.stars == search_star)

    if search_begin == '' and search_end == '':
        pass
    elif search_begin != '' and search_end == '':
        content = content.filter(Reviews.date >= search_begin)
    elif search_begin == '' and search_end != '':
        content = content.filter(Reviews.date <= search_end)
    else:
        content = content.filter(Reviews.date >= search_begin, 
            Reviews.date <= search_end)

    content = content.order_by(Reviews.stars.desc()).limit(3)

    return render_template("index.html", MyResult=content,
     form1=search, form2=reviewPredForm(), 
     search_name=search_name, search_topic=search_topic)


@app.route('/')
def predict_star(text_input):
    text = text_input.data['text_input']
    text = tc.clean_text(text)
    stars = ''
    stars = clf.predict(tfidf.transform([text]))[0]

    return render_template("index.html", form1=TopicSearchForm(),  
     form2=text_input, UserStar=stars)


if __name__ == "__main__":
  app.run(debug=True)