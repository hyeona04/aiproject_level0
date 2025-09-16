# caesar_menu_beginner.py
# Python 3.8+
# 규칙 요약:
# 1) 1차: 시저 암호(우측 shift, 기본 3)로 대문자 변환
# 2) 2차: (1차에서 만든 "시저 이동 알파벳열")을 역순으로 뒤집고,
#         같은 위치끼리 문자 치환
# 복호화: 2차 역치환 → 1차 시저 복원

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
ALPHABET_UP = ALPHABET.upper()

def is_english_or_space(s: str) -> bool:
    """영문/공백만 허용"""
    return all((ch == " ") or (ch.lower() in ALPHABET) for ch in s)

def make_shifted_alphabet(shift: int):
    """
    1차: 시저 우측 shift 적용된 대문자 알파벳열 생성
    예) shift=3 → D E F ... Z A B C
    """
    return [ALPHABET_UP[(i + shift) % 26] for i in range(26)]

def show_tables(shift: int):
    """학습용: 평문/1차시저/역순치환표를 한 번에 보여줌"""
    shifted = make_shifted_alphabet(shift)
    reversed_shifted = list(reversed(shifted))
    print("\n[1차] 시저(+{})".format(shift))
    print("plain : " + " ".join(ALPHABET))
    print("shift : " + " ".join(shifted))
    print("\n[2차] 역순 치환 (같은 인덱스끼리 치환)")
    print("map   : " + " ".join(f"{shifted[i]}→{reversed_shifted[i]}" for i in range(26)))
    print()

def encrypt_stage1(msg: str, shift: int) -> str:
    """1차: 시저(+shift) → 대문자"""
    out = []
    for ch in msg:
        if ch == " ":
            out.append(" ")
        else:
            i = ALPHABET.index(ch.lower())
            out.append(ALPHABET_UP[(i + shift) % 26])
    return "".join(out)

def decrypt_stage1(ct1: str, shift: int) -> str:
    """1차 복원: 시저(-shift) → 소문자"""
    out = []
    for ch in ct1:
        if ch == " ":
            out.append(" ")
        else:
            i = ALPHABET.index(ch.lower())
            out.append(ALPHABET[(i - shift) % 26])
    return "".join(out)

def make_stage2_maps(shift: int):
    """
    2차 치환용 매핑(딕셔너리) 준비
    shifted[i] → reversed_shifted[i] (정방향)
    reversed_shifted[i] → shifted[i] (역방향)
    """
    shifted = make_shifted_alphabet(shift)
    reversed_shifted = list(reversed(shifted))
    forward = {shifted[i]: reversed_shifted[i] for i in range(26)}
    backward = {reversed_shifted[i]: shifted[i] for i in range(26)}
    return forward, backward

def encrypt_double(msg: str, shift: int = 3) -> str:
    """최종 암호화: 1차 시저 → 2차 역순치환"""
    ct1 = encrypt_stage1(msg, shift)
    forward, _ = make_stage2_maps(shift)
    out = []
    for ch in ct1:
        if ch == " ":
            out.append(" ")
        else:
            out.append(forward[ch])
    return "".join(out)

def decrypt_double(ct2: str, shift: int = 3) -> str:
    """최종 복호화: 2차 역치환 복원 → 1차 시저 복원"""
    _, backward = make_stage2_maps(shift)
    # 2차 역치환으로 1차 암호문 복원
    ct1 = []
    for ch in ct2:
        if ch == " ":
            ct1.append(" ")
        else:
            ct1.append(backward[ch])
    # 1차 시저 복원
    return decrypt_stage1("".join(ct1), shift)

def input_message() -> str:
    s = input("입력 문자열(영문/공백만): ").strip()
    if not s:
        print("⚠️  빈 문자열은 허용되지 않습니다.")
        return ""
    if not is_english_or_space(s):
        print("⚠️  영문자와 공백만 입력하세요. (숫자/기호/한글 불가)")
        return ""
    return s

def change_shift(cur: int) -> int:
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

def session(shift: int):
    show_tables(shift)
    print("1. 2단계 암/복 실행")
    print("9. 종료")
    sel = input("선택? ").strip()
    if sel == "9":
        return
    msg = input_message()
    if not msg:
        return
    ct1 = encrypt_stage1(msg, shift)
    ct2 = encrypt_double(msg, shift)
    pt  = decrypt_double(ct2, shift)
    print()
    print(f"입력 문자열 : {msg}")
    print(f"[1차] 시저  : {ct1}")
    print(f"[2차] 최종  : {ct2}")
    print(f"복원 문자열 : {pt}")
    input("\n(메인 메뉴 복귀) Enter ⏎ ")

def main():
    # 간단한 자가검증: APPLE → DSSOH → CNNRY → apple
    assert encrypt_stage1("APPLE", 3) == "DSSOH"
    assert encrypt_double("APPLE", 3) == "CNNRY"
    assert decrypt_double("CNNRY", 3) == "apple"

    shift = 3
    while True:
        print("\n=========== 2단계 시저(+3)+역순 치환 메뉴 ===========")
        print(f"[현재 이동값: {shift}]")
        print("1) 암호화/복호화 실행")
        print("2) 이동값 변경")
        print("9) 프로그램 종료")
        print("====================================================")
        sel = input("메뉴 선택: ").strip()
        if sel == "1":
            session(shift)
        elif sel == "2":
            shift = change_shift(shift)
        elif sel == "9":
            print("프로그램을 종료합니다.")
            break
        else:
            print("⚠️  올바른 번호를 선택하세요.")

if __name__ == "__main__":
    main()
