import os 
import pandas as pd 
import numpy as np 
        
class dashboard_prof:
    """
        Users have to specify the ABSOLUT PATH where
            1. fact_table_bi_exam.csv
            2. eleve.csv
            3. question.csv
        are stored.
        If not, varables are not able to be well initialized.
        
        file_path = "__YOUR_ABSOLUT_PATH__"
            
    """
    
    ## data path, need to be change from user.
    #file_path = "/content/drive/My Drive/S5/F3B_415_G11/data" (only for testing, set file_path in app.py)
    
    
    def __init__(self, file_path):       
#         import os 
#         print("__Path__:",file_path,'\nFiles in the path: \n',os.listdir(file_path))
        self.df_bi = pd.read_csv(file_path+"/fact_table_bi_exam.csv")
        self.df_eleve = pd.read_csv(file_path+"/eleve.csv")
        self.df_que = pd.read_csv(file_path+"/question.csv")

    
    def df_score_by_qcm(self):
        """
        return a data frame which has 
            id_eleve,
            id_groupe,
            name(Nom + Prenom)
            qcm score in Nth qcm(if 3 qcm in total, there will be 3 columns qcm_1 qcm_2 qcm_3 ... which saved score in each qcm)
        """
        qcm_num = self.df_que.id_qcm.max()
        df = self.df_bi[['id_eleve','id_groupe','id_question','note']]
        df = df.merge(self.df_que[['id_question','id_qcm']], right_on='id_question',left_on='id_question',how='left')
        
        new_df = self.df_eleve[['id_eleve','id_groupe','nom','prenom']]
        new_df.loc[:,'name']= new_df['nom'] + ' ' + new_df['prenom'] 
        for i in range(1,qcm_num+1):
            new_df = new_df.merge(df[df.id_qcm == i].groupby('id_eleve')['note'].agg({'qcm_%d'%i: lambda x : x[x > 0].sum()}).reset_index(),how='left')
        return new_df
                
    
    def df_profile(self):
        """
        Return 5 data frames to pages-3 for (analyse par profile)
        """
        df1 = self.df_score_by_qcm()
        df2 = self.df_eleve
        df2.loc[df2['groupe_promo'] == 1, 'professor_name'] = 'Laurent'
        df2.loc[df2['groupe_promo'] == 2, 'professor_name'] = 'Sylvie'
        filter_col = [col for col in df1 if col.startswith('qcm')]
        filter_col.sort()
        df1['Avg'] = np.nan
        df1['Avg'] = df1[filter_col].mean(axis=1).round(2)
        filter_col.extend(['Avg','id_eleve'])
        df2 = df2.merge(df1[filter_col], on='id_eleve')
        df4 = df2.groupby(['niveau_atteint_francais'])['Avg'].mean().round(2).reset_index()
        df5 = df2.groupby(['code_formation'])['Avg'].mean().round(2).reset_index()
        df6 = df2.groupby(['site'])['Avg'].mean().round(2).reset_index()
        df7 = df2.groupby(['professor_name'])['Avg'].mean().round(2).reset_index()
        return df1,df4,df5,df6,df7
        
    
    def all_score(self):
        """
            return a df which shows each student's correct response / mistakes / empty response
        """
        df_groupe = self.df_bi
        df_groupe_1 = df_groupe[df_groupe.note == 1]
        df_groupe_2 = df_groupe[df_groupe.note == 0]
        df_groupe_3 = df_groupe[df_groupe.note == -1]
        
        df = df_groupe[['id_eleve']].drop_duplicates()
        df = df.merge(self.df_eleve[['id_eleve','id_groupe','nom','prenom']],left_on='id_eleve',right_on='id_eleve',how='left')
        # print(df)
        df = df.merge(df_groupe_1.groupby('id_eleve')['note'].agg({'reponse_correcte':'count'}).reset_index(),how='left')
        df = df.merge(df_groupe_2.groupby('id_eleve')['note'].agg({'reponse_fause':'count'}).reset_index(),how='left')
        df = df.merge(df_groupe_3.groupby('id_eleve')['note'].agg({'pas_de_reponse':'count'}).reset_index(),how='left')
        df.fillna(0,inplace = True)
        # print(df)
        return df
     
        
    def df_score(self, id_groupe):
        """
        select a groupe of students from self.all_score()
        """
        df = self.all_score()
        return df[df.id_groupe == id_groupe]


    def df_categorie(self):
        """
        This function will return a data frame which evaluates each student's competance by categories.
        df columns:
            id_eleve: int
            nom	: object
            prenom: object
            id_groupe: int
            categorie: object
            note_par_cate: float
            num_question: int
        """
        cc = self.df_que.groupby(['categorie']).categorie.count()
        df_cc = pd.DataFrame({"categorie":cc.index.values, 'num_question':cc.values})
        competance_cate = self.df_bi.groupby(['id_eleve','id_groupe','categorie'])['note'].agg({'note_par_cate': lambda x : x[x > 0].sum()}).reset_index()
        df = competance_cate.merge(df_cc, left_on= 'categorie', right_on='categorie',how='left')
        df = df.merge(self.df_eleve[['id_eleve','nom','prenom']],left_on='id_eleve',right_on='id_eleve',how='left')      
        return df


    def df_sous_categorie(self,categorie):
        """
        This function will return a data frame which evaluates each student's competance by categories.
        df columns:
            id_eleve: int
            nom	: object
            prenom: object
            id_groupe: int
            sous_categorie: object
            note_par_cate: float
            num_question: int       
        """
        df_cate = self.df_que[self.df_que["categorie"] == categorie]
        cc = df_cate.groupby(['sous_categorie']).sous_categorie.count()
        df_cc = pd.DataFrame({"sous_categorie":cc.index.values, 'num_question':cc.values})
        competance_cate = self.df_bi[self.df_bi['categorie'] == categorie].groupby(['id_eleve','id_groupe','sous_categorie'])['note'].agg({'note_par_sous_cate': lambda x : x[x > 0].sum()}).reset_index()
        df = competance_cate.merge(df_cc, left_on= 'sous_categorie', right_on='sous_categorie',how='left')
        df = df.merge(self.df_eleve[['id_eleve','nom','prenom']],left_on='id_eleve',right_on='id_eleve',how='left')        
        return df
    
    
    def heatmap_categorie(self,id_groupe):
        """
        Data Frame output:
        
        id_groupe	
        id_eleve	
        nom	
        prenom	
        Gestion de projet	
        Architecture	
        Tableaux de bord	
        Entretien	
        Modélisation dimensionnelle
        """      
        if id_groupe < 0:
            print('\n\nError heatmap_categories: id_groupe can not be < 0 !\n\n')
            exit()
        df = self.df_categorie()
        df = df[df.id_groupe == id_groupe]
        df['competance'] = df.note_par_cate/df.num_question
        categorie_list = df.categorie.value_counts().index.values.tolist()
        df_new = df[['id_groupe','id_eleve','nom','prenom']].drop_duplicates().reset_index(drop = True)
        for i in categorie_list:
            df_new=df_new.merge(df[['id_eleve','competance']][df["categorie"] == i].rename(columns={"competance":i}))       
        return df_new
    
    
    def heatmap_sous_categorie(self,id_groupe,categorie):
        """
        Data Frame output:
        
        id_groupe	
        id_eleve	
        nom	
        prenom	
        sous-categorie dans ce categorie
        """       
        if id_groupe < 0:
            print('\n\nError heatmap_categories: id_groupe can not be < 0 !\n\n')
            exit()
        df = self.df_sous_categorie(categorie)
        df = df[df.id_groupe == id_groupe]
        df['competance'] = df.note_par_sous_cate/df.num_question
        sous_categorie_list = df.sous_categorie.value_counts().index.values.tolist()
        df_new = df[['id_groupe','id_eleve','nom','prenom']].drop_duplicates().reset_index(drop = True)
        for i in sous_categorie_list:
            df_new=df_new.merge(df[['id_eleve','competance']][df["sous_categorie"] == i].rename(columns={"competance":i}))       
        return df_new
 
     
    def df_matrix_categorie(self):
        """
        This function will return a data frame which evaluates each student's competance by categories.
        df columns:
            id_eleve: int
            nom	: object
            prenom: object
            id_groupe: int
            categorie: object
            real_note: string       
        """
        df_note = self.df_bi.groupby(['id_eleve','id_groupe','categorie'])['note'].agg({'note_cate': lambda x : x[x > 0].sum()}).reset_index()
        df_note['note_cate'] = df_note['note_cate'].astype(int)
        df_note['note_cate'] = df_note['note_cate'].astype(str)
        df_absence = self.df_bi.groupby(['id_eleve','id_groupe','categorie'])['absence'].agg({'num_absence':'sum'}).reset_index()
        df_ques = self.df_bi.groupby(['id_eleve','id_groupe','categorie']).id_question.agg({'num_question':'count'}).reset_index()
        df = pd.merge(df_absence, df_ques)
        df["actu_resp_ques"] = df["num_question"] - df["num_absence"]
        df_buffer = pd.merge(df_note, df)
        df_buffer["actu_resp_ques"] = df_buffer["actu_resp_ques"].astype(str)
        df_buffer["real_note"]= df_buffer["note_cate"].str.cat(df_buffer['actu_resp_ques'],sep = '/')
        df_buffer = df_buffer.merge(self.df_eleve[['id_eleve','nom','prenom']],left_on='id_eleve',right_on='id_eleve',how='left')
        return df_buffer
    
    
    def matrix_categorie(self,id_groupe):
        """
        Data Frame output:
        
        id_groupe	
        id_eleve	
        nom	
        prenom	
        Gestion de projet	
        Architecture	
        Tableaux de bord	
        Entretien	
        Modélisation dimensionnelle
        """      
        if id_groupe < 0:
            print('\n\nError heatmap_categories: id_groupe can not be < 0 !\n\n')
            exit()
        df = self.df_matrix_categorie()
        df = df[df.id_groupe == id_groupe]
        categorie_list = df.categorie.value_counts().index.values.tolist()
        df_new = df[['id_groupe','id_eleve','nom','prenom']].drop_duplicates().reset_index(drop = True)
        for i in categorie_list:
            df_new=df_new.merge(df[['id_eleve','real_note']][df["categorie"] == i].rename(columns={"real_note":i}),how='left')       
        return df_new
 
    
    def df_matrix_sous_categorie(self,categorie):
        """
        This function will return a data frame which evaluates each student's competance by categories.
        df columns:
            id_eleve: int
            nom	: object
            prenom: object
            id_groupe: int
            souscategorie: object
            real_note: string       
        """
        df_sous = self.df_bi[self.df_bi.categorie == categorie]
        df_note = df_sous.groupby(['id_eleve','id_groupe','sous_categorie'])['note'].agg({'note_souscate': lambda x : x[x > 0].sum()}).reset_index()
        df_note['note_souscate'] = df_note['note_souscate'].astype(int)
        df_note['note_souscate'] = df_note['note_souscate'].astype(str)
        df_absence = df_sous.groupby(['id_eleve','id_groupe','sous_categorie'])['absence'].agg({'num_absence':'sum'}).reset_index()
        df_ques = df_sous.groupby(['id_eleve','id_groupe','sous_categorie']).id_question.agg({'num_question':'count'}).reset_index()
        df = pd.merge(df_absence, df_ques)
        df["actu_resp_ques"] = df["num_question"] - df["num_absence"]
        df_buffer = pd.merge(df_note, df)
        df_buffer["actu_resp_ques"] = df_buffer["actu_resp_ques"].astype(str)
        df_buffer["real_note"]= df_buffer["note_souscate"].str.cat(df_buffer['actu_resp_ques'],sep = '/')
        df_buffer = df_buffer.merge(self.df_eleve[['id_eleve','nom','prenom']],left_on='id_eleve',right_on='id_eleve',how='left')
        return df_buffer
       
        
    def matrix_sous_categorie(self,id_groupe,categorie):
        """
        Data Frame output:
        
        id_groupe	
        id_eleve	
        nom	
        prenom	
        sous-categorie dans ce categorie
        """      
        if id_groupe < 0:
            print('\n\nError heatmap_categories: id_groupe can not be < 0 !\n\n')
            exit()
        df = self.df_matrix_sous_categorie(categorie)
        df = df[df.id_groupe == id_groupe]  
        sous_categorie_list = df.sous_categorie.value_counts().index.values.tolist()
        df_new = df[['id_groupe','id_eleve','nom','prenom']].drop_duplicates().reset_index(drop = True)
        for i in sous_categorie_list:
            df_new=df_new.merge(df[['id_eleve','real_note']][df["sous_categorie"] == i].rename(columns={"real_note":i}),how='left')      
        return df_new
  
    
    def absence_matrix(self,id_groupe,categorie = None):
            
        id_groupe_list = self.df_eleve.id_groupe.unique().tolist()
        categorie_list = self.df_que.categorie.unique().tolist()
        
        # absence matrix for all categorie
        if id_groupe in id_groupe_list and categorie == None:
            return self.matrix_categorie(id_groupe)  
        
        # absence for all categorie
        elif id_groupe in id_groupe_list and categorie not in categorie_list:
            print('categorie is:', categorie, ' which is not in \n','categorie_list:',categorie_list)
            return self.matrix_categorie(id_groupe)
        
        # absence for sous-categorie in categorie 
        elif id_groupe in id_groupe_list and categorie in categorie_list:
            return self.matrix_sous_categorie(id_groupe,categorie)
        
        elif id_groupe not in id_groupe_list:
            raise AttributeError('absence_matric, id_groupe = %d , which is not in id_groupe_list:'%id_groupe, sorted(id_groupe_list))
     
        
    def df_heatmap(self, id_groupe = None,categorie = None):
        """
            This function can return all kinds of df to draw a HeatMap
            id_groupe: choose a group of student by their id_groupe
            categorie: choose a categorie to show the competance of sous-categorie in this categorie, 
                        if categorie == None , show competance of all categorie
        """     
        id_groupe_list = self.df_eleve.id_groupe.unique().tolist()
        categorie_list = self.df_que.categorie.unique().tolist()
        
        # heatmap for all categorie
        if id_groupe in id_groupe_list and categorie == None:
            return self.heatmap_categorie(id_groupe)
        
        # heatmap for all categorie
        elif id_groupe in id_groupe_list and categorie not in categorie_list:
            print('categorie is:', categorie, ' which is not in \n','categorie_list:',categorie_list)
            return self.heatmap_categorie(id_groupe)
        
        # heatmap for sous-categorie in categorie 
        elif id_groupe in id_groupe_list and categorie in categorie_list:
            return self.heatmap_sous_categorie(id_groupe,categorie)
        
        elif id_groupe not in id_groupe_list:
            raise AttributeError('id_groupe = %s , which is not in id_groupe_list:'%id_groupe, sorted(id_groupe_list))

# test            
dashboard_prof('./Data/').df_score_by_qcm()