class ExamException(Exception):
    pass


class CSVTimeSeriesFile():
    def __init__(self,name):
        self.name=name
    
    def get_data(self):

        #controlli sull'input del file 

        #verifico che il nome del file è una stringa
        if type(self.name)!=str : 
            raise ExamException('Il nome del file deve essere una stringa, non {}'.format(type(self.name))) 

        else:
            #il nome del file è una stringa
            try:
                #provo ad aprire il file
                file=open(self.name,'r') 
                file.readline()
                #se il file non esiste alzo un'eccezione
            except FileNotFoundError as e:
                raise ExamException("Errore di apertura del file:'{}'".format(e))
      
            #inizializzo la lista di liste che deve tornare la funzione
            time_series=[]
                
            #scorro riga per riga il file 
            for line in file:
            #divido dopo la virgola
                value=line.split(',')
                row_list=[]

                if value!='date': #'date,passeggeri'=intestazione

                    # controllo che nella seconda colonna ci siano solo valori accettabili   
                    try:
                    #provo a convertire il valore a intero
                        value[1]=int(value[1])

                        #se il valore è un intero positivo
                        if value[1]>0:
                            # per ogni riga crea una lista con la data in stringa e il valore corrispondente
                            row_list.append(str(value[0]))
                            row_list.append(int(value[1]))
                        
                        else:
                            #se il valore è negativo  passo alla riga successiva
                            row_list.append(str(value[0]))
                            row_list.append(None)

                    except ValueError:
                        #se il valore non è convertibile a intero, lo ignoro
                        row_list.append(str(value[0]))
                        row_list.append(None)
                        
                    #aggiungo row_list alla lista finale
                    time_series.append(row_list)
                            

            #controllare l'ordine delle date
            for n in range(1,len(time_series)):
                #controllo che non ci sia un timestamp duplicato 
                if time_series[n][0:4]==time_series[n-1][0:4]:
                   raise ExamException('timestamp duplicato')
                   
                #controllo che il timestamp sia ordinato
                if time_series[n][0:4]<time_series[n-1][0:4]:
                    raise ExamException('timestamp fuori ordine')

            #chiudo il file e ritorno la serie
            file.close()
            return time_series
                


#funzione per calcolare la differenza media 
def compute_avg_monthly_difference(time_series,first_year,last_year):
    #controlli su fist_year e last_year 
    
    #provo a converitire first_year e last_year da stringhe a interi
    try :
        first_year=int(first_year)
        last_year=int(last_year)

        #se non è possibile alzo un'eccezione
    except ValueError as e: 
        raise ExamException('{}'.format(e))


    #controllo che first e last_year sono presenti nella time_series 
    for list in time_series:
        #se sono all'ultima riga e non ho trovato first_year alzo un'eccezione
        if list[0]==time_series[-1][0]: 
            raise ExamException('{} non è presente nel file'.format(first_year))

        #se ho torvato first_year
        elif list[0][0:4]==str(first_year): 
            break #esco dal ciclo
        else:
            continue #altrimenti vado alla lista successiva


    #analogamente per last_year
    for list in time_series:
        if list[0]==time_series[-1][0]: 
            raise ExamException('{} non è presente nel file'.format(last_year))

        elif list[0][0:4]==str(last_year): 
            break 
        else:
            continue


    #creo una lista per ogni anno da considerare 
    liste=[]
    
    for year in range(first_year,last_year+1):

        anno=[None]*12 # lista che dovrà contenere i valori di un anno (12 elementi, inizalizzati a None)

        for list in time_series:
                
            #confronto i primi 4 caratteri di lista con year (anno tra first_year e last_year che sto considerando)
            if list[0][0:4]==str(year):
                #per ogni mese
                for i in range(1,13): 
                    #se ho il data lo sostituisco, altirmento rimane 0
                    if int(list[0][-2:])==(i):
                        anno[i-1]=list[1]
                       
        liste.append(anno)
    
    #calcolo della media
    media=[]

    #ciclo sui mesi (da 0 a 11)
    for i in range(0,12):

        var=[0]*12  #lista per la varianza inizializzata a 0
        cont=0  #variabile per memorizzare il numero di operazioni compiute

        #ciclo su liste 
        for j in range(1,len(liste)):

            #se entrambe le liste che sto considerando non sono None
            if liste[j][i]!=None and liste[j-1][i]!=None: 
                cont=cont+1  #aumento il contatore

                #calcolo la varianza di ogni mese
                var[i]+=liste[j][i]-liste[j-1][i]
                    
            else: #altrimenti sotituisco con 0
                var[i]+=0
                 
        #divido la varianza per il numero di anni considerati
        if cont>0:
            media.append(var[i]/cont)
        else:
            media.append(0)

    #ritorno la media
    return media