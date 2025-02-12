import torchaudio
from src.datasets.base_dataset import BaseDataset
from src.utils.io_utils import ROOT_PATH


class CustomDirAudioDataset(BaseDataset):
    def __init__(self, audio_dir, transcription_dir=None, *args, **kwargs):
        data = []
        data_root = ROOT_PATH / "data" / "datasets"

        for path in (data_root / audio_dir).iterdir():
            entry = {}
            if path.suffix in [".mp3", ".wav", ".flac", ".m4a"]:
                entry["path"] = str(path)
                t_info = torchaudio.info(str(path))
                entry["audio_len"] = t_info.num_frames / t_info.sample_rate

                if transcription_dir and (data_root / transcription_dir).exists():
                    transc_path = data_root / transcription_dir / (path.stem + ".txt")
                    if transc_path.exists():
                        with transc_path.open() as f:
                            entry["text"] = f.read().strip()
            if len(entry) > 0:
                data.append(entry)
        super().__init__(data, *args, **kwargs)
