#EL PARAMETRO DATA DEVUELVE LOS  METADATOS DEL EVENTO DE CLOUD STORAGE

def ds_tes_data (data, context, verbose=True):
    def vprint(s):
        if verbose:
            print(s)

    vprint('Event ID: {}'.format(context.event_id))
    vprint('Event type: {}'.format(context.event_type))
    
    import pandas as pd
    from google.cloud import storage
    import numpy as np 
    from pandasql import sqldf
    from loadtostorage import loadtostorage
    
    vprint('Importing required modules.')

    input_bucket_name = data['bucket']
    source_file = data['name']
    uri = 'gs://{}/{}'.format(input_bucket_name, source_file)

    archivo = source_file.split('.')[0]
    folder = archivo.split('/')[1]

    storage_client = storage.Client()

    if folder == 'raw':
    #Tomo el archivo que subimos del bucket y lo caraga en un dataframe
    #En caso de correr esta el codigo en local cambiar el valor de la variable uri por path de archivo 
    #uri = f'gs://{bucket_name}/{bucket_file}'
        uri = uri
        df = pd.read_csv(uri, sep=',', encoding='UTF-8')
    #Elimina las filas vacias RESPUESTA EJERCICIO 1 PASO VI A
        df = df.dropna()
    #En este etapa identificamos combinaciones unicas de los campos name y company_id antes de crear df agregado
        cat = pd.DataFrame() 
        cat_comp = pd.DataFrame() 
        for f in df[['name']]['name'].unique():
            df_cat = pd.DataFrame(columns=['company_id','name']) 
            df_cat['company_id'] = pd.DataFrame(df[df['name']== f ]['company_id'].unique())
            df_cat['name'] = f
            cat = pd.concat([cat,df_cat],axis = 0, ignore_index=True)
        for f in df[pd.isnull(df['name'])]['company_id'].unique():
            df_cat_comp = pd.DataFrame(columns=['company_id','name']) 
            df_cat_comp['company_id'] = pd.DataFrame(df[df['company_id']== f ]['company_id'].unique())
            #df_cat_comp['name'] = None
            cat = pd.concat([cat,df_cat_comp],axis = 0, ignore_index=True)     
    #creo un catalogo con valores unicos y limpios
        name = ['MiPas0xFFFF','MiP0xFFFF']
        cleancat = cat[~cat['name'].isin(name) & cat.name.notnull() & cat.company_id.notnull()].copy()
        cleancat = cleancat[cleancat['company_id'] != '*******']
        cleancat.reset_index()
    #cruzo el df raw vs el catalogo de atrimutos para limpiar los campos name y company 
    #limpiamos el campo name
        join = pd.merge(df, cleancat, on=["company_id"], how="left")
        join['name'] = np.where(join['name_y'].isnull(),join['name_x'],join['name_y'])
    #limpiamos el camco companany_id
        join = pd.merge(join, cleancat, on=["name"], how="left")
        join['company_id'] = np.where(join['company_id_y'].isnull(),join['company_id_x'],join['company_id_y'])
    #creamos un df dode dejamos la informacion procesada
        df_procesed = join[['id','name','company_id','amount','status','created_at','paid_at']]    
    #Tomo el dataframe processed y lo cargo al bucket anoc001-test-data-armandolara, anoc001-test-armandolara  de storage en la campeta processed
    #Solo ejecutar este bloque si el entorno esta dentro de GCP
        bucketname = ['anoc001-test-data-armandolara' , 'anoc001-test-armandolara']
        for i in bucketname:
            loadtostorage (i, df_procesed,'processed/data_prueba_tecnica_procesed.csv')
    #EN ESTE BLOQUE SE CREA DATAFRAME INSUMO PARA EL DASHBOARD CON LOS DATOS AGREGADOS
        q = """
        SELECT 
            name
            ,company_id
            ,created_at
            , sum(amount) AS Total
        FROM df_procesed 
        GROUP BY     
            name
            ,company_id
            ,created_at
        """
        dfgroupby = sqldf(q, globals())
    #Tomo el dataframe dfgroupby y lo cargo al bucket anoc001-test-data-armandolara, anoc001-test-armandolara  de storage en la campeta processed
    #Insumo para dashbord
    #Solo ejecutar este bloque si el entorno esta dentro de GCP
        bucketname = ['anoc001-test-data-armandolara' , 'anoc001-test-armandolara']
        for i in bucketname:
            loadtostorage (i, dfgroupby,'processed/dash_insumo.csv')