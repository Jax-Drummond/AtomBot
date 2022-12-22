import disnake as discord
from disnake.ext import commands


class General_Discord_Slash_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, inter: discord.MessageInteraction):
        # This is for the /button_role command
        if inter.component.label == "Get/Remove Role":
            role = inter.guild.get_role(int(inter.component.custom_id))
            await inter.response.defer()
            try:
                if inter.user.get_role(int(inter.component.custom_id)) is None:
                    await inter.user.add_roles(role)
                    await inter.send(f"{role.mention} was Added", ephemeral=True, delete_after=5)
                else:
                    await inter.user.remove_roles(role)
                    await inter.send(f"{role.mention} was Removed", ephemeral=True, delete_after=5)
            except discord.HTTPException:
                await inter.send("There was an error. Please try again in a few minutes.", ephemeral=True,
                                 delete_after=15)

    # Creates the /button_roles command
    # Allows the user to send an embed with a button
    # that when clicked adds or removes a role
    @commands.slash_command(description="Create a button role with Message")
    # Sets the slash command perms to administrator only
    @commands.default_member_permissions(administrator=True)
    async def button_roles(self, inter, role: discord.Role, description: commands.String[0, 200],
                           channel: discord.TextChannel = None):
        embed = discord.Embed(title="Get Role", colour=role.color,
                              description=f"Click on the button below to get the ***{role.mention}*** role.")
        embed.add_field(name="Description", value=description, inline=False)
        if channel is None:
            await inter.response.send_message(embed=embed, components=[
                discord.ui.Button(label="Get/Remove Role", style=discord.ButtonStyle.blurple, custom_id=f"{role.id}")
            ])
        else:
            await channel.send(embed=embed, components=[
                discord.ui.Button(label="Get/Remove Role", style=discord.ButtonStyle.blurple, custom_id=f"{role.id}")
            ])
            await inter.send("Button role successfully created", ephemeral=True, delete_after=2)


def setup(bot):
    bot.add_cog(General_Discord_Slash_Commands(bot))
