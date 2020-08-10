# These are the emails you will be censoring. The open() function is opening the text file that the emails are contained in and the .read() method is allowing us to save their contexts to the following variables:
email_one = open("email_one.txt", "r").read()
email_two = open("email_two.txt", "r").read()
email_three = open("email_three.txt", "r").read()
email_four = open("email_four.txt", "r").read()
proprietary_terms = ["she", "personality matrix", "sense of self", "self-preservation", "learning algorithm", "her", "herself"]
negative_words = ["concerned", "behind", "danger", "dangerous", "alarming", "alarmed", "out of control", "help", "unhappy", "bad", "upset", "awful", "broken", "damage", "damaging", "dismal", "distressed", "distressed", "concerning", "horrible", "horribly", "questionable"]
def censor_word(text,key_phrase,replace_with ='REDACTED'):
    censored_text = text.replace(key_phrase,replace_with)#censor text
    censored_text_lower = censored_text.lower()
    if key_phrase in censored_text_lower: #if the key is in the text still with mixed case
        #note this only checks for tittle case, not for upper or mixed case
        key_phase_title = key_phrase.title()
        censored_text = censored_text.replace(key_phase_title,replace_with)
    return censored_text
def censor_key_list(text,key_list):
    censored_text = text
    for key in key_list:#loops though the kew list and censors all of them
        censored_text=censor_word(censored_text,key)
    return censored_text
def censor_negative(text,key_list,tolerance=2):
    alarm = 0
    text_beginning= ''
    text_end = text
    # using an shorteing string method to get rid of first words, and censor everything at the end using above functions
    while alarm < tolerance:
        first_instance = len(text_end)
        instance_len = 0
        # the for loop is to find the first instance of a negative word
        for key in key_list:#brute force aproach, can be optimised so it only loops though the text once and shortens it aproipiately, but not sure how
            if (first_instance > (index := text_end.lower().find(key)) and index != -1):# the := asignment is new in 3.8!!!
                first_instance = index
                instance_len = len(key)
        text_beginning = text_beginning + text_end[:(first_instance + instance_len)]#adds all text up to negative word
        text_end = text_end[(first_instance + instance_len):]#splices the string to start after the negative word
        alarm += 1
    text_end = censor_key_list(text_end,key_list)
    return text_beginning + text_end
def censor_neighbors(text, censor):
    text_list= text.split(' ')#turns text into a list so we can do element operations
    search = 0
    just_replaced = False
    for search in range(len(text_list)):#loop though text_list
        if just_replaced == True:#jumps over new censors added below
            just_replaced = False
            continue
        if censor in text_list[search]:#note this is a string comparason, so it handles  extra chars
            #censors elemets before and after original censor
            #Both trys here acount for the situation where the censor falls on the first or last index
            #however, this butchers any formationg and puncuation in ajacent elements- dont know how how to handel that
            try:
                text_list[search-1] = censor
            except IndexError:
                pass
            try:
                text_list[search + 1] = censor
                just_replaced = True
            except IndexError:
                pass
    '''originally I tried to implement the shortening string method like in censor_niebors
    but while debugging I noticed that if I defined text_list = text_list_end
    any changes made to text_list_end also affected text_list
    Are they pointing to the same space in memory??
    So I just decided to work with text_list directly'''
    censored_text = ' '.join(text_list)
    return censored_text
    
'''an advantage to defining the funtions like this is that the overall code is much shorter!
Corpared to the standard solution 100+ vs 80 with commnets
Its also more modular'''
email_one_censored= censor_word(email_one,'learning algorithms')
email_two_censored= censor_key_list(email_two,proprietary_terms)
email_three_censored= censor_key_list(censor_negative(email_three,negative_words),proprietary_terms)
email_four_censored= censor_key_list(censor_negative(email_four,negative_words),proprietary_terms)
email_four_super_censored = censor_neighbors(email_four_censored,'REDACTED')
#print(email_one)
#print(email_one_censored)
#print(email_two)
#print(email_two_censored)
#print(email_three_censored)
print(email_four_super_censored)