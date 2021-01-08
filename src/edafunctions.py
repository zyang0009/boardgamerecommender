import pandas as pd

def cleandata(df):
    numdf = df.copy()
    wordsdf = df[['game.id','details.name','details.description','attributes.boardgamecategory','attributes.boardgamemechanic']]
    
    filters_ = ['stats.family*','stats.subtype*', 'attributes.t*','polls.*']
    col_to_drop = ['Unnamed: 0','row_names','details.image','details.thumbnail', 'details.name','details.description', 'game.type', 'stats.median', 'stats.numweights']
    
    for filter_ in filters_:
        numdf.drop(list(numdf.filter(regex = filter_)), axis = 1, inplace=True)
    
    numdf.drop(col_to_drop, axis=1, inplace=True)
    numdf.dropna(axis=0, inplace=True)
    
    return wordsdf, numdf

def get_unique(df):
    df_ = df.apply(lambda x : x.str.split(',| / '))
#     print(df_[:,0])
    list_ = df_.iloc[:,0].to_list()
    flattened_list = []
    for row in list_:
        try:
            for item in row:
                flattened_list.append(item.strip())
        except(TypeError):
            pass
    return set(flattened_list)

def clean_worddata(df):
    df_clean = df.dropna(axis=0) #drops any rows with na
    
    #creates new column 'category' with a list of cateories
    categories_ = df_clean[['attributes.boardgamecategory']].apply(lambda x : x.str.split(',| / '))
    df_clean['category'] = categories_.iloc[:,0]
    del df_clean['attributes.boardgamecategory']
    
    #creates new column 'mechanic' with a list of mechanics
    mechanic_ = df_clean[['attributes.boardgamemechanic']].apply(lambda x : x.str.split(',| / '))
    df_clean['mechanic'] = mechanic_.iloc[:,0]
    del df_clean['attributes.boardgamemechanic']
    
#     #sets game ID as index
#     df_clean.set_index('game.id',drop=True,inplace=True)
    
    #renames dataframe columns
    df_clean.columns = ['game.id','name', 'description','category','mechanic']
    df_clean.reset_index()
    
    return df_clean


def print_features(vectorizer, kmeans):
    features = vectorizer.get_feature_names()
    top_centroids = kmeans.cluster_centers_.argsort()[:,-1:-11:-1]
    print("top features (words) for each cluster:")
    
    
    for num, centroid in enumerate(top_centroids):
        print(f"{num}, {', '.join(features[i] for i in centroid)}")
        text = " ".join(features[i] for i in centroid)
        # Create and generate a word cloud image:
        wordcloud = WordCloud(width=400, height=400).generate(text)

        # Display the generated image:
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()

def extract_bow_from_raw_text(text_as_string):
    """Extracts bag-of-words from a raw text string.

    Parameters
    ----------
    text (str): a text document given as a string

    Returns
    -------
    list : the list of the tokens extracted and filtered from the text
    """
    if (text_as_string == None):
        return []

    if (len(text_as_string) < 1):
        return []
    numpattern = r'[0-9]'
    text_as_string = re.sub(numpattern, '', text_as_string)
    
    COMMON_WORDS = ["game","point","board","player","rule","turn","tile","card","deck","hand","points","victory","win","lose","defeat"]

    sent_tokens = sent_tokenize(text_as_string)

    tokens = list(map(word_tokenize, sent_tokens))

    sent_tags = list(map(pos_tag, tokens))

    grammar = r"""
        SENT: {<(J|N).*>}                # chunk sequences of proper nouns
    """

    cp = RegexpParser(grammar)
    ret_tokens = list()
    stemmer_snowball = SnowballStemmer('english')
    lemmatizer = WordNetLemmatizer()

    for sent in sent_tags:
        tree = cp.parse(sent)
        for subtree in tree.subtrees():
            if subtree.label() == 'SENT':
                t_tokenlist = [tpos[0].lower() for tpos in subtree.leaves()]
                
                t_tokens_lemmatize = list(map(lemmatizer.lemmatize, t_tokenlist))
                t_tokens_stemsnowball = list(map(stemmer_snowball.stem, t_tokens_lemmatize))
                #t_token = "-".join(t_tokens_stemsnowball)
                #ret_tokens.append(t_token)
#                 ret_tokens.extend(t_tokens_lemmatize)
                ret_tokens.extend(t_tokens_stemsnowball)
            #if subtree.label() == 'V2V': print(subtree)
    #tokens_lower = [map(string.lower, sent) for sent in tokens]
    for i in range(0,len(ret_tokens)):
        if ret_tokens[i] in COMMON_WORDS:
            ret_tokens[i] = ""
    return(' '.join(ret_tokens))