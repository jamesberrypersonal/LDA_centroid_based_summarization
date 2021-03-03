# Improving Centroid-Based Text Summarization through LDA-based Document Centroids

- **Automatic Text Summarization:** The task of producing a text summary "from one or more texts, that conveys important information in the original text(s), and that is no longer than half of the original text(s) and usually, significantly less than that" [*(Radev, Hovy, McKeown, 2002)*](https://www.mitpressjournals.org/doi/pdf/10.1162/089120102762671927).
- We adapt a recent centroid-based text summarization model, one that takes advantage of the compositionality of word embeddings, in order to obtain a single vector representation of the most meaningful words in a given text. We propose utilizing Latent Dirichlet Allocation (LDA), a probabilistic generative model for collections of discrete data, in order to better obtain the topic words of a document for use in constructing the centroid vector. We see that the LDA implementation results in overall more coherent summaries, suggesting the potential for utilizing topic models to improve upon the general centroid-based method.  

## Our paper

- PDF of final paper available [here](docs/LDA_Centroid_text_summarization.pdf).
- This project is based on work from the following paper: [*(Rossiello, Semeraro, 2017)*](https://www.aclweb.org/anthology/W17-1003.pdf).
  - **Repo of their codebase:** [here](https://github.com/gaetangate/text-summarizer).

## Data Setup Instructions

1. Download the Google word vector corpus from [here](https://github.com/mmihaltz/word2vec-GoogleNews-vectors) and place them into the `data_clean` folder.
2. Copy all directories from `duc2004\testdata\tasks1and2\t1.2\docs` (DUC data not distributed in this repo due to licensing restrictions - see the DUC page [here](https://duc.nist.gov/) for further information on accessing this data) to `data_raw/articles`.
3. Move files from `duc2004\results\ROUGE\eval\peers\2` to `data_raw/summaries`.
4. Run `data_raw/import_corpus.py`.

- Models are avaliable in `src`. Example experiments avaliable in `Evaluate_DUC.ipynb`

## Contributors

Work on this project was done as part of the *COMP 550: Natural Language Processing* course at McGill University during the Fall 2019 semester. Team consisted of James Berry, Jair Parra, and Logan Ralston.

## License

Licensed under the [MIT License](https://choosealicense.com/licenses/mit/).
