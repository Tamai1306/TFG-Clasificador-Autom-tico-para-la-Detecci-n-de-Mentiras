import numpy as np
import scipy.io as sio
import glob

#Inicializar los valores para obtener el Accuray
TP=0
TN=0
FP=0
FN=0

#Cargar los datos de audio y video
for folder in glob.glob("./Ronda_*/"):
    print(folder)

    data_shoulder=np.load(folder+'shoulder.npz')
    data_dominant=np.load(folder+'dominant_emo.npz')
    mat_analitics = sio.loadmat(folder+"analitics.mat")
    mat_tuple_clasification = sio.loadmat(folder+"tuple_clasification.mat")
    mat_tuple_pauses = sio.loadmat(folder+"tuple_pauses.mat")
    data_info_speech=mat_analitics['analitics']
    data_tuple_clasification=mat_tuple_clasification['tuple_clasification']
    data_tuple_pauses=mat_tuple_pauses['tuple_pauses']

    #Almacenar los datos en vectores de diccionarios en el caso de los datos de Matlab
    info_speech={
        data_info_speech[0,0][0]:data_info_speech[0,1][0], #Range Pitch
        data_info_speech[0,2][0]:data_info_speech[0,3][0], #Truthfullness
        data_info_speech[0,4][0]:data_info_speech[0,5][0], #Mean Energy
        data_info_speech[0,6][0]:data_info_speech[0,7][0], #Renge Velocity
    }

    speech_analitics=[]
    for i in range(len(data_tuple_clasification[0])):
        for j in data_tuple_clasification[0][i]:
            speech_analitics.append({
                j[0][0]:j[1][0], #Time
                j[2][0]:j[3][0], #Pitch
                j[4][0]:j[5][0], #Energy
                j[6][0]:j[7][0], #Speech Rate
            })

    speech_pauses=[]
    for i in range(len(data_tuple_pauses[0])):
        for j in data_tuple_pauses[0][i]:
            speech_pauses.append({
                j[0][0]:j[1][0], #Time
                j[2][0]:j[3][0], #Pause Duration
            })

    #Cargar los datos extraidos del video
    time_emotion=data_dominant['time_emo']
    dominant_emotion=data_dominant['dominant']
    time_left_shoulder=data_shoulder['time_left_shoulder']
    time_right_shoulder=data_shoulder['time_right_shoulder']

    #Obtener la pausa de mayor duración
    max_pause=float('-inf')
    for i in speech_pauses:
        if max_pause < i['Pause_Duration']:
            max_pause=float(i['Pause_Duration'])
    
    #Generar árbol de decisión con las ponderaciones
    alpha=0
    for i in speech_analitics:
        if i['Pitch']>info_speech['Range_Pitch'][-1]:
            if speech_pauses[0]['Pause_Duration'] != 0:
                for j in speech_pauses:
                    if i['Time'][1]==j['Time'][0] or i['Time'][0]==j['Time'][1]:
                        if i['Speech_Rate'] < info_speech['Range_velocity'][0]:
                            if i['Energy'] > info_speech['Mean_Energy']:
                                alpha+=1
                            else:
                                alpha+=0.9
                            alpha+=float(j['Pause_Duration'])/max_pause
            else:
                if (i['Speech_Rate'] < info_speech['Range_velocity'][0] or i['Speech_Rate'] > info_speech['Range_velocity'][1]):
                    if i['Energy'] > info_speech['Mean_Energy']:
                        alpha+=0.8
                    else:
                        alpha+=0.7

        else:
            if speech_pauses[0]['Pause_Duration'] != 0:
                for j in speech_pauses:
                    if i['Time'][1]==j['Time'][0] or i['Time'][0]==j['Time'][1]:
                        if i['Speech_Rate'] < info_speech['Range_velocity'][0]:
                            if i['Energy'] > info_speech['Mean_Energy']:
                                alpha+=0.9
                            else:
                                alpha+=0.8
                            alpha+=float(j['Pause_Duration'])/max_pause
            else:
                if (i['Speech_Rate'] < info_speech['Range_velocity'][0] or i['Speech_Rate'] > info_speech['Range_velocity'][1]):
                    if i['Energy'] > info_speech['Mean_Energy']:
                        alpha+=0.8
                    else:
                        alpha+=0.7

    for i in speech_analitics:
        if i['Pitch']>info_speech['Range_Pitch'][1]:
            closest_ini=min(time_emotion,key=lambda x: abs(x-i['Time'][0]))
            closest_fin=min(time_emotion,key=lambda x: abs(x-i['Time'][1]))
            idx_ini=np.where(time_emotion==closest_ini)
            idx_fin=np.where(time_emotion==closest_fin)
            for j in range(int(idx_ini[0]),int(idx_fin[0])):
                if dominant_emotion[j] == 'fear':
                    alpha+=0.1
       
        elif i['Pitch']<(int(info_speech['Range_Pitch'][1])+int(info_speech['Range_Pitch'][0]))/2:
            closest_ini=min(time_emotion,key=lambda x: abs(x-i['Time'][0]))
            closest_fin=min(time_emotion,key=lambda x: abs(x-i['Time'][1]))
            idx_ini=np.where(time_emotion==closest_ini)
            idx_fin=np.where(time_emotion==closest_fin)
            for j in range(int(idx_ini[0]),int(idx_fin[0])):
                if dominant_emotion[j] == 'sad':
                    alpha+=0.1

    print(alpha)

    #Calcular los valores de TP,TN,FP,FN
    if info_speech['Truthfulness'] == 0:
        print("Mentira")
    else:
        print("Verdad")

    if alpha > 2:
        lie=True
        print("Detectado Mentira")
    else:
        lie=False
        print("Detectado Verdad")
    
    if info_speech['Truthfulness'] == 1 and not lie:
        TN+=1
    elif info_speech['Truthfulness'] == 1 and lie:
        FN+=1
    elif info_speech['Truthfulness'] == 0 and lie:
        TP+=1
    elif info_speech['Truthfulness'] == 0 and not lie:
        FP+=1
    #print("TP: {} FP: {} TN: {} FN: {}".format(TP,FP,TN,FN))
    print("############################################################")

#Calcular el Accuracy
print("\n RESULTADOS:")
print("Positive: {} Negative: {}".format(TP+FP,TN+FN))
print("TP: {} FP: {} TN: {} FN: {}".format(TP,FP,TN,FN))
ACC=(TP+TN)/(TP+TN+FP+FN)
DACC=TP/(TP+FP)
HACC=TN/(TN+FN)
print("Accuracy: {}% Deception Accuracy: {}% Honestly Accuracy: {}%".format(ACC*100,DACC*100,HACC*100))
TPR=TP/(TP+TN)
FPR=FP/(FP+TN)
print("True Positive Rate: {} False Positive Rate: {}".format(TPR,FPR))
confusion_matrix=np.array([[TP,FN],[FP,TN]])
print(confusion_matrix)