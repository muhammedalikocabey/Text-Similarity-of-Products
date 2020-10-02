# -*- coding: utf-8 -*-
"""
@author: Muhammed Ali Kocabey
"""

import pandas as pd
import numpy as np

import spacy


class TextSimilarity():
    def __init__(self):
        pass
    
    def levenshtein(self, seq1, seq2):
        size_x = len(seq1) + 1
        size_y = len(seq2) + 1
        matrix = np.zeros ((size_x, size_y))
        for x in range(size_x):
            matrix [x, 0] = x
        for y in range(size_y):
            matrix [0, y] = y
    
        for x in range(1, size_x):
            for y in range(1, size_y):
                if seq1[x-1] == seq2[y-1]:
                    matrix [x,y] = min(
                        matrix[x-1, y] + 1,
                        matrix[x-1, y-1],
                        matrix[x, y-1] + 1
                    )
                else:
                    matrix [x,y] = min(
                        matrix[x-1,y] + 1,
                        matrix[x-1,y-1] + 1,
                        matrix[x,y-1] + 1
                    )
    
        return (matrix[size_x - 1, size_y - 1])
    
    
    
    def sorted_levenshtein_rate(self, seq1, seq2):
        product1 = ''.join(sorted(seq1))
        product2 = ''.join(sorted(seq2))
        distance = self.levenshtein(product1, product2)
        max_len = max(len(product1), len(product2))
        return 1-(distance/max_len)
    
    
    
    def levenshtein_rate(self, product1, product2):
        distance = self.levenshtein(product1, product2)
        max_len = max(len(product1), len(product2))
        return 1 - (distance / max_len)
    
    def jaccard_similarity(self, str1, str2): 
        a = set(str1.split()) 
        b = set(str2.split())
        c = a.intersection(b)
        return float(len(c)) / (len(a) + len(b) - len(c))
    
    # def get_word_embedding_similarity(self, str1, str2):
    #     nlp = spacy.load("en_core_web_md")  # make sure to use larger model!

    #     doc1 = nlp(str(str1))
    #     doc2 = nlp(str(str2))
        
    #     sim = doc1.similarity(doc2)
        
    #     return sim
    
        
    def get_similarity(self, all_df_list):
        marka_1_list = list()
        marka_2_list = list()
        levenshtein_distance_list = list()
        match_score_list = list()
        sorted_levenshtein_rate_list = list()
        jaccard_similarity_list = list()
        # word_embedding_similarity_list = list()
    
        
        similarity_df = pd.DataFrame()
        for X in range(0, len(all_df_list)):
            for Y in range(X+1, len(all_df_list)):
                site_X = all_df_list[X].copy()
                site_Y = all_df_list[Y].copy()
                
                for ind_1 in range(0, len(site_X)):
                    for ind_2 in range(ind_1+1, len(site_Y)):
                        marka_1_list.append(site_X.loc[ind_1, "ürün_ismi"])
                        marka_2_list.append(site_Y.loc[ind_2, "ürün_ismi"])
                        levenshtein_distance_list.append(self.levenshtein_rate(site_X.loc[ind_1, "ürün_ismi"], site_Y.loc[ind_2, "ürün_ismi"]))
                        match_score_list.append(self.levenshtein_rate(site_X.loc[ind_1, "ürün_ismi"], site_Y.loc[ind_2, "ürün_ismi"]))
                        sorted_levenshtein_rate_list.append(self.sorted_levenshtein_rate(site_X.loc[ind_1, "ürün_ismi"], site_Y.loc[ind_2, "ürün_ismi"]))
                        jaccard_similarity_list.append(self.jaccard_similarity(site_X.loc[ind_1, "ürün_ismi"], site_Y.loc[ind_2, "ürün_ismi"]))
                        # word_embedding_similarity_list.append(self.get_word_embedding_similarity(site_X.loc[ind_1, "ürün_ismi"], site_Y.loc[ind_2, "ürün_ismi"]))
        
        similarity_df["marka_1"] = marka_1_list
        similarity_df["marka_2"] = marka_2_list
        similarity_df["levenshtein_distance"] = levenshtein_distance_list
        similarity_df["sorted_levenshtein_rate"] = sorted_levenshtein_rate_list
        similarity_df["match_score"] = match_score_list
        similarity_df["jaccard_similarity"] = jaccard_similarity_list
        # similarity_df["word_embedding_similarity"] = word_embedding_similarity_list
        
        return similarity_df
        
    