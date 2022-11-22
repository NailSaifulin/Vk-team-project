import os
import configparser

config = configparser.ConfigParser()
configpath = "config_bot.cfg"


def startup():
    """Функция запуска и первоначальной настройки программы"""
    if os.path.exists(configpath):
        from vkinder_bot.bot import run_bot
        run_bot()
        return "[INFO]  Bot launched"
    else:
        config.add_section("TOKEN")
        add_token = input("[SET]Введите токен сообщества - ")
        config.set("TOKEN", "vk_token", add_token)
        add_user_token = input("[SET]Введите токен служебной страницы (https://vkhost.github.io/) - ")
        config.set("TOKEN", "vk_user_token", add_user_token)

        config.add_section("DATABASE")
        user_data = input("[SET] Введите имя пользователя базы данных - ")
        config.set("DATABASE", "db_user", user_data)
        password_data = input("[SET] Введите пароль пользователя базы данных - ")
        config.set("DATABASE", "db_password", password_data)
        host_data = input("[SET] Введите хост базы данных - ")
        config.set("DATABASE", "db_host", host_data)

        with open(configpath, "w") as config_file:
            config.write(config_file)


if __name__ == '__main__':
    startup()
