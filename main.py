import re
import telebot

# Insira aqui o ID do seu grupo ou o @ do seu canal público
ID_CANAL = "@ExemploPIE"
CHAVE_API = "8285282045:AAHa7PSI0UmX5AJz-bIO40GHsMkV2HjcKBc"
search_strings = ['suspeita', 'invadindo', 'roubo' , 'Roubo' ,'ROUBO' , 'roubando', 'roubado']
bot = telebot.TeleBot(CHAVE_API)
Contatos = {}

#funcao para validar se o contato ja se cadastrou
def validar(message):
    if (message.from_user.id not in Contatos) :
        print("FLUXO: cadastro")
        # Pede o endereço e registra no next_step_handler...
        Contatos[message.from_user.id] = {
            "status": -1,
            "mensagem_pendente": message.text
        }

        bot.reply_to(
            message,
            "Olá! Identifiquei que este é o seu primeiro contato.\n"
            "Já vou enviar seu alerta preciso apenas que me informe seu endereço para vincular a mensagem e realiazar seu cadastro.\n"
            "Peço que responda essa mensagem apenas com o nome da sua rua."
        )
        return -1
    if Contatos[message.from_user.id].get("status") == -1:
        print(f"FLUXO: Salvando endereço")

        Contatos[message.from_user.id]["status"] = 1
        Contatos[message.from_user.id]["Adress"] = message.text

        bot.reply_to(message, "✅ Cadastro realizado com sucesso! Analisando o seu alerta...")
        enviar_alerta(Contatos[message.from_user.id].get("mensagem_pendente"), message)
        return 2

    return 1

#funcao para filtrar a mensagem
def filtrar_string(msg_ctt):

    print("Searching for:", search_strings)
    # Create pattern: 'Python|data|Java'
    pattern = '|'.join(search_strings)
    matches = re.findall(pattern, msg_ctt.lower())

    if matches:
        print(f"Found: {matches}")
        return matches
    else:
        print("No matches found")
        return []

#Funcao para escolher o tipo de ocorrencia com base na mensagem filtrada
def enviar_alerta(msg_ctt,message):
    for i in filtrar_string(msg_ctt):
        match i:
            case 'roubo' | 'Roubo' | 'ROUBO' | 'roubando' | 'roubado':
                print("Suspeita roubo")
                try:

                    bot.send_message(ID_CANAL, (
                                "Suspeita de roubo no endereço: " + Contatos[message.from_user.id].get("Adress") + " Descrição do relato: " + msg_ctt))

                    bot.reply_to(
                        message, "🚀 Sua mensagem foi enviada para o grupo com sucesso!"
                    )

                except Exception as e:
                    bot.reply_to(
                        message,
                        "⚠️ Não consegui enviar sua mensagem para o grupo. Verifique as configurações.",
                    )
                    print(f"Erro detalhado: {e}")
            case -1:
                bot.reply_to(
                    message,
                    "⚠️ Não consegui entender sua mensagem, tente utilizar termos mais claros sobre o relato. Como por exemplo: Roubo, Invasão, Furto, Vandalismo...",
                )
                print("Nao foi localizada nenhuma palavra chave")

# Esse gatilho captura QUALQUER mensagem de texto enviada para o bot
@bot.message_handler(func=lambda message: True)
def ouvir_msg(message):
    if str(message.chat.id) == str(ID_CANAL):
        return
    else:
        if (validar(message)== 1):
            enviar_alerta(message.text,message)


def  main():
    bot.infinity_polling()
main()