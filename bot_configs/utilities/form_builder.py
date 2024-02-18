from aiogram import types
from database.operations import get_user_by_id, set_user_state


class Step:
    def __init__(self, start_message, state, setter_to_db,
                 success_message,
                 edited_message=None,
                 validation_function=None,
                 error_message=None,
                 keyboard=None):

        """
        :param start_message: Сообщение, которое будет отправлено пользователю при первом обращении к данному шагу
        :param state: Состояние, при котором пользователь попадает на данный шаг
        :param setter_to_db: Функция, которая будет вызвана при получении ответа от пользователя
        :param success_message: Сообщение, которое будет отправлено пользователю после успешной валидации полученого ответа
        :param edited_message: Сообщение, которое будет отправлено пользователю после повторного обращения к данному шагу(при редактировании)
        :param validation_function: Функция, которая будет вызвана при получении ответа от пользователя для валидации ввода
        :param error_message: Сообщение, которое будет отправлено пользователю при неудачной валидации полученого ответа
        :param keyboard: Клавиатура, которая будет отправлена пользователю при первом обращении к данному шагу
        """
        self.start_message = start_message
        self.state = state
        self.setter_to_db = setter_to_db
        self.edited_message = edited_message
        self.success_message = success_message
        self.validation_function = validation_function
        self.error_message = error_message
        self.keyboard = keyboard

    def validate(self, value):
        if self.validation_function:
            return self.validation_function(value)
        return True

    def get_start_message(self):
        return self.start_message

    def get_state(self):
        return self.state

    def __repr__(self):
        return f"<Step({self.state})>"


class Form:
    """
    :param finish_state - Состояние, в которое перейдет пользователь после завершения формы
    :param finish_keyboard - Клавиатура, которая будет отправлена пользователю после завершения формы
    :param finish_message - Сообщение, которое будет отправлено пользователю после завершения формы
    :param finish_action - Функция, которая будет вызвана при завершении формы
    """
    def __init__(self, finish_state, finish_keyboard=None, finish_message=None, finish_action=None):
        self.steps = {}
        self.finish_state = finish_state
        self.finish_keyboard = finish_keyboard
        self.finish_message = finish_message
        self.finish_action = finish_action

    def add_step(self, step: Step):
        self.steps[step.state] = step

    def get_form_states(self):
        return list(self.steps.keys())

    def get_first_message(self):
        return self.steps[list(self.steps.keys())[0]].get_start_message()

    def get_first_state(self):
        return list(self.steps.keys())[0]

    def __get_next_state(self, state):
        all_steps = list(self.steps.keys())
        index = all_steps.index(state)
        if index == len(all_steps) - 1:
            return self.finish_state
        return all_steps[index + 1]

    async def handle_input(self, message: types.Message, state):
        step = self.steps[state]
        value = message.text
        if not step.validate(value):
            await message.answer(step.error_message)
            return

        user_id = message.from_user.id
        user = get_user_by_id(user_id)

        next_state = self.__get_next_state(state)
        answer = step.success_message
        keyboard = step.keyboard

        if user and getattr(user, state.lower()):
            next_state = self.finish_state
            answer = step.edited_message
            keyboard = self.finish_keyboard

        step.setter_to_db(user_id, value)
        set_user_state(user_id, next_state)
        await message.answer(answer, reply_markup=keyboard)

        if next_state != self.finish_state:
            await message.answer(self.steps[next_state].get_start_message())
            return

        if self.finish_message:
            await message.answer(self.finish_message, reply_markup=self.finish_keyboard)

        if self.finish_action:
            self.finish_action()

    def __repr__(self):
        return f"<Form({self.steps})>"
