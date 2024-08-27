import notify2


notify2.init("Bot para Facebook")


def show_message(msg_body: str):
    notificacao = notify2.Notification(
        "Mensagem de Alerta",
        msg_body,
        "notification-message-im",
    )

    notificacao.show()
