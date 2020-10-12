import random
import vk_api.exceptions
class lib_plugin():
    def __init__(self, api, tools):
        self.v = '0.0032'
        self.descr = 'Модуль для работы с message.action и упоминаниями бота'
        self.mentions = ['video-195675828_456239017', 'video-195675828_456239018']
        self.invite = {
            'message': 'Привет, {user}! Чтобы начать работать со мной, отправь "{mention} помощь"',
            'attachment': ''
        }
        self.kick = {
            'message': 'Пользователь вышел из чата. Исключить: "{mention} исключить {user}"',
            'attachment': ''
        }


    def update(self, api, tools, message):
        if message['text'][0] == tools.mention:
            user = tools.getMention(message['from_id'], 'nom')
            api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message="{user},".format(user = user), attachment=random.choice(self.mentions))
            return 1

        elif message['text'][0] == tools.action:
            if message['text'][1] == 'chat_invite_user':
                user = tools.getMention(message['text'][2], 'nom')
                api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message=self.invite['message'].format(mention = tools.group_mention, user = user), attachment=self.invite['attachment'])
                return 1


            elif message['text'][2] == 'chat_kick_user':
                user = tools.getMention(message['text'][2], 'link')
                api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message=self.kick['message'].format(mention = tools.group_mention, user = user), attachment=self.invite['attachment'])
                return 1

        elif message['text'][0] == tools.payload and type(message['text'][1]) is dict:
            api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message=message['text'][1], attachment=self.invite['attachment'])
            return 1

        elif message['text'][0] in ['kick', 'кик', 'исключить']:
            if message['peer_id'] == message['from_id']:
                user = tools.getMention(message['from_id'], 'nom')
                response = '{user}, невозможно исключать пользователей не в беседе.'

                api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message = response)
            
            elif tools.isChatManager(message['from_id'], message['peer_id']):
                test = message['text'][1:-1]
                test.extend([i['from_id'] for i in message['fwd_messages']])
                if 'reply_message' in message: 
                    test.append(message['reply_message']['from_id'])

                user = tools.getMention(message['from_id'], 'nom')

                if tools.ischecktype(test, int):
                    for i in test:
                        if type(i) is int:
                            try:
                                api.messages.removeChatUser(chat_id = message['peer_id'] - 2000000000, member_id = i)
                                
                            except vk_api.exceptions.VkApiError as e:
                                response = 'Не получилось исключить пользователя: '

                                if tools.isChatManager(i, message['peer_id']):
                                    response += 'у человека есть права в чате.'

                                elif not tools.isMember(i, message['peer_id']):
                                    response += 'пользователя нет в чате.'

                                api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message = response)
                            iskicked = True
                        return 1
            else:
                user = tools.getMention(message['from_id'], 'nom')
                response = '{user}, не получилось исключить пользователей: у вас нет прав.'
                api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message = response)
                return 1