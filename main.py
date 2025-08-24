import discord
from discord.ext import commands
from discord import app_commands
import datetime
from sympy import sympify, simplify
import os
import random

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True  # cek role
intents.reactions = True

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

integral_mudah = ["https://cdn.discordapp.com/attachments/1352395370340024430/1409035210913218662/1324375942554058772.png?ex=68abe9cc&is=68aa984c&hm=7517a369522467c00bbb56be528080510e564cb7265e5329e989ef66f7e36930&", 
             "https://media.discordapp.net/attachments/1352395370340024430/1409038955630039131/1324375942554058772.png?ex=68abed49&is=68aa9bc9&hm=3a1c6c3b9b6d3e8f7aa377e5c72ae8b03ceda69cebab2d03e60a9a83b35cd368&=&format=webp&quality=lossless"]

integral_sedang = ["https://media.discordapp.net/attachments/1352395370340024430/1409039720293335161/1324375942554058772.png?ex=68abee00&is=68aa9c80&hm=27a9744815b4adbb038c1dbe39c30a59877d5dfce156aff0ba77927f7f93d0e5&=&format=webp&quality=lossless", 
                  "https://media.discordapp.net/attachments/1352395370340024430/1409043596614565969/1324375942554058772.png?ex=68abf19c&is=68aaa01c&hm=307355269f716d5465fcb5fd25d80786c3bd7d88edd45b4616e05025dd465154&=&format=webp&quality=lossless"]

integral_susah = ["https://media.discordapp.net/attachments/1352395370340024430/1409044687834189844/1324375942554058772.png?ex=68abf2a0&is=68aaa120&hm=6c2c7fade469ec5604cc0b256d4a06691d7c2828b85b1d7258a4927e432466b2&=&format=webp&quality=lossless", 
                 "https://media.discordapp.net/attachments/1352395370340024430/1409045801635942440/1324375942554058772.png?ex=68abf3a9&is=68aaa229&hm=292816a8766e797b9ce5cb964414affd69f3ecd16e1bf18778a44c41609eb9ab&=&format=webp&quality=lossless"]
emoji_level = {
    "🟢": integral_mudah,
    "🟡": integral_sedang,
    "🔴": integral_susah   
}

@bot.command(name="int")
async def soal(ctx):
    embed = discord.Embed(
        title="📘 Pilih Level Integral",
        description="Berikut adalah daftar level soal integral diambil dari banyak sumber:\n\n🟢 Mudah\n🟡 Sedang\n🔴 Susah",
        color=discord.Color.orange()
    )
    pesan = await ctx.send(embed=embed)
    
    for e in emoji_level.keys(): # Tambahkan reaction
        await pesan.add_reaction(e)

    bot.soal_message_id = pesan.id # Simpan pesan ini supaya bisa dicek di on_reaction_add
    bot.soal_user_id = ctx.author.id

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    # pastikan reaction di pesan soal
    if reaction.message.id == getattr(bot, "soal_message_id", None):
        if user.id != getattr(bot, "soal_user_id", None):
            return  # hanya user yang panggil !soal yang bisa pilih

        if reaction.emoji in emoji_level:
            # ambil soal random dari list sesuai level
            soal = random.choice(emoji_level[reaction.emoji])
            await ctx.send(soal)

            # hapus pesan embed pilihan level
            await reaction.message.delete()


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
