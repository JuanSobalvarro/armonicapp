from src.app import App
from src.audio import AudioManager

def main():
    audio_manager = AudioManager()
    app = App(audioManager=audio_manager)
    app.mainloop()


if __name__ == "__main__":
    main()