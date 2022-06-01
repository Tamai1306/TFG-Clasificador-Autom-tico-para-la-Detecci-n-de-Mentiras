## TFG: Clasificador Automatico para la Deteccion de Mentiras
## Índice:
1. [Introducción.](#Intro)
2. [Instalación](#install)

## 1.  Introducción
Desde los inicios del ser humano se han ido desarrollando diversas capacidades para adaptarse al entorno o a las diferentes circunstancias de la vida. Conforme el habla fue desarrollándose junto a las habilidades sociales, también apareció la capacidad de ocultar la verdad. Los seres humanos aprendemos a mentir desde muy pequeños conforme nos relacionamos con el entorno y con el resto de seres humanos.
Este proyecto consta del desarrollo de un sistema automático para la detección de mentiras,
mediante el empleo de herramientas de reconocimiento de audio y de visión por computador en vı́deo. Para llevarlo a cabo, se ha generado una base de datos propia compuesta por vı́deos y audio, a partir de la cual se extraerán las caracterı́sticas principales en las que la voz transmite información útil sobre la veracidad de un discurso. Por otro lado, se analizarán las emociones de las personas de los vı́deos de la base de datos, ası́ como uno de sus movimientos corporales. En conjunto estas caracterı́sticas servirán para generar un clasificador automático que sea capaz de dirimir si una persona ha sido sincera o ha mentido o engañado.

En este repositorio se van a presentar los códigos del Trabajo Fin de Grado del Grado en Ingeniería Robótica de la Universidad de Alicante, proyecto desarrollado por Tamai Ramírez Gordillo.  Este proyecto ha sido desarrollado en `Ubuntu 20.04` mediante el empleo de **MATLAB** y **Python 3**.

## 2. Instalación
Para poder ejecutar este proyecto, es necesario tener instalados tanto las toolboxes de MATLAB como los frameworks de Python3 necesarios.
**Toolboxes de Matlab:**
 [VOICEBOX Toolbox](http://www.ee.ic.ac.uk/hp/staff/dmb/voicebox/voicebox.html#analysis "VOICEBOX Toolbox")
 [The SpeechMark Toolbox](https://speechmrk.com/speechmark-products-downloads/the-speechmark-matlab-toolbox/ "The SpeechMark Toolbox")
[Audio Toolbox](https://es.mathworks.com/products/audio.html "Audio Toolbox")

**Dependencias y Frameworks de Python:**
Para instalar las dependencias y los frameworks de Python se tiene que ejecutar el archivo `requirements.txt`  mediante el siguiente comando de *bash* en una terminal de **Ubuntu**
```bash
$ pip3 install -r requirements.txt
```


