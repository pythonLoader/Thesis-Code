inp_file2 = open("Imputed_StrongILS_ALLGT","r")
count = 0
f1 = inp_file2.readlines()
for i_gt in f1:
    count = count+1
    print(i_gt)

print(count)