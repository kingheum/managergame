import random
import copy
import html
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

PITCH_TYPES = {
    "직구": {"difficulty": 0, "ground_bonus": -0.04, "zone_bonus": 0.04, "description": "빠른 구속으로 승부"},
    "슬라이더": {"difficulty": 4, "ground_bonus": 0.02, "zone_bonus": -0.01, "description": "옆으로 휘어지는 변화구"},
    "커브": {"difficulty": 5, "ground_bonus": 0.08, "zone_bonus": -0.04, "description": "큰 낙폭으로 타이밍을 빼앗는 공"},
    "체인지업": {"difficulty": 3, "ground_bonus": 0.10, "zone_bonus": -0.02, "description": "속도 차이로 타이밍을 빼앗는 공"},
    "포크볼": {"difficulty": 6, "ground_bonus": 0.14, "zone_bonus": -0.08, "description": "타자 앞에서 떨어지는 유인구"},
    "커터": {"difficulty": 3, "ground_bonus": 0.01, "zone_bonus": 0.02, "description": "짧게 휘는 빠른 공"},
    "싱커": {"difficulty": 4, "ground_bonus": 0.16, "zone_bonus": -0.02, "description": "낮게 가라앉아 땅볼을 유도"},
}

TEAM_COLORS = {
    "삼성 라이온즈": "#074CA1", "KT 위즈": "#171717", "KIA 타이거즈": "#EA0029",
    "LG 트윈스": "#C30452", "두산 베어스": "#131230", "롯데 자이언츠": "#041E42",
    "SSG 랜더스": "#CE0E2D", "NC 다이노스": "#315288", "한화 이글스": "#F36F21",
    "키움 히어로즈": "#820024",
}

# KBO 공식 선수 프로필 이미지(확인된 선수만 연결). 나머지는 팀 컬러 일러스트로 표시합니다.
KBO_PROFILE_IMAGES = {
    "김도영": "https://6ptotvmi5753.edge.naverncp.com/KBO_IMAGE/person/middle/2026/52605.jpg",
    "원태인": "https://6ptotvmi5753.edge.naverncp.com/KBO_IMAGE/person/middle/2026/69446.jpg",
    "김택연": "https://6ptotvmi5753.edge.naverncp.com/KBO_IMAGE/person/middle/2026/54263.jpg",
    "류현진": "https://6ptotvmi5753.edge.naverncp.com/KBO_IMAGE/person/middle/2026/76715.jpg",
}


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def make_league() -> Dict[str, List[dict]]:
    """선수 원본 목록을 게임에서 사용하는 선수 카드로 바꾼다."""
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
                    "role": "타자", "overall": overall, "contact": contact,
                    "power": power, "speed": speed_or_def, "defense": speed_or_def,
                    "control": 0, "stamina": 0,
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


def best_starter(roster: List[dict]):
    starters = [p for p in roster if p["role"] == "투수"]
    return max(starters, key=lambda p: (p["stamina"], p["overall"])) if starters else None


def advance_walk(bases: List[bool]) -> Tuple[List[bool], int]:
    b1, b2, b3 = bases
    runs = 1 if (b1 and b2 and b3) else 0
    return [True, (b2 or b1), (b3 or (b1 and b2))], runs


def batting_team(game: dict) -> str:
    return game["opponent"] if game["half"] == "초" else game["my_team"]


def fielding_team(game: dict) -> str:
    return game["my_team"] if game["half"] == "초" else game["opponent"]


def current_batter(game: dict, league: dict) -> dict:
    team = batting_team(game)
    lineup = game["lineups"].get(team, [])
    if not lineup:
        return None
    idx = game["batter_index"].get(team, 0) % len(lineup)
    return get_player(league[team], lineup[idx])


def current_pitcher(game: dict, league: dict, team: str):
    roster = league.get(team, [])
    selected_id = game.get("active_pitchers", {}).get(team)
    player = get_player(roster, selected_id) if selected_id else None
    if player and player.get("role") == "투수":
        return player
    player = best_starter(roster)
    if player:
        game.setdefault("active_pitchers", {})[team] = player["id"]
    return player


def init_game(my_team: str, opponent: str, league: dict) -> dict:
    saved = st.session_state.get("saved_lineup", [])
    valid_saved = [pid for pid in saved if get_player(league[my_team], pid) and get_player(league[my_team], pid)["role"] == "타자"]
    my_lineup = valid_saved[:9] if len(valid_saved) == 9 else default_lineup(league[my_team])
    lineups = {my_team: my_lineup, opponent: default_lineup(league[opponent])}
    pitchers = {}
    for team in [my_team, opponent]:
        pitcher = best_starter(league[team])
        pitchers[team] = pitcher["id"] if pitcher else None
    return {
        "my_team": my_team, "opponent": opponent, "inning": 1, "half": "초", "outs": 0,
        "balls": 0, "strikes": 0, "pitch_count": 0, "pitch_pending": None,
        "last_pitch": None, "bases": [False, False, False],
        "scores": {my_team: 0, opponent: 0}, "lineups": lineups,
        "batter_index": {my_team: 0, opponent: 0}, "fatigue": {},
        "active_pitchers": pitchers,
        "logs": [f"경기 시작! {opponent} 원정, {my_team} 홈 경기입니다."],
        "done": False, "max_innings": 12, "half_runs": 0,
    }


def migrate_game_state(game: dict, league: dict) -> None:
    """이전 버전의 저장된 경기에도 새 투구 카운트를 안전하게 추가한다."""
    game.setdefault("balls", 0)
    game.setdefault("strikes", 0)
    game.setdefault("pitch_count", 0)
    game.setdefault("pitch_pending", None)
    game.setdefault("last_pitch", None)
    game.setdefault("active_pitchers", {})
    game.setdefault("fatigue", {})
    for team in (game.get("my_team"), game.get("opponent")):
        if team and not game["active_pitchers"].get(team):
            pitcher = best_starter(league.get(team, []))
            if pitcher:
                game["active_pitchers"][team] = pitcher["id"]


def record_game_result(game: dict) -> str:
    my_score = game["scores"][game["my_team"]]
    opp_score = game["scores"][game["opponent"]]
    return "승리" if my_score > opp_score else "패배" if my_score < opp_score else "무승부"


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


def end_half_if_needed(game: dict) -> None:
    if game["outs"] < 3:
        return
    runs = game["half_runs"]
    game["logs"].append(f"{game['inning']}회 {game['half']} 공격 종료: {runs}점 득점")
    game["half_runs"] = 0
    game["outs"] = 0
    game["bases"] = [False, False, False]
    game["balls"] = 0
    game["strikes"] = 0
    game["pitch_pending"] = None
    if game["half"] == "초":
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


def make_pitch(pitcher: dict, game: dict, pitch_type: str, intent: str) -> dict:
    """한 구의 구종·코스·스트라이크존 진입 여부를 생성한다."""
    profile = PITCH_TYPES[pitch_type]
    fatigue = game["fatigue"].get(pitcher["id"], 0)
    control = clamp(pitcher["control"] - fatigue * 0.8, 40, 98)
    zone_chance = 0.73 if intent == "스트라이크 승부" else 0.38
    zone_chance += (control - 70) * 0.003 + profile["zone_bonus"]
    in_zone = random.random() < clamp(zone_chance, 0.18, 0.91)
    if in_zone:
        location = random.choice(["가운데", "몸쪽", "바깥쪽", "높은 코스", "낮은 코스"])
    else:
        location = random.choice(["높은 볼", "낮은 볼", "몸쪽 빠진 볼", "바깥쪽 빠진 볼"])
    return {
        "type": pitch_type, "intent": intent, "in_zone": in_zone,
        "location": location, "difficulty": profile["difficulty"],
        "ground_bonus": profile["ground_bonus"],
        "description": profile["description"], "pitcher": pitcher["name"],
    }


def choose_cpu_pitch(pitcher: dict) -> Tuple[str, str]:
    types = list(PITCH_TYPES.keys())
    # 구위가 좋은 투수는 변화구 비중을 조금 더 높인다.
    weights = [1.8, 1.2, 0.9, 1.0, 0.7, 0.8, 0.7]
    if pitcher["overall"] >= 85:
        weights = [1.4, 1.3, 1.1, 1.1, 1.0, 0.9, 0.9]
    ptype = random.choices(types, weights=weights, k=1)[0]
    intent = random.choices(["스트라이크 승부", "유인구"], weights=[0.66, 0.34], k=1)[0]
    return ptype, intent


def award_walk(game: dict, offense: str, batter: dict, pitcher: dict, note: str = "볼넷") -> str:
    bases, runs = advance_walk(game["bases"])
    game["bases"] = bases
    game["scores"][offense] += runs
    game["half_runs"] += runs
    return f"{note}! {batter['name']} 출루" + (f" · {runs}점 득점" if runs else "")


def complete_plate_appearance(game: dict, offense: str) -> None:
    game["batter_index"][offense] = game["batter_index"].get(offense, 0) + 1
    game["balls"] = 0
    game["strikes"] = 0
    game["pitch_pending"] = None
    end_half_if_needed(game)


def resolve_take(game: dict, batter: dict, pitcher: dict, offense: str) -> str:
    pitch = game.get("pitch_pending")
    if not pitch:
        return "먼저 투구를 요청하세요."
    game["pitch_pending"] = None
    if pitch["in_zone"]:
        game["strikes"] += 1
        result = f"스트라이크! ({pitch['type']} · {pitch['location']})"
        if game["strikes"] >= 3:
            game["outs"] += 1
            result += f" 삼진 아웃! {batter['name']} 타석 종료"
            game["logs"].append(result)
            complete_plate_appearance(game, offense)
            return result
    else:
        game["balls"] += 1
        result = f"볼! ({pitch['type']} · {pitch['location']})"
        if game["balls"] >= 4:
            result = award_walk(game, offense, batter, pitcher) + f" · {pitch['type']}"
            game["logs"].append(result)
            complete_plate_appearance(game, offense)
            return result
    game["logs"].append(result)
    return result


def fielding_rating(roster: List[dict]) -> float:
    fielders = [p["defense"] for p in roster if p["role"] == "타자"]
    return sum(fielders) / max(1, len(fielders))


def describe_hit_direction(hit_type: str, direction: str) -> str:
    if hit_type == "홈런":
        return {"좌측": "좌월 홈런", "중앙": "중월 홈런", "우측": "우월 홈런"}[direction]
    if hit_type == "2루타":
        return {"좌측": "좌중간 2루타", "중앙": "중앙 펜스 앞 2루타", "우측": "우중간 2루타"}[direction]
    if hit_type == "3루타":
        return {"좌측": "좌익선상 3루타", "중앙": "중앙을 가르는 3루타", "우측": "우익선상 3루타"}[direction]
    return {"좌측": "좌익수 앞 안타", "중앙": "중전 안타", "우측": "우익수 앞 안타"}[direction]


def apply_hit(game: dict, offense: str, hit_type: str) -> int:
    b1, b2, b3 = game["bases"]
    if hit_type == "홈런":
        runs = 1 + int(b1) + int(b2) + int(b3)
        game["bases"] = [False, False, False]
    elif hit_type == "3루타":
        runs = int(b1) + int(b2) + int(b3)
        game["bases"] = [False, False, True]
    elif hit_type == "2루타":
        runs = int(b2) + int(b3)
        game["bases"] = [False, True, b1]
    else:
        runs = int(b3)
        game["bases"] = [True, b1, b2]
    game["scores"][offense] += runs
    game["half_runs"] += runs
    return runs


def resolve_ball_in_play(game: dict, batter: dict, pitcher: dict, offense: str,
                         batting_mode: str, pitch: dict, defense_roster: List[dict]) -> str:
    """타자 능력치·스윙 선택·구종·수비력으로 타구 결과와 방향을 계산한다."""
    contact_bonus = 17 if batting_mode == "컨택 스윙" else -13 if batting_mode == "파워 스윙" else 0
    power_bonus = -13 if batting_mode == "컨택 스윙" else 18 if batting_mode == "파워 스윙" else 0
    effective_contact = clamp(batter["contact"] + contact_bonus, 25, 110)
    effective_power = clamp(batter["power"] + power_bonus, 25, 115)
    stuff = pitcher["overall"] + pitch["difficulty"] * 1.8
    defense = fielding_rating(defense_roster)
    zone_adjust = 0.035 if pitch["in_zone"] else -0.055
    hit_chance = clamp(
        0.265 + (effective_contact - 70) * 0.0042 + (effective_power - 70) * 0.0009
        - (stuff - 75) * 0.0020 - (defense - 70) * 0.0012 + zone_adjust,
        0.12, 0.46,
    )
    ground_rate = clamp(0.37 + pitch["ground_bonus"] - (effective_power - 70) * 0.0022, 0.18, 0.68)
    # 몸쪽 공은 당겨 치는 타구, 바깥쪽 공은 밀어 치는 타구 비중을 높이고
    # 컨택이 좋은 타자는 중앙 방향 타구 비중을 조금 높인다.
    center_weight = clamp(0.26 + (effective_contact - 70) * 0.002, 0.18, 0.34)
    side_weight = (1.0 - center_weight) / 2
    if pitch["location"] == "몸쪽":
        direction_weights = [side_weight + 0.14, center_weight, max(0.05, side_weight - 0.14)]
    elif pitch["location"] == "바깥쪽":
        direction_weights = [max(0.05, side_weight - 0.14), center_weight, side_weight + 0.14]
    else:
        pull_adjust = clamp((effective_power - 70) * 0.001, -0.07, 0.07)
        direction_weights = [side_weight + pull_adjust, center_weight, side_weight - pull_adjust]
    direction = random.choices(["좌측", "중앙", "우측"], weights=direction_weights, k=1)[0]

    if random.random() < hit_chance:
        homer_w = max(0.012, 0.018 + (effective_power - 70) * 0.0010)
        triple_w = max(0.004, 0.006 + (batter["speed"] - 65) * 0.00025)
        double_w = max(0.035, 0.055 + (effective_power - 70) * 0.00085)
        single_w = max(0.08, 0.20 + (effective_contact - 70) * 0.0015)
        hit_type = random.choices(["홈런", "3루타", "2루타", "안타"],
                                  weights=[homer_w, triple_w, double_w, single_w], k=1)[0]
        runs = apply_hit(game, offense, hit_type)
        result = describe_hit_direction(hit_type, direction)
        if hit_type == "안타" and runs:
            result += f" · {runs}점 득점"
        elif hit_type == "홈런":
            result += f" · {runs}점 홈런"
        elif runs:
            result += f" · {runs}점 득점"
        return result

    if random.random() < ground_rate:
        infield = random.choice(["투수 앞", "1루수 앞", "2루수 앞", "유격수 앞", "3루수 앞"])
        # 주력은 내야 안타 가능성을 조금 높이고, 수비력은 내야 땅볼 처리 확률을 높인다.
        infield_hit = clamp(0.035 + (batter["speed"] - 70) * 0.0018 + (effective_contact - 70) * 0.0007
                            - (defense - 70) * 0.0010, 0.01, 0.15)
        if random.random() < infield_hit:
            runs = apply_hit(game, offense, "안타")
            return f"내야 안타! {infield} 방향 타구 · {runs}점 득점" if runs else f"내야 안타! {infield} 방향 타구"
        if game["bases"][0] and game["outs"] < 2 and random.random() < 0.17:
            game["outs"] += 2
            game["bases"][0] = False
            return f"병살타! {infield} 땅볼, 아웃카운트 2개"
        game["outs"] += 1
        return f"{infield} 땅볼 아웃"

    # 뜬공·직선타는 타자의 파워와 투구 종류에 따라 타구 방향이 달라진다.
    if random.random() < 0.62:
        fielder = {"좌측": "좌익수", "중앙": "중견수", "우측": "우익수"}[direction]
        game["outs"] += 1
        if game["bases"][2] and game["outs"] < 3 and random.random() < 0.48:
            game["bases"][2] = False
            game["scores"][offense] += 1
            game["half_runs"] += 1
            return f"{fielder} 희생플라이 아웃 · 3루 주자 득점"
        return f"{fielder} 뜬공 아웃"
    else:
        fielder = {"좌측": "3루수", "중앙": "유격수", "우측": "2루수"}[direction]
        game["outs"] += 1
        return f"{fielder} 직선타 아웃"


def resolve_swing(game: dict, batter: dict, pitcher: dict, offense: str,
                  batting_mode: str, defense_roster: List[dict]) -> str:
    pitch = game.get("pitch_pending")
    if not pitch:
        return "먼저 투구를 요청하세요."
    game["pitch_pending"] = None
    contact_bonus = 17 if batting_mode == "컨택 스윙" else -13 if batting_mode == "파워 스윙" else 0
    effective_contact = clamp(batter["contact"] + contact_bonus, 25, 110)
    stuff = pitcher["overall"] + pitch["difficulty"] * 1.8
    miss_chance = clamp(0.255 + (stuff - effective_contact) * 0.004 - (7 if pitch["in_zone"] else 0) * 0.01, 0.08, 0.52)
    if random.random() < miss_chance:
        game["strikes"] += 1
        result = f"헛스윙! {pitch['type']}에 타이밍을 놓쳤습니다."
        if game["strikes"] >= 3:
            game["outs"] += 1
            result += " 삼진 아웃!"
            game["logs"].append(result)
            complete_plate_appearance(game, offense)
            return result
        game["logs"].append(result)
        return result

    foul_chance = 0.23 if pitch["in_zone"] else 0.30
    if random.random() < foul_chance:
        if game["strikes"] < 2:
            game["strikes"] += 1
        result = "파울! 2스트라이크 이후 파울은 스트라이크가 추가되지 않습니다."
        game["logs"].append(result)
        return result

    result = resolve_ball_in_play(game, batter, pitcher, offense, batting_mode, pitch, defense_roster)
    game["logs"].append(result)
    complete_plate_appearance(game, offense)
    return result


def cpu_decide_swing(game: dict, batter: dict, pitch: dict) -> bool:
    if pitch["in_zone"]:
        chance = 0.69 + (batter["contact"] - 70) * 0.002
    else:
        chance = 0.13 + (game["strikes"] == 2) * 0.23 - (game["balls"] == 3) * 0.10
    if game["strikes"] == 2:
        chance += 0.12
    if game["balls"] == 3 and not pitch["in_zone"]:
        chance -= 0.20
    return random.random() < clamp(chance, 0.04, 0.94)


def resolve_cpu_pitch(game: dict, batter: dict, pitcher: dict, offense: str,
                      pitch: dict, defense_roster: List[dict]) -> str:
    if cpu_decide_swing(game, batter, pitch):
        style = "컨택 스윙" if game["strikes"] >= 2 else ("파워 스윙" if batter["power"] >= batter["contact"] + 10 else "기본 스윙")
        game["pitch_pending"] = pitch
        return resolve_swing(game, batter, pitcher, offense, style, defense_roster)
    game["pitch_pending"] = pitch
    return resolve_take(game, batter, pitcher, offense)


def throw_user_pitch(game: dict, league: dict, pitch_type: str, intent: str) -> str:
    offense = batting_team(game)
    defense = fielding_team(game)
    batter = current_batter(game, league)
    pitcher = current_pitcher(game, league, defense)
    if batter is None or pitcher is None:
        return "타자 또는 투수를 찾을 수 없습니다."
    pitch = make_pitch(pitcher, game, pitch_type, intent)
    game["pitch_count"] += 1
    game["fatigue"][pitcher["id"]] = game["fatigue"].get(pitcher["id"], 0) + 1
    game["last_pitch"] = pitch
    result = resolve_cpu_pitch(game, batter, pitcher, offense, pitch, league[defense])
    log = f"{game['inning']}회 {game['half']} · {pitcher['name']} {pitch_type}({intent}) → {batter['name']}: {result}"
    if not game["done"]:
        game["logs"].append(log)
    end_half_if_needed(game)
    return log


def run_auto_at_bat(game: dict, league: dict, human_is_batting: bool = False) -> List[str]:
    """자동 타격/자동 수비로 한 타석을 끝까지 진행한다. 최대 18구로 안전 제한한다."""
    offense = batting_team(game)
    defense = fielding_team(game)
    start_batter_idx = game["batter_index"].get(offense, 0)
    start_inning, start_half = game["inning"], game["half"]
    results = []
    for _ in range(18):
        if game["done"] or game["inning"] != start_inning or game["half"] != start_half:
            break
        if game["batter_index"].get(offense, 0) != start_batter_idx:
            break
        batter = current_batter(game, league)
        pitcher = current_pitcher(game, league, defense)
        if batter is None or pitcher is None:
            break
        pitch_type, intent = choose_cpu_pitch(pitcher)
        pitch = make_pitch(pitcher, game, pitch_type, intent)
        game["pitch_count"] += 1
        game["fatigue"][pitcher["id"]] = game["fatigue"].get(pitcher["id"], 0) + 1
        game["last_pitch"] = pitch
        game["pitch_pending"] = pitch
        # 자동 타격은 스트라이크존과 카운트, 타자 능력치에 따라 기다리거나 스윙한다.
        if human_is_batting:
            swing = cpu_decide_swing(game, batter, pitch)
            style = "컨택 스윙" if game["strikes"] == 2 else ("파워 스윙" if batter["power"] > batter["contact"] + 12 else "기본 스윙")
            if swing:
                result = resolve_swing(game, batter, pitcher, offense, style, league[defense])
            else:
                result = resolve_take(game, batter, pitcher, offense)
        else:
            result = resolve_cpu_pitch(game, batter, pitcher, offense, pitch, league[defense])
        detail = f"{pitch_type} · {'존 안' if pitch['in_zone'] else '존 밖'} → {result}"
        results.append(detail)
        game["logs"].append(f"{game['inning']}회 {game['half']} · {batter['name']}: {detail}")
        if game["batter_index"].get(offense, 0) != start_batter_idx:
            break
        if game["done"] or game["inning"] != start_inning or game["half"] != start_half:
            break
    return results


def render_field(bases: List[bool], outs: int) -> None:
    """1·2·3루 점유 상태를 야구장 다이아몬드로 표현한다."""
    base_specs = [(320, 102, bases[1], "2루"), (445, 225, bases[0], "1루"),
                  (195, 225, bases[2], "3루"), (320, 348, False, "홈")]
    marks = []
    for x, y, occupied, label in base_specs:
        fill = "#ffd166" if occupied else "#f7f8fa"
        stroke = "#f9a826" if occupied else "#d4dbe3"
        marks.append(f'<g transform="translate({x} {y}) rotate(45)"><rect x="-17" y="-17" width="34" height="34" rx="3" fill="{fill}" stroke="{stroke}" stroke-width="4"/></g>')
        marks.append(f'<text x="{x}" y="{y+39}" text-anchor="middle" font-size="15" font-weight="700" fill="#ffffff">{label}</text>')
    svg = f'''<div style="background:linear-gradient(180deg,#184f35,#103a29);border:1px solid #2e7352;border-radius:18px;padding:10px;color:white;">
    <div style="display:flex;justify-content:space-between;align-items:center;padding:4px 8px 0;"><b>🏟️ 주자 상황</b><span style="font-size:13px;color:#d9f3df">아웃 {outs}/3</span></div>
    <svg viewBox="0 0 640 410" style="width:100%;height:auto;display:block" role="img" aria-label="야구장 주자 배치">
      <path d="M320 50 L525 225 L320 380 L115 225 Z" fill="#9b6a3e" stroke="#dcb58b" stroke-width="3"/>
      <path d="M320 100 L445 225 L320 350 L195 225 Z" fill="#4d9a55" stroke="#e6d1a8" stroke-width="2"/>
      <path d="M320 102 L445 225 L320 348 L195 225 Z" fill="none" stroke="#fff2d6" stroke-width="3" stroke-dasharray="7 5"/>
      <circle cx="320" cy="246" r="39" fill="#b47b4c" stroke="#e2bd8c" stroke-width="2"/>
      <circle cx="320" cy="246" r="8" fill="#e4c49a"/>
      <path d="M320 348 L320 275" stroke="#ffffff" stroke-width="2" stroke-dasharray="5 5"/>
      {''.join(marks)}
      <text x="320" y="28" text-anchor="middle" font-size="14" fill="#e5f6e8">센터 방향</text>
    </svg>
    <div style="text-align:center;font-size:12px;color:#e4f3e7;padding-bottom:4px">노란 베이스 = 주자 있음</div></div>'''
    st.markdown(svg, unsafe_allow_html=True)


def render_player_profile(player: dict, title: str, fatigue: int = 0, pitch_count: int = 0) -> None:
    if not player:
        st.warning(f"{title}: 선수를 표시할 수 없습니다.")
        return
    team_color = TEAM_COLORS.get(player.get("team", ""), "#174e82")
    name = html.escape(player["name"])
    team = html.escape(player["team"])
    pos = html.escape(player["pos"])
    if player["role"] == "타자":
        stat_items = [("컨택", player["contact"]), ("파워", player["power"]), ("주력", player["speed"])]
        role = "BATTER PROFILE"
    else:
        stat_items = [("구위", player["overall"]), ("제구", player["control"]), ("체력", player["stamina"])]
        role = "PITCHER PROFILE"
    stats_html = "".join(
        f'<div style="flex:1;background:#f0f3f7;border-radius:9px;padding:8px 4px;text-align:center;">'
        f'<div style="font-size:11px;color:#617083">{label}</div><div style="font-size:19px;font-weight:800;color:#162538">{value}</div></div>'
        for label, value in stat_items
    )
    fatigue_html = f'<div style="font-size:11px;color:#6e7c8c;margin-top:8px">피로도 {fatigue} · 누적 투구 {pitch_count}구</div>' if player["role"] == "투수" else '<div style="font-size:11px;color:#6e7c8c;margin-top:8px">타석 능력치 기반 시뮬레이션</div>'
    official_photo = KBO_PROFILE_IMAGES.get(player["name"])
    if official_photo:
        avatar_html = f'<img src="{html.escape(official_photo, quote=True)}" alt="{name} KBO 프로필" style="width:82px;height:94px;object-fit:cover;object-position:top center;border-radius:12px;background:#e9eef5;display:block;" />'
    else:
        avatar_html = f'<svg viewBox="0 0 100 110" width="78" height="86" aria-label="선수 프로필 일러스트"><circle cx="50" cy="27" r="17" fill="#e2b99b"/><path d="M33 25 Q50 2 68 24 L66 17 Q49 2 32 17 Z" fill="#26364a"/><path d="M18 105 Q20 63 50 60 Q80 63 82 105 Z" fill="{team_color}"/><path d="M42 63 L50 78 L58 63" fill="#ffffff" opacity=".9"/><text x="50" y="96" font-size="13" text-anchor="middle" font-weight="800" fill="#ffffff">KBO</text></svg>'
    card = f'''<div style="border:1px solid #d7dee8;border-radius:16px;overflow:hidden;background:#ffffff;box-shadow:0 2px 10px rgba(20,40,60,.06);margin:2px 0 10px">
      <div style="background:{team_color};color:white;padding:7px 12px;display:flex;justify-content:space-between;font-size:11px;letter-spacing:.08em;font-weight:800"><span>KBO · {role}</span><span>{html.escape(title)}</span></div>
      <div style="display:flex;gap:13px;align-items:center;padding:13px 13px 9px">
        <div style="width:82px;height:94px;flex-shrink:0;background:linear-gradient(145deg,#e9eef5,#d5deea);border-radius:12px;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden">
          {avatar_html}
        </div>
        <div style="min-width:0;flex:1">
          <div style="font-size:12px;color:#66778a;font-weight:700">{team} · {pos}</div>
          <div style="font-size:24px;font-weight:900;color:#18283b;line-height:1.25;word-break:keep-all">{name}</div>
          <div style="display:inline-block;margin-top:5px;background:#edf2f8;color:#34465c;border-radius:20px;padding:3px 9px;font-size:11px;font-weight:800">종합 능력치 {player['overall']}</div>
        </div>
      </div>
      <div style="display:flex;gap:7px;padding:0 12px 4px">{stats_html}</div>
      <div style="padding:0 13px 10px">{fatigue_html}</div>
    </div>'''
    st.markdown(card, unsafe_allow_html=True)


def render_scoreboard(game: dict) -> None:
    c = st.columns([1.2, 1, 0.7, 1, 1.2])
    c[0].metric("이닝", f"{game['inning']}회 {game['half']}")
    c[1].metric(game["my_team"], game["scores"][game["my_team"]])
    c[2].metric("VS", "⚾")
    c[3].metric(game["opponent"], game["scores"][game["opponent"]])
    c[4].metric("투구 수", f"{game['pitch_count']}구")


def finish_game_if_needed():
    game = st.session_state.game
    if game and game.get("done") and not game.get("result_recorded"):
        result = record_game_result(game)
        if result == "승리": st.session_state.wins += 1
        elif result == "패배": st.session_state.losses += 1
        else: st.session_state.draws += 1
        game["result_recorded"] = True
        st.session_state.last_result = f"{result} {game['scores'][game['my_team']]}-{game['scores'][game['opponent']]}"


# ----------------------------------------------------------------------------
# Streamlit UI
# ----------------------------------------------------------------------------
st.markdown("""<style>
.block-container{padding-top:1.4rem;padding-bottom:2rem}
.kbo-hint{font-size:12px;color:#718096}
div[data-testid="stMetric"]{background:#f7f9fc;border:1px solid #e4e9f0;border-radius:12px;padding:8px 12px}
.pitch-panel{border:1px solid #d8e1eb;background:#f7faff;border-radius:14px;padding:12px 15px;margin:6px 0 10px;color:#24364a}
.pitch-pill{display:inline-block;padding:5px 10px;border-radius:18px;background:#e3edf9;color:#204e7d;font-weight:800;margin:3px 5px 3px 0}
</style>""", unsafe_allow_html=True)

st.title("⚾ KBO 야구 감독 시뮬레이터")
st.caption("구단 선택부터 선수 운영, 한 구씩 투구·타격 지시까지 직접 플레이하는 야구 감독 게임")

if "league" not in st.session_state:
    st.markdown("### 감독으로 부임할 구단을 선택하세요")
    selected_team = st.selectbox("응원하거나 맡고 싶은 팀", TEAM_NAMES, index=2)
    st.info("실제 KBO 구단·선수 이름을 참고한 게임용 데이터입니다. 능력치, 투구 결과, 이적료는 게임 시뮬레이션 수치입니다.")
    if st.button("감독 부임하기", type="primary", use_container_width=True):
        start_new_career(selected_team)
        st.rerun()
    st.stop()

league = st.session_state.league
my_team = st.session_state.my_team
my_roster = league[my_team]
game = st.session_state.game
if game is not None:
    migrate_game_state(game, league)

with st.sidebar:
    st.header("🏟️ 감독 정보")
    st.subheader(my_team)
    st.metric("구단 운영 자금", f"{st.session_state.budget:.1f}억 원")
    a, b = st.columns(2)
    a.metric("승리", st.session_state.wins)
    b.metric("패배", st.session_state.losses)
    st.metric("무승부", st.session_state.draws)
    st.caption(f"진행 경기: {st.session_state.game_count}")
    st.divider()
    if st.button("구단 다시 선택하기", use_container_width=True):
        for key in ["league", "my_team", "budget", "wins", "losses", "draws", "game", "game_count", "last_result"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    st.caption("※ 현재 게임 정보는 브라우저 세션에 저장됩니다.")

metric_cols = st.columns(4)
metric_cols[0].metric("팀 전력", f"{team_power(my_roster)} / 100")
metric_cols[1].metric("선수단", f"{len(my_roster)}명")
metric_cols[2].metric("승률", f"{st.session_state.wins / max(1, st.session_state.wins + st.session_state.losses + st.session_state.draws):.3f}")
metric_cols[3].metric("최근 경기", st.session_state.last_result)

tab_game, tab_roster, tab_front, tab_guide = st.tabs(["🎮 경기 운영", "📋 선수단·타순", "🔁 구단 운영", "📖 게임 설명"])

with tab_game:
    st.subheader("🎮 한 구씩 진행하는 경기 운영")
    game = st.session_state.game
    if game is None or game.get("done"):
        finish_game_if_needed()
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
            st.info("상대 구단을 선택하고 경기를 시작하세요. 타석마다 투구와 타격을 한 구씩 직접 선택할 수 있습니다.")
    else:
        render_scoreboard(game)
        offense = batting_team(game)
        defense = fielding_team(game)
        batter = current_batter(game, league)
        pitcher = current_pitcher(game, league, defense)
        is_user_batting = offense == my_team

        # 수비 중에는 사용자가 그 타석의 투수를 선택한다.
        if not is_user_batting:
            pitchers = [p for p in my_roster if p["role"] == "투수"]
            if pitchers:
                selected_pid = st.selectbox(
                    "현재 마운드 투수 선택",
                    [p["id"] for p in pitchers],
                    index=next((i for i, p in enumerate(pitchers) if pitcher and p["id"] == pitcher["id"]), 0),
                    format_func=lambda pid: (lambda p: f"{p['name']} · 구위 {p['overall']} · 제구 {p['control']} · 피로 {game['fatigue'].get(pid, 0)}")(get_player(my_roster, pid)),
                    key="game_pitcher_select",
                )
                game["active_pitchers"][my_team] = selected_pid
                pitcher = get_player(my_roster, selected_pid)

        if batter and pitcher:
            st.caption(f"공격: **{offense}**　|　수비: **{defense}**　|　현재 타자: **{batter['name']}**")
            field_col, lineup_col = st.columns([1.0, 1.15], gap="large")
            with field_col:
                render_field(game["bases"], game["outs"])
                count_cols = st.columns(3)
                count_cols[0].metric("볼", game["balls"])
                count_cols[1].metric("스트라이크", game["strikes"])
                count_cols[2].metric("아웃", f"{game['outs']}/3")
                st.markdown(f"**주자:** 1루 {'🟠' if game['bases'][0] else '⚪'}　2루 {'🟠' if game['bases'][1] else '⚪'}　3루 {'🟠' if game['bases'][2] else '⚪'}")
            with lineup_col:
                profile_a, profile_b = st.columns(2)
                with profile_a:
                    render_player_profile(batter, "타석 선수")
                with profile_b:
                    render_player_profile(pitcher, "마운드 투수", game["fatigue"].get(pitcher["id"], 0), game["fatigue"].get(pitcher["id"], 0))

            if game.get("last_pitch") and game.get("pitch_pending"):
                last = game["last_pitch"]
                st.markdown(
                    f'<div class="pitch-panel"><b>⚾ 현재 투구</b><br><span class="pitch-pill">{html.escape(last["type"])}</span>'
                    f'<span class="pitch-pill">{html.escape(last["intent"])}</span>'
                    f'<span class="pitch-pill">{html.escape(last["location"])}</span>'
                    f'<div style="font-size:13px;margin-top:5px">{ "스트라이크존 안" if last["in_zone"] else "스트라이크존 밖" } · {html.escape(last["description"])}</div></div>',
                    unsafe_allow_html=True,
                )

            if is_user_batting:
                st.markdown("### 🏏 타격 작전")
                batting_mode = st.radio(
                    "스윙 방식", ["기본 스윙", "컨택 스윙", "파워 스윙", "자동 타격"],
                    horizontal=True, key="batting_mode_select",
                    help="컨택은 정확도 중심, 파워는 장타 중심, 기본은 균형형입니다. 자동은 카운트와 선수 능력치를 보고 자동으로 판단합니다.",
                )
                if batting_mode == "자동 타격":
                    label = "현재 투구부터 자동으로 타석 끝내기" if game.get("pitch_pending") else "자동 타격 실행 · 타석 끝까지"
                    if st.button(label, type="primary", use_container_width=True, key="auto_bat"):
                        # 이미 대기 중인 투구가 있으면 자동 판단한 뒤 다음 투구를 이어간다.
                        if game.get("pitch_pending"):
                            pending = game["pitch_pending"]
                            pending_pitcher = pitcher
                            before_idx = game["batter_index"].get(offense, 0)
                            before_inning, before_half = game["inning"], game["half"]
                            if cpu_decide_swing(game, batter, pending):
                                style = "컨택 스윙" if game["strikes"] == 2 else ("파워 스윙" if batter["power"] > batter["contact"] + 12 else "기본 스윙")
                                first_result = resolve_swing(game, batter, pending_pitcher, offense, style, league[defense])
                            else:
                                first_result = resolve_take(game, batter, pending_pitcher, offense)
                            game["logs"].append(f"자동 타격: {first_result}")
                            # 대기 중이던 공으로 타석이 끝났다면 다음 타자까지 자동 진행하지 않습니다.
                            if (game["batter_index"].get(offense, 0) == before_idx
                                    and game["inning"] == before_inning and game["half"] == before_half
                                    and not game["done"]):
                                run_auto_at_bat(game, league, human_is_batting=True)
                        else:
                            run_auto_at_bat(game, league, human_is_batting=True)
                        st.rerun()
                elif game.get("pitch_pending") is None:
                    st.caption("먼저 상대 투수가 던진 공을 확인한 뒤 스윙하거나 참을 수 있습니다.")
                    if st.button("상대 투구 받기", type="primary", use_container_width=True, key="request_pitch"):
                        cpu_pitcher = current_pitcher(game, league, defense)
                        ptype, intent = choose_cpu_pitch(cpu_pitcher)
                        pitch = make_pitch(cpu_pitcher, game, ptype, intent)
                        game["pitch_count"] += 1
                        game["fatigue"][cpu_pitcher["id"]] = game["fatigue"].get(cpu_pitcher["id"], 0) + 1
                        game["last_pitch"] = pitch
                        game["pitch_pending"] = pitch
                        st.rerun()
                else:
                    act1, act2 = st.columns(2)
                    if act1.button("🏏 스윙하기", type="primary", use_container_width=True, key="player_swing"):
                        result = resolve_swing(game, batter, pitcher, offense, batting_mode, league[defense])
                        game["logs"].append(f"{batter['name']} · {result}")
                        st.rerun()
                    if act2.button("👀 공을 지켜보기", use_container_width=True, key="player_take"):
                        result = resolve_take(game, batter, pitcher, offense)
                        st.rerun()
                bench = [p for p in my_roster if p["role"] == "타자" and p["pos"] == "벤치"]
                if bench:
                    with st.expander("대타 기용"):
                        bench_id = st.selectbox("대타 후보", [p["id"] for p in bench],
                                                format_func=lambda pid: (lambda p: f"{p['name']} · 컨택 {p['contact']} · 파워 {p['power']}")(get_player(my_roster, pid)),
                                                key="live_pinch_hitter")
                        if st.button("대타 투입", key="live_pinch_button"):
                            idx = game["batter_index"][my_team] % len(game["lineups"][my_team])
                            old_id = game["lineups"][my_team][idx]
                            game["lineups"][my_team][idx] = bench_id
                            old_player = get_player(my_roster, old_id)
                            if old_player:
                                old_player["pos"] = "벤치"
                            get_player(my_roster, bench_id)["pos"] = "대타"
                            game["pitch_pending"] = None
                            st.success(f"{get_player(my_roster, bench_id)['name']} 대타 투입")
                            st.rerun()
            else:
                st.markdown("### 🎯 투구 작전")
                st.caption("한 구를 던질 때마다 구종과 승부 방식을 새로 선택하세요.")
                pc1, pc2 = st.columns([1, 1])
                with pc1:
                    pitch_type = st.selectbox("구종 선택", list(PITCH_TYPES.keys()), key="pitch_type_choice")
                    st.caption(PITCH_TYPES[pitch_type]["description"])
                with pc2:
                    intent = st.radio("투구 의도", ["스트라이크 승부", "유인구"], key="pitch_intent_choice",
                                      help="스트라이크 승부는 존에 넣을 확률이 높고, 유인구는 존 밖으로 빠질 위험이 있지만 헛스윙을 유도할 수 있습니다.")
                pc_buttons = st.columns(2)
                if pc_buttons[0].button("⚾ 한 구 투구하기", type="primary", use_container_width=True, key="one_pitch"):
                    throw_user_pitch(game, league, pitch_type, intent)
                    st.rerun()
                if pc_buttons[1].button("🤖 자동 수비 · 타석 끝까지", use_container_width=True, key="auto_pitch"):
                    results = run_auto_at_bat(game, league, human_is_batting=False)
                    if results:
                        st.session_state.auto_summary = results
                    st.rerun()
                if st.session_state.get("auto_summary"):
                    with st.expander("자동 수비 투구 결과", expanded=True):
                        for line in st.session_state.auto_summary:
                            st.write("• " + line)
                    st.session_state.auto_summary = []
        else:
            st.error("현재 타자 또는 투수가 없습니다. 선수단 탭에서 선수를 확인하세요.")

        st.divider()
        st.markdown("### 📜 경기 중계")
        with st.expander("최근 투구·타구 기록", expanded=True):
            if game["logs"]:
                for item in reversed(game["logs"][-18:]):
                    st.write("• " + item)
            else:
                st.caption("아직 기록이 없습니다.")

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
            row.update({"구위": p["overall"], "제구": p["control"], "체력": p["stamina"]})
        roster_rows.append(row)
    st.dataframe(pd.DataFrame(roster_rows), use_container_width=True, hide_index=True)

    st.markdown("### 선발 타순 편집")
    if game is not None and not game.get("done"):
        st.info("경기 중 타순 편집은 다음 경기부터 적용됩니다.")
    default_ids = default_lineup(my_roster)
    selected_names = st.multiselect(
        "경기에 사용할 타자 9명 선택 (선택한 순서가 타순)",
        [p["id"] for p in hitters],
        default=[pid for pid in default_ids if get_player(my_roster, pid)],
        format_func=lambda pid: (lambda p: f"{p['name']} ({p['pos']}, {p['overall']})")(get_player(my_roster, pid)),
        max_selections=9, key="lineup_editor",
    )
    if st.button("선발 타순 저장", use_container_width=True):
        if len(selected_names) == 9:
            st.session_state.saved_lineup = list(selected_names)
            st.success("선발 타순을 저장했습니다. 새 경기부터 적용됩니다.")
        else:
            st.warning("타순에는 타자 9명을 선택해야 합니다.")
    st.caption("※ 프로필 카드의 수치와 경기 능력치는 실제 KBO 공식 기록이 아닌 게임 밸런스용 가상 수치입니다.")

with tab_front:
    st.subheader("구단 운영: 영입 · 트레이드 · 방출")
    st.caption("선수 이동은 게임 안에서만 적용되는 가상 운영 규칙입니다.")
    game_active = st.session_state.game is not None and not st.session_state.game.get("done", False)
    if game_active:
        st.warning("경기 진행 중에는 영입·트레이드·방출을 할 수 없습니다.")
    sign_tab, trade_tab, release_tab = st.tabs(["💰 선수 영입", "🔄 트레이드", "📤 선수 방출"])
    with sign_tab:
        other_players = [(team, p) for team in TEAM_NAMES if team != my_team for p in league[team]]
        role_filter = st.radio("영입 포지션", ["전체", "타자", "투수"], horizontal=True, key="sign_role")
        candidates = [(team, p) for team, p in other_players if role_filter == "전체" or p["role"] == role_filter]
        candidate_lookup = {p["id"]: (team, p) for team, p in candidates}
        if candidate_lookup:
            selected_id = st.selectbox("영입할 선수", list(candidate_lookup.keys()),
                                       format_func=lambda pid: (lambda item: f"{item[1]['name']} · {item[0]} · {item[1]['pos']} · OVR {item[1]['overall']} · {player_fee(item[1]):.1f}억")(candidate_lookup[pid]), key="sign_candidate")
            from_team, candidate = candidate_lookup[selected_id]
            fee = player_fee(candidate)
            a, b, c = st.columns(3)
            a.metric("선수 능력치", candidate["overall"])
            b.metric("게임 이적료", f"{fee:.1f}억")
            c.metric("영입 후 자금", f"{st.session_state.budget-fee:.1f}억")
            if st.button("이 선수 영입하기", type="primary", disabled=(st.session_state.budget < fee or game_active), use_container_width=True):
                other_hitters = sum(1 for p in league[from_team] if p["role"] == "타자")
                other_pitchers = sum(1 for p in league[from_team] if p["role"] == "투수")
                role_safe = (candidate["role"] == "타자" and other_hitters > 9) or (candidate["role"] == "투수" and other_pitchers > 3)
                if len(league[my_team]) >= 25:
                    st.error("선수단은 최대 25명까지 등록할 수 있습니다.")
                elif len(league[from_team]) <= 10 or not role_safe:
                    st.error("상대 팀 최소 선수 구성을 유지하기 위해 영입할 수 없습니다.")
                else:
                    moved = get_player(league[from_team], candidate["id"])
                    league[from_team] = [p for p in league[from_team] if p["id"] != candidate["id"]]
                    moved["team"] = my_team
                    league[my_team].append(moved)
                    st.session_state.budget = round(st.session_state.budget-fee, 1)
                    st.success(f"{moved['name']} 영입 완료! {fee:.1f}억 원 사용")
                    st.rerun()
    with trade_tab:
        own_choice_id = st.selectbox("우리 구단에서 보낼 선수", [p["id"] for p in my_roster],
                                     format_func=lambda pid: (lambda p: f"{p['name']} ({p['pos']}, {p['overall']})")(get_player(my_roster, pid)), key="trade_own")
        other_team = st.selectbox("트레이드 상대 구단", [t for t in TEAM_NAMES if t != my_team], key="trade_team")
        targets = league[other_team]
        target_id = st.selectbox("상대 구단에서 받을 선수", [p["id"] for p in targets],
                                 format_func=lambda pid: (lambda p: f"{p['name']} ({p['pos']}, {p['overall']})")(get_player(targets, pid)), key="trade_target")
        own_p, target_p = get_player(my_roster, own_choice_id), get_player(targets, target_id)
        if own_p and target_p:
            diff = abs(own_p["overall"]-target_p["overall"])
            same_role = own_p["role"] == target_p["role"]
            st.write(f"능력치 차이: {diff}점")
            if st.button("트레이드 제안", type="primary", disabled=(game_active or not same_role), use_container_width=True):
                if diff > 18:
                    st.error("상대가 전력 차이를 이유로 트레이드를 거절했습니다.")
                else:
                    league[my_team] = [p for p in league[my_team] if p["id"] != own_p["id"]]
                    league[other_team] = [p for p in league[other_team] if p["id"] != target_p["id"]]
                    own_p["team"], target_p["team"] = other_team, my_team
                    league[my_team].append(target_p)
                    league[other_team].append(own_p)
                    st.success(f"트레이드 성사! {target_p['name']} 영입 / {own_p['name']} 이적")
                    st.rerun()
    with release_tab:
        release_id = st.selectbox("방출할 선수", [p["id"] for p in my_roster],
                                  format_func=lambda pid: (lambda p: f"{p['name']} ({p['pos']}, {p['overall']})")(get_player(my_roster, pid)), key="release_player")
        release_player = get_player(my_roster, release_id)
        if st.button("선수 방출", type="primary", disabled=game_active, use_container_width=True):
            hitter_count = sum(1 for p in my_roster if p["role"] == "타자")
            pitcher_count = sum(1 for p in my_roster if p["role"] == "투수")
            if len(my_roster) <= 10:
                st.error("최소 10명의 선수는 유지해야 합니다.")
            elif release_player["role"] == "타자" and hitter_count <= 9:
                st.error("타자는 최소 9명 유지해야 합니다.")
            elif release_player["role"] == "투수" and pitcher_count <= 3:
                st.error("투수는 최소 3명 유지해야 합니다.")
            else:
                league[my_team] = [p for p in my_roster if p["id"] != release_player["id"]]
                st.success(f"{release_player['name']} 선수 방출 완료")
                st.rerun()

with tab_guide:
    st.subheader("게임 설명")
    st.markdown("""
    **경기 화면**  
    야구장 다이아몬드에서 1·2·3루 주자 상황을 확인하고, 타석 프로필과 투수 프로필에서 선수의 주요 능력치를 볼 수 있습니다. 일부 선수는 KBO 공식 프로필 사진을 표시하고, 사진 주소가 확인되지 않은 선수는 구단 색상 프로필 일러스트를 표시합니다.

    **투구**  
    수비에서는 직구·슬라이더·커브·체인지업·포크볼·커터·싱커를 매 구마다 선택할 수 있습니다. `스트라이크 승부`는 존에 들어갈 가능성이 높고, `유인구`는 볼이 될 위험을 감수하고 헛스윙을 노립니다.

    **타격**  
    `컨택 스윙`은 컨택을 높이고 파워를 낮추며, `파워 스윙`은 장타 가능성을 높이는 대신 헛스윙 위험이 커집니다. `기본 스윙`은 균형형입니다. `자동 타격`은 카운트·구종·선수 능력치를 보고 자동으로 스윙하거나 공을 지켜봅니다.

    **결과 계산**  
    타자의 컨택·파워·주력, 투수의 구위·제구·구종, 수비 능력치가 삼진·볼넷·땅볼·뜬공·안타·2루타·3루타·홈런 결과에 반영됩니다. 타구 방향도 좌측·중앙·우측으로 기록됩니다.

    **중요한 안내**  
    선수 이름과 구단은 KBO 선수 정보를 참고한 게임용 명단입니다. 확인된 일부 선수의 사진은 KBO 공식 프로필 이미지 주소를 사용하고, 나머지는 일러스트로 표시합니다. 선수 능력치와 경기 결과 확률은 실제 공식 기록이 아닌 게임 밸런스용 수치입니다.
    """)
    st.markdown("### KBO 참고 사이트")
    st.markdown("- [KBO 선수 등록 현황](https://www.koreabaseball.com/Player/RegisterAll.aspx)")
    st.markdown("- [KBO 구단 소개](https://www.koreabaseball.com/kbo/league/teaminfo.aspx)")
