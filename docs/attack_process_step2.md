#### 2단계: "비밀 알파벳" 매핑 "Secret Alphabet" Mapping

위의 개념 증명 유튜브 쇼츠 영상에서는 이 "비밀 알파벳"으로 길이가 없는 문자인 유니코드 Variation Selectors 영역을 사용합니다. The PoC from the YouTube Short above uses the Variation Selectors range, which are zero-width Unicode characters, as this "secret alphabet."

- 바이트 `0` \~ `15` → `U+FE00` \~ `U+FE0F`
- 바이트 `16` \~ `255` → `U+E0100` \~ `U+E01EF`

개인적으로는 위에서 언급한 길이가 0인 문자를 사용하는 것은 공격의 핵심 원리라기보다는 공격의 성공률을 높이기 위한 *보조 요소*에 가깝다고 생각합니다. In my personal view, using the zero‑width characters mentioned above is not a core principle of the attack but rather *a supplementary measure* intended to improve its success rate.

이는 공격 페이로드를 사람의 눈에 보이지 않게 숨겨, 사용자가 "이상한 텍스트" 인지하고 챗봇에 붙여넣기 전에 삭제하는 것을 방지하기 위함입니다. It's to hide the attack payload invisibly from the human eye, preventing the user from noticing and deleting the "strange text" before pasting it into a chatbot.

하지만 이 공격의 바이트-심볼 매핑 원리는 문자의 시각적 크기와 무관하기 때문에, 눈에 보이는 다른 유니코드 문자 세트 256개를 사용해도 동일한 공격이 가능할 것으로 우려됩니다. However, the byte-to-symbol mapping principle of the attack is independent of the characters' visual size, which means that the same attack might be possible using any other set of 256 visible Unicode characters.

<a id="scenarios"></a>
두가지 상이한 공격 시나리오를 생각해봅시다. Let us think of two different attack scenarios:

- 시나리오 1:
    - 사용자가 유용한 정보를 얻기 위해 한 블로그의 텍스트를 복사합니다. A user copies text from a blog post to get useful information.
    - 하지만 이 텍스트에는 눈에 보이지 않는 이모지 스머글링 페이로드(`😈[...페이로드...]`)가 숨겨져 있었습니다. However, a 'Emoji Smuggling' payload (`😈[...payload...]`) is hidden invisibly within that text.
    - 사용자가 이 텍스트를 자신의 AI 챗봇에 붙여넣는 순간, 눈에 보이지 않아 미처 삭제하지 못했던 악성 프롬프트가 실행됩니다. The moment the user pastes this text into their AI chatbot, the malicious prompt — which they couldn't see and therefore didn't delete — executes.

- 시나리오 2:
    - 한 사용자가 이메일 자동 요약 AI 시스템을 사용 중입니다. A user is running an AI system that automatically summarizes their emails.
    - 공격자가 이 AI 시스템을 노리고 스머글링 된 이메일을 보냅니다. An attacker targets this AI system and sends a smuggled email.
    - 이 경우, 어차피 사람이 아닌 AI 시스템이 이메일 본문을 직접 읽고 처리하기 때문에, 페이로드가 *굳이 눈에 보이지 않을 필요가 없습니다.* In this case, the payload *does not need to be invisible*, since the non-human AI system will be reading and processing the email body directly.

시나리오 1은 보이지 않는 문자의 위험성을 보여주지만, 시나리오 2는 *'보이지 않음'이 공격의 필수 조건이 아니라는 것*을 보여줍니다. Scenario 1 shows the danger of invisible characters, while Scenario 2 shows that *'invisibility' is not a prerequisite for the attack*.

이 부분은 하단 '대안 공격 방안' 섹션에서 더 자세히 다룹니다. This will be discussed further in the 'Alternative Attack Case' section below.