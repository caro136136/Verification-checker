import grobid
import crossref
import compare
import os
import shutil




directory = "outputs"

shutil.rmtree(directory)
os.makedirs(directory)


#get xml from files in directionary
grobid.getxml()


for filename in os.listdir(directory):
    path = os.path.join(directory,filename)



    #references and results storage
    references = []
    result = []
    score = []
    urls = 0
    bad = 0
    alex = 0



    references = grobid.extract_references(path)

    #old funktion not used anymore but similay to extract_references
    #references = grobid.processxml(path)
   

    print("-------------------" + filename  + "----------------------")


    for r in references:

        #if you only want to exclude certain domains you could use this instead the next one
        #if grobid.get_ref_links(r.urls):
            #print("----------THIS REFERENCE IS ONLY A LINK TO A SOFTWARE---------")
            #grobid.print_ref(r)
            #urls += 1
            #continue

        #excludes all references with a link since they are no scientific publication
        if grobid.ref_links(r):
            urls += 1
            continue

        #if no title is found API requests can not be made
        if not r.title:
            print("-------------THIS REFERENCE HAS NO TITLE AND CAN THEREFORE NOT BE SEARCHED FOR----------------------")
            grobid.print_ref(r)
            bad += 1
            continue
        
        #check if there is a doi that matches if not do manualy search
        if crossref.query_doi(r) != True:

            #checking via crossref
            result = crossref.query_crossref_title(r,5)

            if not result:
                
                #checking via openalex
                result = crossref.query_openalex(r,5)

                if not result:
                    print("----------CROSSREF AND OpenAlex COULD NOT FIND SOMETHING TO THIS REFERENCE:--------------")
                    grobid.print_ref(r)
                    bad += 1
                else:
                    score_s = compare.get_compare(r,result)
                    score_final_s , result_final_s = compare.get_min(score,result)

                    if score_final_s >=0.15:
                        print("-------------------------OpenAlex NO MATCHING REFERENCE FOUND-------------")
                        grobid.print_ref(r)
                        print("Score:")
                        print(score_final)
                        print("\n")
                        bad += 1
            
            else:
        



                score = compare.get_compare(r,result)
                #print(r.title)
                #for s in score:
                #print(s)
    
    
                score_final , result_final = compare.get_min(score,result)


                #print("Reference to check : ")
                #grobid.print_ref(r)
                #print("All results:")
                #for re in result:
                    #print(re.title)
                #for s in score:
                    #print(s)

                #print("Best matching Reference : ")
                #crossref.print_res(result_final)
                #print("Score:")
                #print(score_final)
                #print("\n")
            
                if score_final >= 0.15:

                    result_o = crossref.query_openalex(r,5)

                    if not result_o:
                        print("-------------------------NO MATCHING REFERENCE FOUND-------------")
                        grobid.print_ref(r)
                        crossref.print_res(result_final)
                        print("Score:")
                        print(score_final)

                        bad += 1
                    else:
                        #for resu in result:
                            #print(resu.title)
                        score_s = compare.get_compare(r,result_o)
                        #for resu in result:
                            #crossref.print_res(resu)
                        #print(score_s)
                        score_final_s , result_final_s = compare.get_min(score_s,result_o)
                        #print(score_final_s)

                        if score_final_s >=0.15:
                            print("-------------------------NO MATCHING REFERENCE FOUND-------------")
                            grobid.print_ref(r)
                            if score_final_s <= score_final:
                                crossref.print_res(result_final_s)
                                print("Score:")
                                print(score_final_s)
                            else:
                                crossref.print_res(result_final)
                                print("Score:")
                                print(score_final)
                            print("\n")
                            bad += 1
                        else:
                            alex += 1


    #printing to comando line                        
    print("Verhältniss von referenzen:")
    print("There were " + str(len(references)) + " References found")
    print(str(bad) + " of these could not be resolved to an existing Work")
    print(str(urls) + " contained links to a website and wherend scientific papers")
    print(alex)


