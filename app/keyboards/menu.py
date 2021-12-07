from aiogram.utils.callback_data import CallbackData

from app.utils.markup_constructor import InlineMarkupConstructor


class MenuKb(InlineMarkupConstructor):
    callback_data = CallbackData("MENU", "action")
    start_test_callback = CallbackData("BEGIN_TEST", "test_id")

    def main(self, gettext, lang=None):
        schema = [1, 1, 1, 1]
        actions = [
            {"text": gettext("Узнать больше о LocalTrade", locale=lang),
             "cb": self.callback_data.new("LOCALTRADE_INFO")},
            {"text": gettext("Доступные тесты", locale=lang), "cb": self.callback_data.new("AVAILABLE_TESTS")},
            {"text": gettext("Пройденные тесты", locale=lang), "cb": self.callback_data.new("FINISHED_TESTS")},
            {"text": gettext("Сменить язык", locale=lang), "cb": self.callback_data.new("CHANGE_LANGUAGE")}
        ]
        return self.markup(actions, schema)

    def back_to_menu(self, gettext):
        schema = [1]
        actions = [
            {"text": gettext("Вернуться назад"), "cb": self.callback_data.new("BACK_TO_MENU")}
        ]
        return self.markup(actions, schema)

    def after_quiz(self, gettext):
        schema = [1, 1]
        actions = [
            {"text": gettext("Главное меню"), "cb": self.callback_data.new("BACK_TO_MENU")},
            {"text": gettext("Пройти другой тест"), "cb": self.callback_data.new("AVAILABLE_TESTS")}
        ]
        return self.markup(actions, schema)

    def start_test(self, test_id: int, gettext):
        schema = [1, 1]
        actions = [
            {"text": gettext("Начать тест"), "cb": self.start_test_callback.new(test_id=test_id)},
            {"text": gettext("Закрыть тест"), "cb": self.callback_data.new("AVAILABLE_TESTS")}
        ]
        return self.markup(actions, schema)

    def finish_quiz(self, gettext):
        schema = [1]
        actions = [
            {"text": gettext("Завершить тест"), "cb": "FINISH_QUIZ"}
        ]
        return self.markup(actions, schema)

    def confirm_finishing_quiz(self, gettext):
        schema = [1, 1]
        actions = [
            {"text": gettext("Да, завершить тест"), "cb": "CONFIRM_FINISH_QUIZ"},
            {"text": gettext("Нет, продолжить тест"), "cb": "CONTINUE_QUIZ"}
        ]
        return self.markup(actions, schema)
