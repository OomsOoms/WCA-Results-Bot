from PIL import Image, ImageDraw, ImageFont
from functools import reduce
from dataframes import *


def make_image(df1, df2):
    # Select the columns you want to include in the table
    df1 = df1[['eventId', 'best']]
    df2 = df2[['eventId', 'best']]

    # Reset the indexes of the dataframes
    df1 = df1.reset_index(drop=True)
    df2 = df2.reset_index(drop=True)

    # Merge df1 and df2 on the 'eventId' column
    result = reduce(lambda left, right: pd.merge(left, right, on='eventId', how='left'), [df1, df2]).fillna("0000")

    # Create a dictionary mapping event IDs to their respective formats
    event_id_format_map = {row["id"]: row["name"]
                            for i, row in Events_df.iterrows()}

    # Convert all the "eventId" columns in the DataFrame to their respective formats
    for col in result.columns:
        if col.lower() == "eventid":
            result[col] = result[col].apply(
                lambda x: event_id_format_map[x])

    # Convert the values in the 'column' column to the desired format
    result['best_y'] = result['best_y'].astype(int).apply(lambda x: f"{x // 100}.{x % 100:02d}" if x < 6000 else f"{x // 6000}:{x % 6000 // 100}.{x % 100:02d}")
    result['best_x'] = result['best_x'].astype(int).apply(lambda x: f"{x // 100}.{x % 100:02d}" if x < 6000 else f"{x // 6000}:{x % 6000 // 100}.{x % 100:02d}")
    result = result.replace("0.00", "")

    # Convert the dataframes to lists
    data = result.values.tolist()

    # Calculate the number of rows and columns
    rows = len(data)
    columns = 3

    # Calculate the width and height of each cell
    cell_width = 1080 // columns
    cell_height = 100

    # Calculate the total height of the table
    table_height = df1.shape[0] * cell_height

    # Create an image with a white background
    image = Image.new('RGBA', (1080, table_height), (255, 255, 255, 0))

    # Create a drawing object
    draw = ImageDraw.Draw(image)

    # Load a font file and create an ImageFont object
    font = ImageFont.truetype('ggsans-Normal.ttf', 75)

    # Set the padding size
    padding = 10

    # Iterate over the rows and columns
    for i in range(rows):
        for j in range(columns):
            # Calculate the coordinates of the top-left and bottom-right corner of the cell
            x1 = j * cell_width
            y1 = i * cell_height
            x2 = (j+1) * cell_width
            y2 = (i+2) * cell_height

            # Draw the cell border
            draw.rectangle([(x1, y1), (x2, y2)],
                           outline=(255, 255, 255), width=0)

            # Draw the cell contents
            draw.text((x1 + 5, y1 + 5),
                      str(data[i][j]), fill=(255, 255, 255), font=font)

    # image.save("table.png")

    return image






#person_id = "2012PARK03"
## Find the person's average personal best data in the ranksaverage dataframe
#average_data = RanksAverage_df[RanksAverage_df['personId'].isin([
#                                                            person_id])]
#
## Find the person's single personal best data in the rankssingle dataframe
#single_data = RanksSingle_df[RanksSingle_df['personId'].isin([
#                                                            person_id])]
#
#
#start = time.perf_counter()
#make_image(single_data, average_data)
#print(time.perf_counter()-start)





