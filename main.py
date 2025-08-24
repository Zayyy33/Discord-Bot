import discord
from discord.ext import commands
from discord import app_commands
import datetime
from sympy import sympify, simplify
import os

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True  # cek role

bot = commands.Bot(command_prefix='!', intents=intents)

CHANNEL_ID = 1385633782521921536
izin = "probset"  # Role yang diizinkan
data = {
    "materi": None,
    "spesifik": None,
    "difficulty": None,
    "probset": None,
    "image": None,
    "jawaban_benar": None
}


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Bot {bot.user} siap!')


@bot.command(name="problem")
async def tampilkan_soal(ctx):
    # Cek role user
    if any(role.name.lower() == izin.lower() for role in ctx.author.roles):
        channel = bot.get_channel(CHANNEL_ID)
        today = datetime.datetime.now().strftime("%d %B %Y")

        embed = discord.Embed(title=f"Problem 🔍 - {today}",
                              description=f'Materi : {data["materi"]}\n'
                              f'Spesifik : {data["spesifik"]}\n'
                              f'Difficulty : {data["difficulty"]}\n'
                              f'Probset : {data["probset"]}',
                              color=discord.Color.yellow())
        embed.set_image(url=f'{data["image"]}')

        await channel.send(embed=embed)
        await ctx.send(":grey_question: Ketik ``/answer`` untuk menjawab \n"
                       ":exclamation: Jawaban hanya berbentuk angka!")
    else:
        await ctx.send("❌ kamu gk punya akses njir.")


@bot.tree.command(name="answer", description="Jawaban untuk soal terakhir")
@app_commands.describe(jawaban="Masukkan jawaban anda disini")
async def answer(interaction: discord.Interaction, jawaban: str):
    try:
        # Agar spasi tidak dianggap
        jawaban = jawaban.lower().replace(" ", "")

        # Evaluasi ekspresi matematika user
        ekspresi_user = simplify(sympify(jawaban))

        if ekspresi_user == data["jawaban_benar"]:
            await interaction.response.send_message("✅ Jawabanmu benar!",
                                                    ephemeral=True)
            await interaction.channel.send(
                f":dart: {interaction.user.mention} berhasil menjawab soal!")
        else:
            await interaction.response.send_message("❌ Jawabanmu salah.",
                                                    ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(
            "⚠️ Jawaban tidak dapat diproses.", ephemeral=True)


@bot.command(name="info")
async def info(ctx):
    channel = bot.get_channel(CHANNEL_ID)
    info = discord.Embed(
        title=f":question: Info :question:",
        description="Bot masih perlu di update :tools:\n\n"
        "``!problem`` : Untuk memberikan soal-soal terkini (p)\n"
        "``/answer`` : Untuk menjawab pertanyaan/soal-soal\n"
        "``/set ...`` : Untuk mengatur soal-soal (p)\n"
        "``/set mat`` : Untuk mengatur materi (p)\n"
        "``/set spes`` : Untuk mengatur spesifik materi (p)\n"
        "``/set diff`` : Untuk mengatur difficulty (p)\n"
        "``/set prob`` : Untuk mengatur probset (p)\n"
        "``/set img`` : Untuk mengatur gambar soal (p)\n"
        "``/set jwb`` : Untuk mengatur jawaban materi (p)\n\n"
        "note --> (p) artinya command tersebut hanya bisa diakses oleh probset",
        color=discord.Color.purple())
    await ctx.send(embed=info)

@bot.command(name="test")
async def test(ctx):
    pesan = await ctx.send("Tes Emoji :D")
    # Bot menambahkan reaction
    await pesan.add_reaction("👍")
    await pesan.add_reaction("👎")

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:  # Supaya bot tidak membaca reactionnya sendiri
        return
    
    if reaction.emoji == "👍":
        await reaction.message.channel.send(f"{user.name} 👍")
    elif reaction.emoji == "👎":
        await reaction.message.channel.send(f"{user.name} 👎")


class SetGroup(app_commands.Group):

    def __init__(self):
        super().__init__(name="set",
                         description="Atur soal dan informasi lainnya")

    @app_commands.command(name="mat",
                          description="Masukkan materi soal yang dimaksud")
    async def set_materi(self, interaction: discord.Interaction, mat: str):
        if not any(role.name.lower() == izin.lower()
                   for role in interaction.user.roles):
            await interaction.response.send_message(
                "❌ Kamu gk punya akses untuk menggunakan command ``/set``.",
                ephemeral=True)
            return
        data["materi"] = mat
        await interaction.response.send_message(
            f":wrench: Materi soal telah diatur menjadi **{mat}**",
            ephemeral=True)

    @app_commands.command(
        name="spes",
        description="Masukkan lebih spesifik tentang materi dalam soal")
    async def set_spesifik(self, interaction: discord.Interaction, spes: str):
        if not any(role.name.lower() == izin.lower()
                   for role in interaction.user.roles):
            await interaction.response.send_message(
                "❌ Kamu gk punya akses untuk menggunakan command ``/set``.",
                ephemeral=True)
            return
        data["spesifik"] = spes
        await interaction.response.send_message(
            f":wrench: Materi soal telah diatur menjadi **{spes}**",
            ephemeral=True)

    @app_commands.command(name="diff",
                          description="Masukkan tingkat kesulitan soal")
    async def set_difficulty(self, interaction: discord.Interaction,
                             diff: str):
        if not any(role.name.lower() == izin.lower()
                   for role in interaction.user.roles):
            await interaction.response.send_message(
                "❌ Kamu gk punya akses untuk menggunakan command ``/set``.",
                ephemeral=True)
            return
        data["difficulty"] = diff
        await interaction.response.send_message(
            f":wrench: Tingkat kesulitan soal telah diatur menjadi **{diff}**",
            ephemeral=True)

    @app_commands.command(name="prob",
                          description="Masukkan nama/username probset")
    async def set_probset(self, interaction: discord.Interaction, prob: str):
        if not any(role.name.lower() == izin.lower()
                   for role in interaction.user.roles):
            await interaction.response.send_message(
                "❌ Kamu gk punya akses untuk menggunakan command ``/set``.",
                ephemeral=True)
            return
        data["probset"] = prob
        await interaction.response.send_message(
            f":wrench: Probset telah diatur menjadi **{prob}**",
            ephemeral=True)

    @app_commands.command(name="img",
                          description="Masukkan link/url gambar soal")
    async def set_image(self, interaction: discord.Interaction, img: str):
        if not any(role.name.lower() == izin.lower()
                   for role in interaction.user.roles):
            await interaction.response.send_message(
                "❌ Kamu gk punya akses untuk menggunakan command ``/set``.",
                ephemeral=True)
            return
        data["image"] = img
        await interaction.response.send_message(
            f":wrench: Gambar soal telah diatur menjadi \n {img}",
            ephemeral=True)

    @app_commands.command(name="jwb",
                          description="Masukkan jawaban benar dari soal")
    async def set_jawaban(self, interaction: discord.Interaction, jwb: int):
        if not any(role.name.lower() == izin.lower()
                   for role in interaction.user.roles):
            await interaction.response.send_message(
                "❌ Kamu gk punya akses untuk menggunakan command ``/set``.",
                ephemeral=True)
            return
        data["jawaban_benar"] = jwb
        await interaction.response.send_message(
            f":wrench: Jawaban soal telah diatur menjadi **{jwb}**",
            ephemeral=True)
        

bot.tree.add_command(SetGroup())  # Command untuk slash ``/set ...``
bot.run(os.getenv("TOKEN"))
