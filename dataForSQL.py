import dbConnectToSQL as db
import re

class DataForSQL(db.DbConnectSQL):
    def __init__(self) -> None:
        super().__init__()
        self.data = []
        self.ids = {}
        
    
    def createData(self):
        path = r'C:\Users\Abdyushev.R\Documents\VB_word\parse_table\wordData.txt'
        with open(path) as f:
            rawdata = [line.rstrip()[1:-1].split(";") for line in f]
        self.data = list(map(lambda x: [int(x[0]), str(x[1]), int(x[2]), str(x[3]), str(x[4]), str(x[5]), str(x[6]), str(x[7])], rawdata))
        
            
    def checkSorting(self):
        # sorting = [x[2] for x in self.data]
        previous = 0
        previousSorting = self.data[0][2]
        for arr in self.data:
            if arr[3].startswith("*"):
                self.data[arr[0]].append("green")
            elif arr[3].startswith("**"):
                self.data[arr[0]].append("orange")
            else:
                self.data[arr[0]].append(None)
                
            # print(previous)
            if arr[2] == previous: 
                print("hello")
                x = arr[2] + 20
                self.data[arr[0]][2] = x
                
            if arr[2] != 8:
                previous = arr[2]
                self.data[arr[0]].append(0)
                previousSorting = self.data[arr[0]][2]
            else:
                self.data[arr[0]].append(previousSorting)
                
            # index = arr[0]
            # ii = 0
            # for el in arr:
            #     if el in ['null', 'Null']:
            #         self.data[index][ii] = None
            #         ii += 1
            
            
        # for i in range(len(self.data)):
        #     pass
            
        # print(self.data[0])
        
    def writeToFile(self):
        with open("myfile.txt", "w") as file1:
            for line in self.data:
                delim = ";"
                res = delim.join([str(ele) for ele in line])
                res = res + "\n"
                # print(res)
                file1.writelines(res)
                
    def sqlTitleAnswerInsert(self):
        section = 0
        numberOfQuestion = 1
        for line in self.data:
            if line[1] == "title":
                subcat = 0
                u = line[3].replace(".","").rstrip()
                val = str(u)
                # val = "%" + str(u) + "%"
                sql = "SELECT id FROM section WHERE project_id = 17 AND name_rus LIKE '" + val + "'"
                self.mycursor.execute(sql)
                row = [item[0] for item in self.mycursor.fetchall()]
                if len(row) != 0:
                    section = row[0]
                self.data[line[0]].append(section)
                self.data[line[0]].append(section)
                self.data[line[0]].append(section)
                self.data[line[0]].append(0)
                print(val)
                print(line[5])
            elif line[1] == "question":
                subcat += 2
                self.data[line[0]].append(section)
                self.data[line[0]].append(section)
                self.data[line[0]].append(section)
                self.data[line[0]].append(subcat)
                if line[5] == "No":
                    print(line[5])
                    self.data[line[0]][3] = str(numberOfQuestion) + ". " + line[3]
                    numberOfQuestion += 1
                    
    def insertQuestionsSQL(self):
        
        sql = "INSERT INTO efes.test_abdyushev_questions (sorting, project_id, questionnaire_id, name_rus, block_id, section_id, x5cat, x5subcat, color_group) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        for line in self.data:
            if line[1] in ["title", "question"]:
                desc = line[4] if line[4] not in ['None', 'null', 'Null'] else None
                values = (int(line[2]), int(17), int(159), str(line[3]), int(line[10]) ,int(line[11]), int(line[12]), int(line[13]), line[8])
                self.mycursor.execute(sql, values)
                self.ids.update({int(line[0]): self.mycursor.lastrowid})
                self.mydb.commit()
                # print(desc)
                
        sql = "UPDATE efes.test_abdyushev_questions SET max_score = %s WHERE sorting = %s"
        for line in self.data:
            if line[7].isdigit():
                # print(line[7])
                val = (int(line[7]), int(line[2]))
                self.mycursor.execute(sql, val)
                self.mydb.commit()
                
        sql = "UPDATE efes.test_abdyushev_questions SET test_abdyushev_questions.describe = %s WHERE sorting = %s"
        for line in self.data:
            if line[4] not in ['None', 'null']:
                print(line[4], " ", int(line[2]))
                val = (str(line[4]), int(line[2]))
                self.mycursor.execute(sql, val)
                self.mydb.commit()
                
        sql = "UPDATE efes.test_abdyushev_questions SET is_section_name = %s WHERE sorting = %s"
        for line in self.data:
            if line[1] in ["title"]:
                val = (1, int(line[2]))
                self.mycursor.execute(sql, val)
                self.mydb.commit()
                
        sql = "UPDATE efes.test_abdyushev_questions SET is_hidden = %s, is_mandatory=%s WHERE sorting = %s"
        for line in self.data:
            if line[1] in ["question"]:
                if line[5] == "No":
                    val = (0, 1, int(line[2]))
                else:
                    val = (1, 0, int(line[2]))
                self.mycursor.execute(sql, val)
                self.mydb.commit()
            
                
                    
    def answerCreateFile(self):
        delimiters = ["( )", "•", "[ ]"]
        answerData = []
        for line in self.data:
            if line[1] == "answer":
                sorting = 10
                string = line[3]
                for d in delimiters:
                    string = string.replace(d, "•")
                data = []
                subString=""
                for c in string[1:]:
                    if c != "•":
                        subString += c
                    else:
                        key = int(line[0]-1)
                        data.append((sorting, self.data[line[0]-1][2], subString.strip().replace(" .", ""), self.ids[key]))
                        sorting += 20
                        subString = ""
                # print(line[0]-1)
                key = int(line[0]-1)
                
                data.append((sorting, self.data[line[0]-1][2], subString.strip(), self.ids[key]))
                
                
                for d in data:
                    
                    txt = d[2]
                    if re.search(r'\d', d[2][-4:]):
                        score = int("".join(re.findall(r'\d+', d[2][-4:])))
                        txt = d[2][0:-4]
                        if len(d) < 4: print("hello", d[1])
                    else:
                        score = None
                    
                    answerData.append((d[0], d[1],txt,score, d[3]))
        
        print(self.ids)
        # print(self.ids.keys())
        with open("answers.txt", "w") as file1:
            for line in answerData:
                delim = ";"
                res = delim.join([str(ele) for ele in line])
                res = res + "\n"
                # print(res)
                file1.writelines(res)
                
        self.insertAnswersSQL(answerData)
                
    def insertAnswersSQL(self, answerData):
        sql = "INSERT INTO efes.test_abdyushev_answer (sorting, question_id, questionnaire_id, score, name_rus) VALUES (%s, %s, %s, %s, %s)"
        for line in answerData:
            val = (int(line[0]), int(line[4]), int(159), line[3], str(line[2]))
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            
        for line in self.data:
            if line[1] == "question" and line[5] == "Yes":
                pass
        
        
        