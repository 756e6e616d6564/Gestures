# Controlador por gestos
> #
> V 0.1B
> >Controlador Gesture estable
> > visualizador implementado correctamente.
> #
###### (Dígase integración física-virtual)

> ##
> Reglas
> - Los frames mínimos del programa en general no deben bajar de los 10fps
> - El programa no debe concentrar todos los recursos de la máquina
> - En lo posible debe estar contenido en un área virtual específica
> - Debe responder correctamente las instrucciones externas que se le permitan
> - Además, tiene que actuar sin restricción o limitante alguno sobre señales de *Panic* que genere el sistema 
> ##

#### * EN TRABAJO DE CONSTRUCCIÓN *

La fase actual del proyecto se basa en la estructuración de la plataforma adecuada para el reconocimiento de gestos y su posterior uso en diferentes sistemas para el control de lo que se requiera.

Actualmente se encuentra en una fase beta; se está desarrollando el "reconocedor" de visual, que posteriormente se utilizará para su procesamiento en un posible módulo.

---
> #
> ##### *Requisitos indispensables:*
> - Python _________________ == 3.10 *(exclusivamente)*
> - Mediapipe ______________ >= 0.10.14
> - OpenCV-contrib-python ____ >= 4.10.0.84
> - OpenCV-python __________ >= 4.10.0.84
> - OpenCV-python-headless __ >= 4.10.0.84  *(Por un error no detectado en los complementos opencv, estos tienen que ser instalados siguiendo el orden listado, del caso contrario, el programa no dectectará ninguno y por consecuencia, no funcionará)*
> - Pyautogui >=0.9.54
> - Matplotlib >= 3.9.0
> - Numpy >= 2.0.0
> - Threaded >= 4.2.0 *(Revisar versión e importaciones, puede que no sea necesario)*
> #