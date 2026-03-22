from grobid_client.grobid_client import GrobidClient
import xml.etree.ElementTree as ET
import crossref
import compare

#here is everything needed to get reference objects from PDF files

Software_Domains = [
    "github.com",
    "gitlab.com",
    "bitbucket.org",
    "sourceforge.net"
]


class Reference(object):
    title = ""
    authors = []
    date = ""
    doi = ""
    urls = []


def make_reference(title,authors,date,doi,urls):
    reference = Reference()
    reference.authors = authors
    reference.title = title
    reference.date = date
    reference.doi = doi
    reference.urls = urls

    return reference

def print_ref(reference):
    print("Titel:" + str(reference.title))
    print("Autoren :")
    for a in reference.authors:
        print(a)
    print("Datum :" + str(reference.date))
    for u in reference.urls:
        print(u)
    print("DOI:" +reference.doi)
    print("\n")    


def getxml():

   
    client = GrobidClient(grobid_server="http://localhost:8070/")

    client.process(
        service="processReferences",
        input_path="Texts",
        output="outputs",
        n=20
    )


#get references from tei:xml
def extract_references(filename):

    tree = ET.parse(filename)
    root = tree.getroot()

    Refs = []
    n = {"tei": "http://www.tei-c.org/ns/1.0"}

    for bib in root.findall(".//tei:biblStruct", n):
        #print("a")

        title = ""
        names = []
        date = ""
        doi = ""
        urls = []

        t = bib.find(".//tei:title",n)
        if t is not None:
            title = t.text
        
        for a in bib.findall(".//tei:author",n):
            

            forename = a.find(".//tei:forename",n)
            lastname = a.find(".//tei:surname",n)

            name = ""

            if forename is not None:
                name += forename.text + "."
            if lastname is not None:
                name += lastname.text
            
            name = name.strip()

            if name is not None:
                names.append(name)
        
        d = bib.find(".//tei:date",n)
        if d is not None:
            date = d.text

        doi_d = bib.find(".//tei:idno[@type='DOI']",n)
        if doi_d is not None:
            doi = doi_d.text

        for u in bib.findall(".//tei:ptr",n):
            url = u.get("target")
            if url is not None:
                urls.append(url)

        names = compare.normalize_authors(names)
        title = compare.normalize_title(title)
        ref = make_reference(title,names,date,doi,urls)
        
        if ref.doi != "":
            ref.urls = []
        Refs.append(ref)
        #print("test")
        #print_ref(ref)

    return Refs



def get_ref_links(urls):

    for d in Software_Domains:
        for u in urls:
            u = u.lower()
            #print(u)
            if d in u:
                #print("ja")
                return True

    return False    

def ref_links(reference):

    if not reference.urls:
        return False

    return True



#old funktion extract_references is the newer better one
def processxml(filename):
    Refs = []
    with open(filename, encoding='utf8') as file:
        line = file.readline()
        while line.find("</TEI>") == -1:

            if line.find("biblStruct") != -1 :
                titel = ""
                names = []
                date = ""
                
                while line.find("/biblStruct") == -1 :

                    #print(line)
                    if line.find("<title") != -1:
                        #print(line)
                        a = line.replace("<",">")
                        a = a.split(">")
                        titel += a[2] + "\n"


                    if line.find("<author>") != -1:
                        line = file.readline()
                        while line.find("</author>") == -1 :


                            if line.find("<persName>") != -1 :
                                name = ""
                                j = 4
                                a = line.replace("<",">")
                                #print(a)
                                i = a.count(">")
                                splits = a.split(">")
                                while j < i-4:
                                    name += splits[j] +"."
                                    j = j+4
                                name += splits[j]
                                names.append(name)

                            line = file.readline()   

                    if line.find("<date") != -1 :
                        a = line.replace("<",">")
                        a = a.split(">")
                        date = a[2]

                                
                    line = file.readline()
                titel = titel.rstrip()
                t = titel.split("\n")
                if len(t)> 1:
                    titel = t[0]
                ref = make_reference(titel,names,date,None,None)            
                #print_ref(ref) 

                Refs.append(ref)
                line = file.readline()
                
                
            line = file.readline()        

    return Refs

                        
            

