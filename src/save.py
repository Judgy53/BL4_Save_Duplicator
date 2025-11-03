from pathlib import Path
import random
import re
import yaml
import copy
from lib.blcrypt import decrypt_sav_to_yaml, encrypt_yaml_to_sav

STEAM_ID_REGEX = r".*Borderlands 4\/Saved\/SaveGames\/(.*)\/Profiles\/client\/.*\.sav"

class Save:
    def __init__(self, data: dict, steam_id: str):
        self.data = data
        self.steam_id = steam_id

    def clone(self) -> 'Save':
        """Creates a deep copy of the Save instance."""
        return Save(copy.deepcopy(self.data), self.steam_id)

    def get_char_name(self) -> str:
        """Returns the character's name from the save data."""
        return self.data.get("state", {}).get('char_name', "")

    def set_char_name(self, new_name: str):
        """Sets the character's name."""
        self.data.get("state", {})['char_name'] = new_name

    def get_char_guid(self) -> str:
        """Returns the character's GUID."""
        return self.data.get("state", {}).get('char_guid', "")

    def randomize_char_guid(self):
        """Generates and sets a new random character GUID."""
        new_guid = ''.join(random.choice('0123456789ABCDEF') for _ in range(32))
        self.data.get("state", {})['char_guid'] = new_guid
        return new_guid

    def get_playtime(self) -> int:
        """Returns the total playtime from the save data."""
        return self.data.get("state", {}).get('total_playtime', 0)

    def reset_playtime(self):
        """Resets the playtime to zero."""
        self.data.get("state", {})['total_playtime'] = 0

    def reset_challenges(self):
        """Resets all non-UVH challenges."""
        challenges = self.data.get('stats', {}).get('challenge', {})
        for challenge in challenges.copy():
            if challenge.find('uvh') == -1:
                del challenges[challenge]

    def reset_uvh_challenges(self):
        """Resets all UVH challenges and sets UVH level to 1."""
        challenges = self.data.get('stats', {}).get('challenge', {})
        for challenge in challenges.copy():
            if challenge.find('uvh') != -1:
                del challenges[challenge]

        if self.data.get('globals', {}).get('highest_unlocked_vault_hunter_level', 0) > 1:
            self.data['globals']['highest_unlocked_vault_hunter_level'] = 1
            self.data['globals']['vault_hunter_level'] = 1

    def save_to_file(self, file_path: str):
        """Saves the current save data to a file."""
        yaml_output = yaml.dump(self.data, default_flow_style=False, allow_unicode=True, sort_keys=False)

        path = Path(file_path)
        temp_yaml = path.with_suffix('.temp.yaml')
        temp_yaml.write_text(yaml_output, encoding='utf-8')
        sav_bytes = encrypt_yaml_to_sav(temp_yaml, self.steam_id)
        temp_yaml.unlink()

        path.write_bytes(sav_bytes)

    @classmethod
    def try_load_from_file(cls, file_path: str, steam_id: str) -> 'Save':
        """Loads and decrypts a save file, returning a Save instance."""
        if not steam_id:
            match = re.match(STEAM_ID_REGEX, file_path)
            if match:
                steam_id = match.group(1)
            else:
                raise ValueError("Steam ID could not be determined from file path.")

        path = Path(file_path)
        yaml_bytes = decrypt_sav_to_yaml(path, steam_id)
        if yaml_bytes:
            yaml_dict: dict = yaml.safe_load(yaml_bytes.decode('utf-8'))
            return cls(yaml_dict, steam_id)
        raise ValueError("Failed to decrypt or parse the save file.")
