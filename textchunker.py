import nltk
import random


# Takes in a block of text, splits it into sentences, then attaches
# part of speech information to each word in the sentences.
def attach_nlp_info(text):
    sentences = nltk.sent_tokenize(text)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences


# A Trigram sentence chunker. Trigram should be high enough accuracy for the
# purpose of creating rough sentence chunks especially since the results
# will then be n-gram-ified and scored.
class TrigramChunker(nltk.ChunkParserI):
    def __init__(self, training_sentences):
        # Extract only the (POS-TAG, IOB-CHUNK-TAG) pairs
        train_data = [
                    [(pos_tag, chunk_tag) for word, pos_tag, chunk_tag in
                     nltk.tree2conlltags(sent)] for sent in training_sentences]

        # Train a TrigramTagger
        self.tagger = nltk.TrigramTagger(train_data)

    def parse(self, sentence):
        # Get the part of speech tags for the sentence
        pos_tags = [pos for word, pos in sentence]

        # Get the Chunk tags
        tagged_pos_tags = self.tagger.tag(pos_tags)

        # Assemble the results in conll format
        conlltags = [(word, pos_tag, chunk_tag)
                     for ((word, pos_tag), (pos_tag, chunk_tag))
                     in zip(sentence, tagged_pos_tags)]

        # Transform the conll formatted results to nltk tree format
        return nltk.chunk.conlltags2tree(conlltags)


chunking_corpus = list(nltk.corpus.conll2000.chunked_sents())
random.shuffle(chunking_corpus)

# Split the data so 80% is used for training and 20% for validation
training = chunking_corpus[:int(len(chunking_corpus) * 0.8)]
validation = chunking_corpus[int(len(chunking_corpus) * 0.8 + 1):]

# Make a new Trigram chunker
trigram_chunker = TrigramChunker(training)

# Evaluate and print out the acuracy of the trained chunker
# todo -- remove this for production builds
print(trigram_chunker.evaluate(validation))


# Chunk text given as a raw string
def chunk_text(text):
    # Use the created trigram chunker to chunk the text
    tagged_sentences = attach_nlp_info(text)
    result = [trigram_chunker.parse(sentence) for sentence in tagged_sentences]
    return result
