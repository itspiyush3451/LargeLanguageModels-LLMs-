#Step 1: Creating a token
with open("the-verdict.txt", "r" , encoding = "utf-8") as f:
    raw_text = f.read()

# print(" Total num of characters in the file: ", len(raw_text))
# print(raw_text[:99])  # Display the first 100 characters for a preview 

#O/P: 
#  Total num of characters in the file:  20479
# I HAD always thought Jack Gisburn rather a cheap genius--though a good fellow enough--so it was no
#Goal: to tokenize these 20,479 characters into tokens



#split the texts(using regular expressions) 
import re
# text = "Hello . How are you? I hope you're doing well."
# result = re.split(r'([,.?!:;_"()\']|--|\s+)', text)
# #print(result)
# #O/P: ['Hello', ' ', '', '.', '', ' ', 'How', ' ', 'are', ' ', 'you', '?', '', ' ', 'I', ' ', 'hope', ' ', "you're", ' ', 'doing', ' ', 'well', '.', '']
# #still empty strings are present, we can filter them out
# result = [token for token in result if token.strip()]
# print(result)
# #O/P: ['Hello', '.', 'How', 'are', 'you', '?', 'I', 'hope', "you're", 'doing', 'well', '.'] 

# Basic Tokenization using regular expressions        
preprocessed_text = re.split(r'([,.?!:;_"()\']|--|\s+)', raw_text)
preprocessed_text = [token for token in preprocessed_text if token.strip()]
# print(preprocessed_text[:30])
# print(len(preprocessed_text))


#Step 2: Creating tokenIDs
# Create a vocabulary dictionary : vocabulary = tokens arranged in alphabetical order
#Note: vocaubulary contains unique tokens

all_words = sorted(set(preprocessed_text))
vocab_size = len(all_words)
# print("Vocabulary size: ", vocab_size)
#now we create the vocabulary dictionary
vocab = {token:integer for integer, token in enumerate(all_words)} #enumarate gives us a tuple of (index, token)
# print("Vocabulary dictionary: ", list(vocab.items())[:30])  # Display first 30 items with their token IDs
#O/P: Vocabulary dictionary:  [('!', 0), ('"', 1), ("'", 2), ('(', 3), (')', 4), (',', 5), ('--', 6), ('.', 7), (':', 8), (';', 9), ('?', 10), ('A', 11), ('Ah', 12), ('Among', 13), ('And', 14), ('Are', 15), ('Arrt', 16), ('As', 17), ('At', 18), ('Be', 19), ('Begin', 20), ('Burlington', 21), ('But', 22), ('By', 23), ('Carlo', 24), ('Chicago', 25), ('Claude', 26), ('Come', 27), ('Croft', 28), ('Destroyed', 29)]


# creating a tokenizer class 

class SimpleTokenizerv1:
    def __init__(self, vocab):
        self.str_to_int = vocab
        self.int_to_str = {i: s for s, i in vocab.items()}
    

    def encode(self, text): # Convert text to token IDs
        preprocessed_text = re.split(r'([,.?!:;_"()\']|--|\s+)', text) # splits the text into tokens( including the white spaces)
        # print(preprocessed_text[:30])  

        preprocessed_text = [ #got individual tokens (excluding the white spaces)
            item.strip() for item in preprocessed_text if item.strip()
        ]
        # print(preprocessed_text[:30]) 
        ids = [self.str_to_int[token] for token in preprocessed_text] # Convert tokens to IDs   
        return ids
    
    #Summary of Encoding:
    #1. Split the text into tokens using regular expressions.
    #2. Remove any whitespace-only tokens.
    #3. Convert the remaining tokens to their corresponding IDs.
    #4. Return the list of token IDs.


    def decode(self, ids): # Convert token IDs back to text
        text = " ".join([self.int_to_str[id] for id in ids])  # Convert IDs into individual tokens and then you join them
        #replace spaces before the specified punctuation marks
        text = re.sub(r'\s([,.?!:;_"()\'])', r'\1', text)
        return text
    #Summary of Decoding:
    #1. Convert the list of token IDs back to their corresponding tokens.
    #2. Join the tokens into a single string.
    #3. Remove any whitespace before punctuation marks.
    #4. Return the reconstructed text.

# Create an instance of the tokenizer
tokenizer = SimpleTokenizerv1(vocab)
# Encode the raw text into token IDs
text = """"Money's only excuse is to put beauty into circulation," was one of the axioms he laid down across the Sevres and silver of an exquisitely appointed luncheon-table, when, on a later day, I had again run over from Monte Carlo; and Mrs. Gisburn, beaming on him, added for my enlightenment: "Jack is so morbidly sensitive to every form of beauty."""
ids = tokenizer.encode(text)
print(ids) #display the token IDs

# Decode the token IDs back to text
decoded_text = tokenizer.decode(ids)
print(decoded_text) 

#Special Context Tokens : To handle unknown words or tokens.
# <uknown_token> = "<unk>"  # Token for unknown words
# <endof_text_token> = "<endoftext>"  # Token to indicate the end of a text sequence

#Adding two special tokens to the vocabulary
all_tokens = sorted(set(preprocessed_text))
all_tokens.extend(["<|endoftext|>", "<|unk|>"])  # Add special tokens to the vocabulary
vocab = {token: integer for integer, token in enumerate(all_tokens)}  # Update the vocabulary with special tokens
vocab_size = len(all_tokens)
# print("Updated Vocabulary size: ", vocab_size)
print("last 5 items in the updated vocabulary: ", list(vocab.items())[-5:])  # Display last 5 items with their token IDs


#Note:
#GPT did not use <unk> token, rather they used byte pair encoding (BPE) to handle unknown words.
#What is byte pair encoding (BPE)? :- It is used to handle unknown words by breaking the words into subword units and then assigning them uniqueIDs
