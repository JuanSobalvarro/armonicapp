import sounddevice as sd


class AudioManager:
    def __init__(self):
        self.selected_device = None

    @staticmethod
    def get_audio_devices():
        try:
            default_api_id = sd.default.hostapi
        except:
            default_api_id = 0

        devices = sd.query_devices()
        device_names = []
        for device in devices:
            if device['hostapi'] == default_api_id and device['max_input_channels'] > 0:
                device_names.append(device['name'])
        return device_names

    def select_audio_device(self, device_name):
        devices = sd.query_devices()
        for device in devices:
            if device['name'] == device_name and device['max_input_channels'] > 0:
                sd.default.device = (device['name'], None)
                self.selected_device = device['name']
                print(f"Selected audio device: {device['name']}")
                break

    def get_selected_device(self):
        return self.selected_device
