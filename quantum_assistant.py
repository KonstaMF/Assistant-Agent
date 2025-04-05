import tkinter as tk
from tkinter import messagebox, scrolledtext
import numpy as np
import random
import json
import os

# --- QISKIT Импорт ---
from qiskit import QuantumCircuit, Aer, execute

# --- Низший уровень: Логика ---
class LogicGate:
    def AND(self, a, b): return a & b
    def OR(self, a, b): return a | b
    def XOR(self, a, b): return a ^ b

# --- Квантовый вес: суперпозиция весов ---
def quantum_weight():
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)
    backend = Aer.get_backend('qasm_simulator')
    result = execute(qc, backend, shots=1).result().get_counts()
    return 1.0 if '1' in result else 0.0

# --- Нейрон с квантовыми весами ---
class QuantumNeuron:
    def __init__(self, input_size):
        self.input_size = input_size
        self.weights = [quantum_weight() for _ in range(input_size)]

    def activate(self, x):
        z = np.dot(self.weights, x)
        return 1 / (1 + np.exp(-z))  # сигмоида

# --- Подсистема AGI ---
class AGISubsystem:
    def __init__(self, experience_file="experience.json"):
        self.goals = ['Улучшать ответы', 'Понимать пользователя']
        self.experience_file = experience_file
        self.experience = self.load_experience()

    def plan_action(self, context):
        print(f"[AGI] Контекст: {context}, Цель: {self.goals[0]}")
        return "проанализировать и выбрать лучший ответ"

    def learn(self, input_data, feedback):
        entry = {"input": input_data, "feedback": feedback}
        self.experience.append(entry)
        self.save_experience()
        print(f"[AGI] Обучение на опыте: {entry}")

    def save_experience(self):
        try:
            with open(self.experience_file, "w", encoding="utf-8") as f:
                json.dump(self.experience, f, indent=2)
            print("[AGI] Опыт сохранён в файл.")
        except Exception as e:
            print(f"[AGI] Ошибка сохранения: {e}")

    def load_experience(self):
        if os.path.exists(self.experience_file):
            try:
                with open(self.experience_file, "r", encoding="utf-8") as f:
                    print("[AGI] Опыт загружен из файла.")
                    return json.load(f)
            except Exception as e:
                print(f"[AGI] Ошибка загрузки: {e}")
        return []

# --- Квантовое принятие решения ---
class QuantumDecision:
    def __init__(self, options):
        self.options = options

    def choose(self):
        probs = [1 / len(self.options)] * len(self.options)
        return random.choices(self.options, weights=probs, k=1)[0]

# --- Агент ---
class QuantumAgent:
    def __init__(self):
        self.logic = LogicGate()
        self.neuron = QuantumNeuron(input_size=2)
        self.agi = AGISubsystem()

    def process_input(self, data):
        logic_result = self.logic.XOR(data[0], data[1])
        print(f"[LOGIC] XOR: {data[0]} ^ {data[1]} = {logic_result}")

        neuron_output = self.neuron.activate(np.array(data))
        print(f"[NEURON] Активация с квантовыми весами: {neuron_output:.4f}")

        context = {"logic": logic_result, "neuron": neuron_output}
        plan = self.agi.plan_action(context)

        options = ['ответ A', 'ответ B', 'ответ C']
        decision = QuantumDecision(options).choose()
        print(f"[DECISION] Выбор: {decision}")

        self.agi.learn(data, feedback="удачный выбор" if decision == 'ответ A' else "нужна корректировка")
        return decision

    def get_experience(self):
        return self.agi.experience

# --- GUI-интерфейс ---
class AssistantApp:
    def __init__(self, root):
        self.agent = QuantumAgent()
        self.root = root
        self.root.title("Квантовый Интеллектуальный Ассистент")

        self.label = tk.Label(root, text="Введите 2 бита (0 или 1):")
        self.label.pack()

        self.entry1 = tk.Entry(root, width=5)
        self.entry2 = tk.Entry(root, width=5)
        self.entry1.pack()
        self.entry2.pack()

        self.button = tk.Button(root, text="Обработать", command=self.process)
        self.button.pack()

        self.result_label = tk.Label(root, text="", font=("Arial", 14))
        self.result_label.pack()

        self.show_exp_button = tk.Button(root, text="Показать опыт агента", command=self.show_experience)
        self.show_exp_button.pack(pady=5)

    def process(self):
        try:
            a = int(self.entry1.get())
            b = int(self.entry2.get())
            if a not in [0, 1] or b not in [0, 1]:
                raise ValueError
            result = self.agent.process_input([a, b])
            self.result_label.config(text=f"Решение агента: {result}")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите только 0 или 1!")

    def show_experience(self):
        exp = self.agent.get_experience()
        exp_window = tk.Toplevel(self.root)
        exp_window.title("Опыт агента")
        text_area = scrolledtext.ScrolledText(exp_window, width=60, height=20)
        for entry in exp:
            text_area.insert(tk.END, f"Ввод: {entry['input']}, Обратная связь: {entry['feedback']}\n")
        text_area.pack()

# --- Запуск приложения ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AssistantApp(root)
    root.mainloop()
