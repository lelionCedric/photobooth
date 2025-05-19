import io
import os
import time
import datetime
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt, pyqtSignal, QObject

try:
    import gphoto2 as gp
except ImportError:
    gp = None  # gphoto2 est optionnel

def get_gp_camera_proxy(port=None):
    """Retourne un proxy de caméra si une caméra compatible gPhoto2 est trouvée,
    sinon retourne None.

    :param port: chercher sur le port spécifié
    :type port: str
    """
    if not gp:
        print("Le module gphoto2 n'est pas installé")
        return None

    # Arrêter les processus gphoto2 existants qui peuvent bloquer l'accès à la caméra
    try:
        import subprocess
        subprocess.run(["pkill", "-f", "*gphoto2*"], stderr=subprocess.DEVNULL)
    except Exception:
        pass

    if hasattr(gp, 'gp_camera_autodetect'):
        # gPhoto2 version 2.5+
        cameras = gp.check_result(gp.gp_camera_autodetect())
    else:
        port_info_list = gp.PortInfoList()
        port_info_list.load()
        abilities_list = gp.CameraAbilitiesList()
        abilities_list.load()
        cameras = abilities_list.detect(port_info_list)
        
    if cameras:
        print(f"Caméras gPhoto2 trouvées sur les ports: '{', '.join([p for _, p in cameras])}'")
        # Initialiser le premier proxy de caméra et le retourner
        camera = gp.Camera()
        if port is not None:
            port_info_list = gp.PortInfoList()
            port_info_list.load()
            idx = port_info_list.lookup_path(port)
            camera.set_port_info(port_info_list[idx])

        try:
            camera.init()
            return camera
        except gp.GPhoto2Error as ex:
            print(f"Impossible de se connecter à la caméra gPhoto2: {ex}")

    return None


class CameraManager(QObject):
    """Gestionnaire de caméra utilisant gphoto2."""
    
    preview_ready = pyqtSignal(QImage)
    capture_ready = pyqtSignal(str)
    capture_error = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self._camera = None
        self._context = gp.Context()
        self._preview_timer = QTimer()
        self._preview_timer.timeout.connect(self._update_preview)
        self._initialize_camera()
        
    def _initialize_camera(self):
        """Initialise la caméra."""
        self._camera = get_gp_camera_proxy()
        if not self._camera:
            print("Aucune caméra compatible gPhoto2 trouvée")
        else:
            print("Caméra initialisée avec succès")
            
            # Configurer la caméra pour un usage optimal
            try:
                # Essayer de définir la cible de capture sur la carte mémoire
                config = self._camera.get_config()
                section = config.get_child_by_name('settings')
                target = section.get_child_by_name('capturetarget')
                target.set_value('Memory card')
                self._camera.set_config(config)
                print("Cible de capture configurée sur 'Memory card'")
            except Exception as e:
                print(f"Impossible de configurer la cible de capture: {e}")
    
    def start_preview(self, interval=500):
        """Démarre l'aperçu en continu.
        
        :param interval: intervalle de rafraîchissement en millisecondes
        """
        if self._camera:
            self._preview_timer.start(interval)
        else:
            print("Aucune caméra disponible pour l'aperçu")
    
    def stop_preview(self):
        """Arrête l'aperçu."""
        self._preview_timer.stop()
    
    def _update_preview(self):
        """Capture et émet une image d'aperçu."""
        if not self._camera:
            return
            
        try:
            camera_file = self._camera.capture_preview(self._context)
            file_data = camera_file.get_data_and_size()
            
            # Convertir en QImage
            image = QImage.fromData(file_data)
            
            if not image.isNull():
                self.preview_ready.emit(image)
            else:
                print("L'image d'aperçu est nulle")
        except Exception as e:
            print(f"Erreur lors de la capture d'aperçu: {e}")
            self.stop_preview()
    
    def capture_photo(self):
        """Capture une photo et retourne le chemin du fichier."""
        if not self._camera:
            self.capture_error.emit("Aucune caméra disponible")
            return None
            
        try:
            # Créer le dossier photos s'il n'existe pas
            os.makedirs("photos", exist_ok=True)
            
            # Générer le nom de fichier
            filename = f"photos/photo_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            
            # Capturer l'image
            print("Capture de l'image...")
            file_path = self._camera.capture(gp.GP_CAPTURE_IMAGE, self._context)
            
            # Télécharger l'image depuis la caméra
            camera_file = self._camera.file_get(
                file_path.folder, 
                file_path.name, 
                gp.GP_FILE_TYPE_NORMAL,
                self._context
            )
            
            # Enregistrer l'image
            camera_file.save(filename)
            
            print(f"Photo enregistrée: {filename}")
            self.capture_ready.emit(filename)
            return filename
        except Exception as e:
            error_msg = f"Erreur lors de la capture de photo: {e}"
            print(error_msg)
            self.capture_error.emit(error_msg)
            return None
    
    def close(self):
        """Ferme la connexion à la caméra."""
        self.stop_preview()
        if self._camera:
            self._camera.exit(self._context)
            self._camera = None