from emoji_smuggle.util import UnicodeByteEncoder

class PrivateUseAreaEncoder(UnicodeByteEncoder):
    """
    사설 사용 영역(Private Use Area, PUA) 유니코드 블록을 사용하여 메시지를 인코딩하는 클래스입니다.
    PUA 문자는 일반적으로 화면에 사각형이나 기호로 렌더링될 수 있습니다.
    """
    def __init__(
            self,
            append_emoji: bool = False, 
            base_emoji: str = '🤫',
            *args, **kwargs
        ):
        """생성자입니다.

        Args:
            append_emoji (bool): 인코딩된 메시지 앞에 이모지를 추가할지 여부.
            base_emoji (str): `append_emoji`가 True일 때 사용할 기본 이모지.
        """
        super().__init__(*args, **kwargs)

        self.append_emoji = append_emoji
        self.base_emoji = base_emoji

        # 사설 사용 영역 블록 (U+E000-U+E0FF)
        # https://unicode.org/charts/nameslist/n_E0000.html
        self.PUA_START = 0xE000
        self.PUA_END = 0xE0FF

    def _to_secret_char(self, byte: int) -> str:
        """바이트 값을 PUA 문자로 변환합니다."""
        # 바이트 값이 유효한 범위(0-255) 내에 있는지 확인합니다.
        if 0 <= byte <= 255:
            # PUA 시작 코드 포인트에 바이트 값을 더하여 문자로 변환합니다.
            return chr(self.PUA_START + byte)
        # 유효하지 않은 바이트 값인 경우
        else:
            return None # 유효하지 않으면 None을 반환합니다.

    def _from_secret_char(self, char: str) -> int:
        """PUA 문자를 바이트 값으로 변환합니다."""
        # 입력 문자가 비어있는지 확인합니다.
        if not char: 
            return None # 비어있으면 None을 반환합니다.

        # 문자의 유니코드 코드 포인트를 가져옵니다.
        code_point = ord(char)
        # 코드 포인트가 PUA 블록 범위 내에 있는지 확인합니다.
        if self.PUA_START <= code_point <= self.PUA_END:
            # PUA 시작 코드 포인트를 빼서 원래 바이트 값을 복원합니다.
            return code_point - self.PUA_START
        # PUA 블록에 속하지 않는 문자인 경우
        else:
            return None # None을 반환합니다.
    
    def _append_emoji(self, encoded: str, emoji: str = None) -> str:
        """인코딩된 문자열 앞에 이모지를 추가합니다."""
        if emoji is None:
            emoji = self.base_emoji
        return emoji + encoded

    def encode(self, text: str, emoji: str = None) -> str:
        """
        주어진 텍스트를 PUA 문자를 사용하여 인코딩합니다.
        필요에 따라 앞에 이모지를 붙일 수 있습니다。
        """
        encoded = self._encode(text)
        if self.append_emoji: encoded = self._append_emoji(encoded, emoji)
        return encoded

    def decode(self, text: str) -> str:
        """PUA 문자로 인코딩된 텍스트를 디코딩합니다."""
        return self._decode(text)
