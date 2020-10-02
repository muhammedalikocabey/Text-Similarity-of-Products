# -*- coding: utf-8 -*-
"""
@author: Muhammed
"""

from scraping import Scraper
from text_similarity import TextSimilarity

from flask import Flask, render_template, redirect, url_for, request
import pandas as pd




Scraper = Scraper()
TextSimilarity = TextSimilarity()


app = Flask(__name__)


categories = ["Cep Telefonu", "Dizüstü Bilgisayar", "Tablet"]
###
import time

###

@app.route("/", methods=["GET", "POST"])
def home():  
    return render_template("index.html", categories=categories)
    
    
@app.route("/urun-bilgileri", methods=["POST", "GET"])
def urun_bilgileri():
    if request.method == "POST":
        global category
        category = request.form.get("category_selected")
        
        # urunler_df = pd.read_csv("Tüm_Ürünler.csv")
        # urunler_df.fillna("-", inplace=True)
        
        result_list = Scraper.getAll(category=category)
        urunler_df = result_list[1]
        urunler_df.fillna("-", inplace=True)
        global urunler_df_list
        urunler_df_list = result_list[0]
        
        
        return render_template("urun-bilgileri.html", category=category, urunler_df=urunler_df)
    
    else:
        return render_template(url_for("home"))


@app.route("/urun-karsilastirmasi", methods=["POST", "GET"])        
def urun_karsilastirmasi():
    if request.method == "POST":
        similarity_df = TextSimilarity.get_similarity(urunler_df_list)
        
        similarity_df.sort_values(by=["match_score"], ascending=False, inplace=True)
        
        
        return render_template("urun-karsilastirmasi.html", category=category, similarity_df=similarity_df)
    
    else:
        return render_template(url_for("home"))
    

@app.errorhandler(500)
@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run()