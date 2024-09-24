import sys

f = open(sys.argv[1], 'w',encoding='utf-8')

f.write("{:<28} {:<28} {:<10} {:<32} {:<30}".format('AC/ASI','Test ID','Success','Relevant Data', 'Predicate'))
f.write("\n")
f.write("\n")
f.close()