import sys
import dataForSQL
import dbConnectToSQL

def main(args):
    dt = dataForSQL.DataForSQL()
    dt.createData()
    dt.checkSorting()
    dt.sqlTitleAnswerInsert()
    dt.writeToFile()
    dt.answerCreateFile()
    dt.insertQuestionsSQL()

    
if __name__ == "__main__":
    main(sys.argv)