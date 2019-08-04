import random
highest_taxa_del=4

def find_parens(gene_tree,taxa):
    #print(gene_tree)
    idx = gene_tree.find(taxa)
    #print(idx)
    pstack = []
    #print(gene_tree[idx-1] + " " + gene_tree[idx+len(taxa)])
    saved_val = -1
    direction = 0
    if(gene_tree[idx+len(taxa)]==','):
        #print("In here?")
        direction = -1
        #print(" Comma on the right and left element = " + gene_tree[idx-1])
        for i in range(idx,len(gene_tree)):
            if(gene_tree[i] == '('):
                pstack.append(gene_tree[i])
                #print("Got (, stack size after pushing "+ str(len(pstack)))
                #print("stack contents ->" + str(pstack))
            elif(gene_tree[i] == ')'):
                sz = len(pstack)
                if(sz==0):
                    #print("Found the culprit at idx = " + str(i) + " which is: " + gene_tree[i])
                    #saved_val = i
                    #S = S[:Index] + S[Index + 1:]
                    gene_tree = gene_tree[:i] + gene_tree[i+1:]
                    idx = gene_tree.find(taxa)
                    gene_tree = gene_tree[:(idx-1)] + gene_tree[idx:]
                    idx = gene_tree.find(taxa)
                    gene_tree = gene_tree[:idx] + gene_tree[idx+len(taxa)+1:]
                    # idx = gene_tree.find(taxa)
                    # gene_tree = gene_tree[:idx] + gene_tree[idx+len(taxa)+1:]
                    #gene_tree = gene_tree.replace(taxa,'')
                    break
                else:
                    pstack.pop()
                    sz = len(pstack)
                    #print("Got ), stack size after popping "+ str(len(pstack)))
                    #print("stack contents ->" + str(pstack))

                    if(i == (len(gene_tree) - 2) and ((len(pstack)) == 0)):

                        #print("Found the culprit at idx = " + str(i) + " which is: " + gene_tree[i])
                        gene_tree = gene_tree[:i] + gene_tree[i+1:]
                        idx = gene_tree.find(taxa)
                        gene_tree = gene_tree[:(idx-1)] + gene_tree[idx:]
                        idx = gene_tree.find(taxa)
                        gene_tree = gene_tree[:idx] + gene_tree[idx+len(taxa)+1:]
                        break



    elif(gene_tree[idx-1] == ','):

        #print("Starting idx = " + str(idx)+ " Comma on the left and right element = " + gene_tree[idx+len(taxa)])
        for i in range(idx,-1,-1):
            if(gene_tree[i] == ')'):
                pstack.append(gene_tree[i])
                #print("Got ), stack size after pushing "+ str(len(pstack)))
                #print("stack contents ->" + str(pstack))
            elif(gene_tree[i] == '('):
                sz = len(pstack)
                if(sz==0):
                    #print("Found the culprit at idx = " + str(i) + " which is: " + gene_tree[i])
                    saved_val = i
                    gene_tree = gene_tree[:i] + gene_tree[i+1:]
                    idx = gene_tree.find(taxa)
                    gene_tree = gene_tree[:(idx-1)] + gene_tree[idx:]
                    idx = gene_tree.find(taxa)
                    gene_tree = gene_tree[:idx] + gene_tree[idx+len(taxa)+1:]
                    break

                else:
                    pstack.pop()
                    sz = len(pstack)
                    #print("Got (, stack size after popping "+ str(len(pstack)))
                    #print("stack contents ->" + str(pstack))

                    if(i == 0 and sz == 0):
                        #print("Found the culprit at idx = " + str(i) + " which is: " + gene_tree[i])
                        gene_tree = gene_tree[:i] + gene_tree[i+1:]
                        idx = gene_tree.find(taxa)
                        gene_tree = gene_tree[:(idx-1)] + gene_tree[idx:]
                        idx = gene_tree.find(taxa)
                        gene_tree = gene_tree[:idx] + gene_tree[idx+len(taxa)+1:]
                        break

    print(gene_tree)
    return gene_tree

def get_delete_taxas(gene_tree, num_del):
    taxa_map={}
    counter=1
    temp_all_taxa_list=[]
    final_taxa_list=[]
    gene_tree = gene_tree.strip()
    length=len(gene_tree)
    xl = gene_tree.split(',')

    for i in range (0,len(xl)):
        xl[i] = xl[i].replace('(','')
        xl[i] = xl[i].replace(')','')
        xl[i] = xl[i].replace(';','')

    for x in xl:
        temp_all_taxa_list.append(x)
    #print(len(temp_all_taxa_list))

    while(counter < num_del):
        r1 = random.randint(0,len(temp_all_taxa_list)-1)
        
        if(temp_all_taxa_list[r1] not in final_taxa_list):
            counter = counter + 1
            final_taxa_list.append(temp_all_taxa_list[r1])




    return final_taxa_list    




def main():
    #gene_tree = "(11.11,((4.4,(1.1,(3.3,2.2))),(10.10,(((5.5,6.6),(8.8,7.7),9.9))));"
    #gene_tree="(((((5.5,(6.6,(8.8,7.7))),9.9),10.10),(4.4,((3.3,2.2),1.1))),11.11);"
    inp_file = open("StrongILS_ALLGT", "r")
    out_file = open("Imputed_StrongILS_ALLGT","w+")


    f1 = inp_file.readlines()
    
    for gt in f1:
        num_taxa_del = random.randint(0,highest_taxa_del)
        delete_taxa = get_delete_taxas(gt,num_taxa_del)
        for d in delete_taxa:
            gt = find_parens(gt,d)

        out_file.write(gt)
        #print(str(gt) + " " +  str(num_taxa_del) + " " + str(delete_taxa))

    
if __name__== "__main__":
  main()


#find_parens(gene_tree,"11.11")


#find_parens(gene_tree,"")