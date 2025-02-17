# hippodrome754
## Спанж ждёт новых легатов... Но сначала надо подготовиться!

Ипподром - игра-головоломка, в которой игроку предстоит построить дорогу от Фрейма (главного здания) до Коридора с помощью Ядер.
### Подожди, неужели так просто?
Не совсем. Ядра можно установить _только_ на идеально гладкой поверхности и _только_ на определенной высоте - зеро-слое. Для этого Ядра и Фрейм снабжены механизмом __терраформинга__ - краеугольного камня всей игры.

Терраформинг - это выравнивание земли до заветного _зеро-слоя_. Он осуществляется в пределах строго заданной области, поэтому необходимо ставить Ядра как можно ближе к терраформируемой зоне. У Фрейма зона терраформинга больше, да и сам терраформинг идет быстрее, зато 
у Ядер есть возможность объединения областей. Это означает, что, если поставить Ядра друг рядом с другом, терраформинг будет идти в 2 раза быстрее там, где их области терраформинга пересекаются.
### О'кей, а что мы выравниваем?
Помимо обычных неровностей почвы ("травы"), на карте случайным образом генерируются следующие типы рельефа:
- Горы (бывают как высокие, так и низкие, проблемы вызывают лишь очень крупные горы)
- Ямы (в отличие от гор, ямы могут оказаться неожиданным сюрпризом на выбранном маршруте)
- Синие столбы (особое образование местного Спанжа, эти синие столбы вырастают из самых глубоких ям чуть ли не до небес. Терраформиг этих столбов занимает _очень_ много времени - остерегайтесь их!)

Все эти неровности генерируются в случайном количестве в случайных местах на карте. Однако по мере продвижения вглубь Спанжа и повышения уровня количество еровностей будет расти!
### И всё?
Нет, есть ещё кое-что. Спанж-миры этой области Психосферы крайне нестабильны, поэтому пробраться к Коридору надо как можно быстрее - иначе мир может самоуничтожиться, и, что гораздо страшнее, вы проиграете и вам прийдется начинать с начала!
У вас есть таймер и психометр для отслеживания ситуации. Таймер показывает оставшееся время, а психометр наглядно демонстрирует, насколько ситуация опасна - чем меньше времени, тем краснее шар и тем быстрее он двигается.
## Как начать играть
Слава Спиритам, нам удалось собрать первый релиз 1.0! Теперь вы можете запустить игру на Windows без лишних телодвижений!
Просто выберите во вкладке Releases сбоку последнюю версию и наслаждайтесь
### А как игру собрать из исходников?
Игра написана на Python, поэтому для запуска вам потребуется его установить.
Для того, чтобы всё заработало, нужно установить все необходимые зависимости.
Скачав искодный код и перейдя в папку с игрой, введите:
```
pip install -r requirements.txt
```

Эта команда установит все необходимые модули для работы Ипподрома.

Следующим шагом надо собрать библиотеку для отрисовки 3D карт. Однако, чтобы упростить Вам жизнь, я скомпилиовал ее за вас. [Cсылка](https://disk.yandex.ru/d/5Ry6y1NVh-o8-w). Всё, что нужно от вас - скопировать ее в папку с игрой.

Если вы работаете на Linux или просто хотите ее собрать вручную, надо установить компиляторы Go и GCC. Рекомендую ставить из MinGW или MSYS, если вы на Windows.
Сборка выполняется следующим образом:
```
go env -w CGO_ENABLED=1
go build -buildmode=c-shared -o .\ray_casting.dll .\go\ray_casting.go
```

Запуск производится двойным кликом по файлу `main.py` в папке `python`. Если вам по душе консоль, команда следующая:
```
python python\main.py
```

Заранее выберете английскую раскладку.
## Из обучения ничего не понял. Куда жать?
- Для того, чтобы двигать камеру: W A S D
- Для того, чтобы повернуть камеру: H J K L
- Для того, чтобы поднять/опустить камеру: N M
- Для того, чтобы создать ядро: <Пробел>
- Для того, чтобы поставить ядро: \<Enter>
- Для того, чтобы переместить ядро: стрелки

Обратите внимание, что при повороте камеры управление Ядрами _меняется!_ Также заметьте, что по диагонали Ядра перемещаются _быстрее._ Это можно использовать, чтобы тратить меньше времени на постройку Ядер в дальних частях карты, т.к. Ядра __всегда__ появляются на Фрейме.

ВНИМАНИЕ! ДЛЯ СОХРАНЕНИЯ РЕЗУЛЬТАТОВ ЗАПУСКАЙТЕ ИГРУ ИЗ ОДНОЙ И ТОЙ ЖЕ ПАПКИ, ИНАЧЕ ЕСТЬ ШАНС ВСЁ ПОТЕРЯТЬ!

При создании воксельного движка за основу был взят Voxel Space Render ([GitHub](https://github.com/StanislavPetrovV/Voxel-Space-Render))
