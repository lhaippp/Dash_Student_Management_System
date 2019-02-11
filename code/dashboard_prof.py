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
    file_path = "/content/drive/My Drive/S5/F3B_415_G11/data"
    
    
    def __init__(self, file_path = file_path):       
        import os 
        print("__Path__:",file_path,'\nFiles in the path: \n',os.listdir(file_path))
        self.df_bi = pd.read_csv(file_path+"/fact_table_bi_exam.csv")
        self.df_eleve = pd.read_csv(file_path+"/eleve.csv")
        self.df_que = pd.read_csv(file_path+"/question.csv")
        self.df_bi['note'][self.df_bi.absence == 1] = 0
        
    
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
        competance_cate = self.df_bi.groupby(['id_eleve','id_groupe','categorie'])['note'].agg({'note_par_cate':'sum'}).reset_index()
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
        print(categorie,"\n",df_cc)
        competance_cate = self.df_bi[self.df_bi['categorie'] == categorie].groupby(['id_eleve','id_groupe','sous_categorie'])['note'].agg({'note_par_sous_cate':'sum'}).reset_index()
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
            raise AttributeError('id_groupe = %d , which is not in id_groupe_list:'%id_groupe, sorted(id_groupe_list))