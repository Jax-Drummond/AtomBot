import requests
from datetime import datetime, timedelta
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
    total_hours = 0
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

    for day in days_of_the_week:
        current_day = data2[day].capitalize()
        day_shift_time = data2[day + 1]

        try:
            num = 1
            if days_of_the_week.index(day) == 6:
                num = 0

            is_name_not_today = data2.index(name, day) > days_of_the_week[days_of_the_week.index(day) + num]
            tomorrow = days_of_the_week[
                days_of_the_week.index(day) + num]
            today = days_of_the_week[days_of_the_week.index(day)]

            if is_name_not_today and tomorrow != today:
                embed.add_field(name=f"{current_day} - {day_shift_time}\nNo Work", value="", inline=False)
            else:
                for i in range(0, len(data2)):
                    if data2[data2.index(name, day) - i][0].isnumeric():
                        workers = []
                        time = data2[data2.index(name, day) - i]
                        time_index = (data2.index(name, day) - i) + 1
                        split_time = time.split(" - ")
                        split_time = split_time if len(split_time) == 1 else time.split("-")
                        start_time = datetime.strptime(split_time[0], "%H:%M")
                        end_time = datetime.strptime(split_time[1], "%H:%M")
                        if end_time < start_time:
                            end_time += timedelta(hours=12)
                        dif = end_time - start_time
                        shift_hours = dif.total_seconds() / (60 * 60)
                        total_hours += shift_hours

                        for n in range(0, len(data2) - time_index):
                            current_item = data2[time_index + n]
                            is_next_day = current_item == data2[days_of_the_week[days_of_the_week.index(day) + num]]
                            is_work_time = current_item[0].isnumeric()

                            if is_work_time or is_next_day:
                                break

                            if current_item.__contains__('^') or current_item.__contains__(
                                    'change') or current_item.__contains__('update') or current_item == name:
                                continue

                            workers.append(current_item.capitalize())

                        embed.add_field(name=f"{current_day} - {day_shift_time}\n{time}\n{shift_hours} hrs",
                                        value='\n'.join(workers),
                                        inline=False)
                        break
        except ValueError:
            embed.add_field(name=f"{current_day} - {day_shift_time}\nNo Work", value="", inline=False)
    embed.add_field(name=f"Total Hours\n{total_hours}", value="", inline=False)
    return embed
