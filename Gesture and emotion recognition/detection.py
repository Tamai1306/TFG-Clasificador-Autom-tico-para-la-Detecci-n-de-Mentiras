import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
import numpy as np
import os
from deepface import DeepFace
import glob
import os
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose



folder_dataset="../Dataset/video/"
#Obtener videos del dataset
for i in glob.glob("../Dataset/video/Ronda_*"):
  print("Analizando {}...".format(i.split("/")[3]))
  video=i.split("/")[3]
  folder="./"+video.replace(".mp4","")+"/"
  if not os.path.isdir(folder): #Si no existiese la carpeta crearla
      os.mkdir(folder)
  
  #Abrir el video
  cap = cv2.VideoCapture(folder_dataset+video)

  #Crear los vectores de detección de posición de cada hombro
  left_shoulder_y=[]
  right_shoulder_y=[]

  #Cargar el detector Haar Cascade
  face_cascade_name = cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml'  #getting a haarcascade xml file
  face_cascade = cv2.CascadeClassifier()  #processing it for our project
  if not face_cascade.load(cv2.samples.findFile(face_cascade_name)):  #adding a fallback event
      print("Error loading xml file")

  #Crear los vectores de almacenamiento de las emociones
  time=[]
  angry=[]
  disgust=[]
  fear=[]
  happy=[]
  sad=[]
  surprise=[]
  neutral=[]
  time=[]
  dominant=[]
  time_emo=[]

  #Deteccion de la Pose con MediaPipe
  with mp_pose.Pose(
      min_detection_confidence=0.5,
      min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
      success, image = cap.read()
      if not success:
        print("Ignoring empty camera image.")
        # If loading a video, use 'break' instead of 'continue'.
        break

      #Recortar el video para obtener la zona en la que se encuentra la visualización de hombros
      image_crop=image[370:850,660:1400]
      time.append(cap.get(cv2.CAP_PROP_POS_MSEC)/1000)
      
      #Para el frame actual calcular la Pose
      image_crop.flags.writeable = False
      image_crop = cv2.cvtColor(image_crop, cv2.COLOR_BGR2RGB)
      results = pose.process(image_crop)
      image_crop.flags.writeable = True
      image_crop = cv2.cvtColor(image_crop, cv2.COLOR_RGB2BGR)

      # Extraer landmarks
      try:
        landmarks=results.pose_landmarks.landmark
      except:
        pass
      
      #Dibujar los landmarks
      mp_drawing.draw_landmarks(
          image_crop,
          results.pose_landmarks,
          mp_pose.POSE_CONNECTIONS,
          landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
      
      #Almacenar la coordenada y de cada hombro
      left_shoulder_y.append(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y)
      right_shoulder_y.append(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y)
      
      #Deteccion de Emociones
      facecasc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
      gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) 
      faces=face_cascade.detectMultiScale(gray,scaleFactor=1.05,minNeighbors=5)

      #En caso de obtener más de una cara, quedarse solo con la principal
      if np.size(faces)>4:
          faces=[faces[0]]
      #Para la cara detectada en el video extraer las emociones
      for (x,y,w,h) in faces:
      
          cv2.rectangle(image, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)

          #Extraer las emociones
          try:
              analyze = DeepFace.analyze(image,actions=['emotion'],detector_backend='opencv')  
             
          except:
              break
          
          #Almacenar las emociones detectadas
          values=list(analyze['emotion'].values())
          angry.append(values[0])
          disgust.append(values[1])
          fear.append(values[2])
          happy.append(values[3])
          sad.append(values[4])
          surprise.append(values[5])
          neutral.append(values[6])

          cv2.putText(image, analyze['dominant_emotion'], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
          dominant.append(analyze['dominant_emotion'])
          time_emo.append(cap.get(cv2.CAP_PROP_POS_MSEC)/1000)
          #this is the part where we display the output to the user
          
      cv2.imshow("Video", cv2.resize(image,(1280,720),interpolation = cv2.INTER_CUBIC))
      # Flip the image horizontally for a selfie-view display.
      cv2.imshow('Crop', cv2.resize(image_crop,(1280,720)))
      if cv2.waitKey(5) & 0xFF == 27:
        break
  cap.release()
  cv2.destroyAllWindows()

  #Detectar movimientos de los hombros
  offset=50
  left_shoulder_y=np.round(left_shoulder_y,3)
  i=0
  time_left_shoulder=[]#np.array([0,0])
  while(i<len(left_shoulder_y)-offset):
    aux=left_shoulder_y[i:i+offset]
    #max_v=np.max(left_shoulder_y[i:i+offset])
    min_v=np.min(left_shoulder_y[i:i+offset])
    if aux[0]-min_v>=10**-2 and aux[-1]-min_v>=10**-2:
      if aux[0] > aux[1]:
        j=1
        while(j<len(aux) and aux[j-1]>aux[j]):
          j+=1
        
        while(j+1<len(aux) and aux[j]<aux[j+1]):
          j+=1

        if(j<len(aux)-1):
          time_left_shoulder.append([time[i],time[i+offset]])
          i+=offset-1
    i+=1

  i=0
  right_shoulder_y=np.round(right_shoulder_y,3)
  time_right_shoulder=[]
  while(i<len(right_shoulder_y)-offset):
    aux=right_shoulder_y[i:i+offset]
    min_v=np.min(right_shoulder_y[i:i+offset])
    if aux[0]-min_v>10**-2 and aux[-1]-min_v>10**-2:
      if aux[0] > aux[1]:
        j=1
        while(j<len(aux) and aux[j-1]>aux[j]):
          j+=1
        
        while(j+1<len(aux) and aux[j]<aux[j+1]):
          j+=1

        if(j<len(aux)-1):
          time_right_shoulder.append([time[i],time[i+offset]])
          i+=offset-1
    i+=1

  #Guardar las figuras con las emociones detectadas a lo largo del video
  plt.title("angry")
  plt.plot(time_emo,angry)
  plt.savefig(folder+"angry.svg")
  plt.clf()

  plt.title("disgust")
  plt.plot(time_emo,disgust)
  plt.savefig(folder+"disgust.svg")
  plt.clf()

  plt.title("fear")
  plt.plot(time_emo,fear)
  plt.savefig(folder+"fear.svg")
  plt.clf()

  plt.title("happy")
  plt.plot(time_emo,happy)
  plt.savefig(folder+"happy.svg")
  plt.clf()

  plt.title("sad")
  plt.plot(time_emo,sad)
  plt.savefig(folder+"sad.svg")
  plt.clf()

  plt.title("surprise")
  plt.plot(time_emo,surprise)
  plt.savefig(folder+"surprise.svg")
  plt.clf()

  #Guardar los vectores principales, emocion dominante, tiempo de emocion dominante y tiempos en los que se ha detectado los movimientos de hombros
  np.savez(folder+'dominant_emo.npz',dominant=dominant,time=time,time_emo=time_emo)
  np.savez(folder+'shoulder.npz',time_left_shoulder=time_left_shoulder,time_right_shoulder=time_right_shoulder)