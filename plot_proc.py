import csv

#Считываем из файла зависимости
def read_csv_to_dict(file_path):
    """
    Читает CSV-файл и возвращает данные в виде словаря,
    где ключи - названия столбцов, а значения - списки данных из этих столбцов.

    :param file_path: Строка, путь к CSV-файлу.
    :return: Словарь с данными из CSV.
    """
    data_dict = {}

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Чтение заголовков столбцов
        for header in headers:
            data_dict[header] = []  # Инициализация списка для каждого заголовка
        for row in reader:
            for header, value in zip(headers, row):
                data_dict[header].append(value)

    return data_dict

# Пример использования функции
file_path = '/Users/tortolla/Downloads/Data_for_Viktor 3/Zn_100_proc.csv'  # Укажите здесь актуальный путь к вашему файлу
data_dict = read_csv_to_dict(file_path)


import matplotlib.pyplot as plt

#Строим зависимости

def plot_dependencies(data_dict):
    """
    Строит зависимости вида d_xx(t_xx) для всех найденных пар в словаре данных.

    :param data_dict: Словарь с данными, где ключи - названия столбцов.
    """
    plt.figure(figsize=(10, 6))  # Задаем размер графика

    for key in data_dict.keys():
        if key.startswith('d_'):  # Находим ключи, соответствующие d_xx
            time_key = 't_' + key.split('_')[1]  # Формируем имя ключа времени t_xx
            if time_key in data_dict:  # Проверяем, существует ли соответствующий временной столбец
                # Преобразование строк в числа, игнорируя пустые значения
                time_values = [float(x) for x in data_dict[time_key] if x]
                distance_values = [float(x) for x in data_dict[key] if x]

                if len(time_values) == len(distance_values):  # Убедимся, что списки совпадают по длине
                    plt.plot(time_values[0:], distance_values[0:], label=f'{key}({time_key})')
                else:
                    print(f'Warning: Mismatched lengths for {key} and {time_key}')

    plt.xlabel('Time')  # Подпись оси X
    plt.ylabel('Distance')  # Подпись оси Y
    plt.title('Dependencies of Distance on Time')  # Заголовок графика
    plt.legend()  # Отображение легенды
    plt.grid(True)  # Отображение сетки
    plt.show()


plot_dependencies(data_dict)