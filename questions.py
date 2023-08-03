import os
import nltk
import sys
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """

    files_dict = dict()

    for file in os.listdir(directory):
        if file.endswith(".txt"):
            file_path = os.path.join(directory, file)
            with open(file_path, 'r') as f:
                file_value = f.read()
                files_dict[file] = file_value

    return files_dict


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words_list = []
    document = document.lower()

    word_tokens = nltk.tokenize.word_tokenize(document.lower())
    
    for word in word_tokens:
        if word in string.punctuation:
            continue

        if word in nltk.corpus.stopwords.words("english"):
            continue
        
        ok = 0
        for char in word:
            if char not in string.punctuation:
                ok = 1
                break
        if ok:
            words_list.append(word)
    
    return words_list


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    num_of_doccuments = len(documents)

#    print(documents)
    idfs_dict = dict()
    for file in documents:
        for word in documents[file]:
            if word not in idfs_dict:
                idfs_dict[word] = set()
                idfs_dict[word].add(file)
            else:
                if file not in idfs_dict[word]:
                    idfs_dict[word].add(file)


    #print(idfs_dict)
    #print(idfs_dict['index'])
    for word in idfs_dict:
        idfs_dict[word] = math.log(num_of_doccuments / len(idfs_dict[word]))
    
    #print(idfs_dict)
    return idfs_dict


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    #print(query)
    tf_idf_dict = dict()
    query_word_count_dict = dict()

    ### Counting word_cont in a file
    for query_word in query:
        for file in files:
            for file_word in files[file]:
                if file_word == query_word:
                    if query_word not in query_word_count_dict:
                        query_word_count_dict[query_word] = dict()
                        if file not in query_word_count_dict[query_word]:
                            query_word_count_dict[query_word][file] = 1
                        else:
                            query_word_count_dict[query_word][file] += 1
                    else:
                        if file not in query_word_count_dict[query_word]:
                            query_word_count_dict[query_word][file] = 1
                        else:
                            query_word_count_dict[query_word][file] += 1
    

    for file in files:
        tf_idf_dict[file] = 0

    ### Counting tf-idf
    for query_word in query:
        if query_word in query_word_count_dict:
            for file in query_word_count_dict[query_word]:
                tf_idf_dict[file] += query_word_count_dict[query_word][file] * idfs[query_word]
        
    #print(idfs["neural_network.txt"])
    #print("query word dict: ", query_word_count_dict)
    

    tf_ids_dict_list = []

    for file in tf_idf_dict:
        tf_ids_dict_list.append([file, tf_idf_dict[file]])
    #print(tf_ids_dict_list)

    ## Sorting
    tf_ids_dict_list.sort(key=lambda x: x[1])

    ## Reversing
    ret_list = []
    for i in range(len(tf_ids_dict_list)):
        ret_list.append(tf_ids_dict_list[len(tf_ids_dict_list) -i - 1][0])

    #print(tf_ids_dict_list)
    #print(ret_list)
    return ret_list[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    #print(query)
    sentence_idfs_dict = dict()

    for sentence in sentences:
        if sentence not in sentence_idfs_dict:
            sentence_idfs_dict[sentence] = dict()
            sentence_idfs_dict[sentence]['idfs'] = 0
            sentence_idfs_dict[sentence]['q_density'] = 0
        for word in query:
            if word in sentences[sentence]:
                sentence_idfs_dict[sentence]['idfs'] += idfs[word]
                sentence_idfs_dict[sentence]['q_density'] += 1/len(sentences[sentence])

    sentence_idfs_list = []
    for sentence in sentence_idfs_dict:
        sentence_idfs_list.append([sentence, sentence_idfs_dict[sentence]['idfs'],sentence_idfs_dict[sentence]['q_density'] ])

    sorted_list = sorted(sentence_idfs_list, key=lambda x : (x[1], x[2]))
    #sentence_idfs_list.sort(key= lambda x: x[1], )
    
    sorted_list.reverse()
    #print(sentence_idfs_dict)
    # for sent in sorted_list:
    #     print(sent)
    ret_sentences = []
    for i in range(len(sorted_list)):
        ret_sentences.append(sorted_list[i][0])
    #print(sorted_list)

    #print(ret_sentences)
    return ret_sentences[:n]


if __name__ == "__main__":
    main() 
