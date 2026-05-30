import telebot

CHAVE_API = "8285282045:AAHa7PSI0UmX5AJz-bIO40GHsMkV2HjcKBc"
bot = telebot.TeleBot(CHAVE_API)

# Insira aqui o ID do seu grupo ou o @ do seu canal público
ID_DESTINO = "@ExemploPIE"


# Esse gatilho captura QUALQUER mensagem de texto enviada para o bot
@bot.message_handler(func=lambda message: True)
def encaminhar_automatico(message):
    # Evita que o bot tente encaminhar mensagens que foram enviadas DENTRO do próprio grupo de destino
    # Se o ID do chat atual for igual ao ID do grupo, o bot não faz nada
    if str(message.chat.id) == str(ID_DESTINO):
        return

    texto_recebido = message.text

    try:
        # Envia o texto direto para o grupo/canal configurado
        bot.send_message(ID_DESTINO, texto_recebido)

        # Dá um feedback amigável no privado do usuário para ele saber que deu certo
        bot.reply_to(
            message, "🚀 Sua mensagem foi enviada para o grupo com sucesso!"
        )

    except Exception as e:
        bot.reply_to(
            message,
            "⚠️ Não consegui enviar sua mensagem para o grupo. Verifique as configurações.",
        )
        print(f"Erro detalhado: {e}")


print("O bot de encaminhamento direto está rodando...")
bot.infinity_polling()