# caesar_vowel_consonant.py
# Python 3.8+
# 규칙:
# 1) 1차 시저(+k) → 대문자
# 2) 2차 치환: 1차에서 만든 시저열 S를
#    T = [A,E,I,O,U] + [B,C,D,F,G,H,J,K,L,M,N,P,Q,R,S,T,V,W,X,Y,Z]
#    로 재배열한 표와 "같은 인덱스"로 치환 (S[i] -> T[i])
# 복호: 2차 역치환(T[i] -> S[i]) → 1차 시저 복원(-k)

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
ALPHABET_UP = ALPHABET.upper()
VOWELS = set("AEIOU")

def is_english_or_space(s: str) -> bool:
    return all((ch == " ") or (ch.lower() in ALPHABET) for ch in s)

def make_shifted_alphabet(shift: int):
    # S: 시저(+shift) 적용된 대문자 알파벳열 (예: shift=3 → D..C)
    return [ALPHABET_UP[(i + shift) % 26] for i in range(26)]

def make_target_vc_alphabet():
    # T: 모음 먼저, 그 다음 자음(알파벳 순, 모음 제외)
    vowels = [c for c in ALPHABET_UP if c in VOWELS]      # A E I O U
    consonants = [c for c in ALPHABET_UP if c not in VOWELS]  # B C D F ... Z
    return vowels + consonants

def make_stage2_maps_vc(shift: int):
    S = make_shifted_alphabet(shift)
    T = make_target_vc_alphabet()
    fwd = {S[i]: T[i] for i in range(26)}  # S[i] -> T[i]
    bwd = {T[i]: S[i] for i in range(26)}  # T[i] -> S[i]
    return fwd, bwd, S, T

def encrypt_stage1(msg: str, shift: int) -> str:
    out = []
    for ch in msg:
        if ch == " ":
            out.append(" ")
        else:
            i = ALPHABET.index(ch.lower())
            out.append(ALPHABET_UP[(i + shift) % 26])
    return "".join(out)

def decrypt_stage1(ct1: str, shift: int) -> str:
    out = []
    for ch in ct1:
        if ch == " ":
            out.append(" ")
        else:
            i = ALPHABET.index(ch.lower())
            out.append(ALPHABET[(i - shift) % 26])
    return "".join(out)

def encrypt_double_vc(msg: str, shift: int = 3) -> str:
    ct1 = encrypt_stage1(msg, shift)      # 1차(대문자)
    fwd, _, _, _ = make_stage2_maps_vc(shift)
    out = []
    for ch in ct1:
        if ch == " ":
            out.append(" ")
        else:
            out.append(fwd[ch])
    return "".join(out)

def decrypt_double_vc(ct2: str, shift: int = 3) -> str:
    _, bwd, _, _ = make_stage2_maps_vc(shift)
    # 2차 역치환으로 1차 결과 복원
    ct1 = []
    for ch in ct2:
        if ch == " ":
            ct1.append(" ")
        else:
            ct1.append(bwd[ch])
    # 1차 시저 복원
    return decrypt_stage1("".join(ct1), shift)

def show_tables(shift: int):
    S = make_shifted_alphabet(shift)
    T = make_target_vc_alphabet()
    print("\n[1차] 시저(+{})".format(shift))
    print("plain : " + " ".join(ALPHABET))
    print("shift : " + " ".join(S))
    print("\n[2차] 모음우선 표 (같은 인덱스 치환)")
    print("target: " + " ".join(T))
    print("map   : " + " ".join(f"{S[i]}→{T[i]}" for i in range(26)))
    print()

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
    ct2 = encrypt_double_vc(msg, shift)
    pt  = decrypt_double_vc(ct2, shift)
    print()
    print(f"입력 문자열 : {msg}")
    print(f"[1차] 시저  : {ct1}")
    print(f"[2차] 최종  : {ct2}")
    print(f"복원 문자열 : {pt}")
    input("\n(메인 메뉴 복귀) Enter ⏎ ")

def main():
    # 간단 자가검증: APPLE (shift=3)
    # 1차: APPLE -> DSSOH
    # 2차: DSSOH -> ANNJU  (S: D..C, T: AEIOU + 자음순)
    assert encrypt_stage1("APPLE", 3) == "DSSOH"
    assert encrypt_double_vc("APPLE", 3) == "ANNJU"
    assert decrypt_double_vc("ANNJU", 3) == "apple"

    shift = 3
    while True:
        print("\n======= 2단계 시저(+k) + 모음우선 치환 메뉴 =======")
        print(f"[현재 이동값: {shift}]")
        print("1) 암호화/복호화 실행")
        print("2) 이동값 변경")
        print("9) 프로그램 종료")
        print("================================================")
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
