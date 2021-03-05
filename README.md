# Improving Centroid-Based Text Summarization through LDA-based Document Centroids

- **Automatic Text Summarization** is the task of producing a text summary *"from one or more texts, that conveys important information in the original text(s), and that is no longer than half of the original text(s) and usually, significantly less than that"* [(Radev, Hovy, McKeown, 2002)](https://www.mitpressjournals.org/doi/pdf/10.1162/089120102762671927).
- This project develops a machine learning model for automatic text summarization by making use of an existing simple model (found [here](https://www.aclweb.org/anthology/W17-1003.pdf)) and modifying it using a pre-trained topic model (a variety of machine learning model for extracting abstract 'topics' occuring in a group of documents - see [(Blei, 2012)](https://www.semanticscholar.org/paper/Probabilistic-topic-models-Blei/7314be5cd836c8f06bd1ecab565b00b65259eac6) for further background) to obtain a more robust model that performs competitively even against much more complex deep learning based models. (For a more detailed technical breakdown, see [here](#technical-description) or our full paper below.)

## Our Paper

- The PDF of our final paper is available [here](docs/LDA_Centroid_text_summarization.pdf).

## Data Setup Instructions

1. Download the Google word vector corpus from [here](https://github.com/mmihaltz/word2vec-GoogleNews-vectors) and place them into the `data_clean` folder.
2. Copy all directories from `duc2004\testdata\tasks1and2\t1.2\docs` (DUC data not distributed in this repo due to licensing restrictions - see the DUC page [here](https://duc.nist.gov/) for further information on accessing this data) to `data_raw/articles`.
3. Move files from `duc2004\results\ROUGE\eval\peers\2` to `data_raw/summaries`.
4. Run `data_raw/import_corpus.py`.

- Models are avaliable in `src`. Example experiments available in `Evaluate_DUC.ipynb`.

## Technical Description

We adapt a recent centroid-based text summarization model [(Rossiello, Semeraro, 2017)](https://www.aclweb.org/anthology/W17-1003.pdf) that takes advantage of the compositionality of word vector embeddings in order to obtain a single vector representation of the most meaningful words in a given text. We propose utilizing Latent Dirichlet Allocation (LDA), a probabilistic generative model for collections of discrete data, as a topic model in order to obtain the most significant words of a document's topic for use in constructing the that document's centroid vector. We see that the LDA implementation results in overall more coherent summaries, competitive with more computationally complex deep learning models - demonstrating the generality of the centroid-based method, and suggesting the potential for further utilizing topic models or other similar probabilistic models to improve upon the general centroid-based method.

## Acknowledgements

This project is based off of work from the following paper: [(Rossiello, Semeraro, 2017)](https://www.aclweb.org/anthology/W17-1003.pdf), the repo of their original codebase is available [here](https://github.com/gaetangate/text-summarizer).

## Contributors

Work on this project was done as part of the *COMP 550: Natural Language Processing* course at McGill University during the Fall 2019 semester. Team consisted of James Berry, Jair Parra, and Logan Ralston.

## License

Licensed under the [MIT License](https://choosealicense.com/licenses/mit/).
