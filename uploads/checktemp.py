def ru():
    import os
    from difflib import SequenceMatcher
    import pandas as pd
    from tabulate import tabulate
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.feature_extraction.text import CountVectorizer

    
    student_files = [doc for doc in os.listdir() if doc.endswith('.txt')]
    student_notes = [open(file, encoding='utf-8').read() for file in student_files ]
    print(sorted(student_files))
          
    def vectorize(Text): return TfidfVectorizer().fit_transform(Text).toarray()
    def similarity(doc1, doc2): return cosine_similarity([doc1, doc2])


    vectors = vectorize(student_notes)
    s_vectors = list(zip(student_files, vectors))
    plagiarism_results = set()
    match_result = set()

    for student_a, text_vector_a in s_vectors:
        new_vectors = s_vectors.copy()
        current_index = new_vectors.index((student_a, text_vector_a))
        del new_vectors[current_index]
        for student_b, text_vector_b in new_vectors:
            sim_score = similarity(text_vector_a, text_vector_b)[0][1]
            match_score = SequenceMatcher(None,text_vector_a,text_vector_b).ratio()*100
            
            student_pair = sorted((student_a, student_b))
            score = (student_pair[0], student_pair[1], sim_score)
            plagiarism_results.add(score)
            match_result.add(match_score)
#            print(match_result)
            
    if(len(student_files)<2):
        print('Add more files')
    else:
        print("\nThe cosine similarity of all the files are as follows:\n")
        df = pd.DataFrame(plagiarism_results,columns = ['File1','File2','Similarity'])
        print(tabulate(df,headers = 'keys',tablefmt='psql'))
       
        


ru()      



