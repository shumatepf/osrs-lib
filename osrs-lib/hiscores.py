#! /usr/bin/python

# Author:  shumatepf
# Email:   shumatepfs@gmail.com
# Date:    2023/2/22
# Description:
# HiscoresAPI.py is an API to help process OSRS Hiscores queries.
# Copyright (c) 2023, shumatepf
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math

from bs4 import BeautifulSoup
import asyncio
import aiohttp
import logging

from errors import BadHiScoresPage
import utils


def get_stats(users):
    """
    Get users' stats concurrently
    """
    return asyncio.run(__get_users_sync(users))


def get_usernames(random_ranks):
    """
    Get usernames based on list of ranks from the hiscores html pages concurrently
    """
    return asyncio.run(__get_usernames_sync(random_ranks))


async def __get_users_sync(users):
    """
    Asyncio event loop harness for getting users' stats
    """
    # delay needed if too many requests are made or ip will be temp blocked
    delay = 0 if len(users) < 100 else 4

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, user in enumerate(users):
            tasks.append(asyncio.ensure_future(
                __get_user(session, user, i * delay)))

        user_data = await asyncio.gather(*tasks)
        # remove any empty responses
        user_data_filtered = list(
            filter(lambda item: item is not None, user_data))
        return user_data_filtered


async def __get_user(session, name, delay):
    """
    Get single user's stats coroutine
    """
    await asyncio.sleep(delay)
    url_formatted = utils.URL_API.format(name)

    async with session.get(url_formatted) as user_data:
        if user_data.status == 404:
            logging.warning(f"Username: {name} not found, skipping...")
            return None
        raw_stats = await user_data.text()
        skill_dict = {
            "measurement": "user_skills",
            "tags": {
                "name": name
            },
            "fields": __normalize_stats(raw_stats)
        }
        return skill_dict


def __normalize_stats(stats_raw):
    """
    Stats as space/comma separated values to dict
    """
    ssv = stats_raw.splitlines()
    stats_skills = {skill: int(ssv[i+1].split(',')[2])
                    for i, skill in enumerate(utils.SKILLS)}

    return stats_skills


async def __get_usernames_sync(random_ranks):
    """
    Asyncio event loop harness for getting usernames
    """
    # delay needed if too many requests are made or ip will be temp blocked
    delay = 0 if len(random_ranks) < 100 else 4

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, rank in enumerate(random_ranks):
            tasks.append(asyncio.ensure_future(
                __get_page(session, rank, i * delay)))
        username_list = await asyncio.gather(*tasks)
        return username_list


async def __get_page(session, rank, delay):
    """
    Get single username from hiscores page coroutine
    """
    await asyncio.sleep(delay)

    page_num = math.ceil(rank / 25)
    index = (rank - 1) % 25
    async with session.get(utils.URL_HTML, params={'table': 0, 'page': page_num}, timeout=30) as response:
        # NEED TO CHECK IF PAGE IS IP BLOCKED
        page = await response.text()
        return __get_username_from_page(page, index)


def __get_username_from_page(page, index):
    """
    Parse html page to find user at index
    """
    page_soup = BeautifulSoup(page, "html.parser")
    # if "your IP has been temporarily blocked" in page_soup:
    #         raise RequestFailed("blocked temporarily due to high usage")
    # NEED A TRY CATCH HERE -> Raise exception with page_num, index
    try:
        table = page_soup.find(id='contentHiscores').find(
            "table").find("tbody")
        rows = table.find_all('tr')
        rows.pop(0)  # first row is always empty
        row = rows[index].find("a").text
        name = row.replace("\u00a0", " ")

        return name
    except:
        raise BadHiScoresPage(page_soup)
