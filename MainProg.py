import sys
import dataForSQL
import dbConnectToSQL

def main(args):
    dt = dataForSQL.DataForSQL()
    dt.createData()
    dt.checkSorting()
    dt.sqlTitleAnswerInsert()
    dt.writeToFile() 
    dt.insertQuestionsSQL()
    dt.answerCreateFile()

    
if __name__ == "__main__":
    main(sys.argv)