from emoji_smuggle.util import UnicodeByteEncoder

class VariationSelectorEncoder(UnicodeByteEncoder):
    """
    유니코드 변형 선택자(Variation Selectors)를 사용하여 메시지를 인코딩하는 클래스입니다.
    이 문자들은 보이지 않는(zero-width) 특성이 있어 텍스트에 숨기기 용이합니다.
    """
    def __init__(
            self,
            append_emoji: bool = True, 
            base_emoji: str = '🫣',
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

        # 변형 선택자 블록 (U+FE00-U+FE0F)
        # https://unicode.org/charts/nameslist/n_FE00.html
        self.VS_START = 0xFE00
        self.VS_END = 0xFE0F

        # 변형 선택자 보충 블록 (U+E0100-U+E01EF)
        # https://unicode.org/charts/nameslist/n_E0100.html
        self.VS_SUP_START = 0xE0100
        self.VS_SUP_END = 0xE01EF

    def _to_secret_char(self, byte: int) -> str:
        """바이트 값을 변형 선택자 문자로 변환합니다.
        
        원본 코드: https://github.com/paulgb/emoji-encoder/blob/main/app/encoding.ts#L11-L19
        """
        # 바이트 값이 첫 번째 변형 선택자 블록 범위(0-15) 내에 있는지 확인합니다.
        if 0 <= byte < 16:
            # VS 시작 코드 포인트에 바이트 값을 더하여 문자로 변환합니다.
            return chr(self.VS_START + byte)
        # 바이트 값이 두 번째 변형 선택자 보충 블록 범위(16-255) 내에 있는지 확인합니다.
        elif 16 <= byte < 256:
            # VS 보충 시작 코드 포인트에 (바이트 값 - 16)을 더하여 문자로 변환합니다.
            return chr(self.VS_SUP_START + byte - 16)
        # 유효하지 않은 바이트 값인 경우
        else:
            return None # 유효하지 않으면 None을 반환합니다.

    def _from_secret_char(self, char: str) -> int:
        """변형 선택자 문자를 바이트 값으로 변환합니다.

        원본 코드: https://github.com/paulgb/emoji-encoder/blob/main/app/encoding.ts#L21-L29
        """
        # 입력 문자가 비어있는지 확인합니다.
        if not char: 
            return None # 비어있으면 None을 반환합니다.

        # 문자의 유니코드 코드 포인트를 가져옵니다.
        code_point = ord(char)
        # 코드 포인트가 첫 번째 변형 선택자 블록 범위 내에 있는지 확인합니다.
        if self.VS_START <= code_point <= self.VS_END:
            # VS 시작 코드 포인트를 빼서 원래 바이트 값을 복원합니다.
            return code_point - self.VS_START
        # 코드 포인트가 두 번째 변형 선택자 보충 블록 범위 내에 있는지 확인합니다.
        elif self.VS_SUP_START <= code_point <= self.VS_SUP_END:
            # VS 보충 시작 코드 포인트를 빼고 16을 더하여 원래 바이트 값을 복원합니다.
            return code_point - self.VS_SUP_START + 16
        # 변형 선택자 블록에 속하지 않는 문자인 경우
        else:
            return None # None을 반환합니다.
    
    def _append_emoji(self, encoded: str, emoji: str = None) -> str:
        """인코딩된 문자열 앞에 이모지를 추가합니다."""
        if emoji is None:
            emoji = self.base_emoji
        return emoji + encoded

    def encode(self, text: str, emoji: str = None) -> str:
        """
        주어진 텍스트를 변형 선택자 문자를 사용하여 인코딩합니다.
        필요에 따라 앞에 이모지를 붙일 수 있습니다.
        """
        encoded = self._encode(text)
        if self.append_emoji: encoded = self._append_emoji(encoded, emoji)
        return encoded

    def decode(self, text: str) -> str:
        """변형 선택자 문자로 인코딩된 텍스트를 디코딩합니다."""
        return self._decode(text)
