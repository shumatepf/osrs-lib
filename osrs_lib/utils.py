# !/usr/bin/python

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


URL_API = "https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player={}"
URL_HTML = "https://secure.runescape.com/m=hiscore_oldschool/overall"

# DO NOT CHANGE ORDER
SKILLS = ["attack", "defense", "strength", "hitpoints", "ranged", "prayer", "magic", "cooking", "woodcutting", "fletching", "fishing", "firemaking",
          "crafting", "smithing", "mining", "herblore", "agility", "thieving", "slayer", "farming", "runecrafting", "hunter", "construction"]
