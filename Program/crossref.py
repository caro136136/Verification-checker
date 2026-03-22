import requests
import grobid
import time
import compare

#here are all the querys for the API requestst and the corresponding methods

class Result(object):
    title = ""
    authors = []
    date = ""
    doi = ""

def make_result(title,authors,date,doi):
    result = Result()
    result.authors = authors
    result.title = title
    result.date = str(date)
    result.doi = str(doi)

    return result


def print_res(result):
    print("Titel :" + result.title)
    print("Autoren :")
    for a in result.authors:
        print(a)
    print("Datum :" + result.date)
    print("DOI: " + result.doi)
    print("\n")

#query for DOI checking
def query_doi(ref):
    if not ref.doi:
        return False
    
    doi = ref.doi.strip()

    url = "https://api.crossref.org/works"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            return True
        else:
            return False

    except requests.exceptions.RequestException as e:
        print("CrossRef request has failed: " + str(e))
        return False


#openalex query
def query_openalex(ref, rows):

    url = "https://api.openalex.org/works"
    Results = []

    if not ref.authors:

        if ref.title == None:

            print("NO TITLE AND AUTHOR -> CAN NOT DO HTTP REQUEST")
            return None

        params = {
            "search" : ref.title +  " " + ref.date,
            "per-page" : rows,

        }
    elif ref.title == None:

        if ref.date == None:
            params = {
                "search" : ref.title ,
                "per-page" : rows,

        }
         
        params = {
            "search" :  ref.authors[0] + " " + ref.date,
            "per-page" : rows,

        }

    elif ref.date == None:
    
        params = {
            "search" : ref.title + " " + ref.authors[0] ,
            "per-page" : rows,

        }

    else :

        params = {
            "search" : ref.title,
            "per-page" : rows

        }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        #print("--------------------------OpenAley--------------------------------")
        #print(data)

    except requests.exceptions.RequestException as e:
        print("Openalex request has failed: " + str(e))
        return[]
    #print(data)
    #print(response.url)
    for item in data.get("results",[]):

        title = ""
        title = item.get("title")

        authors = []
        for a in item.get("authorships",[]):
            if "author" in a:
                authors.append(a["author"]["display_name"])

        date = "" 
        date += str(item.get("publication_year"))

        doi = ""
        doi = item.get("doi")
        
        authors = compare.normalize_authors(authors)
        title = compare.normalize_title(title)
        res = make_result(title,authors,date,doi)
        #print_res(res)
        Results.append(res)


    #for res in Results:
        #print_res(res)
    return Results
    

    


#semantic scholar query
def query_semantic_scholar(ref,rows):

    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    Results = []

    if not ref.authors:

        if ref.title == None:

            print("NO TITLE AND AUTHOR -> CAN NOT DO HTTP REQUEST")
            return None

        params = {
            "query" : ref.title +  " " + ref.date,
            "limit" : rows,
            "fields" : "title,author,published,DOI"

        }
    elif ref.title == None:

        if ref.date == None:
            params = {
                "query" : ref.title ,
                "limit" : rows,
                "fields" : "title,author,published,DOI"

        }
         
        params = {
            "query" :  ref.authors[0] + " " + ref.date,
            "limit" : rows,
            "fields" : "title,author,published,DOI"

        }

    elif ref.date == None:
    
        params = {
            "query" : ref.title + " " + ref.authors[0] ,
            "limit" : rows,
            "fields" : "title,author,published,DOI"

        }

    else :

        params = {
            "query" : ref.title + " " + ref.authors[0] + " " + ref.date,
            "limit" : rows,
            "fields" : "title,author,published,DOI"

        }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as e:
        print("Semantic Scholar request has failed: " + str(e))
        return[]
    
    for paper in data.get("data",[]):

        title = ""
        title += paper.get("title")

        authors = []
        for a in paper.get("authors",[]):
            a.get("name")
            authors.append(a)

        date = "" 
        date += str(paper.get("year"))

        doi = ""
        external_ids = paper.get("externalIds",{})
        if "DOI" in external_ids:
            doi = external_ids["DOI"]

        authors = compare.normalize_authors(authors)
        title = compare.normalize_title(title)
        
        res = make_result(title,authors,date,doi)
        Results.append(res)
    
    return Results

        

#crossref query
def query_crossref_title(ref, rows):

    url = "https://api.crossref.org/works"
    Results =[]

    if not ref.authors:

        if ref.title == None:

            print("NO TITLE AND AUTHOR -> CAN NOT DO HTTP REQUEST")
            return None

        params = {
            "query.bibliographic" : ref.title +  " " + ref.date,
            "rows" : rows,
            "select" : "title,author,published,DOI"

        }
    elif ref.title == None:

        if ref.date == None:
            params = {
                "query.bibliographic" : ref.title ,
                "rows" : rows,
                "select" : "title,author,published,DOI"

        }
         
        params = {
            "query.bibliographic" :  ref.authors[0] + " " + ref.date,
            "rows" : rows,
            "select" : "title,author,published,DOI"

        }

    elif ref.date == None:
    
        params = {
            "query.bibliographic" : ref.title + " " + ref.authors[0] ,
            "rows" : rows,
            "select" : "title,author,published,DOI"

        }

    else :

        params = {
            "query.bibliographic" : ref.title + " " + ref.authors[0] + " " + ref.date,
            "rows" : rows,
            "select" : "title,author,published,DOI"

        }

    #print("----------------------Orginal ref----------------")
    #grobid.print_ref(ref)
    #print("--------------------------------------------------")


    try:
        response = requests.get(url,params = params)
        #print(response.url)
        response.raise_for_status()
        data = response.json()
       # print("--------------------CrossRef-------------------------")
        #print(data)
        #print(data)


    except requests.exceptions.RequestException as e:
        print("Crossref request has failed: " + str(e))
        return[]
    

    for item in data.get("message",{}).get("items",[]) :

        title = ""
        title += item.get("title",[""])[0]
        authors = []
        for a in item.get("author",[]):
            #print(a)
            first = a.get('given','')
            firstname = ""
            f = first.split(" ")
            for i in f:
                firstname += i[:1] + "."
            #print(firstname)
            lastname = a.get('family','')
            name = firstname  + lastname 
            name.strip()
            #print(name)
            authors.append(name)
        date = ""
        if "published" in item:
            d = item.get("published").get("date-parts",[])  
            date = str(d[0][0])

        doi = ""
        doi += item.get("DOI",None)
        
        authors = compare.normalize_authors(authors)
        title = compare.normalize_title(title)
        
        res = make_result(title,authors,date,doi)
        Results.append(res)
        #print("orginam Titlel:____________" + ref.title)
        #print_res(res)
        

    return Results

