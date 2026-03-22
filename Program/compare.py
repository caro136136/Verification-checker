from Levenshtein import distance as ld


#ensure authors are only the first letter of the first name
def normalize_authors(authors):

    a = []
    for name in authors:
        parts = name.split()

        if len(parts) >= 2:
            first = parts[0][0]
            last = parts[-1]
            a.append( first + "." + last)
        else:
            a.append(name)

    return a


#ensure title is in lower case letters only
def normalize_title(title):
    t =""
    if title != None:
        t = title.lower()
    return t


#compare ref and res with the help of the levenshtein distance
def get_compare(reference,result):

    #print(reference.title)

    Score = []

    if not result:
        print("No results found")
        return []

    min = len(reference.title)
    #print(result[0])
    r = result[0]

    for res in result:
        ref_t = reference.title
        res_t = res.title

        #compare title with the use of the Levenshtein distance:
        ld_title = ld(ref_t,res_t)

        len_title_ref = len(reference.title)
        len_title_res = len(res.title)
        len_title = max(len_title_ref, len_title_res)

        title_sim = ld_title / len_title
        #print(title_sim)



        #compare the aurhors with the use of Levenshtein distance:
        len_authors = -1
        if res.authors:
            res_a = res.authors
            ref_a = reference.authors

            str_res_a = str(res_a)
            str_ref_a = str(ref_a)
            len_authors_ref = len(str_ref_a)
            len_authors_res = len(str_res_a)
            len_authors = max(len_authors_ref,len_authors_res)
            ld_authors = ld(str_res_a,str_ref_a)

            authors_sim = ld_authors / len_authors
            #print(authors_sim)

            Score.append(get_score(title_sim,authors_sim))
        else:
            Score.append(get_score_title(title_sim))
        #print("Score")
        #print(Score)
    return Score


def get_score(t,a):
    i = 0.7 * t + 0.3 * a
    #print("Score berechnung")
    #print(i)

    return i


def get_score_title(t):  

    i =   0.7 * t
    #print("Score berechnung")
    #print(i)
    return i


#get the result with the lowest score
def get_min(score,result):

    m = 1
    id = 0
    i = 0
    temp = 0
    for s in score:
        if s != None:
            if m  < s:
                temp = m
            else :
                temp = s
            if temp != m:
                id = i
            m = temp
        i += 1

    return score[id] , result[id]