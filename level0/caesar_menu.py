# caesar_menu.py
# Python 3.8+
# - 기본 우측 이동값: 3
# - 영문 알파벳과 공백만 허용(대소문자 미구분)
# - 암호문은 대문자, 복원문은 소문자
# - 메인 메뉴에서 이동값(1~25) 변경 가능, 기능 반복 실행
#
# [프로그램 개요]
# 1) 사용자가 영문/공백으로만 된 메시지를 입력하면
# 2) 시저 암호 규칙(우측으로 shift칸 이동)에 따라 암호화(대문자)하고
# 3) 같은 shift로 즉시 복호화(소문자) 결과를 보여준다.
# 4) 메인 메뉴에서 같은 기능을 반복 실행하거나, 이동값을 바꿀 수 있다.
#
# [설계 포인트]
# - 입력 검증: 정규식으로 영문/공백만 통과시켜 예외를 사전에 차단
# - wrap-around: z 다음이 a로 자연스럽게 이어지도록 모듈로(%) 연산 사용
# - 대/소문자 정책: 암호문은 가독성을 위해 대문자, 복호문은 소문자로 고정
# - 사용자 경험: 현재 매핑표를 먼저 보여줘 규칙을 직관적으로 이해하도록 함

# ===== 초보자 친화: 알파벳 문자열로 처리 =====
ALPHABET = "abcdefghijklmnopqrstuvwxyz"
ALPHABET_UP = ALPHABET.upper()

def _is_english_or_space(s: str) -> bool:
    """영문(26자)과 공백만으로 이루어졌는지 간단히 확인"""
    return all((ch == " ") or (ch.lower() in ALPHABET) for ch in s)

def show_mapping(shift: int) -> None:
    """현재 이동값 기준 매핑표 출력
    - 교육용/확인용 기능.
    - 평문 알파벳(a~z)이 암호문(D~C)으로 어떻게 치환되는지 한눈에 보여준다.
    """
    plain = " ".join(ALPHABET)
    cipher = " ".join(ALPHABET_UP[(i + shift) % 26] for i in range(26))
    print("\n우측으로 {}칸 이동 결과".format(shift))
    print("평문  : " + plain)
    print("암호문: " + cipher)
    print()

def encrypt(msg: str, shift: int) -> str:
    """평문 -> 암호문 (대문자, 공백 유지)
    - 입력 문자열을 한 글자씩 읽어 알파벳이면 우측으로 shift칸 이동.
    - 공백은 그대로 보존하여 단어 경계를 유지한다.
    - 시간복잡도: O(n) (n=문자 수), 공간복잡도: O(n)
    """
    out_chars = []
    for ch in msg:
        if ch == " ":
            out_chars.append(" ")  # 공백 유지
        else:
            i = ALPHABET.index(ch.lower())     # 'a'->0 ... 'z'->25
            out_chars.append(ALPHABET_UP[(i + shift) % 26])  # 대문자로 출력
    return "".join(out_chars)

def decrypt(ct: str, shift: int) -> str:
    """암호문 -> 평문 (소문자, 공백 유지)
    - 암호문을 같은 shift 값으로 반대로 이동시켜 원문 복원.
    - 공백은 그대로 보존.
    - 시간복잡도: O(n)
    """
    out_chars = []
    for ch in ct:
        if ch == " ":
            out_chars.append(" ")  # 공백 유지
        else:
            i = ALPHABET.index(ch.lower())     # 암호문도 같은 0~25 인덱스 사용
            out_chars.append(ALPHABET[(i - shift) % 26])     # 소문자로 출력
    return "".join(out_chars)

def input_message() -> str:
    """사용자 메시지 입력 + 유효성 검사
    - 빈 문자열은 거부.
    - 정규식을 이용해 영문/공백 이외의 문자가 섞여 있으면 거부.
    - 잘못된 입력은 안내 메시지를 보여주고 빈 문자열을 반환(상위 로직이 처리).
    """
    s = input("입력 문자열(영문/공백만): ").strip()
    if not s:
        print("⚠️  빈 문자열은 허용되지 않습니다.")
        return ""
    if not _is_english_or_space(s):
        print("⚠️  영문자와 공백만 입력하세요. (숫자/기호/한글 불가)")
        return ""
    return s

def change_shift(cur: int) -> int:
    """메인 메뉴에서 이동값(shift) 변경
    - 숫자가 아닌 입력, 범위 밖(1~25 아님) 입력은 거부하고 기존 값을 유지.
    - 0 또는 26은 원문 그대로가 되므로 금지한다.
    """
    print(f"\n현재 이동값: {cur}")
    raw = input("새 이동값(1~25): ").strip()
    if not raw.isdigit():
        print("⚠️  숫자를 입력하세요.")
        return cur
    val = int(raw)
    if not (1 <= val <= 25):
        print("⚠️  1~25 범위만 허용됩니다.")
        return cur
    print(f"✅ 이동값이 {val}로 변경되었습니다.")
    return val

def session(shift: int) -> None:
    """암호화-복호화 시나리오 1회 실행
    - 1) 현재 매핑표 출력
    - 2) '1. 암호화 시작 / 9. 종료' 메뉴 노출
    - 3) 정상 입력이면 암호화 → 복호화 결과를 한 번에 보여줌
    - 4) Enter 입력으로 메인 메뉴로 복귀
    """
    show_mapping(shift)
    print("1. 암호화 시작")
    print("9. 종료")
    sel = input("선택? ").strip()
    if sel == "9":
        return
    msg = input_message()
    if not msg:
        return
    ct = encrypt(msg, shift)
    pt = decrypt(ct, shift)
    print()
    print(f"입력 문자열: {msg}")
    print(f"암호 문자열: {ct}")
    print(f"복원 문자열: {pt}")
    input("\n(메인 메뉴 복귀) Enter ⏎ ")

def main():
    """메인 루프
    - 기본 이동값을 3으로 설정.
    - 무한 루프에서 다음 세 가지 동작 중 하나를 수행:
      1) 암호화/복호화 세션 실행
      2) 이동값 변경
      3) 프로그램 종료
    - 잘못된 메뉴 입력에 대해서는 경고 후 계속 루프를 유지하여 안정적으로 동작.
    """
    shift = 3  # 기본값
    while True:
        print("\n================ 시저 암호 메뉴 ================")
        print(f"[현재 이동값: {shift}]")
        print("1) 암호화/복호화")
        print("2) 이동값 변경")
        print("9) 프로그램 종료")
        print("===============================================")
        sel = input("메뉴 선택: ").strip()
        if sel == "1":
            session(shift)                 # 한 번의 암/복 과정을 실행
        elif sel == "2":
            shift = change_shift(shift)    # 이동값 갱신(검증 포함)
        elif sel == "9":
            print("프로그램을 종료합니다.")
            break
        else:
            print("⚠️  올바른 번호를 선택하세요.")  # 예외 처리: 메뉴 외 입력

if __name__ == "__main__":
    # 파이썬 스크립트를 직접 실행한 경우에만 메인 루프 시작.
    # (다른 파일에서 import할 때는 자동 실행되지 않음)
    main()
