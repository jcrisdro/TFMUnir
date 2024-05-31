# 1. Modelo

## Flow
![Alt text](image.png)


# 2. Configuracion

## Configuración ambientes

### Windows

### Linux

### Mac OS

Instale los paquetes y lance la funcion de exportar
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
export PATH="/opt/homebrew/bin:$PATH"

brew install pyenv
brew install pyenv-virtualenv
brew install ffmpeg
brew install hdf5
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


## Configurar virtual envs
Instale la version de python con `pyenv`
> ```
> pyenv install --list
> pyenv install 3.11.0
> ```

Ubique el directorio de trabajo y corra los siguientes comandos
> ```
> pyenv local 3.11.0
> pyenv virtualenv
> pyenv virtualenv 3.11.0 .ia_venv
> ```

Donde `.ia_venv` es el nombre del folder de nuestro entorno virtual local
> ```
> pyenv local .ia_venv 
> python --version
> which python
> ```

## Activar virtual envs
Para activar el ambiente virtual hagalo ingresando al proyecto y vera en el shell `(.ia_venv)` o si no ejecute la ruta completa
> ```
> cd project
> source /Users/joseph.diaz/.pyenv/versions/3.11.0/envs/.ia_venv/bin/activate
> ```

## Instalacion paquetes
Para instalar los paquetes necesarios ejecute

> ```
> pip3 install --upgrade pip
> pip3 install -r requirements.txt
> ```
y puede validar que todos los paquetes quedaran instalados dando `pip3 freeze` o `pip3 list`


Si tiene problemas con los paquetes puede validar usando la opcion de `pipx`
> ```
> pipx install nltk
> pipx install scikit-learn
> pipx install gensim
> ```

# 3. Lanzar proyecto
Para lanzar el proyecto se cuenta con las opciones de `api` y de `cli`

## API
Con api tendras la posiblidad de cargar un video a traves los siguientes pasos:

### 1. Levante el servicio
Levante el ambiente a traves de servicios api rest de fastapi con el comando
> ```
> uvicorn project.adapters.rest:app --host 0.0.0.0 --port 8000 --reload
> ```

Y ejecute todo el contenido desde [http://localhost:8000/docs](http://localhost:8000/docs) 

- `POST /v1/load`
- `POST /v1/training/cvv1`
- `POST /v1/training/cav1`


## CLI

