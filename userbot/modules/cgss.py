# Copyright 2020, Dicky Herlambang "Nicklas373" <herlambangdicky5@gmail.com>
# Copyright 2016-2020, HANA-CI Build Project
# SPDX-License-Identifier: GPL-3.0-or-later
# This module based on https://github.com/Nicklas373/CGSS_ACB_Downloader that only
# have minimal function to track DB manifest version and report to user.

import requests
import json

from userbot import CMD_HELP
from userbot.events import register

@register(outgoing=True, pattern=r"^\.cgss (.*)")
async def get_cgss(cgss):

    version=None
    verbose=True

    await cgss.edit("Loading...")

    if not version:
        if verbose:
            try:
                await cgss.edit("Getting game version ...")
                url="https://starlight.kirara.ca/api/v1/info"
                r=requests.get(url)
                jsonData=json.loads(r.content)
                version=jsonData['truth_version']
            except Exception as e:
                await cgss.edit("No DB service was available!...")
                version="NULL"
            else:
                await cgss.edit("Getting game version from esterTion source...")
                url="https://raw.githubusercontent.com/esterTion/cgss_master_db_diff/master/!TruthVersion.txt"
                r=requests.get(url)
                version=r.text.rstrip()

            await cgss.edit("Getting game version from local repository...")
            url="https://raw.githubusercontent.com/Nicklas373/CGSS_ACB_Downloader/master/Static_version"
            r=requests.get(url)
            old_version=r.text.rstrip()

            if (version > old_version):
                reason="Local DB older than Dynamic DB!"
            elif (version == old_version):
                reason="Local DB on latest version!"
            elif (version < old_version):
                reason="Local DB higher than Dynamic DB, ERROR"

            result=(
                    f"**CGSS DB Manifest Ver.**\n"
                    f"\n"
                    f"**Local DB Ver.** : `{old_version}`\n"
                    f"**Online DB Ver.** : `{version}`\n"
                    f"**Status** : `{reason}`\n"
                    f"\n"
                    )
            await cgss.edit(result)

CMD_HELP.update(
        {
                "cgss": ">`.cgss` **start**\
                \nUsage: Get information for DB version on CGSS."
        }
)
