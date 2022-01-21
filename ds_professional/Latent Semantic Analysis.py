# Databricks notebook source
# MAGIC %md # Latent Semantic Analysis
# MAGIC 
# MAGIC Before we begin, let's define some basic vocabulary. 
# MAGIC 
# MAGIC **Natural language processing** refers to a family of techniques used to derive meaning from text data.
# MAGIC 
# MAGIC A **document** refers to some collection of words and represents the instances or "rows" of our dataset. 
# MAGIC 
# MAGIC A **body** is a collection of documents and is our entire data set.
# MAGIC 
# MAGIC A **dictionary** is the set of all words that appear in at least one document in our body.
# MAGIC 
# MAGIC A **topic** is a collection of words that co-occur.
# MAGIC 
# MAGIC The word **latent** means hidden. In this context, we are referring to features that are "hidden" in the data. That they are hidden referes to the fact that they can not be directly measured. These latent features are essential to the data, but are not the orginal features of the data set.

# COMMAND ----------

# MAGIC %md **Latent Semantic Analysis (LSA)** is:
# MAGIC 
# MAGIC - a natural language processing technique
# MAGIC - an unsupervised learning technique
# MAGIC - aims to create representations of the documents in a body based on the topics inherent to that body
# MAGIC - reducing the dimensionality of a text-based dataset
# MAGIC - consists of two steps:
# MAGIC    - creating a document-term matrix
# MAGIC    - dimensionality reduction via a singular value decomposition

# COMMAND ----------

# MAGIC %md ## Document-Term Matrix
# MAGIC 
# MAGIC A basic idea of a Document-Term Matrix is that documents can be represented as points in Euclidean space aka **vectors**.
# MAGIC 
# MAGIC Here is an example of a document-term matrix.
# MAGIC 
# MAGIC ![](https://www.evernote.com/l/AAE9rZErr9BCcLX-wE6dpPbqNTsxKNmxH3UB/image.png)
# MAGIC 
# MAGIC Here, each document is a simple statement describing the nature of a canine and defines the rows of our matrix. The dictionary defines the columns of our matrix.

# COMMAND ----------

# MAGIC %md #### Documents as Vectors
# MAGIC 
# MAGIC According to this Document-Term matrix,
# MAGIC 
# MAGIC $$\text{"the quick brown fox"} = (1,0,1,0,1,0,0,1,0)$$
# MAGIC $$\text{"the slow brown dog"}  = (1,1,0,0,0,0,1,1,0)$$
# MAGIC $$\text{"the quick red dog"}   = (0,1,0,0,1,1,0,1,0)$$
# MAGIC $$\text{"the lazy yellow fox"} = (0,0,1,1,0,0,0,1,1)$$

# COMMAND ----------

# MAGIC %md ## Singular Value Decomposition
# MAGIC 
# MAGIC The Singular Value Decomposition (SVD) 
# MAGIC 
# MAGIC - is similar to a Principal Component Analysis
# MAGIC - reduces the dimension of the original data
# MAGIC - transforms the data to be encoded using latent, or hidden, variables
# MAGIC - for LSA, these latent variables represent topics

# COMMAND ----------

# MAGIC %md ## Implementation in Scikit-Learn
# MAGIC 
# MAGIC We will first demonstrate a trivial implementation using the Python library, [Scikit-Learn](https://scikit-learn.org/stable/).
# MAGIC 
# MAGIC ![](https://www.evernote.com/l/AAGiYGcKcIxIaJ7sCg97K9JDtUO2dY9mywoB/image.png)

# COMMAND ----------

# MAGIC %md ### Raw Text Data
# MAGIC 
# MAGIC <img src="https://www.evernote.com/l/AAFfAyDQQ1xGPLTIxT2hcUSLrHuQDbYzsuYB/image.png" width=600px>
# MAGIC 
# MAGIC Here each line of text is a **document** and the collection of all lines of text is the **body**.

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC One advantage of working in databricks is that the Databricks Runtime for ML contains many popular machine learning libraries, including Scikit-Learn, TensorFlow, and XGBoost. We will the Databricks Runtime for ML to implement our Latent Semantic Analysis in Scikit-Learn.

# COMMAND ----------

body = [
    "the quick brown fox",
    "the slow brown dog",
    "the quick red dog",
    "the lazy yellow fox"
]

# COMMAND ----------

# MAGIC %md ### Document-Term Matrix
# MAGIC 
# MAGIC <img src="https://www.evernote.com/l/AAFtjaKOjT5CYr5N_NPHKU6vpBWNnBgbWLIB/image.png" width=600px>
# MAGIC 
# MAGIC The Document-Term Matrix can be created using the `CountVectorizer` model [[doc]](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html) in Scikit-Learn.

# COMMAND ----------

from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer()
bag_of_words = vectorizer.fit_transform(body)

# COMMAND ----------

# MAGIC %md 
# MAGIC 
# MAGIC This process has converted each **document** into a vector. The matrix consists of a vector for each "document" in the **body**.
# MAGIC 
# MAGIC $$\text{"the quick brown fox"} = (1,0,1,0,1,0,0,1,0)$$
# MAGIC $$\text{"the slow brown dog"}  = (1,1,0,0,0,0,1,1,0)$$
# MAGIC $$\text{"the quick red dog"}   = (0,1,0,0,1,1,0,1,0)$$
# MAGIC $$\text{"the lazy yellow fox"} = (0,0,1,1,0,0,0,1,1)$$

# COMMAND ----------

bag_of_words.todense()

# COMMAND ----------

# MAGIC %md ### Singular Value Decomposition
# MAGIC 
# MAGIC <img src="https://www.evernote.com/l/AAEhTiOBufhPwKBx-Hgufx4XZ5XyfsCp8cMB/image.png" width=600px>
# MAGIC 
# MAGIC This can be achieved using the `TruncatedSVD` model. 
# MAGIC 
# MAGIC The function is named "truncated" SVD because it is capable of returning a dataset with fewer features than it is passed without significant loss of information, that is, it is great for reducing the dimension of data.

# COMMAND ----------

from sklearn.decomposition import TruncatedSVD

svd = TruncatedSVD(n_components=2)
lsa = svd.fit_transform(bag_of_words)

# COMMAND ----------

# MAGIC %md ### Topic Encoded Data
# MAGIC 
# MAGIC <img src="https://www.evernote.com/l/AAGhSgfs1nZHAIYfbnmNaHU8YjMV2i9fTmgB/image.png" width=600px>
# MAGIC 
# MAGIC The process transforms the original data into **topic-encoded data**.
# MAGIC 
# MAGIC Here, each row is indexed by its original text value. The data now consists of two columns of data one representing each of the two topics used to encode the **body**. Recall that this value of 2 was passed as an argument to the `TruncatedSVD` in the previous step. 

# COMMAND ----------

import pandas as pd

topic_encoded_df = pd.DataFrame(lsa, columns = ["topic_1", "topic_2"])
topic_encoded_df["body"] = body
display(topic_encoded_df[["body", "topic_1", "topic_2"]])

# COMMAND ----------

# MAGIC %md ## Byproducts of the Latent Semantic Analysis
# MAGIC 
# MAGIC The LSA generates a few byproducts that are useful for analysis:
# MAGIC 
# MAGIC - the **dictionary** or the set of all words that appear at least once in the **body**
# MAGIC - the **encoding matrix** used to encode the documents into topics. The **encoding matrix** can be studied to gain an understanding of the **topics** that are latent to the **body**. 

# COMMAND ----------

# MAGIC %md #### The Dictionary
# MAGIC 
# MAGIC The dictionary is an attribute of a fit `CountVectorizer` model and can be accessed using the `.get_feature_names` method.

# COMMAND ----------

dictionary = vectorizer.get_feature_names()
dictionary

# COMMAND ----------

# MAGIC %md #### The Encoding Matrix
# MAGIC 
# MAGIC The **encoding matrix** is comprised of the `components_` stored as an attribute of a fit `TruncatedSVD`. We can examine this matrix to gain an understanding of the **topics** latent to the **body**.
# MAGIC 
# MAGIC **Note:** in `sklearn`, attributes of a model that are generated by a fitting process have a trailing underscore in their name as can be seen here with `svd.components_`. 

# COMMAND ----------

encoding_matrix = pd.DataFrame(svd.components_,
                               index=['topic_1', 'topic_2'],
                               columns=dictionary).T
encoding_matrix

# COMMAND ----------

# MAGIC %md #### Interpret The Encoding Matrix
# MAGIC 
# MAGIC What are the top words for each topic? What dimensions in word-space explain most of the variance in the data? 
# MAGIC 
# MAGIC To analyze this, we will need to look at the *absolute value* of the expression of each word in the topic. 

# COMMAND ----------

import numpy as np

encoding_matrix['abs_topic_1'] = np.abs(encoding_matrix['topic_1'])
encoding_matrix['abs_topic_2'] = np.abs(encoding_matrix['topic_2'])
encoding_matrix.sort_values('abs_topic_1', ascending=False)

# COMMAND ----------

encoding_matrix.sort_values('abs_topic_2', ascending=False)

# COMMAND ----------

# MAGIC %md ## Latent Semantic Analysis of Two Poems

# COMMAND ----------

# MAGIC %md **Latent Semantic Analysis (LSA)** is:
# MAGIC 
# MAGIC - a natural language processing technique
# MAGIC - an unsupervised learning technique
# MAGIC - aims to create representations of the documents in a body based on the topics inherent to that body
# MAGIC - reducing the dimensionality of a text-based dataset
# MAGIC - consists of two steps:
# MAGIC    - creating a document-term matrix
# MAGIC    - dimensionality reduction via a singular value decomposition
# MAGIC 
# MAGIC ![](https://www.evernote.com/l/AAGiYGcKcIxIaJ7sCg97K9JDtUO2dY9mywoB/image.png)

# COMMAND ----------

# MAGIC %md ### Raw Text Data
# MAGIC 
# MAGIC <img src="https://www.evernote.com/l/AAFfAyDQQ1xGPLTIxT2hcUSLrHuQDbYzsuYB/image.png" width=600px>
# MAGIC 
# MAGIC Here each line of text from a book is a **document** and the collection of all lines of text from the two books is the **body**.

# COMMAND ----------

import urllib
import sys

if sys.version[0] == "3":
  retrieve = urllib.request.urlretrieve
else:
  rerieve = urllib.urlretrieve
  
retrieve("https://files.training.databricks.com/classes/lsa-videos/body.csv","/dbfs/tmp/body.csv")
bodyDF = (spark.read
  .option("header", "true")
  .csv("/tmp/body.csv"))
display(bodyDF)


# COMMAND ----------

body_df = bodyDF.toPandas()
sample_df = body_df.sample(5)
sample_indices = sample_df.index
display(sample_df)

# COMMAND ----------

# MAGIC %md ### Document-Term Matrix
# MAGIC 
# MAGIC <img src="https://www.evernote.com/l/AAFtjaKOjT5CYr5N_NPHKU6vpBWNnBgbWLIB/image.png" width=600px>
# MAGIC 
# MAGIC Again, we use `CountVectorizer`, now with a few more arguments:
# MAGIC 
# MAGIC - `min_df` signifies the number of documents in which a term must appear in order for it to be counted
# MAGIC - You can view the `english` `stop_words` here: https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/feature_extraction/stop_words.py
# MAGIC 
# MAGIC Note that `CountVectorizer` returns a [sparse](https://en.wikipedia.org/wiki/Sparse_matrix) matrix [[doc](http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html#sklearn.feature_extraction.text.CountVectorizer.transform)].

# COMMAND ----------

from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(min_df=1, stop_words='english')
bag_of_words = vectorizer.fit_transform(body_df.sentence)

# COMMAND ----------

# MAGIC %md ### Singular Value Decomposition
# MAGIC 
# MAGIC <img src="https://www.evernote.com/l/AAEhTiOBufhPwKBx-Hgufx4XZ5XyfsCp8cMB/image.png" width=600px>

# COMMAND ----------

svd = TruncatedSVD(n_components=2)
lsa = svd.fit_transform(bag_of_words)

# COMMAND ----------

# MAGIC %md ### Topic Encoded Data
# MAGIC 
# MAGIC <img src="https://www.evernote.com/l/AAGhSgfs1nZHAIYfbnmNaHU8YjMV2i9fTmgB/image.png" width=600px>

# COMMAND ----------

topic_encoded_df = pd.DataFrame(lsa, columns = ["topic_1", "topic_2"])
topic_encoded_df['sentence'] = body_df.sentence
topic_encoded_df['Is_Poe'] = (body_df.title == "The Raven")
display(topic_encoded_df.iloc[sample_indices])

# COMMAND ----------

# MAGIC %md #### The Dictionary

# COMMAND ----------

dictionary = vectorizer.get_feature_names()
dictionary[:10]

# COMMAND ----------

# MAGIC %md #### The Encoding Matrix

# COMMAND ----------

encoding_matrix = pd.DataFrame(svd.components_,
                               index=['topic_1', 'topic_2']).T
encoding_matrix["terms"] = dictionary
display(encoding_matrix)

# COMMAND ----------

# MAGIC %md #### Interpret The Encoding Matrix
# MAGIC 
# MAGIC What are the top "concepts"? What dimensions in term-space explain most of the variance in the data?

# COMMAND ----------

encoding_matrix['abs_topic_1'] = np.abs(encoding_matrix['topic_1'])
encoding_matrix['abs_topic_2'] = np.abs(encoding_matrix['topic_2'])
display(encoding_matrix.sort_values('abs_topic_1', ascending=False))

# COMMAND ----------

display(encoding_matrix.sort_values('abs_topic_2', ascending=False))

# COMMAND ----------

# MAGIC %md ### Plot Topic Encoded Data

# COMMAND ----------

import matplotlib.pyplot as plt

fig, ax = plt.subplots()

for val in topic_encoded_df.Is_Poe.unique():
  topic_1 = topic_encoded_df[topic_encoded_df.Is_Poe == val]['topic_1'].values
  topic_2 = topic_encoded_df[topic_encoded_df.Is_Poe == val]['topic_2'].values
  print(val)
  color = "red" if val else "green"
  label = "The Raven" if val else "Charge of the Light Brigade"
  ax.scatter(topic_1, topic_2, c=color, alpha=0.5, label=label)
# made the colors represent different books

ax.set_xlabel('First Topic')
ax.set_ylabel('Second Topic')
ax.axvline(linewidth=0.5)
ax.axhline(linewidth=0.5)
ax.legend()

display(fig)

# COMMAND ----------

# MAGIC %md ## Revising the LSA with a TF-IDF Document-Term Matrix

# COMMAND ----------

# MAGIC %md **Latent Semantic Analysis (LSA)** is:
# MAGIC 
# MAGIC - a natural language processing technique
# MAGIC - an unsupervised learning technique
# MAGIC - aims to create representations of the documents in a body based on the topics inherent to that body
# MAGIC - reducing the dimensionality of a text-based dataset
# MAGIC - consists of two steps:
# MAGIC    - creating a document-term matrix
# MAGIC    - dimensionality reduction via a singular value decomposition
# MAGIC 
# MAGIC ![](https://www.evernote.com/l/AAGiYGcKcIxIaJ7sCg97K9JDtUO2dY9mywoB/image.png)

# COMMAND ----------

# MAGIC %md ### The SVD is deterministic
# MAGIC 
# MAGIC Finding the vectors generated by an SVD is analogous to finding the eigenvectors of the covariance matrix of the data. Without going to deeply into the meaning of this suffice it to say that these vectors are deterministic and will not change with subsequent fiitting of the model. 
# MAGIC 
# MAGIC In other words, as data scientists we have very little control of the output of an SVD. We can choose a number of output vectors, but the number of vectors returned has no bearing on the output. We can not tune the model in the conventional sense by, that is, by adjusting hyperparameters. The only hyperparameter to be tuned has no impact on any one individual vector returned.

# COMMAND ----------

# MAGIC %md ### Tuning a Latent Semantic Analysis
# MAGIC 
# MAGIC The word "eigen" is German for "own" or "inherent". Each eigenvector returned is in some way "of" or "inherent to" the underlying Document-Term Matrix. The LSA is based upon these eigenvectors, but the SVD being deterministic, there is no way to directly alter them.
# MAGIC 
# MAGIC What can be done is to alter the Document-Term Matrix itself. One popular method for doing this is to use the term frequency-inverse document frequency algorithm in the preparation of the Document-Term Matrix rather than a simple count.

# COMMAND ----------

# MAGIC %md #### Term Frequency-Inverse Document Frequency
# MAGIC 
# MAGIC A simple count collects term frequency, the number of times a term appears in a document. A TFIDF weighs this term frequency by the inverse of the document frequency, that is, the number of documents in which the term appears.
# MAGIC 
# MAGIC Without going into the details of how a [TFIDF](https://spark.apache.org/docs/latest/mllib-feature-extraction.html) is calculated we can note conceptually that will help to reflect the importance of a term to a document in the body. If we only use term frequency to measure the importance, it is very easy to over-emphasize terms that appear very often but carry little information about the document, e.g. “a”, “the”, and “of”. If a term appears very often across the body, it means it doesn’t carry special information about a particular document. Inverse document frequency is a numerical measure of how much information a term provides.
# MAGIC 
# MAGIC Here, we will look at using TFIDF to generate the Document-Term Matrix and how it effects the LSA.

# COMMAND ----------

# MAGIC %md ### Raw Text Data
# MAGIC 
# MAGIC <img src="https://www.evernote.com/l/AAFfAyDQQ1xGPLTIxT2hcUSLrHuQDbYzsuYB/image.png" width=600px>
# MAGIC 
# MAGIC Here each line of text from a book is a **document** and the collection of all lines of text from the two books is the **body**.

# COMMAND ----------

# MAGIC %md ### Document-Term Matrix
# MAGIC 
# MAGIC <img src="https://www.evernote.com/l/AAFtjaKOjT5CYr5N_NPHKU6vpBWNnBgbWLIB/image.png" width=600px>
# MAGIC 
# MAGIC Again, we use `CountVectorizer`, now with a few more arguments:
# MAGIC 
# MAGIC - `min_df` signifies the number of documents in which a term must appear in order for it to be counted
# MAGIC - You can view the `english` `stop_words` here: https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/feature_extraction/stop_words.py
# MAGIC 
# MAGIC Note that `CountVectorizer` returns a [sparse](https://en.wikipedia.org/wiki/Sparse_matrix) matrix [[doc](http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html#sklearn.feature_extraction.text.CountVectorizer.transform)].

# COMMAND ----------

from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(min_df=1, stop_words='english')
bag_of_words = vectorizer.fit_transform(body_df.sentence)

# COMMAND ----------

# MAGIC %md ### Singular Value Decomposition
# MAGIC 
# MAGIC <img src="https://www.evernote.com/l/AAEhTiOBufhPwKBx-Hgufx4XZ5XyfsCp8cMB/image.png" width=600px>

# COMMAND ----------

svd = TruncatedSVD(n_components=2)
lsa = svd.fit_transform(bag_of_words)

# COMMAND ----------

# MAGIC %md ### Topic Encoded Data
# MAGIC 
# MAGIC <img src="https://www.evernote.com/l/AAGhSgfs1nZHAIYfbnmNaHU8YjMV2i9fTmgB/image.png" width=600px>

# COMMAND ----------

topic_encoded_tfidf_df = pd.DataFrame(lsa, columns = ["topic_1", "topic_2"])
topic_encoded_tfidf_df['sentence'] = body_df.sentence
topic_encoded_tfidf_df['Is_Poe'] = (body_df.title == "The Raven")
display(topic_encoded_tfidf_df.iloc[sample_indices])

# COMMAND ----------

# MAGIC %md #### The Dictionary

# COMMAND ----------

dictionary = vectorizer.get_feature_names()
dictionary[:10]

# COMMAND ----------

# MAGIC %md #### The Encoding Matrix

# COMMAND ----------

encoding_matrix = pd.DataFrame(svd.components_,
                               index=['topic_1', 'topic_2']).T
encoding_matrix["terms"] = dictionary
display(encoding_matrix)

# COMMAND ----------

# MAGIC %md #### Interpret The Encoding Matrix
# MAGIC 
# MAGIC What are the top "concepts"? What dimensions in term-space explain most of the variance in the data?

# COMMAND ----------

encoding_matrix['abs_topic_1'] = np.abs(encoding_matrix['topic_1'])
encoding_matrix['abs_topic_2'] = np.abs(encoding_matrix['topic_2'])
display(encoding_matrix.sort_values('abs_topic_1', ascending=False))

# COMMAND ----------

display(encoding_matrix.sort_values('abs_topic_2', ascending=False))

# COMMAND ----------

# MAGIC %md ### Plot Top Two Components

# COMMAND ----------

fig, ax = plt.subplots()

for val in topic_encoded_df.Is_Poe.unique():
  topic_1 = topic_encoded_df[topic_encoded_df.Is_Poe == val]['topic_1'].values
  topic_2 = topic_encoded_df[topic_encoded_df.Is_Poe == val]['topic_2'].values
  print(val)
  color = "red" if val else "green"
  label = "The Raven" if val else "Charge of the Light Brigade"
  ax.scatter(topic_1, topic_2, c=color, alpha=0.3, label=label)
# made the colors represent different books

ax.set_xlabel('First Topic')
ax.set_ylabel('Second Topic')
ax.axvline(linewidth=0.5)
ax.axhline(linewidth=0.5)
ax.legend()

display(fig)

# COMMAND ----------

fig, ax = plt.subplots()

for val in topic_encoded_tfidf_df.Is_Poe.unique():
  topic_1 = topic_encoded_tfidf_df[topic_encoded_tfidf_df.Is_Poe == val]['topic_1'].values
  topic_2 = topic_encoded_tfidf_df[topic_encoded_tfidf_df.Is_Poe == val]['topic_2'].values
  print(val)
  color = "red" if val else "green"
  marker = "x" if val else "."
  label = "The Raven" if val else "Charge of the Light Brigade"
  ax.scatter(topic_1, topic_2, marker=marker, c=color, alpha=0.5, label=label)
# made the colors represent different books

ax.set_xlabel('First Topic')
ax.set_ylabel('Second Topic')
ax.axvline(linewidth=0.5)
ax.axhline(linewidth=0.5)
ax.legend()

display(fig)
