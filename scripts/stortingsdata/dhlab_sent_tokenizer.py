from dhlab.nbtokenizer import tokenize

def find_sent_end(toks):
    """Get index of sentence ending tokens"""
    
    #count = 0
    for i, x in enumerate(toks):
        if x in ["!", "?", ".", ":"]:
            #count += 1
            yield i, x
            
    # if count == 0:
    #     yield toks

def join_sent(toks):
    """Insert space between tokens that start with
    alphanumeric chars."""
    
    string = ''
    
    for tok in toks:
        # check if first char is alphanum
        if tok[0].isalnum():
            string = string + ' '
        
        string = string + tok
        
    return string

def check_if_punct_in_sent(toks):
    targets = ["!", "?", ".", ":"]

    res = [x for x in toks if x in targets]
    
    return len(res) > 0
    

def dhlab_sent_tokenize(text):
    """Tokenize a text into sentences using the dhlab tokenizer"""
    
    w_toks = tokenize(text)
    
    #if check_if_punct_in_sent(w_toks):
            
    ind1 = 0
    ind2 = 0

    #sublists = list()


    for i, x in find_sent_end(w_toks):
        ind2 = i + 1
        sublist = w_toks[ind1:ind2]
        ind1 = ind2
        yield join_sent(sublist).strip()
        
    
        
    # for sublist in sublists:
    #     # Yield joined and stripped sentence tokens
        

            
        
    # for sublist in sublists:
    #     # Yield joined and stripped sentence tokens
    #     yield join_sent(sublist).strip()

    
    