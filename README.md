
# 1. Modelo

## 1.1. Flow
<picture>
  <img 
    align="center" width="75%" height="75%"
    alt="Flow" src="backend/resources/readme/flow.png" />
</picture>


## 1.2. Arquitectura
<picture>
  <img 
    width="45%" height="45%"
    alt="Archicture" src="backend/resources/readme/arquitectura.png">
</picture>

<picture>
  <img 
    width="45%" height="45%"
    alt="Hearing Aid Model" src="backend/resources/readme/hamodel.png">
</picture>

<picture>
  <img 
    width="45%" height="45%"
    alt="Visual Support Model" src="backend/resources/readme/vsmodel.png">
</picture>

# 2. Configuracion paquetes y ambientes backend

## 2.1. Instalación paquetes

### 2.1.1. Linux

```
sudo apt-get update && apt-get upgrade
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev
```
Y se actualizan los archivos
```
curl https://pyenv.run | bash
sudo apt-get install liblzma-dev
sudo apt-get install ffmpeg
sudo apt-get instal libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
sudo apt-get build-dep hdf5
sudo apt-get pipx
```

Adicione estas lineas de codigo en los archivos `~/.profile` y `~/.bash_profile`

```
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

```
eval "$(pyenv virtualenv-init -)"
```


### 2.1.2. Mac OS

Instale los paquetes y lance la funcion de exportar
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
export PATH="/opt/homebrew/bin:$PATH"

brew install pyenv
brew install pyenv-virtualenv
brew install ffmpeg
brew install hdf5
brew install portaudio 
```

Adicione estas lineas de codigo en los archivos `~/.bash_profile` y `~/.bashrc`

```
# Brew
export PATH="/opt/homebrew/bin:$PATH"

# PyEnv
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

Reinicie la configuracion de perfil de bash
> ```
> source ~/.bash_profile 
> source ~/.bashrc
> ```


## 2.2. Configurar virtual envs
Instale la version de python con `pyenv`
> ```
> pip3 install poetry
> poetry init
> poetry shell
> poetry add git+https://github.com/openai/whisper.git\n
> xargs poetry add < requirements.txt
> ```
y puede validar que todos los paquetes quedaran instalados dando `pip3 freeze` o `pip3 list`


Si tiene problemas con los paquetes puede validar usando la opcion de `pipx`
> ```
> pipx install nltk
> pipx install scikit-learn
> pipx install gensim
> ```

## 2.5. Lanzar proyecto
Para lanzar el proyecto se cuenta con las opciones de `api` y de `cli`

### 2.5.1. Levante el servicio API
Con api tendras la posiblidad de cargar un video a traves los siguientes pasos:
Levante el ambiente a traves de servicios api rest de fastapi con el comando
> ```
> cd backend
> uvicorn project.adapters.rest:app --host 0.0.0.0 --port 8000 --reload
> ```

Y ejecute todo el contenido desde [http://localhost:8000/docs](http://localhost:8000/docs) 

**Correr modelo apoyo personas con idioma de señas**
- `POST /v1/run/models/hamodel`
- `GET /v1/run/models/hamodel`

**Correr modelo apoyo personas con discapacidad visual**
- `POST /v1/run/models/vsmodel`
- `GET /v1/run/models/vsmodel`

### 2.5.2. Modelo HAModel

**CLI**

Validar modelo hamodel desde una oracion
> ```
> cd backend
> PYTHONPATH=. python3 project/adapters/cli/v1/__init__.py --model hamodel --sentences 'sentences'
> ```

Validar modelo hamodel desde un video
> ```
> cd backend
> PYTHONPATH=. python3 project/adapters/cli/v1/__init__.py --model hamodel --sentences 'sentences' --path 'video.mp4'
> ```

Validar modelo hamodel desde una entrada de audio
> ```
> cd backend
> PYTHONPATH=. python3 project/adapters/cli/v1/__init__.py --model hamodel --audio True
> ```
Ejemplos de frases y respuestas
* _fqEO3MuTlEE_15-5-rgb_front	87.94	88.72	Oh!_
* _fqEO3MuTlEE_16-5-rgb_front	88.73	91.52	That's a little bit more than a little bit._
* _fqEO3MuTlEE_17-5-rgb_front	92.4	95.79	Give it a straw and bottoms up!_
* _fqEO3MuTlEE_2-5-rgb_front	13.47	20.84	Find that real quick, here we go._
* _fqEO3MuTlEE_3-5-rgb_front	21.76	24.89	And, also, one shot of dark rum._
* _fqEO3MuTlEE_4-5-rgb_front	25.54	26.84	Here we go._
* _fqEO3MuTlEE_5-5-rgb_front	27.43	30.18	And, some lime juice._
* _fqEO3MuTlEE_6-5-rgb_front	36.64	41.76	About a teaspoon of lime juice._
* _fqEO3MuTlEE_7-5-rgb_front	42.03	48.12	Next we're going to add pineapple juice and orange juice._
* _fqEO3MuTlEE_8-5-rgb_front	48.81	52.62	There's orange juice and pineapple juice._
* _fqEO3MuTlEE_9-5-rgb_front	52.7	54.31	Equal parts of both._
* _fsfTrRxuJ-c_0-5-rgb_front	0.84	1.26	Hi!_


Testear modelo hamodel con datos prueba
> ```
> cd backend
> PYTHONPATH=. python3 project/adapters/cli/v1/__init__.py --model hamodel --test_audio_v2 True
> ```


**REST**

Validar modelo hamodel desde una oracion
> ```
> curl -X 'POST' \
> 'http://127.0.0.1:8000/v1/run/models/hamodel?sentences=sentences' \
> -H 'accept: application/json' \
> -H 'Content-Type: multipart/form-data' \
> -F 'file='
> ```


Validar modelo hamodel desde un video
> ```
> curl -X 'POST' \
>  'http://127.0.0.1:8000/v1/run/models/hamodel?sentences=sentences' \
>  -H 'accept: application/json' \
>  -H 'Content-Type: multipart/form-data' \
>  -F 'file=@video.mp4;type=video/mp4'
> ```


### 2.5.3. Modelo VSModel

**CLI**

Validar modelo vsmodel desde la camara
> ```
> cd backend
> PYTHONPATH=. python3 project/adapters/cli/v1/__init__.py --model vsmodel --cam True
> ```

## 2.6. Despliegues
El despliegue de los servicios de backend se hará a traves de tuneles con ngrok exponiendo el puerto 8000 a la nube
> ```
> ngrok http http://localhost:8000
> ```

# 3. Configuracion paquetes y ambientes mobile


# 4. Autores

- @victor1404 Victor Llinares
- @kakaroto2202 Cesar Montero
- @jcrisdro Joseph Diaz

