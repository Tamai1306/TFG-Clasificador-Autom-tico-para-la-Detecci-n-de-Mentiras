# TFG: Clasificador Automatico para la Deteccion de Mentiras
## Índice:
- [1. Introducción](#intro)
- [2. Instalación](#install)
- [3. Cómo usar](#use)
- [4. Demostración](#demo)

## Introducción: <a name="intro"/>
Desde los inicios del ser humano se han ido desarrollando diversas capacidades para adaptarse al entorno o a las diferentes circunstancias de la vida. Conforme el habla fue desarrollándose junto a las habilidades sociales, también apareció la capacidad de ocultar la verdad. Los seres humanos aprendemos a mentir desde muy pequeños conforme nos relacionamos con el entorno y con el resto de seres humanos.
Este proyecto consta del desarrollo de un sistema automático para la detección de mentiras,
mediante el empleo de herramientas de reconocimiento de audio y de visión por computador en vı́deo. Para llevarlo a cabo, se ha generado una base de datos propia compuesta por vı́deos y audio, a partir de la cual se extraerán las caracterı́sticas principales en las que la voz transmite información útil sobre la veracidad de un discurso. Por otro lado, se analizarán las emociones de las personas de los vı́deos de la base de datos, ası́ como uno de sus movimientos corporales. En conjunto estas caracterı́sticas servirán para generar un clasificador automático que sea capaz de dirimir si una persona ha sido sincera o ha mentido o engañado.

En este repositorio se van a presentar los códigos del Trabajo Fin de Grado del Grado en Ingeniería Robótica de la Universidad de Alicante, proyecto desarrollado por Tamai Ramírez Gordillo.  Este proyecto ha sido desarrollado en `Ubuntu 20.04` mediante el empleo de **MATLAB** y **Python 3**.
## Instalación <a name="install"/>
Para poder ejecutar este proyecto, es necesario tener instalados tanto las toolboxes de MATLAB como los frameworks de Python3 necesarios.
**Toolboxes de Matlab:**
Estas toolboxes servirán para extraer las características de cada audio de la base de datos, las cuales son `pitch`, `speech rate`, `energía` y `pausas` de la voz.
 [VOICEBOX Toolbox](http://www.ee.ic.ac.uk/hp/staff/dmb/voicebox/voicebox.html#analysis "VOICEBOX Toolbox")
 [The SpeechMark Toolbox](https://speechmrk.com/speechmark-products-downloads/the-speechmark-matlab-toolbox/ "The SpeechMark Toolbox")
[Audio Toolbox](https://es.mathworks.com/products/audio.html "Audio Toolbox")
Una vez descargadas las toolboxes, agregarlas al *path* de MATLAB.

**Dependencias y Frameworks de Python:**
Para instalar las dependencias y los frameworks de Python se tiene que ejecutar el archivo `requirements.txt`  mediante el siguiente comando de *bash* en una terminal de **Ubuntu**.
```bash
$ pip3 install -r requirements.txt
```
Una vez instalado, estos frameworks y dependencias servirán para extraer las emociones y la detección de los movimientos del torso de las personas de los vídeos de la base de datos.
Por último, es necesario descargar el [dataset](www.kaggle.com/dataset/6bb95f89ef2bfd8df571ad3cc6e70f862d198e6748bd7ba807543a9d3589c7c5 "dataset") de kaggle. **Importante:** el dataset debe estar guardado en la misma carpeta que el proyecto y con el nombre `Dataset`.
## Modo de Uso: <a name="use"/>
1. Ejecutar el código `main.m`que se encuentra en la carpeta `Speech_Matlab`, una vez realizado este paso, se habrán generado para cada archivo de audio una subcarpeta dentro de la carpeta de `Gesture and emotion recognition`. En cada una de estas subcarpetas, cuyos nombres serán los nombres de los archivos de audio,  se habrán almacenado los archivos *.mat* con las características de audio extraídas. Por otro lado, en la propia carpeta `Speech_Matlab`, se habrán generado dos subcarpetas, la subcarpeta `Figures` contendrá laspresentaciones gráficas de las características extraídas y la subcarpeta `DataFiles` contendrá los archivos *.txt* con los resúmenes de las características extraídas y los datos importantes de cada audio.
2. Estando dentro de la carpeta  `Gesture and emotion recognition` ejecutar el comando:
```bash
$ python3 detection.py
```
Este código cargará cada vídeo de la base de datos y extraerá las emociones del rostro de cada persona así como la detección del movimiento de los hombros, que se almacenarán en las subcarpetas donde se ha extraído las características del audio asociado a ese vídeo.

3. Ejecutar el comando:
```bash
$ python3 main.py
```
Este código cargará los datos extraídos anteriormente de cada subcarpeta y generará el árbol de decisión que dirimirá a partir de estos datos, que vídeos y audios pertenecen a una persona que ha mentido o a una persona que ha sido sincera.

## Demostración: <a name="demo"/>
Para ejemplificar la ejecución de los códigos anteriores, se ha creado un vídeo demostracion en el que se muestra el funcionamiento del sistema en tiempo real con los vídeos del dataset. El vídeo en cuestión se encuentra [Aquí](https://youtu.be/NqE1uMfK7sQ "Aquí").
