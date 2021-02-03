import testcanarybot
# kensoi.github.io/testcanarybot/

bot = testcanarybot.app(
    access_token = """:::PASTE:TOKEN:::""",
    group_id = 0
)

mentions = ['павел', 'паша', 'павлик', 'дуров', 'дурашка']
bot.setMentions(mentions) 

# какие слова воспринимает как упоминания, например "паша помощь" 
# с текущими настройками будет считаться командой

bot.setValue("ALL_MESSAGES", True) # Если True, то будет обрабатывать обычные сообщения и отправлять их в void. 
bot.setValue("ADD_MENTIONS", True) # Для упоминаний вашего сообщества
bot.setValue("LISTITEM", "💎") # Специальный значок для списков.

bot.start_polling()