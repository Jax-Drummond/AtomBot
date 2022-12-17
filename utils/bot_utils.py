import os


# Gets all python files in the cogs directory and loads them as extensions
def load_cogs(bot):
    cog_dir = "cogs"

    for obj in os.walk("cogs"):
        files = filter(lambda f: f.endswith('.py'), obj[-1])
        for file in files:
            filename, _ = os.path.splitext(file)
            cog_filepath = os.path.join(cog_dir, filename).replace('\\', '.').replace("/", '.')
            bot.load_extension(cog_filepath)
