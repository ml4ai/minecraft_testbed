

class MapBlockRow (object):

    total_rows = 0

    def __init__(self,x:int,y:int,z:int,type,rowId:int) -> None:
        
        super().__init__()

        self.x = x

        self.y = y

        self.z = z

        self.type = type

        self.rowId = rowId

        #print(  x,y,z,type )
