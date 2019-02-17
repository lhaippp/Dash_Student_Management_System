import os 
import sys 
import pandas as pd 
import numpy as np 

def update_qcm(new_qcm,path,old_file = None):
    def table_question(qcm_file,id_qcm,path=path):
        catalogue = pd.read_csv(path+'catalogue.csv',header=None)
        catalogue.columns = ['code','name']
        categories = pd.read_csv(path+'categories.csv')
        qcm = pd.read_csv(path+qcm_file)
        observations = [x for x in list(qcm.columns) if x not in ['nom', 'id_eleve']]
        cat = []
        sous_cat =[]
        for idx,i in enumerate(observations):
            name = catalogue.name[catalogue['code']== i].values.tolist()
            name = ''.join(name)
            categorie =categories['nom_categorie'][categories['code_sous-categorie']==name].values.tolist()
            categorie = ''.join(categorie)
            sous_categorie =categories['nom_sous-categorie'][categories['code_sous-categorie']==name].values.tolist()
            sous_categorie = ''.join(sous_categorie)
            cat.append(categorie)
            categorie = ''
            sous_cat.append(sous_categorie)
            sous_categorie=''
            name = ''
        data={'nom_question':observations,'sous_categorie': sous_cat,'categorie': cat,'id_qcm': id_qcm }
        question = pd.DataFrame(data)
        return question
    
    list_df = []
    if old_file != None and (type(new_qcm) == list)  :
        df_question = pd.read_csv(path+old_file)
        end_qcm = df_question.id_qcm.max()        
        for i in range(len(new_qcm)):
            question = table_question(new_qcm[i], end_qcm+1+i)
            list_df.append(question)
        df_question = pd.concat([df_question]+list_df,ignore_index = True) 
        df_question['id_question'] = np.nan
        df_question['id_question'] = [x for x in range(df_question.shape[0])]
        
    elif old_file == None and (type(new_qcm) == list):       
        for i in range(len(new_qcm)):
            question = table_question(new_qcm[i], 1+i)
            list_df.append(question)
        df_question = pd.concat(list_df,ignore_index = True)
        df_question.insert(0,'id_question',[x for x in range(df_question.shape[0])])
    
    df_question.to_csv(path+'question.csv',index = False)

def update_eleve(eleve_file,path):
    def table_eleve(eleve_file,path = path):
        df_student = pd.read_csv(path+eleve_file)
        df = df_student[['ID_ELEVE','NOM_ELE','PRENOM_ELE','num_groupe_etudiant','NIVEAU_INIT_MAX_FRANCAIS','NIVEAU_ATTEINT_MAX_FRANCAIS','groupe_promo','CODE_FORMATION','site']]
        df.columns = ['id_eleve','nom','prenom','id_groupe','niveau_init_francais','niveau_atteint_francais','groupe_promo','code_formation','site']
        df.fillna('Maternel',inplace=True)
        return df
    df_eleve = table_eleve(eleve_file)
    df_eleve.to_csv(path+'eleve.csv',index=False)

def update_fact(qcm_list,path):   
    def bi_exam(qcm_file,id_qcm,path=path):     
        ## Table de fait:
        df_qcm = pd.read_csv(path+qcm_file)
        df_question = pd.read_csv(path+'question.csv')
        df_student = pd.read_csv(path+'eleve.csv')

        colnames = ['id_eleve','id_question','note','absence','sous_categorie','categorie','id_groupe']
        dict_bi_exam = {}
        for col in colnames:
            dict_bi_exam[col] = []
        dict_bi_exam

        ## Questions
        questions_id = df_question.id_question.values.tolist()
        students_id = df_student['id_eleve'].values.tolist()

        for s in students_id:
            absence = 0
            if (df_qcm[df_qcm['id_eleve']==s].isna().sum(axis = 1).values[0]) >= 20: 
                absence = 1          
            for q in questions_id:
                if df_question['id_qcm'][(df_question['id_question'] == q)].values[0] == id_qcm:
                    dict_bi_exam[colnames[0]].append(s)

                    dict_bi_exam[colnames[2]].append(df_qcm[df_question['nom_question'][(df_question['id_question'] == q) & (df_question['id_qcm'] == id_qcm)]][df_qcm['id_eleve'] == s].values[0,0])
                    dict_bi_exam[colnames[3]].append(absence)
                    dict_bi_exam[colnames[1]].append(q)
                    dict_bi_exam[colnames[4]].append(df_question["sous_categorie"][df_question['id_question'] == q].values[0])
                    dict_bi_exam[colnames[5]].append(df_question["categorie"][df_question['id_question'] == q].values[0])
                    dict_bi_exam[colnames[6]].append(df_student['id_groupe'][df_student['id_eleve']==s].values[0])

        # df_bi-exam = pd.DataFrame()
        a = pd.DataFrame(data = dict_bi_exam)
        #Don't use a['note'][a.note.isna()] = -1 (SettingWithCopyWarning!!!)
        a.loc[a.note.isna(), 'note'] = -1       
        return a
    
    list_df = []
    for i in range(len(qcm_list)):
        bi = bi_exam(qcm_list[i],i+1)
        list_df.append(bi)

    df_bi = pd.concat(list_df,ignore_index = True)
    df_bi.to_csv(path+'fact_table_bi_exam.csv',index = False)
    
    
def update_all(qcm_list,eleve = None,data_path = './Data/'):
    """
    Example:    update_all(qcm_list = ['QCM.csv','QCM2.csv','QCM3.csv'],
                           eleve = 'ExportElevesUVSimple.csv',
                           data_path = '../data/')
    """
    print('Files in this path:\n',os.listdir(data_path))
    update_qcm(qcm_list,data_path)
    if eleve != None:
        update_eleve(eleve,data_path)
    update_fact(qcm_list,data_path)
    print('Mis_a_jour est fini, path:',data_path)

### Test    
update_all(['QCM.csv','QCM2.csv','QCM3.csv'],'ExportElevesUVSimple.csv')   