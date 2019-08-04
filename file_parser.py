import numpy as np
import subprocess
import collections

def all_triplet_generator(taxa_list):
    l=len(taxa_list)
    no_of_triplets=(l*(l-1)*(l-2))/6
    #no_of_triplets.is_integer()
    #print(no_of_triplets)
    used = 0
    list3=[]

    for i in range(0,l-2):

        # print(taxa_list[i])
        pointer1=i
        elem = taxa_list[pointer1]
        elem += ','
        for j in range(1,l-used-1):
            pointer2 = pointer1+j
            elem += taxa_list[pointer2]
            elem += ','
            # print("Upto 2nd elem-> " + elem)
            # list3.append(taxa_list[pointer2])
            for k in range (1, l-pointer2):
                pointer3 = pointer2+k
                elem += taxa_list[pointer3]
                #print("Testing individual 3 taxa seq:" + elem)
                list3.append(elem)
                temp = elem.split(',')
                elem = temp[0] + ',' + temp[1] + ','

            temp = elem.split(',')
            elem = temp[0] + ','
        elem = ""
        used = used + 1

    #print(len(list3))
    return list3




taxa_map={}
genetree_list=[]
fl = open("removed_taxa_weakILSGT","r+")
#fl = open("weakILSGT","r+")
#fl = open("StrongILS_ALLGT","r+")
#fl = open("Imputed_StrongILS_ALLGT","r+")

while True:
    line = fl.readline().strip()
    if line == '':
        break
    else:
		genetree_list.append(line)

		xl = line.split(',');
		

		for i in range(0,len(xl)):
			xl[i] = xl[i].replace('(','')
			xl[i] = xl[i].replace(')','')
			xl[i] = xl[i].replace(';','')
			'''
			xl[i] = float(xl[i])
			xl[i] = int(xl[i])
			xl[i] = str(xl[i])
			'''

		for x in xl:
			if(x not in taxa_map.keys()):
				taxa_map[x] = 1
				



#print(genetree_list)
taxa_map = collections.OrderedDict(sorted(taxa_map.items()))
print(taxa_map.keys())
three_taxa_sequence=all_triplet_generator(taxa_map.keys())

# print('three_taxa_sequence: ')
# print(three_taxa_sequence)

# print('\n')

column_determinator={}
val=1
type_1=1
type_2=2
type_3=3
for each_seq in three_taxa_sequence:
	temp2 = each_seq.split(',')
	t1=temp2[0]
	t2=temp2[1]
	t3=temp2[2]
	s1='('+t1+','+'('+t2+','+t3+'))'
	s2='('+t1+','+'('+t3+','+t2+'))'
	s3='('+t2+','+'('+t1+','+t3+'))'
	s4='('+t2+','+'('+t3+','+t1+'))'
	s5='('+t3+','+'('+t1+','+t2+'))'
	s6='('+t3+','+'('+t2+','+t1+'))'
	#s2=t1+t3+t2
	
	column_determinator[s1]=str(val)+','+str(type_1)
	column_determinator[s2]=str(val)+','+str(type_1)
	column_determinator[s3]=str(val)+','+str(type_2)
	column_determinator[s4]=str(val)+','+str(type_2)
	column_determinator[s5]=str(val)+','+str(type_3)
	column_determinator[s6]=str(val)+','+str(type_3)
	val+=1

# for index,triplet in enumerate(column_determinator):
# 	print(str(triplet) + " " + str(index))

'''
for x,y in column_determinator.items():
	print(x + " " + y)
'''
no_of_gene_trees = len(genetree_list)
print(no_of_gene_trees)
no_of_three_taxa_seq = len(three_taxa_sequence)
print(no_of_three_taxa_seq)


table = np.zeros((no_of_gene_trees,no_of_three_taxa_seq,3))

print(genetree_list[0])
#genetree_list = genetree_list[0]
count=0
for index,gene_tree in enumerate(genetree_list):

    print("Index-> "+ str(index) + "\nWorking with the tree " + gene_tree)
    if(index != -1):
		with open("Tree_Input.tree", "w+") as f:
		    f.write(gene_tree)
		subprocess.call(['./triplet-encoding-controller.sh','Tree_Input.tree','output.trip'])
		with open("output.trip", "r") as f2:
		    data = f2.read()
		    lines=data.split("\n")
		    no_of_lines=len(lines)

	    #print("line: ")
		#print(lines)
		#print(no_of_lines)
		for i in range(0,no_of_lines-1):
			triplet = lines[i].split(';')[0];
			#print(triplet)
			
			#triplet=lines[i][1]+lines[i][4]+lines[i][6]
			if triplet in column_determinator.keys():
				
				count+= 1
				res = column_determinator[triplet].split(',')

				axis_y = int(res[0])
				axis_z = int(res[1])

				#if(axis_y == 46) : print("Printing 46->" + str(triplet))

				#print(res[0] + " " + res[1])
				table[index][axis_y-1][axis_z-1] = 1

# print(count)
# print(np.sum(table[0]))
# for i in range(table.shape[1]):
# 	if(np.sum(table[0][i]) == 1):
# 		print(str(table[0][i]) + "idx-> " + str(i))
# 	else:
# 		print(table[0][i])
# print(table.shape)

# test_file = open("Valid_file.npy","w+")
# np.save(test_file,table)
test_file = "weak_ILS_train_tree_final"
np.save(test_file,table,allow_pickle=True,fix_imports=True)

