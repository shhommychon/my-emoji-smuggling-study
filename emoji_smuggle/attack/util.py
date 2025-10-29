class UnicodeByteEncoder:
    """
    유니코드 문자를 사용하여 바이트 시퀀스를 인코딩하고 디코딩하는 기본 클래스입니다.
    이 클래스는 특정 인코딩 방식을 구현하는 서브클래스를 위한 템플릿 역할을 합니다.

    원본 코드: https://github.com/paulgb/emoji-encoder/blob/main/app/encoding.ts
    """
    def __init__(self, *args, **kwargs):
        """생성자입니다.
        서브클래스에서 구현 바랍니다.
        """
        pass

    def _to_secret_char(self, byte: int) -> str:
        """하나의 바이트를 비밀 문자로 변환합니다.
        서브클래스에서 반드시 구현해야 합니다.
        """
        raise NotImplementedError # 서브클래스에서 미구현 시, 에러 발생.

    def _from_secret_char(self, char: str) -> int:
        """비밀 문자 하나를 바이트로 변환합니다.
        서브클래스에서 반드시 구현해야 합니다.
        """
        raise NotImplementedError # 서브클래스에서 미구현 시, 에러 발생.

    def _encode(self, text: str) -> str:
        """
        주어진 텍스트를 UTF-8 바이트로 변환한 뒤, 각 바이트를 비밀 문자로 매핑하여
        인코딩된 문자열을 생성합니다.

        원본 코드: https://github.com/paulgb/emoji-encoder/blob/main/app/encoding.ts#L31-L41
        """
        bytes_text = text.encode("utf-8")
        encoded = ''
        for byte in bytes_text:
            encoded_char = self._to_secret_char(byte)
            if encoded_char:
                encoded += encoded_char
        return encoded

    def _decode(self, text: str) -> str:
        """
        비밀 문자로 인코딩된 텍스트를 디코딩하여 원본 메시지를 복원합니다.

        원본 코드: https://github.com/paulgb/emoji-encoder/blob/main/app/encoding.ts#L43-L61
        """
        decoded_bytes = []
        for char in text:
            byte = self._from_secret_char(char)
            if byte is not None:
                decoded_bytes.append(byte)
            # 비밀 문자가 아닌 문자를 만나면 디코딩을 중단합니다.
            # (이미 디코딩된 바이트가 있는 경우에만)
            elif decoded_bytes:
                break
        return bytes(decoded_bytes).decode("utf-8", errors="ignore")
