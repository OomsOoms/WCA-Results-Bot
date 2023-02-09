import time
import pandas as pd
import nextcord

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

def testrr(bot):
    # Define the `search_profiles` function as a command for the bot
    @bot.slash_command(name="testr", description="Searches for user profiles")
    async def testr(ctx, id_or_name):
        # Start a timer to track the duration of the search
        start = time.perf_counter()

        # Send a message to the user indicating that the search is in progress
        msg = await ctx.send("Searching...")
        columns = ['value1', 'value2', 'value3', 'value4', 'value5']

        # Check if the input is a valid WCA ID or name
        is_valid, result_type = check_string(id_or_name)
        if not is_valid:
            # If the input is invalid, send an error message to the user and return
            await ctx.send(f"Invalid input: {result_type}")
            return

        # Capitalize the input if it is a name and keep the original string
        original_string = id_or_name
        if result_type == "ID":
            id_or_name = id_or_name.upper()
        else:
            id_or_name = id_or_name.title()

        # Find the person's data in the persons dataframe
        person_data = persons_df[
            persons_df['id'].isin([id_or_name]) |
            persons_df['name'].isin([id_or_name])
        ]

        # Check if the input is valid and if only one person was found in the dataframe
        if len(person_data) != 1:
            # If the input is valid but no person was found or more than one person was found,
            # send an error message to the user and return
            await ctx.send(f"{result_type} not found")
            return

        # Get the person's ID and name
        person_id = person_data['id'].iloc[0]
        person_name = person_data['name'].iloc[0]

        # Find the person's results data in the results dataframe
        results_data = results_df[results_df['personId'].isin([person_id])]

        # Count the number of unique competitions the person has competed in
        competitions = len(
            results_data[['competitionId', 'personId', 'personName']].drop_duplicates()
        )

        # Count the number of personal best results the person has achieved
        pb_count = results_data[~results_data[columns].isin(['-1', '0', '-2'])][columns].size

        # Find the person's average personal best data in the ranksaverage dataframe
        average_data = RanksAverage_df[RanksAverage_df['personId'].isin([person_id])]
        
        # Find the person's single personal best data in the rankssingle dataframe
        single_data = RanksSingle_df[RanksSingle_df['personId'].isin([person_id])]

        # Create a dictionary mapping event IDs to their respective formats
        event_id_format_map = {row["id"]: row["name"] for i, row in Events_df.iterrows()}

        # Convert all the "eventId" columns in the DataFrame to their respective formats
        for col in single_data.columns:
            if col.lower() == "eventid":
                single_data[col] = single_data[col].apply(lambda x: event_id_format_map[x])

        # Create an embed object to display the user's profile information
        embed = nextcord.Embed()
        embed.title = f"{person_name} Profile"

        # Add fields to the embed object with the user's information
        embed.add_field(name="Country", value=person_data['countryId'].iloc[0], inline=True)
        embed.add_field(name="WCA ID", value=person_id, inline=True)
        embed.add_field(name="Competitions", value=competitions, inline=True)
        embed.add_field(name="Personal Bests", value=pb_count, inline=True)

        # Add a field for each event containing the user's single personal best time
        for i, row in single_data.iterrows():
            event_name = row["eventId"]
            best_time = row["best"]
           
            embed.add_field(name=event_name, value=best_time, inline=True)

        # Send the embed object to the user as a message
        await ctx.send(embed=embed)

        # Calculate and print the elapsed time for the search
        elapsed_time = time.perf_counter() - start
        print(f"Search took {elapsed_time:.2f} seconds.")
