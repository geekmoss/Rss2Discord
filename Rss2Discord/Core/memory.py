import msgpack
import os


class Memory:
    def __init__(self, backup_file: str = 'memory.msgpack'):
        self.__backup = backup_file

        if os.path.exists(backup_file):
            self.load_backup()
        else:
            self.__l: dict[str, set[str]] = {}
        pass

    @staticmethod
    def __decode_set(obj):
        if '__set__' in obj:
            obj = set(obj['val'])
        return obj

    @staticmethod
    def __encode_set(obj):
        if isinstance(obj, set):
            return {'__set__': True, 'val': list(obj)}
        return obj

    def is_new(self, key: str, id_: str) -> bool:
        d = self.__l.get(key)
        return d is not None and id_ in d

    def save_ids(self, key: str, ids: set[str]) -> None:
        self.__l[key] = self.__l.get(key, set()) | ids
        self.save_backup()
        return

    def get_ids(self, key) -> set[str] | None:
        return self.__l.get(key)

    def load_backup(self):
        with open(self.__backup, 'rb') as f:
            try:
                d = msgpack.load(f, object_hook=self.__decode_set)
            except ValueError:
                d = {}
            self.__l = d or dict()

    def save_backup(self):
        with open(self.__backup, 'wb') as f:
            msgpack.dump(self.__l, f, default=self.__encode_set)
            pass
        pass
    pass
