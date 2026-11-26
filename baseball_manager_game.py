import random
import copy
from typing import Dict, List, Tuple

import streamlit as st
import pandas as pd

st.set_page_config(page_title="KBO 야구 감독 시뮬레이터", page_icon="⚾", layout="wide")

# -----------------------------------------------------------------------------
# 2026 KBO 시즌 선수 이름을 참고한 게임용 예시 선수단입니다.
# 능력치/연봉/이적료는 실제 공식 기록이나 실제 계약 금액이 아닌 게임 밸런스용 수치입니다.
# -----------------------------------------------------------------------------

TEAM_DATA = {
    "삼성 라이온즈": [
        ("강민호", "C", 78, 73, 58, 75, 0, 0), ("디아즈", "1B", 86, 80, 48, 62, 0, 0),
        ("류지혁", "2B", 75, 73, 70, 78, 0, 0), ("김영웅", "3B", 83, 72, 84, 70, 0, 0),
        ("이재현", "SS", 79, 72, 68, 82, 0, 0), ("김성윤", "LF", 76, 77, 78, 83, 0, 0),
        ("김지찬", "CF", 77, 75, 55, 90, 0, 0), ("최형우", "DH", 82, 80, 82, 55, 0, 0),
        ("김현준", "RF", 73, 71, 58, 80, 0, 0), ("김헌곤", "벤치", 69, 68, 60, 75, 0, 0),
        ("원태인", "SP", 0, 0, 0, 0, 84, 88), ("후라도", "SP", 0, 0, 0, 0, 82, 90),
        ("백정현", "SP", 0, 0, 0, 0, 74, 78), ("이승현", "RP", 0, 0, 0, 0, 77, 70),
        ("김재윤", "RP", 0, 0, 0, 0, 82, 72),
    ],
    "KT 위즈": [
        ("장성우", "C", 75, 72, 65, 72, 0, 0), ("문상철", "1B", 77, 68, 79, 58, 0, 0),
        ("오윤석", "2B", 70, 70, 58, 74, 0, 0), ("허경민", "3B", 80, 78, 65, 83, 0, 0),
        ("김상수", "SS", 74, 76, 52, 82, 0, 0), ("김현수", "LF", 81, 82, 68, 61, 0, 0),
        ("안현민", "CF", 84, 78, 82, 78, 0, 0), ("배정대", "RF", 75, 70, 59, 88, 0, 0),
        ("힐리어드", "DH", 80, 70, 85, 67, 0, 0), ("최원준", "벤치", 76, 75, 60, 85, 0, 0),
        ("고영표", "SP", 0, 0, 0, 0, 86, 90), ("소형준", "SP", 0, 0, 0, 0, 82, 85),
        ("오원석", "SP", 0, 0, 0, 0, 78, 82), ("배제성", "RP", 0, 0, 0, 0, 75, 75),
        ("박영현", "RP", 0, 0, 0, 0, 88, 76),
    ],
    "KIA 타이거즈": [
        ("김태군", "C", 72, 70, 54, 72, 0, 0), ("황대인", "1B", 72, 65, 75, 55, 0, 0),
        ("김선빈", "2B", 78, 83, 55, 62, 0, 0), ("김도영", "3B", 93, 88, 89, 94, 0, 0),
        ("하주석", "SS", 70, 68, 62, 77, 0, 0), ("나성범", "LF", 84, 77, 88, 66, 0, 0),
        ("김호령", "CF", 74, 70, 55, 91, 0, 0), ("카스트로", "RF", 79, 75, 78, 77, 0, 0),
        ("변우혁", "DH", 73, 66, 78, 58, 0, 0), ("박재현", "벤치", 68, 68, 53, 82, 0, 0),
        ("양현종", "SP", 0, 0, 0, 0, 83, 89), ("이의리", "SP", 0, 0, 0, 0, 82, 78),
        ("올러", "SP", 0, 0, 0, 0, 84, 86), ("조상우", "RP", 0, 0, 0, 0, 83, 72),
        ("정해영", "RP", 0, 0, 0, 0, 86, 74),
    ],
    "LG 트윈스": [
        ("박동원", "C", 83, 72, 85, 74, 0, 0), ("오스틴", "1B", 89, 85, 88, 67, 0, 0),
        ("신민재", "2B", 79, 84, 50, 91, 0, 0), ("문보경", "3B", 86, 82, 82, 74, 0, 0),
        ("오지환", "SS", 82, 75, 75, 86, 0, 0), ("문성주", "LF", 80, 85, 60, 78, 0, 0),
        ("박해민", "CF", 78, 76, 50, 94, 0, 0), ("홍창기", "RF", 88, 94, 57, 78, 0, 0),
        ("이재원", "DH", 73, 68, 78, 65, 0, 0), ("천성호", "벤치", 71, 75, 58, 80, 0, 0),
        ("임찬규", "SP", 0, 0, 0, 0, 82, 87), ("손주영", "SP", 0, 0, 0, 0, 82, 84),
        ("톨허스트", "SP", 0, 0, 0, 0, 83, 85), ("장현식", "RP", 0, 0, 0, 0, 83, 72),
        ("고우석", "RP", 0, 0, 0, 0, 86, 74),
    ],
    "두산 베어스": [
        ("양의지", "C", 91, 88, 83, 70, 0, 0), ("양석환", "1B", 82, 72, 86, 57, 0, 0),
        ("강승호", "2B", 76, 72, 72, 69, 0, 0), ("박찬호", "SS", 79, 80, 60, 87, 0, 0),
        ("오명진", "3B", 71, 72, 60, 73, 0, 0), ("손아섭", "LF", 84, 91, 59, 68, 0, 0),
        ("정수빈", "CF", 78, 77, 52, 93, 0, 0), ("조수행", "RF", 73, 72, 48, 92, 0, 0),
        ("김민석", "DH", 74, 74, 63, 82, 0, 0), ("김기연", "벤치", 68, 66, 54, 68, 0, 0),
        ("곽빈", "SP", 0, 0, 0, 0, 88, 85), ("이영하", "SP", 0, 0, 0, 0, 79, 85),
        ("최승용", "SP", 0, 0, 0, 0, 77, 80), ("김택연", "RP", 0, 0, 0, 0, 89, 72),
        ("이용찬", "RP", 0, 0, 0, 0, 78, 75),
    ],
    "롯데 자이언츠": [
        ("유강남", "C", 75, 70, 70, 65, 0, 0), ("나승엽", "1B", 80, 78, 79, 62, 0, 0),
        ("고승민", "2B", 79, 80, 73, 74, 0, 0), ("한동희", "3B", 77, 70, 83, 60, 0, 0),
        ("전민재", "SS", 72, 71, 56, 80, 0, 0), ("레이예스", "LF", 88, 88, 82, 72, 0, 0),
        ("황성빈", "CF", 77, 78, 48, 94, 0, 0), ("윤동희", "RF", 81, 79, 75, 82, 0, 0),
        ("전준우", "DH", 82, 82, 80, 58, 0, 0), ("손성빈", "벤치", 69, 67, 57, 78, 0, 0),
        ("박세웅", "SP", 0, 0, 0, 0, 83, 88), ("김원중", "RP", 0, 0, 0, 0, 85, 74),
        ("최준용", "RP", 0, 0, 0, 0, 82, 72), ("구승민", "RP", 0, 0, 0, 0, 78, 70),
        ("박세진", "SP", 0, 0, 0, 0, 72, 78),
    ],
    "SSG 랜더스": [
        ("조형우", "C", 72, 69, 64, 74, 0, 0), ("고명준", "1B", 75, 70, 77, 63, 0, 0),
        ("정준재", "2B", 75, 77, 55, 85, 0, 0), ("최정", "3B", 91, 83, 93, 68, 0, 0),
        ("박성한", "SS", 85, 84, 66, 82, 0, 0), ("최지훈", "CF", 83, 82, 66, 91, 0, 0),
        ("에레디아", "LF", 87, 90, 78, 72, 0, 0), ("한유섬", "RF", 82, 75, 87, 63, 0, 0),
        ("김재환", "DH", 79, 72, 88, 54, 0, 0), ("이지영", "벤치", 72, 73, 50, 70, 0, 0),
        ("노경은", "SP", 0, 0, 0, 0, 80, 85), ("문승원", "SP", 0, 0, 0, 0, 80, 82),
        ("조병현", "RP", 0, 0, 0, 0, 85, 73), ("서진용", "RP", 0, 0, 0, 0, 80, 72),
        ("이로운", "RP", 0, 0, 0, 0, 78, 70),
    ],
    "NC 다이노스": [
        ("김형준", "C", 80, 74, 76, 84, 0, 0), ("데이비슨", "1B", 89, 78, 94, 58, 0, 0),
        ("박민우", "2B", 87, 90, 62, 86, 0, 0), ("서호철", "3B", 75, 78, 61, 76, 0, 0),
        ("김주원", "SS", 83, 77, 70, 89, 0, 0), ("권희동", "LF", 78, 77, 72, 68, 0, 0),
        ("박건우", "CF", 86, 88, 78, 76, 0, 0), ("이우성", "RF", 77, 73, 76, 65, 0, 0),
        ("김휘집", "DH", 78, 70, 78, 68, 0, 0), ("안중열", "벤치", 68, 65, 54, 68, 0, 0),
        ("구창모", "SP", 0, 0, 0, 0, 87, 77), ("이재학", "SP", 0, 0, 0, 0, 78, 84),
        ("신민혁", "SP", 0, 0, 0, 0, 80, 84), ("김영규", "RP", 0, 0, 0, 0, 81, 73),
        ("라일리", "SP", 0, 0, 0, 0, 84, 83),
    ],
    "한화 이글스": [
        ("허인서", "C", 75, 72, 70, 73, 0, 0), ("채은성", "1B", 81, 80, 78, 60, 0, 0),
        ("황영묵", "2B", 75, 77, 58, 80, 0, 0), ("노시환", "3B", 91, 80, 94, 70, 0, 0),
        ("심우준", "SS", 80, 76, 59, 91, 0, 0), ("문현빈", "LF", 86, 83, 77, 83, 0, 0),
        ("페라자", "CF", 84, 78, 83, 78, 0, 0), ("김태연", "RF", 79, 82, 70, 68, 0, 0),
        ("강백호", "DH", 87, 84, 89, 72, 0, 0), ("최재훈", "벤치", 74, 78, 55, 73, 0, 0),
        ("류현진", "SP", 0, 0, 0, 0, 90, 87), ("문동주", "SP", 0, 0, 0, 0, 86, 78),
        ("황준서", "SP", 0, 0, 0, 0, 78, 78), ("김서현", "RP", 0, 0, 0, 0, 86, 70),
        ("박상원", "RP", 0, 0, 0, 0, 81, 73),
    ],
    "키움 히어로즈": [
        ("김동헌", "C", 75, 72, 66, 76, 0, 0), ("안치홍", "1B", 81, 85, 69, 65, 0, 0),
        ("김태진", "2B", 72, 75, 55, 80, 0, 0), ("김형빈", "3B", 68, 66, 62, 76, 0, 0),
        ("김건희", "SS", 73, 70, 67, 78, 0, 0), ("이형종", "LF", 76, 73, 75, 62, 0, 0),
        ("임병욱", "CF", 73, 69, 68, 88, 0, 0), ("추재현", "RF", 72, 75, 60, 81, 0, 0),
        ("히우라", "DH", 82, 75, 86, 65, 0, 0), ("김시앙", "벤치", 68, 66, 55, 70, 0, 0),
        ("안우진", "SP", 0, 0, 0, 0, 94, 76), ("알칸타라", "SP", 0, 0, 0, 0, 84, 88),
        ("박준현", "SP", 0, 0, 0, 0, 78, 80), ("김윤하", "RP", 0, 0, 0, 0, 77, 72),
        ("최현우", "RP", 0, 0, 0, 0, 74, 70),
    ],
}

TEAM_NAMES = list(TEAM_DATA.keys())
HITTING_POSITIONS = ["C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "DH"]


def make_league() -> Dict[str, List[dict]]:
    """정적 선수 데이터를 게임에서 사용하는 선수 카드 목록으로 변환한다."""
    league = {}
    for t_idx, (team, rows) in enumerate(TEAM_DATA.items()):
        roster = []
        for p_idx, row in enumerate(rows):
            name, pos, overall, contact, power, speed_or_def, control, stamina = row
            if pos in ("SP", "RP"):
                player = {
                    "id": f"{t_idx}-{p_idx}", "name": name, "team": team, "pos": pos,
                    "role": "투수", "overall": overall or round((control + stamina) / 2),
                    "contact": 0, "power": 0, "speed": 0, "defense": 0,
                    "control": control, "stamina": stamina,
                }
            else:
                player = {
                    "id": f"{t_idx}-{p_idx}", "name": name, "team": team, "pos": pos,
                    "role": "타자", "overall": overall, "contact": contact, "power": power,
                    "speed": speed_or_def, "defense": speed_or_def, "control": 0, "stamina": 0,
                }
            roster.append(player)
        league[team] = roster
    return league


def get_player(roster: List[dict], player_id: str):
    for player in roster:
        if player["id"] == player_id:
            return player
    return None


def player_fee(player: dict) -> float:
    """게임 밸런스용 영입 비용(억 원). 실제 계약금·연봉이 아니다."""
    return round(max(0.8, (player["overall"] - 48) * 0.16 + 1.2), 1)


def team_power(roster: List[dict]) -> float:
    hitters = [p["overall"] for p in roster if p["role"] == "타자"]
    pitchers = [p["overall"] for p in roster if p["role"] == "투수"]
    h = sum(sorted(hitters, reverse=True)[:9]) / max(1, min(9, len(hitters)))
    q = sum(sorted(pitchers, reverse=True)[:5]) / max(1, min(5, len(pitchers)))
    return round(h * 0.55 + q * 0.45, 1)


def default_lineup(roster: List[dict]) -> List[str]:
    hitters = [p for p in roster if p["role"] == "타자" and p["pos"] != "벤치"]
    hitters.sort(key=lambda p: p["overall"] + p["contact"] * 0.15 + p["speed"] * 0.05, reverse=True)
    return [p["id"] for p in hitters[:9]]


def advance_walk(bases: List[bool]) -> Tuple[List[bool], int]:
    b1, b2, b3 = bases
    runs = 1 if (b1 and b2 and b3) else 0
    new_bases = [True, (b2 or b1), (b3 or (b1 and b2))]
    return new_bases, runs


def simulate_plate_appearance(
    batter: dict, pitcher: dict, bases: List[bool], outs: int,
    offense_tactic: str, defense_tactic: str, fatigue: int,
) -> Tuple[str, List[bool], int, int, bool]:
    """한 타석 또는 도루/번트 작전을 간단한 확률 모델로 처리한다."""
    b = list(bases)
    runs = 0

    if offense_tactic == "도루" and b[0] and not b[1] and outs < 2:
        steal_chance = min(0.88, max(0.48, 0.48 + batter["speed"] * 0.004))
        if random.random() < steal_chance:
            b[1], b[0] = True, False
            return "도루 성공! 주자가 2루로 진루했습니다.", b, outs, 0, False
        b[0] = False
        return "도루 실패! 주자가 아웃되었습니다.", b, outs + 1, 0, False

    if offense_tactic == "희생번트" and any(b) and outs < 2:
        if random.random() < 0.78:
            if b[2]:
                runs += 1
            b = [False, b[0], b[1]]
            return "희생번트 성공! 주자들이 한 베이스씩 진루했습니다.", b, outs + 1, runs, True
        return "번트 타구가 좋지 않아 타자만 아웃되었습니다.", b, outs + 1, 0, True

    contact = batter["contact"]
    power = batter["power"]
    control = max(45, pitcher["control"] - fatigue * 1.25)
    stuff = max(45, pitcher["overall"] - fatigue * 1.0)

    walk = 0.075 + (70 - control) * 0.0007
    strikeout = 0.185 + (stuff - 70) * 0.0018 - (contact - 70) * 0.0015
    homer = 0.018 + (power - 60) * 0.00075 - (stuff - 70) * 0.0002
    triple = 0.004 + (batter["speed"] - 60) * 0.00015
    double = 0.045 + (power - 60) * 0.00055
    single = 0.155 + (contact - 60) * 0.00135

    if offense_tactic == "강공":
        homer += 0.018
        strikeout += 0.035
        single -= 0.025
    elif offense_tactic == "히트앤런":
        single += 0.035
        double -= 0.006
        homer -= 0.006
    if defense_tactic == "유인구":
        walk += 0.025
        single -= 0.012
    elif defense_tactic == "정면 승부":
        strikeout += 0.025
        walk -= 0.012
    elif defense_tactic == "고의4구":
        b, runs = advance_walk(b)
        return "고의4구! 타자가 1루로 출루했습니다.", b, outs, runs, True

    weights = [max(0.005, homer), max(0.002, triple), max(0.01, double),
               max(0.04, single), max(0.015, walk), max(0.05, strikeout)]
    out_weight = max(0.1, 1.0 - sum(weights))
    outcomes = ["홈런", "3루타", "2루타", "안타", "볼넷", "삼진", "아웃"]
    weights.append(out_weight)
    outcome = random.choices(outcomes, weights=weights, k=1)[0]

    if outcome == "홈런":
        runs = 1 + sum(b)
        b = [False, False, False]
        message = f"홈런! {runs}점 득점했습니다."
    elif outcome == "3루타":
        runs = sum(b)
        b = [False, False, True]
        message = "3루타! 주자들이 모두 홈으로 들어왔습니다."
    elif outcome == "2루타":
        runs = int(b[2]) + int(b[1])
        # 1루 주자는 3루, 타자는 2루에 도착합니다.
        b = [False, True, b[0]]
        message = f"2루타! {runs}점 득점했습니다." if runs else "2루타! 주자가 득점권에 진루했습니다."
    elif outcome == "안타":
        runs = int(b[2])
        b = [True, b[0], b[1]]
        if offense_tactic == "히트앤런" and b[2]:
            b[2] = False
            runs += 1
        message = f"안타! {runs}점 득점했습니다." if runs else "안타! 주자가 출루했습니다."
    elif outcome == "볼넷":
        b, runs = advance_walk(b)
        message = "볼넷! 타자가 1루로 출루했습니다."
    elif outcome == "삼진":
        outs += 1
        message = "삼진 아웃!"
    else:
        # 땅볼 병살 가능성을 낮은 확률로 반영한다.
        if b[0] and outs < 2 and random.random() < 0.12:
            outs += 2
            b[0] = False
            message = "병살타! 아웃카운트 2개가 올라갔습니다."
        else:
            outs += 1
            message = "타구가 야수 정면으로 향해 아웃되었습니다."
    return message, b, outs, runs, True


def init_game(my_team: str, opponent: str, league: dict) -> dict:
    saved = st.session_state.get("saved_lineup", [])
    valid_saved = [pid for pid in saved if get_player(league[my_team], pid) and get_player(league[my_team], pid)["role"] == "타자"]
    my_lineup = valid_saved[:9] if len(valid_saved) == 9 else default_lineup(league[my_team])
    lineups = {my_team: my_lineup, opponent: default_lineup(league[opponent])}
    return {
        "my_team": my_team, "opponent": opponent, "inning": 1, "half": "초", "outs": 0,
        "bases": [False, False, False], "scores": {my_team: 0, opponent: 0},
        "lineups": lineups, "batter_index": {my_team: 0, opponent: 0},
        "fatigue": {}, "logs": [f"경기 시작! {opponent} 원정, {my_team} 홈 경기입니다."],
        "done": False, "max_innings": 12, "half_runs": 0,
    }


def batting_team(game: dict) -> str:
    return game["opponent"] if game["half"] == "초" else game["my_team"]


def fielding_team(game: dict) -> str:
    return game["my_team"] if game["half"] == "초" else game["opponent"]


def end_half_if_needed(game: dict) -> None:
    if game["outs"] < 3:
        return
    current_offense = batting_team(game)
    runs = game["half_runs"]
    game["logs"].append(f"{game['inning']}회 {game['half']} 공격 종료: {runs}점 득점")
    game["half_runs"] = 0
    game["outs"] = 0
    game["bases"] = [False, False, False]

    if game["half"] == "초":
        # 9회 초 종료 시 홈팀이 앞서면 9회 말을 생략한다.
        if game["inning"] >= 9 and game["scores"][game["my_team"]] > game["scores"][game["opponent"]]:
            game["done"] = True
            return
        game["half"] = "말"
    else:
        if game["inning"] >= 9 and game["scores"][game["my_team"]] != game["scores"][game["opponent"]]:
            game["done"] = True
            return
        if game["inning"] >= game["max_innings"]:
            game["done"] = True
            game["logs"].append("12회까지 승부가 나지 않아 무승부로 종료되었습니다.")
            return
        game["inning"] += 1
        game["half"] = "초"


def current_batter(game: dict, league: dict) -> dict:
    team = batting_team(game)
    lineup = game["lineups"][team]
    if not lineup:
        return None
    idx = game["batter_index"][team] % len(lineup)
    return get_player(league[team], lineup[idx])


def record_game_result(game: dict) -> str:
    my_score = game["scores"][game["my_team"]]
    opp_score = game["scores"][game["opponent"]]
    if my_score > opp_score:
        return "승리"
    if my_score < opp_score:
        return "패배"
    return "무승부"


def start_new_career(team: str):
    st.session_state.league = make_league()
    st.session_state.my_team = team
    st.session_state.budget = 25.0
    st.session_state.wins = 0
    st.session_state.losses = 0
    st.session_state.draws = 0
    st.session_state.game = None
    st.session_state.game_count = 0
    st.session_state.last_result = "아직 경기 기록이 없습니다."
    st.session_state.saved_lineup = []


# -----------------------------------------------------------------------------
# UI
# -----------------------------------------------------------------------------

st.title("⚾ KBO 야구 감독 시뮬레이터")
st.caption("구단 선택부터 작전 지시, 선수 영입·트레이드·방출, 투수 교체까지 직접 운영하는 감독 게임")

if "league" not in st.session_state:
    st.markdown("### 감독으로 부임할 구단을 선택하세요")
    selected_team = st.selectbox("응원하거나 맡고 싶은 팀", TEAM_NAMES, index=2)
    st.info("2026 KBO 시즌의 실제 구단과 선수 이름을 참고한 시뮬레이션입니다. 선수 능력치와 이적료는 게임 진행을 위한 가상 밸런스 수치입니다.")
    if st.button("감독 부임하기", type="primary", use_container_width=True):
        start_new_career(selected_team)
        st.rerun()
    st.stop()

league = st.session_state.league
my_team = st.session_state.my_team
my_roster = league[my_team]
game = st.session_state.game

with st.sidebar:
    st.header("🏟️ 감독 정보")
    st.subheader(my_team)
    st.metric("구단 운영 자금", f"{st.session_state.budget:.1f}억 원")
    c1, c2 = st.columns(2)
    c1.metric("승리", st.session_state.wins)
    c2.metric("패배", st.session_state.losses)
    st.metric("무승부", st.session_state.draws)
    st.caption(f"경기 수: {st.session_state.game_count}")
    st.divider()
    if st.button("구단 다시 선택하기", use_container_width=True):
        for key in ["league", "my_team", "budget", "wins", "losses", "draws", "game", "game_count", "last_result"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    st.caption("게임 데이터는 현재 브라우저 세션에서 관리됩니다. 새 세션에서는 초기화될 수 있습니다.")

# Header metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("팀 전력", f"{team_power(my_roster)} / 100")
m2.metric("선수단", f"{len(my_roster)}명")
m3.metric("승률", f"{st.session_state.wins / max(1, st.session_state.wins + st.session_state.losses + st.session_state.draws):.3f}")
m4.metric("최근 경기", st.session_state.last_result)

# Create tabs
tab_game, tab_roster, tab_front, tab_guide = st.tabs(["🎮 경기 운영", "📋 선수단·타순", "🔁 구단 운영", "📖 게임 설명"])

with tab_game:
    st.subheader("경기 운영")
    if game is None or game.get("done"):
        if game is not None and game.get("done") and not game.get("result_recorded"):
            result = record_game_result(game)
            if result == "승리": st.session_state.wins += 1
            elif result == "패배": st.session_state.losses += 1
            else: st.session_state.draws += 1
            game["result_recorded"] = True
            st.session_state.last_result = f"{result} {game['scores'][my_team]}-{game['scores'][game['opponent']]}"
        eligible_opponents = [t for t in TEAM_NAMES if t != my_team]
        opponent_choice = st.selectbox("다음 경기 상대 구단", eligible_opponents, key="new_opponent")
        if st.button("새 경기 시작", type="primary", use_container_width=True):
            st.session_state.game = init_game(my_team, opponent_choice, league)
            st.session_state.game_count += 1
            st.rerun()
        if game is not None and game.get("done"):
            st.success(f"경기 종료: {st.session_state.last_result}")
            st.write(f"최종 스코어 — {my_team} {game['scores'][my_team]} : {game['scores'][game['opponent']]} {game['opponent']}")
        else:
            st.info("상대 팀을 선택하고 새 경기를 시작하세요. 한 경기씩 진행하며 매 타석 작전을 직접 선택할 수 있습니다.")
    else:
        score_cols = st.columns([1, 1, 1, 1, 1])
        score_cols[0].metric("이닝", f"{game['inning']}회 {game['half']}")
        score_cols[1].metric(my_team, game["scores"][my_team])
        score_cols[2].metric(game["opponent"], game["scores"][game["opponent"]])
        score_cols[3].metric("아웃", f"{game['outs']} / 3")
        score_cols[4].metric("주자", " ".join(["●" if x else "○" for x in [game['bases'][2], game['bases'][1], game['bases'][0]]]))

        offense = batting_team(game)
        defense = fielding_team(game)
        batter = current_batter(game, league)
        if batter is None:
            st.error("타순에 등록된 타자가 없습니다. 선수단 탭에서 타순을 확인하세요.")
        else:
            st.markdown(f"**현재 공격:** {offense}　|　**현재 수비:** {defense}")
            if offense == my_team:
                st.markdown(f"### 타석: {batter['name']} ({batter['pos']})")
                tactic = st.selectbox("공격 작전", ["기본 공격", "강공", "희생번트", "도루", "히트앤런"], key="off_tactic")
                bench = [p for p in my_roster if p["role"] == "타자" and p["pos"] == "벤치"]
                current_lineup = game["lineups"][my_team]
                if bench:
                    with st.expander("대타 작전 (선택 사항)"):
                        bench_player_id = st.selectbox(
                            "대타 후보", [p["id"] for p in bench],
                            format_func=lambda pid: (lambda p: f"{p['name']} (능력치 {p['overall']})")(get_player(my_roster, pid)),
                            key="pinch_hitter",
                        )
                        bench_player = get_player(my_roster, bench_player_id)
                        if st.button("현재 타자를 대타로 교체"):
                            idx = game["batter_index"][my_team] % len(current_lineup)
                            old_id = current_lineup[idx]
                            current_lineup[idx] = bench_player["id"]
                            bench_player["pos"] = "대타로 출전"
                            # 기존 타자는 벤치로 이동
                            old_player = get_player(my_roster, old_id)
                            if old_player:
                                old_player["pos"] = "벤치"
                            st.success(f"{bench_player['name']} 선수가 대타로 들어갑니다.")
                            st.rerun()
                if st.button("작전 실행 · 다음 타석 진행", type="primary", use_container_width=True):
                    opponent_pitchers = [p for p in league[defense] if p["role"] == "투수"]
                    pitcher = max(opponent_pitchers, key=lambda p: p["overall"])
                    fatigue = game["fatigue"].get(pitcher["id"], 0)
                    tactic_map = {"기본 공격": "기본 공격", "강공": "강공", "희생번트": "희생번트", "도루": "도루", "히트앤런": "히트앤런"}
                    message, bases, outs, runs, consumed = simulate_plate_appearance(
                        batter, pitcher, game["bases"], game["outs"], tactic_map[tactic], "기본", fatigue
                    )
                    game["bases"] = bases
                    game["outs"] = outs
                    game["scores"][my_team] += runs
                    game["half_runs"] += runs
                    game["fatigue"][pitcher["id"]] = fatigue + 1
                    game["logs"].append(f"{game['inning']}회 {game['half']} · {batter['name']}: {message}")
                    if consumed:
                        game["batter_index"][my_team] += 1
                    end_half_if_needed(game)
                    st.rerun()
            else:
                st.markdown(f"### 상대 타석: {batter['name']} ({batter['pos']})")
                st.caption("수비 감독으로서 투수와 승부 전략을 선택하세요.")
                my_pitchers = [p for p in my_roster if p["role"] == "투수"]
                if not my_pitchers:
                    st.error("등록된 투수가 없습니다. 구단 운영에서 투수를 영입하세요.")
                else:
                    selected_pitcher_id = st.selectbox(
                        "마운드에 올릴 투수", [p["id"] for p in my_pitchers],
                        format_func=lambda pid: (lambda p: f"{p['name']} · {p['pos']} · 능력치 {p['overall']} · 피로 {game['fatigue'].get(pid, 0)}")(get_player(my_roster, pid)),
                        key="active_pitcher",
                    )
                    selected_pitcher = get_player(my_roster, selected_pitcher_id)
                    defense_tactic = st.selectbox("투수 작전", ["정면 승부", "유인구", "고의4구"], key="def_tactic")
                    if st.button("투수 작전 실행 · 다음 타석 진행", type="primary", use_container_width=True):
                        opponent_tactic = "기본 공격"
                        fatigue = game["fatigue"].get(selected_pitcher["id"], 0)
                        message, bases, outs, runs, consumed = simulate_plate_appearance(
                            batter, selected_pitcher, game["bases"], game["outs"], opponent_tactic, defense_tactic, fatigue
                        )
                        game["bases"] = bases
                        game["outs"] = outs
                        game["scores"][offense] += runs
                        game["half_runs"] += runs
                        game["fatigue"][selected_pitcher["id"]] = fatigue + 1
                        game["logs"].append(f"{game['inning']}회 {game['half']} · {batter['name']}: {message}")
                        if consumed:
                            game["batter_index"][offense] += 1
                        end_half_if_needed(game)
                        st.rerun()

        st.divider()
        st.markdown("**주자 상황**")
        base_cols = st.columns(3)
        base_cols[0].markdown(f"2루: {'🟠 주자 있음' if game['bases'][1] else '⚪ 비어 있음'}")
        base_cols[1].markdown(f"3루: {'🟠 주자 있음' if game['bases'][2] else '⚪ 비어 있음'}")
        base_cols[2].markdown(f"1루: {'🟠 주자 있음' if game['bases'][0] else '⚪ 비어 있음'}")
        with st.expander("경기 진행 기록", expanded=True):
            for item in reversed(game["logs"][-12:]):
                st.write("• " + item)

with tab_roster:
    st.subheader(f"{my_team} 선수단 관리")
    hitters = [p for p in my_roster if p["role"] == "타자"]
    pitchers = [p for p in my_roster if p["role"] == "투수"]
    c1, c2 = st.columns(2)
    c1.metric("타자", f"{len(hitters)}명")
    c2.metric("투수", f"{len(pitchers)}명")
    roster_rows = []
    for p in my_roster:
        row = {"선수": p["name"], "포지션": p["pos"], "구분": p["role"], "게임 능력치": p["overall"]}
        if p["role"] == "타자":
            row.update({"컨택": p["contact"], "파워": p["power"], "주력": p["speed"]})
        else:
            row.update({"제구": p["control"], "체력": p["stamina"]})
        roster_rows.append(row)
    st.dataframe(pd.DataFrame(roster_rows), use_container_width=True, hide_index=True)

    st.markdown("### 선발 타순 편집")
    if game is not None and not game.get("done"):
        st.info("경기 중에는 다음 경기를 위한 타순만 바꿀 수 있습니다. 진행 중인 경기 타순은 유지됩니다.")
    default_ids = default_lineup(my_roster)
    hitter_options = hitters
    selected_names = st.multiselect(
        "경기에 사용할 타자 9명 선택 (선택한 순서가 타순)",
        [p["id"] for p in hitter_options],
        default=[pid for pid in default_ids if get_player(my_roster, pid)],
        format_func=lambda pid: (lambda p: f"{p['name']} ({p['pos']}, {p['overall']})")(get_player(my_roster, pid)),
        max_selections=9,
        key="lineup_editor",
    )
    if st.button("선발 타순 저장", use_container_width=True):
        if len(selected_names) == 9:
            st.session_state.saved_lineup = list(selected_names)
            st.success("선발 타순을 저장했습니다. 새 경기부터 적용됩니다.")
        else:
            st.warning("타순에는 타자 9명을 선택해야 합니다.")
    st.caption("※ 이 게임의 능력치는 실제 KBO 공식 기록이 아니라 게임 밸런스를 위한 가상 수치입니다.")

with tab_front:
    st.subheader("구단 운영: 영입 · 트레이드 · 방출")
    st.caption("선수 이동은 게임 안에서만 적용되는 가상 운영 규칙입니다. 실제 구단 계약이나 FA 자격을 뜻하지 않습니다.")
    game_active = st.session_state.game is not None and not st.session_state.game.get("done", False)
    if game_active:
        st.warning("경기가 진행 중이므로 영입·트레이드·방출은 경기 종료 후 이용할 수 있습니다.")
    front_sign, front_trade, front_release = st.tabs(["💰 선수 영입", "🔄 트레이드", "📤 선수 방출"])

    with front_sign:
        st.markdown("### 영입 시장")
        st.write("다른 구단 선수를 영입하면 게임 운영 자금에서 이적료가 차감되고, 해당 선수는 원 소속팀 명단에서 빠집니다.")
        other_players = [(team, p) for team in TEAM_NAMES if team != my_team for p in league[team]]
        role_filter = st.radio("영입 포지션", ["전체", "타자", "투수"], horizontal=True, key="sign_role")
        candidates = [(team, p) for team, p in other_players if role_filter == "전체" or p["role"] == role_filter]
        candidate_lookup = {p["id"]: (team, p) for team, p in candidates}
        selected_candidate_id = st.selectbox(
            "영입할 선수 선택", list(candidate_lookup.keys()),
            format_func=lambda pid: (lambda item: f"{item[1]['name']} · {item[0]} · {item[1]['pos']} · 능력치 {item[1]['overall']} · {player_fee(item[1]):.1f}억")(candidate_lookup[pid]),
            key="sign_candidate",
        )
        selected_tuple = candidate_lookup.get(selected_candidate_id)
        if selected_tuple:
            from_team, candidate = selected_tuple
            fee = player_fee(candidate)
            a, b, c = st.columns(3)
            a.metric("선수 능력치", candidate["overall"])
            b.metric("게임 이적료", f"{fee:.1f}억")
            c.metric("영입 후 자금", f"{st.session_state.budget - fee:.1f}억")
            if st.button("이 선수 영입하기", type="primary", disabled=(st.session_state.budget < fee or game_active), use_container_width=True):
                other_hitters = sum(1 for p in league[from_team] if p["role"] == "타자")
                other_pitchers = sum(1 for p in league[from_team] if p["role"] == "투수")
                role_safe = (candidate["role"] == "타자" and other_hitters > 9) or (candidate["role"] == "투수" and other_pitchers > 3)
                if len(league[my_team]) >= 25:
                    st.error("선수단은 최대 25명까지 등록할 수 있습니다.")
                elif len(league[from_team]) <= 10 or not role_safe:
                    st.error("상대 구단의 최소 선수 구성(타자 9명, 투수 3명)을 유지하기 위해 영입할 수 없습니다.")
                else:
                    moved = get_player(league[from_team], candidate["id"])
                    league[from_team] = [p for p in league[from_team] if p["id"] != candidate["id"]]
                    moved["team"] = my_team
                    league[my_team].append(moved)
                    st.session_state.budget = round(st.session_state.budget - fee, 1)
                    st.success(f"{moved['name']} 선수 영입 완료! 이적료 {fee:.1f}억 원을 사용했습니다.")
                    st.rerun()
        else:
            st.info("현재 조건에 맞는 영입 후보가 없습니다.")

    with front_trade:
        st.markdown("### 1:1 선수 트레이드")
        own_tradeables = [p for p in my_roster]
        own_choice_id = st.selectbox(
            "우리 구단에서 보낼 선수", [p["id"] for p in own_tradeables],
            format_func=lambda pid: (lambda p: f"{p['name']} ({p['pos']}, 능력치 {p['overall']})")(get_player(my_roster, pid)),
            key="trade_own",
        )
        own_choice = get_player(my_roster, own_choice_id)
        other_team = st.selectbox("트레이드 상대 구단", [t for t in TEAM_NAMES if t != my_team], key="trade_team")
        target_choice_id = st.selectbox(
            "상대 구단에서 받을 선수", [p["id"] for p in league[other_team]],
            format_func=lambda pid: (lambda p: f"{p['name']} ({p['pos']}, 능력치 {p['overall']})")(get_player(league[other_team], pid)),
            key="trade_target",
        )
        target_choice = get_player(league[other_team], target_choice_id)
        if own_choice and target_choice:
            diff = abs(own_choice["overall"] - target_choice["overall"])
            same_role = own_choice["role"] == target_choice["role"]
            st.write(f"선수 능력치 차이: {diff}점")
            if not same_role:
                st.info("선수단 구성을 유지하기 위해 타자는 타자끼리, 투수는 투수끼리 트레이드할 수 있습니다.")
            if st.button("트레이드 제안", type="primary", disabled=(game_active or not same_role), use_container_width=True):
                if diff > 18:
                    st.error("상대 구단이 전력 차이가 크다는 이유로 트레이드를 거절했습니다. 능력치 차이가 18점 이하인 선수를 제안해 보세요.")
                else:
                    own_id, target_id = own_choice["id"], target_choice["id"]
                    p_out = get_player(league[my_team], own_id)
                    p_in = get_player(league[other_team], target_id)
                    league[my_team] = [p for p in league[my_team] if p["id"] != own_id]
                    league[other_team] = [p for p in league[other_team] if p["id"] != target_id]
                    p_out["team"], p_in["team"] = other_team, my_team
                    league[my_team].append(p_in)
                    league[other_team].append(p_out)
                    st.success(f"트레이드 성사! {p_in['name']} 영입 / {p_out['name']} 이적")
                    st.rerun()

    with front_release:
        st.markdown("### 선수 방출")
        st.warning("방출한 선수는 구단 선수단에서 제외됩니다. 방출로 운영 자금이 늘어나지는 않습니다.")
        release_choice_id = st.selectbox(
            "방출할 선수", [p["id"] for p in my_roster],
            format_func=lambda pid: (lambda p: f"{p['name']} ({p['pos']}, 능력치 {p['overall']})")(get_player(my_roster, pid)),
            key="release_player",
        )
        release_choice = get_player(my_roster, release_choice_id)
        if st.button("선수 방출", type="primary", disabled=game_active, use_container_width=True):
            hitter_count = sum(1 for p in my_roster if p["role"] == "타자")
            pitcher_count = sum(1 for p in my_roster if p["role"] == "투수")
            if len(my_roster) <= 10:
                st.error("최소 10명의 선수는 유지해야 합니다.")
            elif release_choice["role"] == "타자" and hitter_count <= 9:
                st.error("경기를 위해 타자는 최소 9명 유지해야 합니다.")
            elif release_choice["role"] == "투수" and pitcher_count <= 3:
                st.error("경기를 위해 투수는 최소 3명 유지해야 합니다.")
            else:
                league[my_team] = [p for p in league[my_team] if p["id"] != release_choice["id"]]
                st.success(f"{release_choice['name']} 선수를 방출했습니다.")
                st.rerun()

with tab_guide:
    st.subheader("게임 설명")
    st.markdown("""
    **1. 감독 부임**  
    KBO 10개 구단 중 하나를 선택하면 해당 구단의 감독이 됩니다.

    **2. 경기 운영**  
    9이닝 경기를 한 타석씩 진행합니다. 공격할 때는 강공, 희생번트, 도루, 히트앤런을 선택할 수 있고, 수비할 때는 투수와 정면 승부·유인구·고의4구를 선택할 수 있습니다. 9회까지 동점이면 연장 12회까지 진행합니다.

    **3. 선수단 관리**  
    타자 9명 선발 타순을 편집하고, 벤치 선수를 대타로 기용할 수 있습니다. 투수는 매 타석 수비 화면에서 바꿀 수 있습니다.

    **4. 구단 운영**  
    - 영입: 다른 구단 선수를 게임 이적료를 내고 데려옵니다.
    - 트레이드: 다른 구단 선수와 1:1 교환합니다. 능력치 차이가 너무 크면 상대가 거절합니다.
    - 방출: 선수를 선수단에서 제외합니다.

    **5. 승률 관리**  
    경기를 마치면 승·패·무가 누적됩니다. 여러 경기를 진행하며 감독으로서 팀 성적을 관리하세요.

    **주의:** 구단과 선수 이름은 2026 KBO 시즌 선수단 자료를 참고했습니다. 게임 능력치, 이적료, 작전 성공 확률은 실제 공식 기록·연봉·계약 조건이 아닌 재미를 위한 시뮬레이션 값입니다. 실제 트레이드·FA 규정을 그대로 재현한 게임은 아닙니다.
    """)
    st.markdown("### KBO 10개 구단")
    st.write(" · ".join(TEAM_NAMES))
    st.markdown("### 선수 자료 참고")
    st.markdown("- [KBO 선수 등록 현황](https://www.koreabaseball.com/Player/RegisterAll.aspx)")
    st.markdown("- [KBO 2026년 소속 선수 621명 등록 보도자료](https://www.koreabaseball.com/MediaNews/Notice/View.aspx?bdSe=11831)")
    st.markdown("- [KBO 구단 소개](https://www.koreabaseball.com/kbo/league/teaminfo.aspx)")

