import os
from _authentications import Authenticate
# from telegram_bot._authentications import Authenticate
import redshift_connector
import pandas as pd
from datetime import datetime


class ListQuestionaire:
    def __init__(self):
        self.secret = Authenticate().get_secret()
        self.host = self.secret['db_host']
        self.dbname = self.secret['db_dev']
        self.port = int(os.environ.get("DB_PORT", 5439))
        self.username = self.secret['redshift_username']
        self.password = self.secret['redshift_password']
        self.con = redshift_connector.connect(host=self.host
                                              , database=self.dbname
                                              , port=self.port
                                              , user=self.username
                                              , password=self.password
                                              )

    def fetch_data(self, quizid: int):
        cursor = self.con.cursor()
        cursor.execute('select'
                       '  q.quizid'
                       ', q.questionid'
                       ', q.context as question_content'
                       ', o.optionid'
                       ', o.option_no'
                       ', o.context as option_content'
                       ', o.iscorrect'
                       ' from accp.dim_question q '
                       ' join accp.dim_option o on q.questionid=o.questionid '
                       ' where 1=1'
                       f' and q.quizid = {str(quizid)}')
        result = pd.DataFrame(cursor.fetchall(),
                              columns=['quizid', 'questionid', 'question_content', 'optionid', 'optin_no',
                                       'option_content', 'iscorrect'])
        cursor.close()

        # Reconstruct the fetched result to appropriate json
        questions = {}
        grouped = result.groupby('questionid')
        for questionid, gr in grouped:
            questions[int(questionid)] = {
                'question': result[result['questionid'] == questionid].question_content.dropna().unique()[0]
                , 'options': {}
                , 'correct_optionid': int(result[(result['questionid'] == questionid) & (
                        result['iscorrect'] == True)].optionid.dropna().unique()[0])
            }
            for index, row in gr.iterrows():
                option = {int(row.optionid): row.option_content}
                questions[int(row.questionid)]['options'].update(option)

        return questions

    def fetch_question_options(self):
        cursor = self.con.cursor()
        cursor.execute("select "
                       " quizid"
                       " , SPLIT_PART(quizname, ' - ', 1) as quiz_topic "
                       " , SPLIT_PART(quizname, ' - ', 2) as quiz_level "
                       " from accp.dim_quiz;")
        result = pd.DataFrame(cursor.fetchall(), columns=['quizid', 'quiz_topic', 'quiz_level'])
        cursor.close()

        # Reconstruct the fetched result to appropriate json
        topics = result.quiz_topic.unique()
        levels = result.quiz_level.unique()
        option_info = {}
        level_dict = {'message': 'Choose level of difficulty:',
                      'levels': {}
                      }
        for i in topics:
            option_info[i] = {'id': i.lower()}
        for i in levels:
            level_dict['levels'][i] = i.capitalize()
        level_dict['levels']['main'] = 'Main Menu'

        return option_info, level_dict

    def fetch_quizid(self, topic: str, level: str):
        cursor = self.con.cursor()
        cursor.execute("select quizid from accp.dim_quiz where 1=1"
                       f" and SPLIT_PART(quizname, ' - ', 1) ilike '{topic}'"
                       f" and SPLIT_PART(quizname, ' - ', 2) ilike '{level}'")
        result = pd.DataFrame(cursor.fetchall(), columns=['quizid'])
        cursor.close()

        return result.quizid.values[0]

    def fetch_chosen_quiztopic(self, participantid):
        cursor = self.con.cursor()
        cursor.execute("select top 1 "
                       "    quizid"
                       " from accp.fact_quizoption_selected "
                       f" where participantid = {participantid} "
                       " order by selected_quiz_ts desc")
        result = pd.DataFrame(cursor.fetchall(), columns=['quizid'])
        cursor.close()
        if len(result) == 0:
            return 1
        else:
            return result.quizid.values[0]


class UpdateData:
    def __init__(self):
        self.secret = Authenticate().get_secret()
        self.host = self.secret['db_host']
        self.dbname = self.secret['db_dev']
        self.port = int(os.environ.get("DB_PORT", 5439))
        self.username = self.secret['redshift_username']
        self.password = self.secret['redshift_password']

    def insert_users_quiz_optionlevel(self, quizid, userid):
        con = redshift_connector.connect(host=self.host
                                         , database=self.dbname
                                         , port=self.port
                                         , user=self.username
                                         , password=self.password
                                         )
        selected_quiz_ts = datetime.now()
        cursor = con.cursor()
        cursor.execute('select max(quizselectedid) from accp.fact_quizoption_selected')
        quizselected_id = cursor.fetchone()[0]
        if quizselected_id is None:
            quizselected_id = 1
        else:
            quizselected_id += 1
        sql = f"INSERT INTO accp.fact_quizoption_selected (quizselectedid, participantid, quizid, selected_quiz_ts) VALUES ({quizselected_id}, {userid}, {quizid}, '{selected_quiz_ts}')"
        cursor.execute(sql)
        cursor.close()
        con.commit()
        con.close()


# option_info, level_dict = ListQuestionaire().fetch_question_options()
# print(json.dumps(option_info, indent=4))
# print(json.dumps(level_dict, indent=4))
# test = ListQuestionaire().fetch_chosen_quiztopic(3)
# print(test)
