import requests
from bs4 import BeautifulSoup
import disnake as discord


def work_embed(url: str, name: str):
    name = name.lower()
    # Send a request to the URL and retrieve the HTML content
    response = requests.get(url)
    html = response.text

    # Parse the HTML content
    soup = BeautifulSoup(html, 'html.parser')

    # Find all the rows in the sheet (`<tr>` tags)
    rows = soup.find_all('tr')

    # Create a list to store the data
    data = []

    # Iterate through the rows
    for row in rows:
        # Find all the cells in the row (`<td>` tags)
        cells = row.find_all('td')

        # Create a list to store the cell values
        row_data = []

        # Iterate through the cells and extract the data
        for cell in cells:
            # Add the cell value to the row data list
            row_data.append(cell.text.strip())

        # Add the row data to the data list
        data.append(row_data)

    counter = 0
    data2 = []
    for text in data[4]:
        if text == "Start":
            for i in range(3, len(data)):

                if data[i][counter] != '​' and data[i][counter] != '' and data[i][counter] != 'Start':
                    data2.append(data[i][counter])
                if data[i][counter + 1] != '​' and data[i][counter + 1] != '' and i != 6:
                    data2.append(data[i][counter + 1])

        counter = counter + 1

    data2 = list(map(lambda x: x.lower(), data2))
    days_of_the_week = [data2.index('monday'),
                        data2.index('tuesday'),
                        data2.index('wednesday'),
                        data2.index('thursday'),
                        data2.index('friday'),
                        data2.index('saturday'),
                        data2.index('sunday')]

    embed = discord.Embed(title=f"{name.capitalize()}\n{data[1][2]}", color=discord.Color.orange(), url=url)

    for days in days_of_the_week:
        try:
            num = 1
            if days_of_the_week.index(days) == 6:
                num = 0
            if data2.index(name, days) > days_of_the_week[days_of_the_week.index(days) + num] and days_of_the_week[
                days_of_the_week.index(days) + num] != days_of_the_week[days_of_the_week.index(days)]:
                embed.add_field(name=data2[days].capitalize(), value="No Work", inline=False)
            else:
                for i in range(0, len(data2)):
                    if data2[data2.index(name, days) - i][0].isnumeric():
                        embed.add_field(name=data2[days].capitalize(),
                                        value=data2[data2.index(name, days) - i],
                                        inline=False)
                        break
        except ValueError:
            embed.add_field(name=data2[days].capitalize(), value="No Work", inline=False)

    return embed
