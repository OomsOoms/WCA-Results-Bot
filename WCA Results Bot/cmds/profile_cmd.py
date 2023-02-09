import time
import pandas as pd
import nextcord
import io
from io import BytesIO
from image import make_image

from dataframes import *


def check_string(string):
    # Check if the input is a valid WCA ID
    if len(string) == 10 and string[:4].isdigit() and string[4:8].isalpha() and string[8:].isdigit():
        return (True, "ID")
    # Check if the input is a valid name
    elif len(string.split()) == 2 and string.split()[0].isalpha() and string.split()[1].isalpha():
        return (True, "User not found")
    # Check if the input is an invalid single word name
    elif len(string.split()) == 1 and string.isalpha():
        return (False, "Invalid name")
    # If none of the above conditions are met, the input is invalid
    else:
        return (False, "Invalid")

def init_profile_cmd(bot):
    @bot.slash_command(name="search-profiles", description="Searches")
    async def search_profiles(ctx, id_or_name):
        # Start a timer to track the duration of the search
        start = time.perf_counter()

        # Send a message to the user indicating that the search is in progress
        msg = await ctx.send("Searching...")

        # Capitalize the input if it is a name and keep the original string
        original_string = id_or_name
        if check_string(id_or_name)[1] == "ID":
            id_or_name = id_or_name.upper()
        else:
            id_or_name = id_or_name.title()

        # Find the person's data in the persons dataframe
        person_data = persons_df[persons_df['id'].isin(
            [id_or_name]) | persons_df['name'].isin([id_or_name])]

        # Check if the input is valid and if only one person was found in the dataframe
        if check_string(id_or_name)[0] and len(person_data) == 1:
            # Get the person's ID and name
            person_id = person_data['id'].iloc[0]
            person_name = person_data['name'].iloc[0]

            # Find the person's results data in the results dataframe
            results_data = results_df[results_df['personId'].isin([person_id])]

            # Count the number of unique competitions the person has competed in
            competitions = len(
                results_data[['competitionId', 'personId', 'personName']].drop_duplicates())

            columns = ['value1', 'value2', 'value3', 'value4', 'value5']
            count = 0

            for column in columns:
                count += results_data[~results_data[column]
                                      .isin(['-1', '0', '-2'])][column].size

            # Find the person's average personal best data in the ranksaverage dataframe
            average_data = RanksAverage_df[RanksAverage_df['personId'].isin([
                                                                            person_id])]

            # Find the person's single personal best data in the rankssingle dataframe
            single_data = RanksSingle_df[RanksSingle_df['personId'].isin([
                                                                         person_id])]

            image = make_image(single_data, average_data)

            # Create a BytesIO object
            bytes = BytesIO()
            # Save the image to the BytesIO object in PNG format
            image.save(bytes, format='PNG')
            # Seek to the beginning of the BytesIO object
            bytes.seek(0)
            # Create a File object with the correct data and filename
            dfile = nextcord.File(bytes, filename="image.png")


            embed = nextcord.Embed()
            embed.title = f"{person_name} Profile"
            embed.add_field(name="Country", value=person_data['countryId'].iloc[0], inline=True)
            embed.add_field(name="WCA ID", value=person_id, inline=True)
            embed.add_field(name="Gender", value="Male" if person_data['gender'].iloc[0] == "m" else "Female", inline=True)
            embed.add_field(name="Competitions",value=competitions, inline=True)
            embed.add_field(name="Completed Solves", value=count, inline=True)
            embed.add_field(name="ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ", value="ㅤ", inline=True)

            # Set the file as the image for the embed
            embed.add_field(name="Personal Records", value="ㅤ", inline=False)
            embed.set_image(url='attachment://{}'.format(dfile.filename))

            #embed.add_field(name="Link", value=f"[WCA Profile](https://www.worldcubeassociation.org/persons/{person_id})", inline=False)
            embed.set_footer(text="WCA Profile", icon_url=f"https://www.worldcubeassociation.org/persons/{person_id}")
            #embed.set_footer(text=f"About 3,290,000 results ({format(time.perf_counter()-start, '.2f')} seconds)")

            await msg.edit(embed=embed, file=dfile)
            await msg.edit(f"Search results for '{original_string}'")

        else:
            await msg.edit(check_string(id_or_name)[1])
