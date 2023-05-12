from pyrogram import Client , filters , enums
from pyromod import listen
import random , time , datetime ,pytz
from pyromod.helpers import ikb, kb, array_chunk
from pyrogram.types import Message
from subprocess import call
import sqlite3

Bot = Client("Mee"  , "Api Id" , "Api Hash" , bot_token="توکن ربات")
Botid = "Fdfdjgfati64bot"
Admin = "آیدی عددی ادمین"
conn = sqlite3.connect('Files.db')
Database = conn.cursor()
Database.execute("""CREATE TABLE IF NOT EXISTS Uploaded_File(
    userid INT PRIMARY KEY,
    Fileunique TEXT UNIQUE,
    File_ID TEXT UNIQUE)""")
Database.execute("""CREATE TABLE IF NOT EXISTS Users(
    userid INT PRIMARY KEY Not NULL)""")
conn.commit()


StartKb = kb([ 
      ["📊 آمار ربات" , "آپلود"],
      ["ارسال همگانی"]],
      resize_keyboard=True)

@Bot.on_message(filters.private & filters.command("Start" , "/"))
async def Start(Client , m:Message):
    Userid = (m.from_user.id,)
    try :
        Database.execute("""INSERT INTO Users(userid) VALUES(?);""" , Userid)
        conn.commit()
    except:pass
    try:
        Unique = m.command[1]
        Database.execute("SELECT File_ID FROM Uploaded_File WHERE Fileunique=?;", (Unique,)) 
        File_ID = Database.fetchall()
        File = str(File_ID[0]).removeprefix("('").removesuffix("',)")
        Sendned_Message = await Bot.send_cached_media(m.chat.id ,File )
        await m.reply("مدیای ارسالی تا 20 ثانیه دیگر حذف میشود. \nلطفا در مناسب آنرا ذخیره کنید.")
        time.sleep(20)
        await Bot.delete_messages(m.chat.id , Sendned_Message.id)
    except:
        if m.from_user.id == Admin:
            await m.reply("سلام به آپلودر خوش آمدید " , reply_markup=StartKb)
    
@Bot.on_message(filters.user(Admin) & filters.command("📊 آمار ربات" , ""))
async def Amar(Client , m:Message):
    Database.execute("SELECT COUNT(File_ID) FROM Uploaded_File;") 
    C = Database.fetchall()
    FileCount = str(C).removeprefix("[(").removesuffix(",)]")
    S = datetime.datetime.now()
    E = (datetime.datetime.now() - S).total_seconds()
    Database.execute("SELECT COUNT(userid) FROM Users")
    C = Database.fetchall()
    MembersCount = str(C).removeprefix("[(").removesuffix(",)]")
    Roz =f"🗓 {datetime.datetime.now(pytz.timezone('Asia/Tehran')).year}/{datetime.datetime.now(pytz.timezone('Asia/Tehran')).month}/{datetime.datetime.now(pytz.timezone('Asia/Tehran')).day} ⏰ {datetime.datetime.now(pytz.timezone('Asia/Tehran')).hour}:{datetime.datetime.now(pytz.timezone('Asia/Tehran')).minute}"
    await m.reply(f"""╗  🤖  آمار ربات @{Botid}      ╔
║
╣ 👥 کل کاربران: {MembersCount} نفر
║ 
╣ 🎛 پینگ و لود سرور : 
╣ 📂 تعداد فایل ها: {FileCount}
║ ‏
{Roz}""")

@Bot.on_message(filters.user(Admin) & filters.command("ارسال همگانی"  , ""))
async def SendToAll(Client , m:Message):
    message = await m.chat.ask("لطفا پیام مورد نظر خود را ارسال کنید")
    Database.execute("SELECT (userid) FROM Users")
    C = Database.fetchall()
    Count = 0
    for X in C :
        try:
            await Bot.copy_message(X[0] , message.chat.id , message.id)
            Count =+1
            time.sleep(1)
        except: pass
    await m.reply(f"پیام شما با موفقیت به {Count} کاربر ارسال شد")
@Bot.on_message(filters.private & filters.command("آپلود" , ""))
async def UploadFile(Client , m:Message):
    File = await m.chat.ask("لطفا فایل خود را ارسال کنید")
    if File.media :
        if File.media == enums.MessageMediaType.AUDIO:
            Link = File.audio.file_unique_id 
            Value = (f"{Link}" , f"{File.audio.file_id}")
            try:
                Database.execute("INSERT INTO Uploaded_File(Fileunique,File_ID) VALUES(?,?);" , Value)
            except:pass
            await m.reply(f"لینک شما \n https://telegram.me/{Botid}?start={Link}")
            conn.commit()
        if File.media == enums.MessageMediaType.PHOTO:
            Link = File.photo.file_unique_id 
            Value = (f"{Link}" , f"{File.photo.file_id}")
            try:
                Database.execute("INSERT INTO Uploaded_File(Fileunique,File_ID) VALUES(?,?);" , Value)
            except:pass
            await m.reply(f"لینک شما \n https://telegram.me/{Botid}?start={Link}")
            conn.commit()
        if File.media == enums.MessageMediaType.VIDEO:
            Link = File.video.file_unique_id 
            Value = (f"{Link}" , f"{File.video.file_id}")
            try:
                Database.execute("INSERT INTO Uploaded_File(Fileunique,File_ID) VALUES(?,?);" , Value)
            except:pass            
            await m.reply(f"لینک شما \n https://telegram.me/{Botid}?start={Link}")
            conn.commit()
        if File.media == enums.MessageMediaType.DOCUMENT:
            Link = File.document.file_unique_id 
            Value = (f"{Link}" , f"{File.document.file_id}")
            try:
                Database.execute("INSERT INTO Uploaded_File(Fileunique,File_ID) VALUES(?,?);" , Value)
            except:pass
            await m.reply(f"لینک شما \n https://telegram.me/{Botid}?start={Link}")
            conn.commit()


Bot.run()