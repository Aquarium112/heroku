from asyncio import sleep
import discord, datetime, time
from discord.ext import commands
import discord
import json


def has_rights():
    def predicate(ctx):
        return ctx.author.guild_permissions.kick_members

    return commands.check(predicate)


class KnastCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='knast')
    @has_rights()
    @commands.has_any_role(829727147677188115)
    async def knast(self, ctx, member: discord.Member):
        await ctx.message.delete()
        config = self.bot.config
        roleid = config['knast_roleId']
        if ctx.guild.get_role(roleid) in member.roles:
            await member.remove_roles(ctx.guild.get_role(roleid))
            users = self.bot.users
            if users[f'{member.id}']:
                roles = users[f'{member.id}']
                blacklisted = config['blacklisted_roles']
                for roleid in roles:
                    if roleid not in blacklisted:
                        await member.add_roles(ctx.guild.get_role(roleid))
                await ctx.send(f'Der User {member.display_name} wurde entknasted!')
                del users[f'{member.id}']
                self.bot.users = users
                with open(f'{self.bot.config_path}/users.json', 'w') as f:
                    json.dump(users, f, indent=4)
            else:
                await ctx.send(f'{member.display_name} ist nicht in der Knastconfig.')
        else:
            users = self.bot.users
            memb_roles = []
            for role in member.roles[1:]:
                memb_roles.append(role.id)
                await member.remove_roles(role)
            users[f'{member.id}'] = memb_roles
            self.bot.users = users
            with open(f'{self.bot.config_path}/users.json', 'w') as f:
                json.dump(users, f, indent=4)

            await member.add_roles(ctx.guild.get_role(roleid))
            await ctx.send(f'Der User {member.display_name} Wurde geknastet!')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await sleep(5)
        users = self.bot.users
        if users[f'{member.id}']:
            for role in member.roles[1:]:
                await member.remove_roles(role)
            config = self.bot.config
            roleid = config['knast_roleId']
            await member.add_roles(member.guild.get_role(827540941728251926))

    @commands.command()
    async def hilfe(self, ctx):
        embed = discord.Embed(title="Help commands", color=discord.Color.random())
        embed.add_field(name="`.knast (user mention)`\n**Knaste ein user**\n=--------------=\n`.knast (user id)`\n**Entknaste einen user**.",value="Lade mich [Hier](https://discord.ly/globaldestroyer) Ein")
        await ctx.send(embed=embed)
    
    @commands.command(pass_context=True)
    async def uptime(self, ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(colour=0xc8dc6c)
        embed.add_field(name="Uptime", value=text)
        embed.set_footer(text="<Destroyer Support>")
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send("Bot uptime: " + text)
#######################################################


def setup(bot):
    bot.add_cog(KnastCommand(bot))
