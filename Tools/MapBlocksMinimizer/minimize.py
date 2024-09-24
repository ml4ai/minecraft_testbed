import csv,sys
from io import TextIOWrapper

# this will make sure python can find your source files from the same directory
sys.path.append('.')

from MapBlockObjects import MapBlockRow



mapblock_rows=[]

def process(row,rowIndex):           
        
    #starts on row 1
    if(rowIndex != 0):

        split = str(row[0]).split(' ')
        
        x = int(split[0])
        
        y = int(split[1])
        z = int(split[2])
        
        MapBlockRow.total_rows +=1       
        
        mapblock_rows.append( MapBlockRow(x,y,z,str(row[1]),rowIndex ) )
        
        
    
       

def magic(file:TextIOWrapper):

    csv_reader = csv.reader(file,dialect='excel')

    index = 0

    for row in csv_reader:
        
        process(row,index)
        
        index+=1

if __name__ == "__main__":

    incoming_file = sys.argv[1]
    #outgoing_file = sys.argv[2]

    if(incoming_file != None):
        
        with open(incoming_file, 'r') as f:

            # DO THE THING
            magic(f)

            row:MapBlockRow
            
            for row in mapblock_rows:
                
                print(row.x, row.y, row.z, row.type, row.rowId)

        






    

