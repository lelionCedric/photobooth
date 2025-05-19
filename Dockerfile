FROM python:3

# Dépendances pour PyQt6 + gphoto2 + X11
RUN apt-get update && apt-get install -y \
    libgphoto2-dev gphoto2 \
    ffmpeg libsm6 libxext6 \
    x11-apps libxcb-xinerama0 \
    libxcb-cursor0 \
    && apt-get clean

# Copier le code
WORKDIR /app
COPY . /app

# Installer dépendances Python
RUN pip install PyQt5 gphoto2
# Installer d'autres dépendances si présentes dans requirements.txt
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

CMD ["python3", "main.py"]