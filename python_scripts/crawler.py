"""
This module is responsible for retrieving data from the clash royale API.
Module is used by db.py to write retrieved data to the database.
"""

import os
from datetime import datetime

import requests
import pandas as pd

from sql import session, Location, Clan, Player, Battle

from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, and_, or_, desc as sa_desc

API_TOKEN = os.environ.get("CLASH_ROYALE_API_TOKEN")
API_URL = "https://api.clashroyale.com/v1"
HEADERS = {"Authorization": "Bearer " + API_TOKEN}


def fetch_locations():
    END_POINT = "/locations"
    try:
        with requests.get(API_URL + END_POINT, headers=HEADERS) as response:
            response.raise_for_status()
            json_data = response.json()
            locations = [(item["id"], item["name"]) for item in json_data["items"]]
            return locations
    except requests.exceptions.RequestException as e:
        print("Error: ", str(e))

def fetch_and_export_cards_as_csv():
    END_POINT = "/cards"
    try:
        response = requests.get(API_URL + END_POINT, headers=HEADERS)
        response.raise_for_status()
        json_data = response.json()

        cards = [{'id': item['id'], 'name': item['name'], 'elixirCost': item.get('elixirCost', None), 'iconUrl': item['iconUrls']['medium']}
                 for item in json_data.get('items', [])]

        support_cards = [{'id': item['id'], 'name': item['name'], 'iconUrl': item['iconUrls']['medium']}
                         for item in json_data.get('supportItems', [])]

        cards_df = pd.DataFrame(cards)
        support_cards_df = pd.DataFrame(support_cards)

        cards_csv_path = "cards.csv"
        support_cards_csv_path = "support_cards.csv"

        cards_df.to_csv(cards_csv_path, index=False)
        support_cards_df.to_csv(support_cards_csv_path, index=False)

        print(f"Cards data exported to {cards_csv_path}")
        print(f"Support cards data exported to {support_cards_csv_path}")

    except requests.exceptions.RequestException as e:
        print("Error: ", str(e))


def add_locations():
    locations = fetch_locations()

    for location_id, name in locations:
        existing_location = session.query(Location).filter_by(location_id=location_id).first()

        if existing_location is None:
            location = Location(location_id=location_id, name=name)
            session.add(location)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()


def fetch_best_clans(location_id):
    END_POINT = "/locations/" + str(location_id) + "/rankings/clans"
    try:
        with requests.get(API_URL + END_POINT, headers=HEADERS) as response:
            response.raise_for_status()
            json_data = response.json()
            clans = [item["tag"] for item in json_data["items"]]
            return clans
    except requests.exceptions.RequestException as e:
        print("Error: ", str(e))


def add_new_clans_for_all_locations():
    all_locations = session.query(Location).all()

    for location in all_locations:
        clans = fetch_best_clans(location.location_id)

        for clan_tag in clans:
            existing_clan = session.query(Clan).filter_by(tag=clan_tag).first()

            if existing_clan is None:
                clan = Clan(tag=clan_tag)
                session.add(clan)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()


def fetch_player_info(player_tag):
    END_POINT = "/players/%23" + player_tag
    try:
        with requests.get(API_URL + END_POINT, headers=HEADERS) as response:
            response.raise_for_status()
            json_data = response.json()
            player_stats = {
                "trophies": json_data['trophies'],
                "bestTrophies": json_data["bestTrophies"],
                "wins": json_data['wins'],
                "losses": json_data['losses'],
                "battleCount": json_data['battleCount']
            }
            return player_stats
    except requests.exceptions.RequestException as e:
        print("Error: ", str(e))


def fetch_clan_members(clan_tag):
    END_POINT = "/clans/%23" + clan_tag[1:] + "/members"
    clan_members = []
    try:
        with requests.get(API_URL + END_POINT, headers=HEADERS) as response:
            response.raise_for_status()
            json_data = response.json()
            clan_members = [item["tag"] for item in json_data["items"]]
            return clan_members
    except requests.exceptions.RequestException as e:
        print("Error: ", str(e))


def add_clan_members():
    clans = session.query(Clan).limit(10).all()

    for clan in clans:
        clan_members = fetch_clan_members(clan.tag)

        for member_tag in clan_members:
            existing_member = session.query(Player).filter_by(tag=member_tag).first()

            if existing_member is None:
                member = Player(tag=member_tag)
                session.add(member)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()


def fetch_player_battles(player_tag):
    END_POINT = "/players/%23" + player_tag + "/battlelog"
    player_battles = []
    try:
        with requests.get(API_URL + END_POINT, headers=HEADERS) as response:
            response.raise_for_status()
            json_data = response.json()
            for battle in json_data:
                battle_data = {}
                battle_data["battle_time"] = battle["battleTime"]
                battle_data["battle_time"] = datetime.strptime(battle_data["battle_time"], "%Y%m%dT%H%M%S.%fZ")
                battle_data["game_mode"] = battle["gameMode"]["name"]
                battle_data["p1_tag"] = player_tag
                p1_stats = fetch_player_info(player_tag)
                battle_data["p1_trophies"] = p1_stats["trophies"]
                battle_data["p1_best_trophies"] = p1_stats["bestTrophies"]
                battle_data["p1_wins"] = p1_stats["wins"]
                battle_data["p1_losses"] = p1_stats["losses"]
                battle_data["p1_battle_count"] = p1_stats["battleCount"]
                battle_data["p1_crowns"] = battle["team"][0]["crowns"]
                battle_data["p1_elixir_leaked"] = battle["team"][0]["elixirLeaked"]
                battle_data["p1_cards"] = battle["team"][0]["cards"]
                battle_data["p1_support_cards"] = battle["team"][0]["supportCards"]

                p2_tag = battle["opponent"][0]["tag"][1:]
                p2_stats = fetch_player_info(p2_tag)
                battle_data["p2_tag"] = p2_tag
                battle_data["p2_trophies"] = p2_stats["trophies"]
                battle_data["p2_best_trophies"] = p2_stats["bestTrophies"]
                battle_data["p2_wins"] = p2_stats["wins"]
                battle_data["p2_losses"] = p2_stats["losses"]
                battle_data["p2_battle_count"] = p2_stats["battleCount"]
                battle_data["p2_crowns"] = battle["opponent"][0]["crowns"]
                battle_data["p2_elixir_leaked"] = battle["opponent"][0]["elixirLeaked"]
                battle_data["p2_cards"] = battle["opponent"][0]["cards"]
                battle_data["p2_support_cards"] = battle["opponent"][0]["supportCards"]

                player_battles.append(battle_data)
            return player_battles
    except requests.exceptions.RequestException as e:
        print("Error: ", str(e))


def add_player_battles(player_tag):
    player_battles = fetch_player_battles(player_tag)

    for battle_data in player_battles:
        existing_battle = session.query(Battle).filter(
            or_(
                and_(Battle.p1_tag == battle_data["p1_tag"], Battle.p2_tag == battle_data["p2_tag"]),
                and_(Battle.p1_tag == battle_data["p2_tag"], Battle.p2_tag == battle_data["p1_tag"])
            )
        ).first()

        if not existing_battle:
            battle = Battle(
                battle_time=battle_data["battle_time"],
                game_mode=battle_data["game_mode"],
                p1_tag=battle_data["p1_tag"],
                p1_trophies=battle_data["p1_trophies"],
                p1_best_trophies=battle_data["p1_best_trophies"],
                p1_wins=battle_data["p1_wins"],
                p1_losses=battle_data["p1_losses"],
                p1_battle_count=battle_data["p1_battle_count"],
                p1_crowns=battle_data["p1_crowns"],
                p1_elixir_leaked=battle_data["p1_elixir_leaked"],
                p1_cards=battle_data["p1_cards"],
                p1_support_cards=battle_data["p1_support_cards"],
                p2_tag=battle_data["p2_tag"],
                p2_trophies=battle_data["p2_trophies"],
                p2_best_trophies=battle_data["p2_best_trophies"],
                p2_wins=battle_data["p2_wins"],
                p2_losses=battle_data["p2_losses"],
                p2_battle_count=battle_data["p2_battle_count"],
                p2_crowns=battle_data["p2_crowns"],
                p2_elixir_leaked=battle_data["p2_elixir_leaked"],
                p2_cards=battle_data["p2_cards"],
                p2_support_cards=battle_data["p2_support_cards"],
            )
            session.add(battle)

            try:
                session.commit()
            except IntegrityError:
                session.rollback()


def add_player_battles_of_n_players(n):
    players = session.query(Player).order_by(Player.last_retrieved)
    for player in players:
        add_player_battles(player.tag[1:])


# add_locations()
# add_new_clans_for_all_locations()
# add_clan_members()


# b = add_player_battles("2P8VLCR0Y")

add_player_battles_of_n_players(10)

# fetch_and_export_cards_as_csv()
