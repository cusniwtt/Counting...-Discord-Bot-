import discord
import os
import requests
import json
import random
from datetime import datetime
from keep_alive import keep_alive

client = discord.Client()

#temp user
user_list = []
testuser = {'wat' : 0, 'ma' : 0, 'nean' : 0}


#keyword
count_word = ['wat', 'ma', 'nean']
kaowpan_word = ['kaowpan', '@kaowpan', 'kaowpun', 'nurse', 'ln', 'looknam', 'dream']


#content random
ma_message = ['ma พ่อมึงดิ', 'ma เหี้ยไรทั้งวัน', 'ma nean', 'ma monai','ma กูไม่ใช่โมไนย']
wat_message = ['wat พ่อมึงดิ', 'wat เหี้ยไรทั้งวัน', 'wat nean', 'wat monai','wat กูไม่ใช่โมไนย']


#API tools
def get_time():
  now = datetime.now()
  timestamp = datetime.timestamp(now)
  dt = datetime.fromtimestamp(timestamp)
  dt = str(dt)
  return dt[:19]

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def check_user(user):
  if (user in user_list):
    return False
  return True


#Loged in check
@client.event
async def on_ready():
  print(get_time() + " | [SYS] | " + "We have logged in as {0.user}".format(client))


#Main event
@client.event
async def on_message(message):

  #for bot will not reply yourself
  if message.author == client.user:
    return

  #Wat message
  if message.content.startswith('wat'):
    await message.channel.send(wat_message[random.randint(0,4)])

  #ma message
  if message.content.startswith('ma'):
    await message.channel.send(ma_message[random.randint(0,4)])

  #nean message
  if message.content.startswith('nean'):
    await message.channel.send('nean x2!')
    #quote = get_quote()
    #await message.channel.send(quote)

  #kaowpan message
  for word in kaowpan_word:
    if message.content.startswith(word):
      await message.channel.send('tour')

  #tour message
  if message.content.startswith('tour'):
    await message.channel.send(kaowpan_word[random.randint(0,6)])

  #bush message
  if message.content.startswith('bush'):
    await message.channel.send('jerry')

  #add user to user list
  if check_user(str(message.author)):
    init = ['wat',0,'ma',0,'nean',0]
    user_list.append(str(message.author))
    user_list.append(init)
    user_index = user_list.index(str(message.author))
    word_index = user_index + 1
    print(get_time() + " | [CRE] | ", end = '')
    print(user_list[user_index], end = ' ')
    print(user_list[word_index])

  #counting func
  for word in count_word:
    if message.content.startswith(word):
      if not check_user(str(message.author)):
        user_index = user_list.index(str(message.author))
        word_index = user_index + 1
        if word == 'wat':
          key_index = 1
        elif word == 'ma':
          key_index = 3
        elif word == 'nean':
          key_index = 5
        user_list[word_index][key_index] +=1
        print(get_time() + " | [UPD] | ", end = '')
        print(user_list[user_index], end = ' ')
        print(user_list[word_index])

  #Notify Func
  for word in count_word:
    if message.content.startswith(word):
      if (str(message.author) in user_list):
        key_index = [1,3,5]
        for i in key_index:
          #Check not reply if 0 word
          if user_list[word_index][i] == 0:
            pass
          #Check reply lower 100
          elif user_list[word_index][i] <= 100:
            modV = user_list[word_index][i] % 10
            if modV == 0:
              await message.channel.send("เก่งมากไอเหี้ย มึงพิม '{}' มา '{}' ครั้งละ".format(user_list[word_index][i-1], user_list[word_index][i]))
          #Check reply lower 500
          elif user_list[word_index][i] <= 500:
            modV = user_list[word_index][i] % 50
            if modV == 0:
              await message.channel.send("เก่งมากไอเหี้ย มึงพิม '{}' มา '{}' ครั้งละ".format(user_list[word_index][i-1], user_list[word_index][i]))
          #Check reply lower 1000
          elif user_list[word_index][i] <= 1000:
            modV = user_list[word_index][i] % 100
            if modV == 0:
              await message.channel.send("เก่งมากไอเหี้ย มึงพิม '{}' มา '{}' ครั้งละ".format(user_list[word_index][i-1], user_list[word_index][i]))

  #Command recent word
  if message.content.startswith('-now'):
    user_index = user_list.index(str(message.author))
    word_index = user_index + 1
    await message.channel.send("{} {}".format(user_list[user_index],user_list[word_index]))


#Call Function
keep_alive()
client.run(os.getenv('TOKEN'))