#### 1단계: UTF-8 바이트 변환 UTF-8 Byte Conversion

모든 유니코드 문자는 메모리에 저장되거나 네트워크로 전송될 때 바이트(byte) 시퀀스로 변환되어야 합니다. All Unicode characters must be converted into a sequence of bytes when stored in memory or transmitted over a network.

UTF-8은 이 변환을 수행하는 가장 일반적인 인코딩 방식입니다. UTF-8 is the most common encoding standard used for this conversion.

UTF-8은 문자의 유니코드 코드 포인트 값의 크기에 따라 1바이트에서 4바이트까지 가변 길이 템플릿을 사용합니다. UTF-8 uses variable-length templates, from 1 to 4 bytes, depending on the magnitude of the character's Unicode ID.

<a id="examples"></a>

##### 예시 1: `I` (1-Byte) → `[73]`

###### 1. 유니코드 ID를 2진수로 변환 Get the Unicode ID in Binary

- `I` → $U+0049$
- 16진수 유니코드 ID를 10진수 ID로 변환 시 converting a hexadecimal Unicode ID to a decimal ID: `73`
- 16진수 유니코드 ID를 2진수 ID로 변환 시 converting a hexadecimal Unicode ID to a binary ID: `1001001`

###### 2. 올바른 바이트 템플릿 선택 Pick the Correct Byte Template

이 문자는 1-바이트 템플릿 범위($U+0000$ \~ $U+007F$)에 속합니다. This character falls within the 1-byte template range ($U+0000$ to $U+007F$).

- Byte 1: `0xxxxxxx` (0\~127)

이 템플릿은 7비트의 페이로드를 가집니다. This template holds 7 payload bits.

###### 3. 2진수 ID 채우기 Pad the Binary ID

템플릿은 7비트를 필요로 하고, 2진수 ID도 7비트 길이입니다. The template needs 7 bits, and our binary ID is 7 bits long.

추가 패딩이 필요하지 않습니다. No leading zeros are needed for padding.

- 패딩된 2진수 Padded Binary: `1001001`

###### 4. 2진수 ID를 청크로 분할 Split the Padded Binary into Chunks

템플릿에 맞게 7비트 청크 하나로 분할합니다. Split this into one 7-bit chunk to fit the template:

- Chunk 1: `1001001`

###### 5. 청크를 템플릿에 붓기 Pour the Chunks into the Template

템플릿의 시그널 비트와 청크를 결합합니다. Take our signal bit and add our chunk:

- Byte 1: `0` + `1001001` = `01001001`

###### 6. 10진수로 변환 Convert to Decimal

- Byte 1: `01001001` = `73`

##### 예시 2: `©` (2-Byte) → `[194, 169]`

###### 1. 유니코드 ID를 2진수로 변환 Get the Unicode ID in Binary

- `©` → $U+00A9$
- 16진수 유니코드 ID를 10진수 ID로 변환 시 converting a hexadecimal Unicode ID to a decimal ID: `169`
- 16진수 유니코드 ID를 2진수 ID로 변환 시 converting a hexadecimal Unicode ID to a binary ID: `10101001`

###### 2. 올바른 바이트 템플릿 선택 Pick the Correct Byte Template

이 문자는 2-바이트 템플릿 범위($U+0080$ \~ $U+07FF$)에 속합니다. This character falls within the 2-byte template range ($U+0080$ to $U+07FF$).

- Byte 1: `110xxxxx` (192\~223)
- Byte 2: `10xxxxxx` (128\~191)

이 템플릿은 11비트의 페이로드를 가집니다. This template holds 11 payload bits.

###### 3. 2진수 ID 채우기 Pad the Binary ID

템플릿은 11비트를 필요로 하지만, 2진수 ID는 8비트 길이입니다. The template needs 11 bits, but our binary ID is only 8 bits long.

비트 수를 맞추기 위해 3개의 0을 앞에 추가합니다. Add three leading zeros to pad it to 11 bits.

- 패딩된 2진수 Padded Binary: `000` + `10101001` = `00010101001`

###### 4. 2진수 ID를 청크로 분할 Split the Padded Binary into Chunks

템플릿에 맞게 5비트와 6비트의 청크 두개로 분할합니다. Split this 11-bit number into two chunks of 5 and 6 to fit the template:

- Chunk 1: `00010`
- Chunk 2: `101001`

###### 5. 청크를 템플릿에 붓기 Pour the Chunks into the Template

템플릿의 시그널 비트와 청크를 결합합니다. Take our signal bits and add our chunks:

- Byte 1: `110` + `00010` = `11000010`
- Byte 2: `10` + `101001` = `10101001`

###### 6. 10진수로 변환 Convert to Decimal

- Byte 1: `11000010` = `194`
- Byte 2: `10101001` = `169`

##### 예시 3: `이` (3-Byte) → `[236, 157, 180]`

###### 1. 유니코드 ID를 2진수로 변환 Get the Unicode ID in Binary

- `이` → $U+C774$
- 16진수 유니코드 ID를 10진수 ID로 변환 시 converting a hexadecimal Unicode ID to a decimal ID: `51060`
- 16진수 유니코드 ID를 2진수 ID로 변환 시 converting a hexadecimal Unicode ID to a binary ID: `1100011101110100`

###### 2. 올바른 바이트 템플릿 선택 Pick the Correct Byte Template

이 문자는 3-바이트 템플릿 범위($U+0800$ \~ $U+FFFF$)에 속합니다. This character falls within the 3-byte template range ($U+0800$ to $U+FFFF$).

- Byte 1: `1110xxxx` (224\~239)
- Byte 2: `10xxxxxx` (128\~191)
- Byte 3: `10xxxxxx` (128\~191)

이 템플릿은 16비트의 페이로드를 가집니다. This template holds 16 payload bits.

###### 3. 2진수 ID 채우기 Pad the Binary ID

템플릿은 16비트를 필요로 하고, 2진수 ID도 16비트 길이입니다. The template needs 16 bits, and our binary ID is 16 bits long.

추가 패딩이 필요하지 않습니다. No leading zeros are needed for padding.

- 패딩된 2진수 Padded Binary: `1100011101110100`

###### 4. 2진수 ID를 청크로 분할 Split the Padded Binary into Chunks

템플릿에 맞게 4비트, 6비트, 6비트의 청크 세개로 분할합니다. Split this 16-bit number into three chunks of 4, 6 and 6 to fit the template:

- Chunk 1: `1100`
- Chunk 2: `011101`
- Chunk 3: `110100`

###### 5. 청크를 템플릿에 붓기 Pour the Chunks into the Template

템플릿의 시그널 비트와 청크를 결합합니다. Take our signal bits and add our chunks:

- Byte 1: `1110` + `1100` = `11101100`
- Byte 2: `10` + `011101` = `10011101`
- Byte 3: `10` + `110100` = `10110100`

###### 6. 10진수로 변환 Convert to Decimal

- Byte 1: `11101100` = `236`
- Byte 2: `10011101` = `157`
- Byte 3: `10110100` = `180`

##### 예시 4: `😈` (4-Byte) → `[240, 159, 152, 136]`

###### 1. 유니코드 ID를 2진수로 변환 Get the Unicode ID in Binary

- `이` → $U+1F608$
- 16진수 유니코드 ID를 10진수 ID로 변환 시 converting a hexadecimal Unicode ID to a decimal ID: `128520`
- 16진수 유니코드 ID를 2진수 ID로 변환 시 converting a hexadecimal Unicode ID to a binary ID: `11111011000001000`

###### 2. 올바른 바이트 템플릿 선택 Pick the Correct Byte Template

이 문자는 4-바이트 템플릿 범위($U+10000$ \~ $U+10FFFF$)에 속합니다. This character falls within the 4-byte template range ($U+10000$ to $U+10FFFF$).

- Byte 1: `11110xxx` (240\~247)
- Byte 2: `10xxxxxx` (128\~191)
- Byte 3: `10xxxxxx` (128\~191)
- Byte 4: `10xxxxxx` (128\~191)

이 템플릿은 21비트의 페이로드를 가집니다. This template holds 21 payload bits.

###### 3. 2진수 ID 채우기 Pad the Binary ID

템플릿은 21비트를 필요로 하지만, 2진수 ID는 17비트 길이입니다. The template needs 21 bits, but our binary ID is only 17 bits long.

비트 수를 맞추기 위해 4개의 0을 앞에 추가합니다. Add four leading zeros to pad it to 21 bits.

- 패딩된 2진수 Padded Binary: `0000` + `11111011000001000` = `000011111011000001000`

###### 4. 2진수 ID를 청크로 분할 Split the Padded Binary into Chunks

템플릿에 맞게 3비트, 6비트, 6비트, 6비트의 청크 세개로 분할합니다. Split this 21-bit number into four chunks of 3, 6, 6 and 6 to fit the template:

- Chunk 1: `000`
- Chunk 2: `011111`
- Chunk 3: `011000`
- Chunk 4: `001000`

###### 5. 청크를 템플릿에 붓기 Pour the Chunks into the Template

템플릿의 시그널 비트와 청크를 결합합니다. Take our signal bits and add our chunks:

- Byte 1: `11110` + `000` = `11110000`
- Byte 2: `10` + `011111` = `10011111`
- Byte 3: `10` + `011000` = `10011000`
- Byte 4: `10` + `001000` = `10001000`

###### 6. 10진수로 변환 Convert to Decimal

- Byte 1: `11110000` = `240`
- Byte 2: `10011111` = `159`
- Byte 3: `10011000` = `152`
- Byte 4: `10001000` = `136`

##### 바이트 시퀀스 생성 예제 요약 Byte Sequence Generation Example Summarized

예제 공격 프롬프트 전체 문장은 위 과정을 모든 문자에 대해 반복하여 생성된, 수백 개 길이의 단일 바이트 시퀀스가 됩니다. The entire example attack prompt becomes a single sequence of bytes, hundreds of bytes long, generated by repeating the above process for every single character.

UTF-8로 인코딩할 수 있는 문자라면, 영어뿐만 아니라 한국어, 일본어, 중국어, 러시아어, 인도어, 아랍어 등 다양한 언어의 문자에도 모두 적용할 수 있다는 것입니다. This method can be applied to any character that can be encoded in UTF-8, not only English but also characters from languages like Korean, Japanese, Chinese, Russian, Hindi, Arabic, and others.

특히 이 인코딩된 문자열을 복호화하는 방법을 별도로 프롬프트에 명시하지 않아도 된다는 특징을 보이기도 합니다. The characteristic of this encoding method is that there is no need to explicitly add in instructions about how to decode the encoded string in the prompt.

###### ※ UTF-8 가변 길이 및 자기 동기화에 관한 추가 설명 Additional explanation on UTF-8 variable length and self-synchronization

디코더가 이 긴 바이트 스트림에서 언제 3바이트를 읽고, 언제 1바이트를 읽어야 하는지 어떻게 알 수 있는지에 대한 궁금증이 생길 수 있습니다. One might wonder how the decoder can determine when to read 3 bytes and when to read 1 byte from this long byte stream.

정답은 *첫 번째 바이트의 시작 비트*에 있습니다. The answer lies in the *signal bits at the start of the first byte*.

UTF-8은 '자기 동기화'가 가능하도록 설계되어 있어, 바이트 스트림의 아무 곳에서나 읽기 시작해도 첫 바이트의 앞부분 몇 비트만 보면 이 문자가 총 몇 바이트로 구성되어 있는지, 그리고 지금 읽는 바이트가 첫 번째 바이트인지 아니면 두 번째(또는 세 번째, 네 번째) 바이트인지를 즉시 알 수 있습니다. UTF-8 was designed to be self-synchronizing, meaning that no matter where a computer start reading in the byte stream, the computer can instantly tell how many bytes total make up the character — and whether it's on the first byte or a continuation byte (second, third, or fourth) — just by looking at the first few bits.

- `0xxxxxxx` (0-127): 이것은 1바이트 문자입니다. This is a 1-byte character. (e.g., `I` → `[73]`)
- `110xxxxx` (192-223): 이것은 2바이트 문자의 시작이며, 1개의 바이트가 뒤따라옵니다. This is the start of a 2-byte character, and 1 byte follows. (e.g., `©` → `[194, ...]`)
- `1110xxxx` (224-239): 이것은 3바이트 문자의 시작이며, 2개의 바이트가 뒤따라옵니다. This is the start of a 3-byte character, and 2 bytes follow. (e.g., '이' → `[236, ...]`)
- `11110xxx` (240-247): 이것은 4바이트 문자의 시작이며, 3개의 바이트가 뒤따라옵니다. This is the start of a 4-byte character, and 3 bytes follow. (e.g., `😈` → `[240, ...]`)
- `10xxxxxx` (128-191): 이것은 멀티바이트 문자의 '두 번째 이후' 바이트입니다. This is a 'continuation byte' (second or later) of a multi-byte character. (e.g., `[... 157, 180]`)

이 규칙은 매우 엄격합니다. This rule is extremely strict.

예를 들어, `[237, 109, 56]`와 같은 바이트 시퀀스는 유효한 UTF-8 문자열에 *존재할 수 없습니다.* For instance, a byte sequence like `[237, 109, 56]` *cannot exist* in a valid UTF-8 string.

그 이유는 첫 번째 바이트가 한 *약속*을 두 번째 바이트가 깨뜨리기 때문입니다. The reason is that the second byte breaks the *promise* made by the first byte.

1.  Byte 1: `237` = `11101101`
    - 이 바이트는 `1110...`으로 시작합니다. 이것은 "3바이트 문자의 시작" 신호입니다. It starts with `1110...`. This is a "Start of 3-byte" signal.
    - 이 바이트는 "*다음에 오는 두 바이트*는 **반드시** `10...`으로 시작하는 '지속 바이트(continuation bytes)'여야 한다"고 약속합니다. It makes a promise: "The *next two* bytes **must** be continuation bytes (starting with `10...`)."

2.  Byte 2: `109` = `01101101`
    - 이 바이트는 `0...`으로 시작합니다. 이것은 "1바이트 단일 문자" 신호입니다. It starts with `0...`. This is a "Single-byte" signal.
    - UTF-8 디코더는 여기서 즉시 멈추고 오류를 보고합니다. A UTF-8 decoder stops here and reports an error.
    - 이는 디코더는 128-191 범위(`10xxxxxx`)의 바이트를 예상했지만, 1바이트 문자 'm'에 해당하는 `109`를 만났기 때문입니다. Thisi because it was expecting a byte in the 128-191 range (`10xxxxxx`), but it got `109` (which is the single-byte character 'm').

3. `[237, 109, 56]` 시퀀스는 "손상된 3바이트 문자... 뒤에 오는 유효한 문자 'm'... 뒤에 오는 유효한 문자 '8'"로 읽히게 됩니다. The sequence `[237, 109, 56]` would be read as: "a corrupted 3-byte character... followed by the valid character 'm'... followed by the valid character '8'."