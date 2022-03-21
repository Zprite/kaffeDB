import os
class Utils:
    def deleteDB():
        if os.path.exists("KaffeDB.db"):
            os.remove("KaffeDB.db")
            print("Sucessfully removed KaffeDB.db")
        else:
            print("KaffeDB does not exist.") 

    def runSqlScript():
        print("Creating KaffeDB.db from SQL script...")
        os.system('cmd /c "sqlite3 KaffeDB.db -init KaffeDB.sql .quit"')